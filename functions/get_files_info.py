import os
from google.genai import types


def get_files_info(working_directory, directory="."):
    directory = os.path.abspath(os.path.join(working_directory, directory))

    if not directory.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if os.path.isdir(directory) is False:
        return f'Error: "{directory}" is not a directory'

    try:
        files = os.listdir(directory)
        string = ""
        for file in files:
            file_size = os.path.getsize(os.path.join(directory, file))
            is_dir = not os.path.isfile(os.path.join(directory, file))
            string += f"- {file}: file_size={file_size} bytes, is_dir={is_dir}\n"
        return string

    except Exception as error:
        return f"Error: {str(error)}"


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
