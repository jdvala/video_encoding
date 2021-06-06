# Utils functions
import os


def get_file_name_extension(path):
    """Get the file name and extension from the path.

    Args:
        path (str): Path of the file.

    Returns:
        Tuple(str, str): Tuple of file name and file extension.
    """
    if not isinstance(path, str):
        return
    filename, file_extension = os.path.splitext(path)
    return filename, file_extension
