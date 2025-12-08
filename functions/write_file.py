import os


def write_file(working_directory, file_path, content):
    true_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not true_file_path.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    try:
        directory_name = os.path.dirname(true_file_path)
        if not os.path.exists(directory_name) and directory_name:
            os.makedirs(directory_name)
        with open(true_file_path, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as error:
        return f"Error: {str(error)}"
