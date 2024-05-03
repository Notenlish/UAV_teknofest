import cv2
import numpy as np
import time


def contrast(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    thresh = cv2.adaptiveThreshold(
        blur,
        225,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        21,
        3,  # this value is important
    )

    # Draw largest enclosing circle onto a mask
    mask = np.zeros(img.shape[:2], dtype=np.uint8)
    cnts, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Bitwise-and for result
    result = cv2.bitwise_and(img, img, mask=mask)
    result[mask == 0] = (255, 255, 255)

    inverted_thresh = cv2.bitwise_not(thresh)

    kernel = np.ones((2, 2), np.uint8)
    img_erosion = cv2.erode(inverted_thresh, kernel, iterations=1)

    # result = np.hstack((img_erosion, inverted_thresh))
    result = inverted_thresh
    return result


if __name__ == "__main__":
    img = cv2.imread("qr/test.jpg", -1)
    result = contrast(img)

    cv2.imwrite("qr/flower2.jpg", result)
