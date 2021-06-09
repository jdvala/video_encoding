# video-encoding

video encoding via opencv-python

---

## Features
* Pure Python API for video encoding.
* Uses OpenCV to convert the video.
* Currently only supports local files


## Roadmap
* Add s3 support.
* Docker image.
* Setup Actions.
* Write tests.
* Helm chart for easy deployment.
* Multiprocessing in frame by frame video conversion.

## Quick Start
```python
from video_encoding.encoding.video_encoding import Process

encode = Process(in_path="path/to/file", resolution="360", out_path="path/to/file")

encode.encode_video
```

## Installation
**Stable Release:** `pip install video_encoding`<br>
**Development Head:** `pip install git+https://github.com/jdvala/video_encoding.git`

## Documentation
For full package documentation please visit [jdvala.github.io/video_encoding](https://jdvala.github.io/video_encoding).

## Development
See [CONTRIBUTING.md](CONTRIBUTING.md) for information related to developing the code.

## Important commands for development.
1. `pip install -e .[dev]`

    This will install your package in editable mode with all the required development
    dependencies (i.e. `tox`).

2. `make build`

    This will run `tox` which will run all your tests in both Python 3.6, Python 3.7,
    and Python 3.8 as well as linting your code.

3. `make clean`

    This will clean up various Python and build generated files so that you can ensure
    that you are working in a clean environment.

4. `cd docs && make html`

    This will generate and launch a web browser to view the most up-to-date
    documentation for your Python package.
