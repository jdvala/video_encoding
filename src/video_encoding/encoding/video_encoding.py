import os
from collections import namedtuple

import cv2
import s3fs
import structlog
from moviepy.editor import AudioFileClip, VideoClip, VideoFileClip

from video_encoding.encoding.local import create_temp_folder
from video_encoding.encoding.utils import clean_up, get_file_name_extension
from video_encoding.encoding.video_information import get_video_information
from video_encoding.properties.video_format import VideoFormat
from video_encoding.properties.video_resolution import VideoResolution

encoding_logger = structlog.get_logger(component="video_encoding")


class Process:
    def __init__(self, in_path: str, out_path: str, resolution: str) -> None:
        """Process and convert the incoming video into the resolution provided.

        Args:
            in_path (str): Input path to the video to be encoded.
            out_path (str): Path to store the encoded video.
            resolution (str): Value of the resolution to which the video is to be converted.
            convert (bool): If True convert the video.
            extract_audio (bool): If True extract audio.
        """
        self.in_path = in_path
        self.out_path = out_path
        self.audio = None
        self.resolution = resolution
        self.out_height = None
        self.out_width = None

        encoding_logger.info(
            "Initialization complete.",
            in_path=self.in_path,
            resolution=self.resolution,
            out_path=self.out_path,
        )

    @property
    def load_video(self):
        video = cv2.VideoCapture(self.in_path)
        return video

    def get_height_width_res(self) -> namedtuple:
        """Get the height and width for a given resolution.

        Returns:
            namedtuple: Height and width for a given resolution.
        """
        res = VideoResolution()
        named = res.get_w_h(self.resolution)
        return named

    def extract_audio(self) -> AudioFileClip:
        """Extract audio from video.

        Returns:
            AudioFileClip: Audio extracted from the video.
        """
        video = VideoFileClip(self.in_path)

        self.audio = video.audio
        encoding_logger.info("Audio extraction complete", in_path=self.in_path)
        breakpoint()
        return self.audio

    def encode_audio(self, temp_video_path: str) -> VideoFileClip:
        """Encode the audio into resized video.

        Args:
            temp_video_path (str): Temporary file path where the resized video is stored.

        Returns:
            VideoFileClip : Final resized video to choosen resolution.
        """
        audio = self.extract_audio
        encoding_logger.info("Splitting of Audio and Video done.")

        video = VideoFileClip(temp_video_path)
        final = video.set_audio(self.audio)

        return final

    def writer_setup(
        self, temp_path: str, fps: float, codec: str, width: int, height: int
    ) -> cv2.VideoWriter:
        """Video writer setup according to the original frame per second, codec, width and height.

        Here it is ensured that we preseve the original codec and frames per second (fps) of the original video. Hence the fps and the codec are extracted from the video information before the conversion of the video.

        Args:
            temp_path (str): Temporary path where encoded video is stored.
            fps (float): Frame per second of the original video before encoding. This is to preserve the fps from the original video.
            codec (str): Video coded to be used. This is determined by the extension currently.
            width (int): Width to set according to the resolution.
            height (int): Height to set according to the resolution.

        Returns:
            cv2.VideoWriter: OpenCV video writer object with the settings from the original video.
        """
        fourcc = cv2.VideoWriter_fourcc(*f"{codec}")
        writer = cv2.VideoWriter(temp_path, fourcc, fps, (width, height))
        return writer

    def convert(
        self, video: cv2.VideoCapture, writer: cv2.VideoWriter, width: int, height: int
    ) -> None:
        """Convert the video frame by frame into the provided resolution frame by frame.

        # TODO: Make this function parallel.

        Args:
            video (cv2.VideoCapture): Video that is to be encoded into a given resolution.
            writer (cv2.VideoWriter): Video writer which writes the encoded video frame by frame.
            width (int): Width according to the resolution to be set for the video.
            height (int): Height according to the resolution to be set for the video.
        """
        while True:
            ret, frame = video.read()
            if ret == True:
                frame_resized = cv2.resize(
                    frame,
                    dsize=(width, height),
                    fx=0,
                    fy=0,
                    interpolation=cv2.INTER_CUBIC,
                )
                writer.write(frame_resized)
            else:
                break
        video.release()
        writer.release()
        encoding_logger.info("Cleaning up video conversion.")
        cv2.destroyAllWindows()

    @property
    def encode_video(self) -> None:
        """Encode the video and perform the process of conversion of and saving the video."""
        # read the video file with opencv
        encoding_logger.info("Reading video file from ", in_path=self.in_path)

        res = self.get_height_width_res()

        cap_video = self.load_video

        # Generate the information of the video
        file_name, file_extension = get_file_name_extension(self.in_path)

        encoding_logger.info(
            "File name and extension read complete",
            name=file_name,
            extension=file_extension,
        )

        video_information = get_video_information(cap_video)
        encoding_logger.info(
            "Video Information",
            frame_rate=video_information.frame_rate,
            width=video_information.width,
            height=video_information.height,
            total_frames=video_information.total_frames,
        )

        encoding_logger.info("Setting up the encoder")

        ext = file_extension.strip(".").upper()
        # find the codec based on extension
        if not ext in VideoFormat.list():
            encoding_logger.error(
                "Invalid Format of the video",
                extension=file_extension,
                allowed_extensions=VideoFormat.list(),
            )
            return

        codec = VideoFormat[ext].value
        encoding_logger.info("Setting up codec", codec=codec)

        temp_folder = create_temp_folder()
        encoding_logger.info("Temporary folder created at ", temp_folder=temp_folder)

        temp_path_with_res = os.path.join(
            temp_folder.name, f"{file_name}_{self.resolution}{file_extension}"
        )

        writer = self.writer_setup(
            temp_path=temp_path_with_res,
            fps=video_information.frame_rate,
            codec=codec,
            width=res.width,
            height=res.height,
        )
        encoding_logger.info("Writer setup complete.")

        encoding_logger.info("Converting Video.")
        self.convert(video=cap_video, writer=writer, width=res.width, height=res.height)
        final_file = self.encode_audio(temp_path_with_res)

        encoding_logger.info("Encoding audio done, patching things up.")
        final_file.write_videofile(self.out_path, fps=video_information.frame_rate)
        encoding_logger.info("Cleaning up.")
        clean_up(temp_folder.name)
