import os
import subprocess
from google.genai import types


def run_python_file(working_directory, file_path, args=[]):
    true_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not true_file_path.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(true_file_path):
        return f'Error: File "{file_path}" not found.'
    if not true_file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        completed_process = subprocess.run(
            ["python", true_file_path] + args,
            timeout=30,
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
            text=True,
        )

        if not completed_process.stdout and not completed_process.stderr:
            return "No output produced"

        completed_string = (
            "STDOUT:"
            + completed_process.stdout
            + "\nSTDERR:"
            + completed_process.stderr
        )

        if completed_process.returncode != 0:
            return (
                completed_string
                + f"\nProcess exited with code {completed_process.returncode}"
            )

        return completed_string

    except Exception as error:
        return f"Error: executing Python file: {error}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a python file with given file_path within the working directory, as well will given args.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file_path representes the name of the file within the working directory.",
            ),
        },
    ),
)
