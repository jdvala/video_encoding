from collections import namedtuple

Resolution = namedtuple("Resolution", "width height")


class VideoResolution:
    """For all the resolutions."""

    def __init__(self):
        self.width = None
        self.height = None
        self.resolutions = {
            "360": {"width": 480, "height": 360},
            "480": {"width": 640, "height": 480},
            "720": {"width": 1280, "height": 720},
            "1080": {"width": 1920, "height": 1080},
        }

    def get_w_h(self, resolution):
        if not isinstance(resolution, str):
            raise ValueError(
                f"Resolution should of a string, but instead is of type {type(resolution)}"
            )
        items = self.resolutions.get(resolution)
        if not items:
            raise ValueError(
                f"Resolution provided is not valid, the values available currently are 360p, 480p, 720p, 1080p"
            )

        return Resolution(width=items["width"], height=items["height"])
