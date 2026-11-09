"""Private Windows Job supervisor. JSON request, JSON receipt, stdin lifeline."""
import ctypes
from ctypes import wintypes as W
import json
import msvcrt
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import threading
import time


class Startup(ctypes.Structure):
    _fields_ = [('cb', W.DWORD), ('reserved', W.LPWSTR), ('desktop', W.LPWSTR),
                ('title', W.LPWSTR), ('x', W.DWORD), ('y', W.DWORD),
                ('width', W.DWORD), ('height', W.DWORD), ('xchars', W.DWORD),
                ('ychars', W.DWORD), ('fill', W.DWORD), ('flags', W.DWORD),
                ('show', W.WORD), ('reserved_size', W.WORD), ('reserved_ptr', ctypes.c_void_p),
                ('stdin', W.HANDLE), ('stdout', W.HANDLE), ('stderr', W.HANDLE)]


class StartupEx(ctypes.Structure):
    _fields_ = [('info', Startup), ('attributes', ctypes.c_void_p)]


class ProcessInfo(ctypes.Structure):
    _fields_ = [('process', W.HANDLE), ('thread', W.HANDLE), ('pid', W.DWORD), ('tid', W.DWORD)]


class BasicLimits(ctypes.Structure):
    _fields_ = [('process_time', ctypes.c_longlong), ('job_time', ctypes.c_longlong),
                ('flags', W.DWORD), ('min_ws', ctypes.c_size_t), ('max_ws', ctypes.c_size_t),
                ('active_limit', W.DWORD), ('affinity', ctypes.c_size_t),
                ('priority', W.DWORD), ('scheduling', W.DWORD)]


class IoCounters(ctypes.Structure):
    _fields_ = [(n, ctypes.c_ulonglong) for n in ['read_ops', 'write_ops', 'other_ops',
                                                 'read_bytes', 'write_bytes', 'other_bytes']]


class Limits(ctypes.Structure):
    _fields_ = [('basic', BasicLimits), ('io', IoCounters),
                ('process_memory', ctypes.c_size_t), ('job_memory', ctypes.c_size_t),
                ('peak_process', ctypes.c_size_t), ('peak_job', ctypes.c_size_t)]


class Accounting(ctypes.Structure):
    _fields_ = [('user', ctypes.c_longlong), ('kernel', ctypes.c_longlong),
                ('period_user', ctypes.c_longlong), ('period_kernel', ctypes.c_longlong),
                ('faults', W.DWORD), ('total', W.DWORD), ('active', W.DWORD), ('terminated', W.DWORD)]


K = ctypes.WinDLL('kernel32', use_last_error=True)
def api(name, args, result=W.BOOL):
    f = getattr(K, name)
    f.argtypes, f.restype = args, result
    return f


create_job = api('CreateJobObjectW', [ctypes.c_void_p, W.LPCWSTR], W.HANDLE)
set_job = api('SetInformationJobObject', [W.HANDLE, ctypes.c_int, ctypes.c_void_p, W.DWORD])
query_job = api('QueryInformationJobObject', [W.HANDLE, ctypes.c_int, ctypes.c_void_p, W.DWORD, ctypes.c_void_p])
terminate_job = api('TerminateJobObject', [W.HANDLE, W.UINT])
close = api('CloseHandle', [W.HANDLE])
init_attrs = api('InitializeProcThreadAttributeList', [ctypes.c_void_p, W.DWORD, W.DWORD, ctypes.POINTER(ctypes.c_size_t)])
update_attr = api('UpdateProcThreadAttribute', [ctypes.c_void_p, W.DWORD, ctypes.c_size_t, ctypes.c_void_p,
                                               ctypes.c_size_t, ctypes.c_void_p, ctypes.c_void_p])
delete_attrs = api('DeleteProcThreadAttributeList', [ctypes.c_void_p], None)
create_process = api('CreateProcessW', [W.LPCWSTR, W.LPWSTR, ctypes.c_void_p, ctypes.c_void_p,
                                      W.BOOL, W.DWORD, ctypes.c_void_p, W.LPCWSTR,
                                      ctypes.POINTER(StartupEx), ctypes.POINTER(ProcessInfo)])
