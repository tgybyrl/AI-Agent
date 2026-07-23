import os
from config import MAX_CHARS

def get_file_content(working_directory: str, file_path: str) -> str:
  try:
    working_dir_abs = os.path.abspath(working_directory)


    if os.path.commonpath([file_path, working_directory]) == file_path:
      raise Exception(f'Error: Cannot read "{file_path}" as it is outside the permitted working directory')
      
    if not os.path.isfile(os.path.join(working_directory, file_path)):
      raise Exception(f'Error: File not found or is not a regular file: "{file_path}"')


    with open(file_path, 'r') as f:
      content = f.read(MAX_CHARS)
    if f.read(1):
      content += f'[...File "{file_path}" truncated at {MAX_CHARS}]'
    return content

  except Exception as e:
    return f'Error: {e}'


