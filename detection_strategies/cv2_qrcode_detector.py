import ast

from cv2 import (
    QRCodeDetector,
)

from detection_strategy import DetectionStrategy


class CV2QRCodeDetector(DetectionStrategy):
    def detect_votes_from_frame(self, frame):
        detector = QRCodeDetector()
        result, multi_content, multi_corner_points, _ = detector.detectAndDecodeMulti(frame)
        detetected_voters = []
        if result:
            for content, corner_points in zip(multi_content, multi_corner_points):
                try:
                    content_dict = ast.literal_eval(content)
                    display_text = ", ".join(str(key) for key in content_dict.values())
                    detetected_voters.append(content_dict["id_number"])
                    frame = self.make_detected_qrcodes_visible(frame, corner_points)
                    frame = self.label_detected_qrcodes(frame, corner_points, display_text)
                except Exception:
                    pass
        return frame, detetected_voters