in_job = api('IsProcessInJob', [W.HANDLE, W.HANDLE, ctypes.POINTER(W.BOOL)])
resume = api('ResumeThread', [W.HANDLE], W.DWORD)
wait = api('WaitForSingleObject', [W.HANDLE, W.DWORD], W.DWORD)
exit_code = api('GetExitCodeProcess', [W.HANDLE, ctypes.POINTER(W.DWORD)])
terminate_process = api('TerminateProcess', [W.HANDLE, W.UINT])


def checked(ok):
    if not ok:
        raise ctypes.WinError(ctypes.get_last_error())
    return ok


def atomic_json(file, value):
    temp = file.with_suffix('.tmp')
    temp.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')
    os.replace(temp, file)


def remove_owned(path):
    path = Path(path)

    def writable(function, name, error):
        info = Path(name).lstat()
        if not isinstance(error[1], PermissionError) or getattr(info, 'st_file_attributes', 0) & 0x400:
            raise error[1]
        os.chmod(name, stat.S_IWRITE)
        function(name)

    for attempt in range(6):
        try:
            info = path.lstat()
            if getattr(info, 'st_file_attributes', 0) & 0x400:
                path.rmdir() if path.is_dir() else path.unlink()
            elif path.is_dir():
                shutil.rmtree(path, onerror=writable)
            else:
                path.unlink()
            return
        except FileNotFoundError:
            return
        except OSError:
            if attempt == 5:
                raise
            time.sleep(.1 * 2 ** attempt)


def clean_paths(paths):
    errors = []
    for path in paths:
        try:
            remove_owned(path)
        except OSError as error:
            errors.append(f'{path}: {error}')
    return errors


