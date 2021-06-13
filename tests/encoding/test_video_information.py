import os

import cv2
import pytest
from moviepy.editor import VideoFileClip

from video_encoding.encoding.video_information import get_video_information


@pytest.fixture
def load_video() -> cv2.VideoCapture:
    video = cv2.VideoCapture(
        "/home/jay-vala/video_encoding/tests/assets/test_video.mp4"
    )
    return video


@pytest.fixture
def load_different_video() -> VideoFileClip:
    video = VideoFileClip("/home/jay-vala/video_encoding/tests/assets/test_video.mp4")
    return video


def test_get_video_information(
    load_video: cv2.VideoCapture, load_different_video: VideoFileClip
) -> None:
    videoinfo = get_video_information(load_video)

    assert isinstance(videoinfo.frame_rate, float)

    with pytest.raises(
        ValueError,
        match="Video object is not from CV2. Its of type <class 'moviepy.video.io.VideoFileClip.VideoFileClip'>",
    ):
        get_video_information(load_different_video)
