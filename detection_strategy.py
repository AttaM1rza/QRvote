from abc import ABC, abstractmethod

from cv2 import (
    FONT_HERSHEY_SIMPLEX,
    LINE_AA,
    polylines,
    putText,
)

from config import red_rgb


class DetectionStrategy(ABC):
    @abstractmethod
    def detect_votes_from_frame(self, frame):
        pass

    def label_detected_qrcodes(self, frame, corner_points, content):
        frame = putText(
            img=frame,
            text=content,
            org=corner_points[0].astype(int),
            fontFace=FONT_HERSHEY_SIMPLEX,
            fontScale=1,
            color=(0, 0, 0),
            thickness=2,
            lineType=LINE_AA,
        )
        return frame

    def make_detected_qrcodes_visible(self, frame, corner_points):
        frame = polylines(
            img=frame,
            pts=[corner_points.astype(int)],
            isClosed=True,
            color=red_rgb,
            thickness=5,
        )
        return frame