def main():
    request = json.loads(sys.stdin.buffer.readline().decode('utf-8'))
    evidence = Path(request['evidenceDir'])
    receipt_file = evidence / 'receipt.json'
    receipt = dict(schema=1, runId=request['runId'], backend='windows-job', status='blocked',
                   exitCode=None, supervisorPid=os.getpid(), python=sys.executable,
                   pythonVersion=sys.version.split()[0],
                   cleanup=dict(confirmed=False, method='job-list-kill-on-close'))
    cancelled, finished, abandoned = threading.Event(), threading.Event(), threading.Event()
    reason = {'value': 'parent-eof'}
    def watch():
        try:
            for raw in sys.stdin.buffer:
                command = json.loads(raw.decode('utf-8'))
                if command.get('op') == 'finish':
                    finished.set()
                    return
                reason['value'] = 'cancelled'
                cancelled.set()
        except Exception:
            reason['value'] = 'invalid-control'
        abandoned.set()
        cancelled.set()
        finished.set()
    threading.Thread(target=watch, daemon=True).start()
    job, attrs, proc = None, None, ProcessInfo()
    streams = []
    initialized = False
    try:
        job = checked(create_job(None, None))
        limits = Limits()
        limits.basic.flags = 0x2000  # JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
        checked(set_job(job, 9, ctypes.byref(limits), ctypes.sizeof(limits)))
        size = ctypes.c_size_t()
        init_attrs(None, 2, 0, ctypes.byref(size))
        attrs_buffer = ctypes.create_string_buffer(size.value)
        attrs = ctypes.cast(attrs_buffer, ctypes.c_void_p)
        checked(init_attrs(attrs, 2, 0, ctypes.byref(size)))
        initialized = True
        for file, mode in [(os.devnull, 'rb'), (evidence / 'worker.stdout', 'wb'),
                           (evidence / 'worker.stderr', 'wb')]:
            streams.append(open(file, mode))
        handles = [msvcrt.get_osfhandle(f.fileno()) for f in streams]
        for handle in handles:
            os.set_handle_inheritable(handle, True)
        handle_array = (W.HANDLE * 3)(*handles)
        job_array = (W.HANDLE * 1)(job)
        checked(update_attr(attrs, 0, 0x20002, handle_array, ctypes.sizeof(handle_array), None, None))
        # Assign at process creation, including the supervisor-crash-before-resume window.
        checked(update_attr(attrs, 0, 0x2000D, job_array, ctypes.sizeof(job_array), None, None))
        startup = StartupEx()
        startup.info.cb = ctypes.sizeof(startup)
        startup.info.flags, startup.info.show = 0x101, 0
        startup.info.stdin, startup.info.stdout, startup.info.stderr = handles
        startup.attributes = attrs
        argv = request['argv']
        command = ctypes.create_unicode_buffer(subprocess.list2cmdline(argv))
        child_env = {**os.environ, **request.get('env', {})}
        environment = ctypes.create_unicode_buffer('\0'.join(f'{k}={v}' for k, v in
                                                              sorted(child_env.items(), key=lambda x: x[0].upper())) + '\0\0')
        checked(create_process(argv[0], command, None, None, True,
                               0x4 | 0x80000 | 0x8000000 | 0x400,
                               environment, request['cwd'], ctypes.byref(startup), ctypes.byref(proc)))
        membership = W.BOOL()
        checked(in_job(proc.process, job, ctypes.byref(membership)))
        if not membership.value:
            raise RuntimeError('Worker was not created inside its private Job')
        receipt['workerPid'] = proc.pid
        atomic_json(evidence / 'startup.json', dict(supervisorPid=os.getpid(), workerPid=proc.pid,
                                                   createdInJob=True, runId=request['runId']))
        if cancelled.is_set():
            receipt['status'] = reason['value']
        else:
            if resume(proc.thread) == 0xFFFFFFFF:
                raise ctypes.WinError(ctypes.get_last_error())
            start = time.monotonic()
            while True:
                if cancelled.is_set():
                    receipt['status'] = reason['value']
                    break
                if request.get('timeoutMs', 0) and (time.monotonic() - start) * 1000 >= request['timeoutMs']:
                    receipt['status'] = 'timeout'
                    break
                result = wait(proc.process, 25)
                if result == 0:
                    code = W.DWORD()
                    checked(exit_code(proc.process, ctypes.byref(code)))
                    receipt.update(status='exited', exitCode=code.value)
                    break
                if result != 258:
                    raise ctypes.WinError(ctypes.get_last_error())
    except Exception as error:
        receipt.update(status='blocked', error=str(error))
    finally:
        if job:
            try:
                checked(terminate_job(job, 2))
                deadline = time.monotonic() + 5
                while True:
                    stats = Accounting()
                    checked(query_job(job, 1, ctypes.byref(stats), ctypes.sizeof(stats), None))
                    if stats.active == 0:
                        receipt['cleanup'].update(confirmed=True, activeProcesses=0)
                        break
                    if time.monotonic() >= deadline:
                        raise TimeoutError(f'Job still contains {stats.active} processes')
                    time.sleep(.01)
            except Exception as error:
                receipt.update(status='cleanup-failed', error=str(error))
        if proc.process:
            if wait(proc.process, 0) == 258:
                terminate_process(proc.process, 2)
                wait(proc.process, 5000)
            close(proc.process)
        if proc.thread:
            close(proc.thread)
        if job:
            close(job)
        if attrs and initialized:
            delete_attrs(attrs)
        for f in streams:
            f.close()
    prepare = list(request.get('prepareCleanupDirs', []))
    try:
        if request.get('stageDir'):
            prepare.extend(str(path) for path in Path(request['stageDir']).iterdir() if path.name != 'done')
        preparation_errors = clean_paths(prepare) if receipt['cleanup']['confirmed'] else ['Process cleanup is unconfirmed']
    except OSError as error:
        preparation_errors = [str(error)]
    receipt['prepared'] = not preparation_errors
    if preparation_errors:
        receipt.update(status='cleanup-failed', pathCleanupErrors=preparation_errors)
    atomic_json(receipt_file, receipt)
    try:
        print(json.dumps(receipt, ensure_ascii=True), flush=True)
    except (OSError, ValueError):
        finished.set()
    finished.wait()
    errors = clean_paths(request['cleanupDirs']) if receipt['cleanup']['confirmed'] else ['Process cleanup is unconfirmed']
    receipt['finalized'] = not errors
    if errors:
        receipt.update(status='cleanup-failed', pathCleanupErrors=errors)
    atomic_json(receipt_file, receipt)
    if abandoned.is_set() and request.get('abandonDir') and not errors:
        remove_owned(request['abandonDir'])
    return 0 if receipt['cleanup']['confirmed'] and not errors else 2


if __name__ == '__main__':
    sys.exit(main())
