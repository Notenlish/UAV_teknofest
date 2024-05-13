import cv2
import numpy as np
from time import sleep

def transform(width, height, frame: cv2.Mat, points: list[list[np.int32]]):
    rows, cols, ch = frame.shape

    pts1 = points.astype(np.float32)
    pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])

    M = cv2.getPerspectiveTransform(pts1, pts2)

    result_frame = cv2.warpPerspective(frame, M, (300, 300))
    return result_frame


img = cv2.imread("qr/flower.webp")
height, width, channels = img.shape
print(height, width)
result = transform(
    width, height, img, np.array([[152, 65], [368, 52], [152, 387], [452, 390]])
)
cv2.imwrite("qr/result.webp", result)
sleep(10)