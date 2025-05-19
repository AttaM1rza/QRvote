import os

base_dir = os.path.dirname(os.path.abspath(__file__))
voters_dir = os.path.join(base_dir, "voters")
videos_dir = os.path.join(base_dir, "videos")
pdf_output_file = os.path.join(base_dir, "output.pdf")

dummy_camera_stream_1 = os.path.join(videos_dir, "camera_stream_1.mp4")
dummy_camera_stream_2 = os.path.join(videos_dir, "camera_stream_2.mp4")
dummy_camera_stream_little_1 = os.path.join(videos_dir, "camera_stream_little_1.mp4")


green_rgb = (0, 255, 0)
red_rgb = (0, 0, 255)
