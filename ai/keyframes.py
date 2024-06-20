import cv2
import numpy as np
import os
import sys


def get_keyframes(video_name, video_folder, threshold=30, min_diff=350_000):
    video_path = os.path.join(video_folder, video_name)
    """
    Extracts keyframes from a video based on frame differences.

    :param video_path: Path to the input video file.
    :param threshold: Pixel-wise difference threshold to consider a frame as keyframe.
    :param min_diff: Minimum number of different pixels to consider a frame as keyframe.
    :return: List of keyframes as numpy arrays.
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError("Error opening video file")

    keyframes = []
    ret, prev_frame = cap.read()
    if not ret:
        raise ValueError("Error reading the first frame")

    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

    frame_idx = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_diff = cv2.absdiff(prev_gray, gray)
        non_zero_count = np.count_nonzero(frame_diff > threshold)

        if non_zero_count > min_diff:
            keyframes.append(frame)
            prev_gray = gray

        frame_idx += 1

    cap.release()
    return keyframes


def save_keyframes(video_name, keyframes, output_folder):
    """
    Saves the extracted keyframes to the specified output folder.

    :param keyframes: List of keyframes as numpy arrays.
    :param output_folder: Path to the folder where keyframes will be saved.
    """
    a = video_name.removesuffix(".mp4")
    for i, frame in enumerate(keyframes):
        filename = f"{output_folder}/keyframe_{a}_{i:04d}.jpg"
        cv2.imwrite(filename, frame)


def clean_keyframes(output_folder):
    for file in os.listdir(output_folder):
        path = os.path.join(output_folder, file)
        os.remove(path)


if __name__ == "__main__":
    video_folder = "input_vid"
    output_folder = "keyframes"

    args = sys.argv[1:]
    cmd = args[0]

    if cmd == "clean":
        clean_keyframes(output_folder)
    elif cmd == "keyframe":
        video_filename = args[1]
        frames = get_keyframes(video_filename, video_folder)
        print(len(frames))
        save_keyframes(video_filename, frames, output_folder)
