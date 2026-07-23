import os

def write_file(working_directory: str, file_path: str, content: str) -> str:

  working_directory_abs = os.path.abspath(working_directory)

  file_path_abs = os.path.join(working_directory_abs, file_path)