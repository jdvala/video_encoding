"""
Function or utilities to get more information about the video.
These includes functions to get video properties like:
    * Frame Rate
    * Video Height
    * Video Width
    * Total number of frames
"""
from collections import namedtuple

import cv2
import structlog

info_logger = structlog.get_logger(component="video_infromation")

Video_information = namedtuple("VideoInfo", "frame_rate width height total_frames")


def get_video_information(video: cv2.VideoCapture) -> Video_information:
    """Collect and present information about the video.

    This function get the following information about a video.
    * Frame Rate
    * Width of the video.
    * Height of the video.
    * Total frames in a video.

    Args:
        video (cv2.VideoCapture): Video for which the information is required.

    Returns:
        Video_information: Frame rate, width, height and total frames in a video.
    """
    frame_rate = _get_frame_rate(video)
    width = _get_width_video(video)
    height = _get_height_video(video)
    total_frames = _get_total_frames(video)

    return Video_information(
        frame_rate=frame_rate, width=width, height=height, total_frames=total_frames
    )


def _get_frame_rate(video: cv2.VideoCapture) -> float:
    """Get the frame rate of the video.

    Args:
        video (cv2.VideoCapture): Video for which the frame rate is required.

    Returns:
        float: Frame rate of the video.
    """
    if _check_video_type(video):
        return
    frame_rate = video.get(cv2.CAP_PROP_FPS)
    return frame_rate


def _get_width_video(video: cv2.VideoCapture) -> int:
    """Get the height of the video.

    Args:
        video (cv2.VideoCapture): Video for which the frame rate is required.

    Returns:
        int: Width of the video.
    """
    if _check_video_type(video):
        return

    width = video.get(cv2.CAP_PROP_FRAME_HEIGHT)
    return width


def _get_height_video(video: cv2.VideoCapture) -> int:
    """Get the height of the video.

    Args:
        video (cv2.VideoCapture): Video for which the frame rate is required.

    Returns:
        int: Height of the video.
    """
    if _check_video_type(video):
        return

    height = video.get(cv2.CAP_PROP_FRAME_HEIGHT)
    return height


def _get_total_frames(video: cv2.VideoCapture) -> int:
    """Get the total frames of the video.

    Args:
        video (cv2.VideoCapture): Video for which the frame rate is required.

    Returns:
        int: Total frames of the video.
    """
    if _check_video_type(video):
        return

    total_frames = video.get(cv2.CAP_PROP_FRAME_COUNT)
    return total_frames


def _check_video_type(video: cv2.VideoCapture):
    """Check if the video is of required type.

    Args:
        video (cv2.VideoCapture): Video for which the frame rate is required.

    Raises:
        ValueError: If the video is not of type cv2.VideoCapture.
    """
    if not isinstance(video, cv2.VideoCapture):
        raise ValueError(f"Video object is not from CV2. {type(video)}")
