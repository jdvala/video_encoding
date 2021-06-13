import pytest

from video_encoding.properties.video_resolution import VideoResolution


@pytest.mark.parametrize(
    "resolution, width, height",
    [("360", 480, 360), ("480", 640, 480), ("720", 1280, 720), ("1080", 1920, 1080)],
)
def test_video_resolution_get_w_h(resolution, width, height) -> None:
    video_resolution = VideoResolution()

    assert video_resolution.get_w_h(resolution=resolution).width == width
    assert video_resolution.get_w_h(resolution=resolution).height == height

    with pytest.raises(
        ValueError,
        match="Resolution provided is not valid, the values available currently are 360p, 480p, 720p, 1080p",
    ):
        video_resolution.get_w_h(resolution="180")

    with pytest.raises(
        ValueError,
        match="Resolution should of a string, but instead is of type <class 'int'>",
    ):
        video_resolution.get_w_h(resolution=1)
