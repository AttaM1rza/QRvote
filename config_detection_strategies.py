from detection_strategies.cv2_detection import CV2detection
from detection_strategies.qreader_detection import QreaderDetection

detection_strategies = {
    "CV2detection": CV2detection(),
    "QreaderDetection": QreaderDetection(),
}
