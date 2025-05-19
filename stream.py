from queue import Queue

from cv2 import (
    VideoCapture,
)

from threadsafe_list import ThreadSafeList


class Stream:
    __camera_id: int
    __video_capture: VideoCapture
    __name: str
    __frame_queue = Queue(maxsize=1)
    __detected_voters = ThreadSafeList()

    def __init__(self, camera_id: int, name: str):
        self.__camera_id = camera_id
        self.__video_capture = VideoCapture(self.__camera_id)
        self.__name = name

    @property
    def camera_id(self) -> int:
        return self.__camera_id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def latest_frame(self):
        if not self.__frame_queue.empty():
            frame = self.__frame_queue.get()
            return frame

    @latest_frame.setter
    def latest_frame(self, value):
        self.__frame_queue.put(value)

    @property
    def detected_voters(self):
        return self.__detected_voters

    @detected_voters.setter
    def detected_voters(self, value):
        self.__detected_voters = value

    @property
    def video_capture(self):
        return self.__video_capture
