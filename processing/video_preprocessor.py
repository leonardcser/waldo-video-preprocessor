from dataclasses import dataclass
from pathlib import Path
import time
from typing import Union
import cv2
import numpy as np
from utils.arg_parser import ArgParser

from utils.logger import logger
from processing.io_video_manager import IOVideoManager
from processing.video_file_stream import VideoFileStream


@dataclass
class VPOptions(object):
    """Dataclass for 'VideoPreprocessor' options"""

    fps: int
    width: Union[int, None]
    height: Union[int, None]
    cxmin: Union[int, None]
    cxmax: Union[int, None]
    cymin: Union[int, None]
    cymax: Union[int, None]
    gray: bool
    silent: bool


class VideoPreprocessor(object):
    """VideoPreprocessor class that processes a video file"""

    def __init__(
        self, vm: IOVideoManager, video_path_obj: Path, dest: Path, opts: VPOptions
    ) -> None:
        self._vm = vm
        self._video_path_obj = video_path_obj
        self._dest = dest
        self._opts = opts

    def _to_grayscale(self, img: np.array) -> np.array:
        """Converts an image to grayscale"""
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    def _resize(self, img: np.array, w: int, h: int) -> np.array:
        """Resizes an image"""
        return cv2.resize(img, (w, h))

    def _crop(
        self,
        img: np.array,
        cxmin: int,
        cxmax: int,
        cymin: int,
        cymax: int,
    ) -> np.array:
        """Crops an image"""
        return img[cymin:cymax, cxmin:cxmax]

    def _preprocess_frame(self, frame: np.array, metadata: dict) -> np.array:
        """Preprocess a frame with the given argument options"""

        new_frame = frame.copy()
        w = metadata["w"]
        h = metadata["h"]
        if self._opts.gray:
            new_frame = self._to_grayscale(new_frame)
        if self._opts.width or self._opts.height:
            w = self._opts.width or w
            h = self._opts.height or h
            new_frame = self._resize(new_frame, w, h)
        if self._opts.cxmin or self._opts.cxmax or self._opts.cymin or self._opts.cymax:
            cxmn = self._opts.cxmin
            cxmx = self._opts.cxmax
            cymn = self._opts.cymin
            cymx = self._opts.cymax

            vx, mx = ArgParser.validate_crop_axis(cxmn, cxmx, w, "x")
            vy, my = ArgParser.validate_crop_axis(cymn, cymx, h, "y")

            if all([vx, vy]):
                new_frame = self._crop(
                    new_frame,
                    cxmn or 0,
                    cxmx or w,
                    cymn or 0,
                    cymx or h,
                )
            else:
                for m in [mx, my]:
                    logger.error(m)
                exit(1)

        return new_frame

    def process(self) -> None:
        """Processes the video file path"""

        if not self._opts.silent:
            logger.info(f"Processing video '{self._video_path_obj['name']}'...")
        vfs = VideoFileStream(
            path=self._video_path_obj["path"].as_posix(), fps=self._opts.fps
        )
        meta = vfs.get_metadata()

        vfs.start()
        # Allow the buffer to start to fill
        time.sleep(1.0)

        count = 0
        while vfs.more():
            frame = vfs.read()
            # Saves the frames with frame-count
            folder_name = self._video_path_obj["name"].replace(".", "_")
            save_path = Path(f"{folder_name}/frame_{count}.png")
            self._vm.save_img(save_path, self._preprocess_frame(frame, meta))
            count += 1
        if not self._opts.silent:
            logger.success(
                f"Finished processing video '{self._video_path_obj['name']}'"
            )
