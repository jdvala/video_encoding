from enum import Enum
from typing import List


class VideoFormat(Enum):
    """
    This class contains the mapping of the different extensions to the codec that are used to process the videos.
    """

    AVI = "XVID"
    MP4 = "mp4v"
    M4V = "H264"
    MPG = "MPG1"

    @staticmethod
    def list() -> List:
        """Lists all the available codec available for conversion.

        Returns:
            List: List of all the codec available for conversion.
        """
        return list(map(lambda v: v.name, VideoFormat))
