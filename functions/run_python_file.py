import os, subprocess

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:

  try:
    working_dir_abs = os.path.abspath(working_directory)
    file_path_abs = os.path.abspath(os.path.join(working_directory, file_path))
    if os.path.commonpath([working_dir_abs, file_path_abs]) != working_dir_abs:
      return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(file_path_abs):
      return f'Error: "{file_path}" does not exist or is not a regular file'
    if not file_path_abs.endswith(".py"):
      return f'Error: "{file_path}" is not a Python file'

    command = ["python", file_path_abs]

    if args != None:
        command.extend(args)

    result = subprocess.run(command, capture_output=True, cwd=working_dir_abs, text=True, timeout=30)

    #output part
    output = ""
    if result.returncode != 0:
       return output + f"Process exited with code X"
    if (result.stdout == None and result.stderr == None):
      return output + f"No output produced"

    return output + f"STDOUT: {result.stdout}" + "\n" + f"STDERR: {result.stderr}"
    
  except Exception as e: 
    return f"Error: executing Python file: {e}"