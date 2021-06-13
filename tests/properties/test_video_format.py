import pytest

from video_encoding.properties.video_format import VideoFormat


def test_video_formats() -> None:

    assert VideoFormat.AVI.value == "XVID"

    assert isinstance(VideoFormat.list(), list)
