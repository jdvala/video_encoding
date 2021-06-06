# Utils functions
import os
import shutil


def get_file_name_extension(path):
    """Get the file name and extension from the path.

    Args:
        path (str): Path of the file.

    Returns:
        Tuple(str, str): Tuple of file name and file extension.
    """
    if not isinstance(path, str):
        return
    filepath, file_extension = os.path.splitext(path)

    filename = os.path.split(filepath)[-1]

    return filename, file_extension


def clean_up(path):
    """Remove the folder

    Args:
        path (str): Path or folder to remove.
    """
    shutil.rmtree(path)
