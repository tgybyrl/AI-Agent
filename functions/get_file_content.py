from config import MAX_CHARS

def get_file_content(working_directory: str, file_path: str) -> str:
  if os.path.commonpath(file_path, working_directory):
    raise Exception(f'Error: Cannot read "{file_path}" as it is outside the permitted working directory')
  if not os.path.isfile(file_path):
    raise Exception(f'Error: File not found or is not a regular file: "{file_path}"')


  with open(file_path, 'r') as f:
    file_content_string = f.read(MAX_CHARS)
  if f.read(1):
    pass
