# local functions
import tempfile


def create_temp_folder() -> tempfile.TemporaryDirectory:
    """Create temporary directory.

    Returns:
        Tempfile object.
    """
    return tempfile.TemporaryDirectory()
