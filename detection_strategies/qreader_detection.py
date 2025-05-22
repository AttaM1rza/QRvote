import cv2
from qreader import QReader

from detection_strategy import DetectionStrategy


class QreaderDetection(DetectionStrategy):
    def detect_votes_from_frame(self, frame):
        detector = QReader(model_size="n")
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        detetected_voters = []
        multi_content, detections = detector.detect_and_decode(image=frame, return_detections=True)
        print(multi_content)
        for text, detection in zip(multi_content, detections):
            try:
                detetected_voters.append(text)
                corner_points = detection["quad_xy"]
                frame = self.make_detected_qrcode_visible(frame, corner_points)
                frame = self.label_detected_qrcode(frame, corner_points[0], text)
            # TODO confidence = detection["confidence"]
            except Exception:
                pass
        return frame, detetected_voters
