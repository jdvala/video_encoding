from enum import Enum


class VideoFormat(Enum):
    """Video format and its codecs."""

    AVI = "XVID"
    MP4 = "mp4v"
    M4V = "H264"
    MPG = "MPG1"

    @staticmethod
    def list():
        return list(map(lambda v: v.name, VideoFormat))
