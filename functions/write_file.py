import os
from google.genai import types


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


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes to files given a file path and content, constrained to the current working_directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file_path representes the name of the file within the working directory. If the file does not exist the function will create a file matching the given file name.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to be added to the file given by file_path.",
            ),
        },
    ),
)
