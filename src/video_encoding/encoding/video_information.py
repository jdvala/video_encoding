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


def get_video_information(video):
    frame_rate = _get_frame_rate(video)
    width = _get_width_video(video)
    height = _get_height_video(video)
    total_frames = _get_total_frames(video)

    return Video_information(
        frame_rate=frame_rate, width=width, height=height, total_frames=total_frames
    )


def _get_frame_rate(video):
    """[summary]

    Args:
        video ([type]): [description]

    Returns:
        [type]: [description]
    """
    if _check_video_type(video):
        return
    frame_rate = video.get(cv2.CAP_PROP_FPS)
    return frame_rate


def _get_width_video(video):
    """[summary]

    Args:
        video ([type]): [description]

    Returns:
        [type]: [description]
    """
    if _check_video_type(video):
        return

    width = video.get(cv2.CAP_PROP_FRAME_HEIGHT)
    return width


def _get_height_video(video):
    """[summary]

    Args:
        video ([type]): [description]

    Returns:
        [type]: [description]
    """
    if _check_video_type(video):
        return

    height = video.get(cv2.CAP_PROP_FRAME_HEIGHT)
    return height


def _get_total_frames(video):
    """[summary]

    Args:
        video ([type]): [description]

    Returns:
        [type]: [description]
    """
    if _check_video_type(video):
        return

    total_frames = video.get(cv2.CAP_PROP_FRAME_COUNT)
    return total_frames


def _check_video_type(video):
    """[summary]

    Args:
        video ([type]): [description]
    """
    if not isinstance(video, cv2.VideoCapture):
        info_logger.error("Video object is not from CV2.", object_type=type(video))
        return
