import os
import subprocess


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
