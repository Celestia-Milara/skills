"""Resolve native host entry points and bound local process lifetimes.

Windows jobs and POSIX process groups clean up ordinary descendants. This is
process management, not a sandbox for programs that deliberately escape it.
On Windows, job assignment follows Popen. A child created before assignment can
escape the job; the wrapper does not provide atomic launch-time containment.
"""
from contextlib import contextmanager, ExitStack
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import time


CHECK_TIMEOUT = 30


def host_command(host):
    names = {'codex': ('codex', '@openai/codex'),
             'claude-code': ('claude', '@anthropic-ai/claude-code')}
    name, package_name = names[host]
    executable = shutil.which(name)
    if not executable:
        raise FileNotFoundError(f'{host} executable is unavailable')
    shim = Path(executable).absolute()
    if shim.suffix.lower() not in ('.cmd', '.bat', '.ps1'):
        return [str(shim)]
    package = shim.parent / 'node_modules' / package_name
    manifest = package / 'package.json'
    try:
        metadata = json.loads(manifest.read_text(encoding='utf-8'))
        bins = metadata.get('bin')
        entry_name = bins.get(name) if isinstance(bins, dict) else bins
        if not isinstance(entry_name, str) or not entry_name:
            raise ValueError(f'missing bin entry for {name}')
    except (OSError, ValueError, AttributeError) as error:
        raise RuntimeError(f'Cannot resolve {host} shim from {manifest}: {error}') from error
    entry = package / entry_name
    if not entry.is_file():
        raise FileNotFoundError(f'{host} entry point is unavailable: {entry}')
    if entry.suffix.lower() not in ('.js', '.cjs', '.mjs'):
        if entry.suffix.lower() in ('.cmd', '.bat', '.ps1'):
            raise RuntimeError(f'{host} bin must resolve to a native executable or Node script: {entry}')
        return [str(entry)]
    local_node = shim.parent / ('node.exe' if os.name == 'nt' else 'node')
    node = str(local_node) if local_node.is_file() else shutil.which('node')
    if not node:
        raise FileNotFoundError(f'Node.js executable is unavailable for {host}: {entry}')
    return [node, str(entry)]


class _WindowsJob:
    """Kill attached processes when this private job handle closes."""
    def __init__(self):
        import ctypes
        from ctypes import wintypes

        class BasicLimits(ctypes.Structure):
            _fields_ = [('process_time', ctypes.c_longlong), ('job_time', ctypes.c_longlong),
                        ('flags', wintypes.DWORD), ('min_working_set', ctypes.c_size_t),
                        ('max_working_set', ctypes.c_size_t), ('active_processes', wintypes.DWORD),
                        ('affinity', ctypes.c_size_t), ('priority', wintypes.DWORD),
                        ('scheduling', wintypes.DWORD)]

        class IoCounters(ctypes.Structure):
            _fields_ = [(name, ctypes.c_ulonglong) for name in
                        ('read_ops', 'write_ops', 'other_ops', 'read_bytes', 'write_bytes', 'other_bytes')]

        class ExtendedLimits(ctypes.Structure):
            _fields_ = [('basic', BasicLimits), ('io', IoCounters),
                        ('process_memory', ctypes.c_size_t), ('job_memory', ctypes.c_size_t),
                        ('peak_process_memory', ctypes.c_size_t), ('peak_job_memory', ctypes.c_size_t)]

        self.api = ctypes.WinDLL('kernel32', use_last_error=True)
        self.api.CreateJobObjectW.argtypes = [ctypes.c_void_p, wintypes.LPCWSTR]
        self.api.CreateJobObjectW.restype = wintypes.HANDLE
        self.api.SetInformationJobObject.argtypes = [wintypes.HANDLE, ctypes.c_int, ctypes.c_void_p, wintypes.DWORD]
        self.api.SetInformationJobObject.restype = wintypes.BOOL
        self.api.AssignProcessToJobObject.argtypes = [wintypes.HANDLE, wintypes.HANDLE]
        self.api.AssignProcessToJobObject.restype = wintypes.BOOL
        self.api.CloseHandle.argtypes = [wintypes.HANDLE]
        self.api.CloseHandle.restype = wintypes.BOOL
        self.api.TerminateJobObject.argtypes = [wintypes.HANDLE, wintypes.UINT]
        self.api.TerminateJobObject.restype = wintypes.BOOL
        self.api.QueryInformationJobObject.argtypes = [wintypes.HANDLE, ctypes.c_int,
                                                       ctypes.c_void_p, wintypes.DWORD, ctypes.c_void_p]
        self.api.QueryInformationJobObject.restype = wintypes.BOOL
        self.handle = self.api.CreateJobObjectW(None, None)
        if not self.handle:
            raise ctypes.WinError(ctypes.get_last_error())
        limits = ExtendedLimits()
        limits.basic.flags = 0x2000  # JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
        if not self.api.SetInformationJobObject(self.handle, 9, ctypes.byref(limits), ctypes.sizeof(limits)):
            error = ctypes.WinError(ctypes.get_last_error())
            self.close()
            raise error

    def assign(self, process):
        import ctypes
        if not self.api.AssignProcessToJobObject(self.handle, int(process._handle)):
            raise ctypes.WinError(ctypes.get_last_error())

    def close(self):
        if not self.handle:
            return
        import ctypes
        from ctypes import wintypes

        class Accounting(ctypes.Structure):
            _fields_ = [('user_time', ctypes.c_longlong), ('kernel_time', ctypes.c_longlong),
                        ('period_user_time', ctypes.c_longlong), ('period_kernel_time', ctypes.c_longlong),
                        ('page_faults', wintypes.DWORD), ('total', wintypes.DWORD),
                        ('active', wintypes.DWORD), ('terminated', wintypes.DWORD)]

        try:
            if not self.api.TerminateJobObject(self.handle, 1):
                raise ctypes.WinError(ctypes.get_last_error())
            deadline = time.monotonic() + 5
            while True:
                state = Accounting()
                if not self.api.QueryInformationJobObject(self.handle, 1, ctypes.byref(state), ctypes.sizeof(state), None):
                    raise ctypes.WinError(ctypes.get_last_error())
                if not state.active:
                    break
                if time.monotonic() >= deadline:
                    raise RuntimeError('Host descendants did not exit within 5s')
                time.sleep(0.01)
        finally:
            self.api.CloseHandle(self.handle)
            self.handle = None


