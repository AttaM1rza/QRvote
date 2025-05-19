import datetime
import os

import qrcode

from config import images_dir


def create_qr_code(text: str):
    qr_code_image = qrcode.make(text)
    current_date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    qr_code_image_path = os.path.join(images_dir, f"{current_date_time}.png")
    qr_code_image.save(qr_code_image_path)
    return qr_code_image, qr_code_image_path
