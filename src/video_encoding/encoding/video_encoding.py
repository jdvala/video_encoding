import os

import cv2
import s3fs
import structlog
from moviepy.editor import VideoClip, VideoFileClip

from video_encoding.encoding.local import create_temp_folder
from video_encoding.encoding.utils import clean_up, get_file_name_extension
from video_encoding.encoding.video_information import get_video_information
from video_encoding.properties.video_format import VideoFormat
from video_encoding.properties.video_resolution import VideoResolution

encoding_logger = structlog.get_logger(component="video_encoding")


class Process:
    def __init__(self, in_path, resolution, out_path):

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

    def set_height_width_out(self):
        res = VideoResolution()
        named = res.get_w_h(self.resolution)
        return named

    def split_audio_video(self):
        video = VideoFileClip(self.in_path)

        self.audio = video.audio
        encoding_logger.info("Audio extraction complete", in_path=self.in_path)
        return self.audio

    def combine_audio(self, video_in_path):

        video = VideoFileClip(video_in_path)
        final = video.set_audio(self.audio)

        return final

    def encode_audio(self, temp_video_path):
        audio = self.split_audio_video()
        encoding_logger.info("Splitting of Audio and Video done.")

        final = self.combine_audio(temp_video_path)
        return final

    def writer_setup(self, temp_path, fps, codec, width, height):

        fourcc = cv2.VideoWriter_fourcc(*f"{codec}")
        writer = cv2.VideoWriter(temp_path, fourcc, fps, (width, height))
        return writer

    def convert(self, video, writer, width, height):
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

    def encode_video(self):

        # read the video file with opencv
        encoding_logger.info("Reading video file from ", in_path=self.in_path)

        res = self.set_height_width_out()

        cap_video = cv2.VideoCapture(self.in_path)

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
        breakpoint()
        clean_up(temp_folder.name)
