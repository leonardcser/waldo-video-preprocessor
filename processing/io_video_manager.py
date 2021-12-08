import os
from pathlib import Path
from typing import List

import cv2
import numpy as np

from variables import (
    IS_DOCKER,
    MOUNT_IMAGE_DEST,
    MOUNT_IMAGE_SRC,
    VIDEO_FILE_EXTENSIONS,
)
from utils.logger import logger


class IOVideoManager(object):
    """IOVideoManager class to work with IO"""

    def __init__(self, src_folder: Path, dest_folder: Path, silent=False) -> None:
        self._src_folder = src_folder
        self._dest_folder = dest_folder
        # The '_silent' variable is currently not used but it could be useful for logging
        # purposes
        self._silent = silent

    def _log_found_files(self, file_names: List[str]) -> None:
        """Helper function to log all the valid files found in the src folder"""

        logger.info(f"Found {len(file_names)} valid file(s).")
        for f in file_names:
            logger.info(f"   - {f}")

    def get_video_paths(self) -> List[dict]:
        """Gets the paths of the videos in the src folder"""

        path_objs = []
        abs_src_folder = self._src_folder.absolute()
        for p in os.listdir(abs_src_folder.as_posix()):
            if p.lower().endswith(tuple(VIDEO_FILE_EXTENSIONS)):
                full_path = ""
                if IS_DOCKER:
                    full_path = Path(os.path.join(MOUNT_IMAGE_SRC, p))
                else:
                    full_path = Path(os.path.join(abs_src_folder.as_posix(), p))

                tmp = {"name": p, "path": full_path}
                path_objs.append(tmp)

        self._log_found_files([p_obj["name"] for p_obj in path_objs])
        return path_objs

    def save_img(self, dest_path: Path, image: np.array) -> None:
        """Saves a np.array with cv2 to dest folder"""
        full_save_path = ""
        if IS_DOCKER:
            full_save_path = os.path.join(MOUNT_IMAGE_DEST, dest_path.as_posix())
        else:
            full_save_path = os.path.join(
                self._dest_folder.as_posix(), dest_path.as_posix()
            )

        # Create dirs if they do not exist already
        os.makedirs(os.path.dirname(full_save_path), exist_ok=True)
        cv2.imwrite(full_save_path, image)
