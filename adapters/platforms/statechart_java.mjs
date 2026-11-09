import childProcess from "node:child_process";
import { syncBuiltinESMExports } from "node:module";

const spawn = childProcess.spawn;
const java = process.env.JAVA;
const flags = ["-Dline.separator=\n", "-Dfile.encoding=UTF-8", "-Dstdout.encoding=UTF-8", "-Dstderr.encoding=UTF-8"];

childProcess.spawn = function (file, args, ...options) {
  if (file === java && Array.isArray(args) && args.includes("-cp")) {
    args = [...flags, ...args];
  }
  return Reflect.apply(spawn, this, [file, args, ...options]);
};
syncBuiltinESMExports();
