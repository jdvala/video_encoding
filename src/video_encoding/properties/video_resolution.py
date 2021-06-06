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

    @property
    def width_360(self):
        return self.resolutions.get("360").get("width")

    @property
    def height_360(self):
        return self.resolutions.get("360").get("height")

    @property
    def width_480(self):
        return self.resolutions.get("480").get("width")

    @property
    def height_480(self):
        return self.resolutions.get("480").get("height")

    @property
    def width_720(self):
        return self.resolutions.get("720").get("width")

    @property
    def height_720(self):
        return self.resolutions.get("720").get("height")

    @property
    def width_1080(self):
        return self.resolutions.get("1080").get("width")

    @property
    def height_1080(self):
        return self.resolutions.get("1080").get("height")
