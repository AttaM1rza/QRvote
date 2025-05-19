import ast
import os
from pathlib import Path
from threading import Thread
from typing import List, Union

import qrcode
from cv2 import (
    FONT_HERSHEY_SIMPLEX,
    LINE_AA,
    QRCodeDetector,
    destroyAllWindows,
    imshow,
    polylines,
    putText,
    waitKey,
)
from fpdf import FPDF

from config import pdf_output_file, voters_dir
from stream import Stream


class QRvote:
    window_name = "QRvote"
    streams: List[Stream] = []

    def __init__(self, sources: List[Union[int, Path]]):
        self.detector = QRCodeDetector()
        for source in sources:
            stream = Stream(camera_id=source, name=str(source))
            self.streams.append(stream)

    def detect_votes_from_camera_stream(self):
        for stream in self.streams:
            Thread(
                target=self.__detect_votes_from_camera_stream,
                args=(stream.name,),
                daemon=True,
            ).start()

        while True:
            for stream in self.streams:
                latest_frame = stream.latest_frame
                if latest_frame is not None:
                    imshow(stream.name, latest_frame)
                    print([f"{stream.name}:{stream.detected_voters}" for stream in self.streams])

            if waitKey(1) & 0xFF == ord("q"):
                break

        [stream.video_capture.release() for stream in self.streams]
        destroyAllWindows()
        waitKey(1)

    def __detect_votes_from_camera_stream(self, stream_name: str):
        stream = next((s for s in self.streams if s.name == stream_name), None)
        if stream is None:
            return
        while True:
            result, frame = stream.video_capture.read()
            if result:
                processed_frame, voters = self.detect_votes_from_frame(frame)
                stream.latest_frame = processed_frame
                stream.detected_voters = voters

    def detect_votes_from_frame(self, frame):
        result, multi_content, multi_corner_points, _ = self.detector.detectAndDecodeMulti(frame)
        detetected_voters = []
        if result:
            for content, corner_points in zip(multi_content, multi_corner_points):
                try:
                    content_dict = ast.literal_eval(content)
                    display_text = ", ".join(str(key) for key in content_dict.values())
                    detetected_voters.append(content_dict["id_number"])
                    frame = self.__make_detected_qrcodes_visible(frame, corner_points)
                    frame = self.__label_detected_qrcodes(frame, corner_points, display_text)
                except Exception:
                    pass
        return frame, detetected_voters

    def __label_detected_qrcodes(self, frame, corner_points, content):
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

    def __make_detected_qrcodes_visible(self, frame, corner_points):
        frame = polylines(
            img=frame,
            pts=[corner_points.astype(int)],
            isClosed=True,
            color=(0, 0, 255),
            thickness=5,
        )
        return frame

    @staticmethod
    def create_voting_qr_code(id_number: int, name: str):
        voter_data = {
            "id_number": id_number,
            "name": name,
        }
        # TODO implement DB connection to store the id_number and name and the corresponding qr_code for later use too.
        # TODO check if the id_number is already registered -> or a simplier approach would be to overwrite it
        qr_code_image = qrcode.make(voter_data)
        qr_code_image_path = os.path.join(voters_dir, f"{id_number}.png")
        if not os.path.exists(voters_dir):
            os.makedirs(voters_dir)
        qr_code_image.save(qr_code_image_path)
        return qr_code_image, qr_code_image_path

    @staticmethod
    def create_voting_qr_code_pdf(qr_code_image: Path, id_number: int, name: str):
        # TODO create templates
        # TODO add voting instructions and hadayaat/rules
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("helvetica", size=12)
        pdf.cell(text="Voting QR Code")
        pdf.cell(text=f"ID Number: {id_number}")
        pdf.cell(text=f"Name: {name}", ln=True)
        pdf.image(qr_code_image)
        pdf.output(pdf_output_file)
        return pdf_output_file
