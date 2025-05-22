import os
from pathlib import Path
from threading import Thread
from typing import List, Union

import qrcode
from cv2 import (
    destroyAllWindows,
    imshow,
    waitKey,
)
from fpdf import FPDF

from config import pdf_output_file, voters_dir
from detection_strategy import DetectionStrategy
from stream import Stream


class QRvote:
    window_name = "QRvote"
    streams: List[Stream] = []

    def __init__(self, sources: List[Union[int, Path]], detection_strategy: DetectionStrategy):
        self.__detection_strategy = detection_strategy
        for source in sources:
            stream = Stream(camera_id=source, name=str(source))
            self.streams.append(stream)

    @property
    def detection_strategy(self) -> DetectionStrategy:
        return self.__detection_strategy

    @detection_strategy.setter
    def detection_strategy(self, detection_strategy: DetectionStrategy) -> None:
        self.__detection_strategy = detection_strategy

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
                processed_frame, voters = self.detection_strategy.detect_votes_from_frame(frame)
                stream.latest_frame = processed_frame
                stream.detected_voters = voters

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
