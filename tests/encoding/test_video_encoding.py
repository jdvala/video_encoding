import os
from tempfile import TemporaryDirectory

import cv2
import pytest

from video_encoding.encoding.video_encoding import Process


@pytest.fixture
def video_path() -> str:
    return "tests/assets/test_video.mp4"


def test_process(video_path: str) -> None:
    with TemporaryDirectory() as tmpdir:
        process_video = Process(
            in_path=video_path,
            resolution="360",
            out_path=os.path.join(tmpdir, "test_video_360.mp4"),
        )

        resolution_to_set = process_video.get_height_width_res()
        assert resolution_to_set.width == 480
        assert resolution_to_set.height == 360

        process_video.encode_video

        assert os.path.exists(os.path.join(tmpdir, "test_video_360.mp4"))

        # test the attributes of the encoded video
        encoded_video = cv2.VideoCapture(os.path.join(tmpdir, "test_video_360.mp4"))

        assert encoded_video.get(cv2.CAP_PROP_FRAME_HEIGHT) == 360.0
        assert encoded_video.get(cv2.CAP_PROP_FRAME_WIDTH) == 480.0

        with pytest.raises(ValueError):
            process_video = Process(
                in_path="test_video.mp3",
                resolution="360",
                out_path=os.path.join(tmpdir, "test_video_360.mp3"),
            )
            process_video.encode_video
