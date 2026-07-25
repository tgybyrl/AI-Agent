import os

def get_files_info(working_directory: str, directory: str = ".") -> str:

  try:
    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

    if not os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs:
      return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(target_dir):
      return f'Error: "{directory}" is not a directory'

    files_info = []

    for filename in os.listdir(target_dir):
      filepath = os.path.join(target_dir, filename)
      name = filename
      file_size = os.path.getsize(filepath)
      files_info.append(f"- {name}: file_size={file_size} bytes, is_dir={os.path.isdir(filepath)}")
    
    return "\n".join(files_info)

    return f'Success: "{directory}" is within the working directory'

  except Exception as e:
    return f'Error: {e}'
    

schema_get_files_info = {
  "type": "function",
  "function": {
    "name": "get_files_info",
    "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
    "parameters": {
      "type": "object",
      "properties": {
        "directory":{
        "type": "string",
        "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
        }
      }
    }
  }
}