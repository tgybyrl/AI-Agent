import os

def write_file(working_directory: str, file_path: str, content: str) -> str:
  try:
    working_dir_abs = os.path.abspath(working_directory)

    file_path_abs = os.path.abspath(os.path.join(working_dir_abs, file_path))

    if os.path.commonpath([working_dir_abs, file_path_abs]) != working_dir_abs:
      return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if os.path.isdir(file_path_abs):
      return f'Error: Cannot write to "{file_path}" as it is directory'
      
    os.makedirs(os.path.dirname(file_path_abs), exist_ok=True)

    with open(file_path_abs, "w") as f:
      f.write(content)
      
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
  except Exception as e:
    return f'Error: {e}'

schema_write_file = {
  "type": "function",
  "function": {
    "name": "write_file",
    "description": "Opens file, write and change the content of the file relative to the working directory.",
    "parameters": {
      "required": ["file_path", "content"],
      "type": "object",
      "properties": {
        "file_path": {
          "type": "string",
          "description" : "File path containing the content file, relative to the working directory.",
        },
        "content": {
          "type": "string",
          "description": "It is the content that user want to change/add in file."
        }
      }
    }
  }
}