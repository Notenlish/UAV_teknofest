import subprocess
import threading
import random
import cv2
import numpy as np
from PIL import Image
from io import BytesIO
from ultralytics import YOLO
from ultralytics.engine.results import Results

# Assuming you have a function `load_yolov8_model` to load your YOLOv8 model
# and `run_yolov8_prediction` to run predictions on the frames


def load_yolov8_model():
    model = YOLO("iha.pt")
    return model


def run_yolov8_prediction(model: YOLO, frame):
    results: Results = model.predict(frame)
    # Run your YOLOv8 prediction here and return the result
    pass


quality = 30  # 0 - 100 (highest quality)
framerate = 20
v = random.randint(0, 1000)
filename = f"output-{v}.mp4"

gst_args = (
    "gst-launch-1.0",
    "nvarguscamerasrc",
    "!",
    "video/x-raw(memory:NVMM), width=1280, height=720, framerate=20/1, format=NV12",
    "!",
    "nvjpegenc",
    f"quality={quality}",
    "!",
    "image/jpeg, framerate=20/1",
    "!",
    "filesink",
    "location=/dev/stdout",
)

ffmpeg_args = (
    "ffmpeg",
    "-f",
    "image2pipe",
    "-framerate",
    "20",
    "-vcodec",
    "mjpeg",
    "-i",
    "-",
    "-r",
    "20",
    "-vcodec",
    "libx264",
    "-preset",
    "fast",
    "-pix_fmt",
    "yuv420p",
    "-f",
    "mp4",
    filename,
)


def gstreamer_pipeline(gst_args):
    return subprocess.Popen(gst_args, stdout=subprocess.PIPE)


def read_and_process_frames(pipe, model):
    while True:
        # Read frame length
        length_bytes = pipe.stdout.read(2)
        if len(length_bytes) != 2:
            break

        # Convert to length
        length = int.from_bytes(length_bytes, "big")

        # Read frame data
        frame_data = pipe.stdout.read(length)
        if len(frame_data) != length:
            break

        # Decode frame
        frame = Image.open(BytesIO(frame_data))
        frame = cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR)

        # Run YOLOv8 prediction
        predictions = run_yolov8_prediction(model, frame)

        # Process predictions (e.g., draw bounding boxes, save results, etc.)
        # ...


def main():
    model = load_yolov8_model()

    gst_pipe = gstreamer_pipeline(gst_args)

    read_thread = threading.Thread(
        target=read_and_process_frames, args=(gst_pipe, model)
    )
    read_thread.start()

    # Use ffmpeg to save the video output if needed
    ffmpeg_pipe = subprocess.Popen(ffmpeg_args, stdin=gst_pipe.stdout)

    read_thread.join()
    gst_pipe.terminate()
    ffmpeg_pipe.terminate()


if __name__ == "__main__":
    main()