@contextmanager
def managed_process(command, **kwargs):
    job = _WindowsJob() if os.name == 'nt' else None
    process = None
    try:
        if os.name == 'nt':
            kwargs['creationflags'] = kwargs.get('creationflags', 0) | subprocess.CREATE_NO_WINDOW
        else:
            kwargs['start_new_session'] = True
        process = subprocess.Popen(command, **kwargs)
        if job:
            job.assign(process)
        yield process
    finally:
        try:
            if job:
                job.close()
        finally:
            if process:
                try:
                    if os.name != 'nt':
                        try:
                            os.killpg(process.pid, signal.SIGKILL)
                        except ProcessLookupError:
                            pass
                    if process.poll() is None:
                        process.kill()
                    process.wait(timeout=5)
                finally:
                    with ExitStack() as streams:
                        for stream in (process.stdin, process.stdout, process.stderr):
                            if stream is not None:
                                streams.callback(stream.close)


def run_process(command, *, timeout=CHECK_TIMEOUT, input=None, capture_output=False, check=False, **kwargs):
    """Like subprocess.run, with descendant cleanup on every exit path."""
    if input is not None:
        kwargs['stdin'] = subprocess.PIPE
    if capture_output:
        kwargs['stdout'] = kwargs['stderr'] = subprocess.PIPE
    with managed_process(command, **kwargs) as process:
        stdout, stderr = process.communicate(input=input, timeout=timeout)
        result = subprocess.CompletedProcess(command, process.returncode, stdout, stderr)
    if check:
        result.check_returncode()
    return result


def probe(command, *, cwd, timeout=CHECK_TIMEOUT):
    """Keep failed, missing, and timed-out postchecks visible in text evidence."""
    try:
        return run_process(command, cwd=cwd, capture_output=True, text=True,
                           encoding='utf-8', errors='replace', timeout=timeout)
    except subprocess.TimeoutExpired as error:
        def text(value):
            return value.decode('utf-8', errors='replace') if isinstance(value, bytes) else value or ''
        return subprocess.CompletedProcess(command, 124, text(error.stdout),
                                           text(error.stderr) + f'\nPostcheck timed out after {timeout}s\n')
    except OSError as error:
        return subprocess.CompletedProcess(command, 127, '', f'Postcheck failed: {error}\n')
