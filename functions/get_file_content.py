import os
from config import MAX_CHARS

def get_file_content(working_directory: str, file_path: str) -> str:
  try:
    working_dir_abs = os.path.abspath(working_directory)
    file_path_abs = os.path.abspath(os.path.join(working_dir_abs, file_path))

    if os.path.commonpath([file_path_abs, working_dir_abs]) != working_dir_abs:
      raise Exception(f'Cannot read "{file_path}" as it is outside the permitted working directory')

    if not os.path.isfile(file_path_abs):
      raise Exception(f'File not found or is not a regular file: "{file_path}"')


    with open(file_path_abs, 'r') as f:
      content = f.read(MAX_CHARS)
      if f.read(1):
        content += f'[...File "{file_path}" truncated at {MAX_CHARS}]'
      return content

  except Exception as e:
    return f'Error: {e}'


