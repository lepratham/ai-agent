import os
from config import MAX_CHARS


def get_file_content(working_directory, file_path):
    true_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not true_file_path.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if os.path.isfile(true_file_path) is False:
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(true_file_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            tl_file_content_string = f.read(1)
            if len(tl_file_content_string) == 1:
                adj_string = f'{file_content_string} [...File "{file_path}" truncated at 10000 characters]'
                return adj_string
            return file_content_string

    except Exception as error:
        return f"Error: {str(error)}"
