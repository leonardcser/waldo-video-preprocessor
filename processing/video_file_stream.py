from threading import Thread
from queue import Queue
import cv2
import numpy as np

# Stolen and modified from:
# https://www.pyimagesearch.com/2017/02/06/faster-video-file-fps-with-cv2-videocapture-and-opencv/


class VideoFileStream(Thread):
    """VideoFileStream Thread class that reads a video and puts it into a queue"""

    def __init__(self, path, fps, max_queue_size=128) -> None:
        Thread.__init__(self, daemon=True)
        # initialize the file video stream along with the boolean
        # used to indicate if the thread should be stopped or not
        self._stream = cv2.VideoCapture(path)
        self._stopped = False
        self._fps = fps
        # initialize the queue used to store frames read from
        # the video file
        self._Q = Queue(maxsize=max_queue_size)

    def get_metadata(self) -> dict:
        return {
            "fps": self._stream.get(cv2.CAP_PROP_FPS),
            "w": int(self._stream.get(cv2.CAP_PROP_FRAME_WIDTH)),
            "h": int(self._stream.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        }

    def read(self) -> np.array:
        # return next frame in the queue
        return self._Q.get()

    def more(self) -> bool:
        # return True if there are still frames in the queue
        return not self._stopped or not self._Q.empty()

    def _stop(self) -> None:
        # indicate that the thread should be stopped
        self._stopped = True

    def run(self) -> None:
        meta = self.get_metadata()
        # Get video fps
        curr_fps = meta["fps"]

        # Make sure that the requested fps is valid
        target_fps = min(self._fps, curr_fps)
        target_fps = max(target_fps, 1)
        fps_count_to_save = round(curr_fps / target_fps)

        count = 0
        # keep looping infinitely
        while True:
            # if the thread indicator variable is set, stop the
            # thread
            if self._stopped:
                return
            # otherwise, ensure the queue has room in it
            if not self._Q.full():
                # read the next frame from the file
                (grabbed, frame) = self._stream.read()
                # if the `grabbed` boolean is `False`, then we have
                # reached the end of the video file
                if not grabbed:
                    self._stop()
                    return
                if count % fps_count_to_save == 0:
                    # add the frame to the queue
                    self._Q.put(frame)
                count += 1
