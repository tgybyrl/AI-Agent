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
      output += f"Process exited with code {result.returncode}"
    if (result.stdout == "" and result.stderr == ""):
      output += "No output produced"
    if result.stdout != "":
      output += f"STDOUT: {result.stdout}"
    if result.stderr != "":
      output += f"STDERR: {result.stderr}"

    return output
    
  except Exception as e: 
    return f"Error: executing Python file: {e}"


schema_run_python_file = {
  "type": "function",
  "function": {
    "name": "run_python_file",
    "description": "Execute python code in a specified file relative to the working directory.",
    "parameters": {
      "required": ["file_path"],
      "type": "object",
      "properties": {
        "file_path": {
          "type": "string",
          "description" : "File path containing the python file, relative to the working directory.",
        },
        "args": {
          "type": "array",
          "items": {
            "type": "string",
          },
          "description": "Args are passed to the script when it runs and meant to hold command-line-arguments. It is optional."
        }
      }
    }
  }
}