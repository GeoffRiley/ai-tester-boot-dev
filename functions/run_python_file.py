import os
import subprocess

def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

        valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if target_file[-3:] != ".py":
            return f'Error: "{file_path}" is not a Python file'

        command = ["python3", target_file]
        if not args is None:
            command.extend(args)

        completed_process = subprocess.run(command,
                                           capture_output=True,
                                           cwd=working_dir_abs,
                                           text=True,
                                           timeout=30)
        
        rv = []
        if completed_process.returncode != 0:
            rv.append(f"Process exited with code {completed_process.returncode}")
        if completed_process.stdout is None and completed_process.stderr is None:
            rv.append(f"No output produced")
        else:
            so = completed_process.stdout
            se = completed_process.stderr
            if not so is None and len(so)>0:
                rv.append(f"STDOUT: {so}")
            if not se is None and len(se)>0:
                rv.append(f"STDERR: {se}")

        return "\n".join(rv)


    except Exception as e:
        return f"Error: {e}"
