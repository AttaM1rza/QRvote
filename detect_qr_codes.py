from pathlib import Path

from cv2 import (
    FONT_HERSHEY_SIMPLEX,
    LINE_AA,
    QRCodeDetector,
    VideoCapture,
    destroyAllWindows,
    destroyWindow,
    imshow,
    polylines,
    putText,
    waitKey,
)

from config import green_rgb, red_rgb


def detect_qr_code_from_image(qr_codes_image):
    detector = QRCodeDetector()

    result, qr_codes_content, qr_codes_corner_points, _ = detector.detectAndDecodeMulti(
        qr_codes_image
    )
    if not result:
        raise ValueError("No QR codes found in the image.")

    bordered_qr_codes_image = polylines(
        qr_codes_image, qr_codes_corner_points.astype(int), True, green_rgb, 5
    )

    for text, corner_points in zip(qr_codes_content, qr_codes_corner_points):
        output_image = putText(
            bordered_qr_codes_image,
            text,
            corner_points[0].astype(int),
            FONT_HERSHEY_SIMPLEX,
            1,
            red_rgb,
            2,
            LINE_AA,
        )
    imshow("QR Codes", output_image)
    waitKey(0)
    destroyAllWindows()
    return


def detect_from_camera_stream(camera_id: Path):
    window_name = "OpenCV QR Code"

    detector = QRCodeDetector()
    capturer = VideoCapture(camera_id)

    while True:
        result, frame = capturer.read()

        if result:
            result_qr, qr_codes_content, qr_codes_corner_points, _ = detector.detectAndDecodeMulti(
                frame
            )
            if result_qr:
                for text, corner_points in zip(qr_codes_content, qr_codes_corner_points):
                    color = green_rgb if text else red_rgb

                    frame = polylines(frame, [corner_points.astype(int)], True, color, 5)
                    frame = putText(
                        frame,
                        text,
                        corner_points[0].astype(int),
                        FONT_HERSHEY_SIMPLEX,
                        1,
                        red_rgb,
                        2,
                        LINE_AA,
                    )
            imshow(window_name, frame)

        if waitKey(0):
            break

    destroyWindow(window_name)
    return
