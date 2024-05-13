import cv2
import numpy as np

detector = cv2.QRCodeDetector()

from kraken import lib, binarization
from PIL import Image


DEBUG = False


def getSign(v: float | int):
    if v > 0:
        return 1
    elif v < 0:
        return -1
    else:
        raise ValueError("Value is Zero, can't get sign")


def detect(frame):
    retval, points = detector.detect(frame)

    result_points = np.array([[0, 0], [0, 0], [0, 0], [0, 0]])

    if retval:
        if DEBUG:
            frame = cv2.polylines(frame, points.astype(int), True, (0, 255, 0), 3)
        quad = points[0]
        # get center
        center = [0, 0]
        center[0] = (quad[0][0] + quad[1][0] + quad[2][0] + quad[3][0]) / 4
        center[1] = (quad[0][1] + quad[1][1] + quad[2][1] + quad[3][1]) / 4

        for i, p in enumerate(quad):
            white_space = 35  # px

            diff_x = (center[0]) - p[0]
            diff_y = (center[1]) - p[1]

            add_x = -getSign(diff_x) * white_space
            add_y = -getSign(diff_y) * white_space

            p2 = np.array([p[0] + add_x, p[1] + add_y])
            result_points[i] = p2
            if DEBUG:
                cv2.line(
                    frame,
                    np.array(p).astype(np.int32),
                    p2.astype(np.int32),
                    (0, 0, 255),
                    3,
                )
                cv2.drawMarker(
                    frame,
                    p2.astype(np.int32),
                    (0, i * (255 // 4), 0),
                    markerSize=8,
                    thickness=2,
                )

        if DEBUG:
            cv2.drawMarker(
                frame,
                np.array(center).astype(np.int32),
                (0, 255, 0),
                markerSize=8,
                thickness=2,
            )
    else:
        retval = None
        decoded_info = None
    return retval, result_points, frame


def transform(width, height, frame: cv2.Mat, points: list[list[np.int32]]):
    rows, cols, ch = frame.shape
    for p in points:
        p[0] += 18  # half of whitespace
    points = np.array([points[0], points[1], points[3], points[2]])  # new points

    # points = np.array([points[0], points[3], points[1], points[2]])  # new points
    # np.array([points[0], points[1], points[3], points[2]])  # new points

    pts1 = points.astype(np.float32)
    pts2 = np.array([[0, 0], [width, 0], [0, height], [width, height]]).astype(
        np.float32
    )

    M = cv2.getPerspectiveTransform(pts1, pts2)

    new_frame = cv2.warpPerspective(frame, M, (450, 450))
    im_pil = Image.fromarray(new_frame)
    if im_pil is not None:
        try:
            im_pil = binarization.nlbin(im_pil, threshold=0.8, border=0.2)
        except lib.exceptions.KrakenInputException:  # Img is empty
            return None
        open_cv_image = np.array(im_pil.convert("RGB"))
        # Convert RGB to BGR
        result = open_cv_image[:, :, ::-1].copy()
    else:
        result = None
    print(result)

    return result


cap = cv2.VideoCapture(0)

ret, frame = cap.read()
while ret:
    ret, frame = cap.read()
    width = cap.get(3)
    height = cap.get(4)
    # frame = contrast(frame)

    retval, points, frame = detect(frame)

    frame2 = None
    if retval:
        frame2 = transform(width, height, frame, points)

    # it can detect at far distances but actually decoding is a problem,
    # we might need to scale up the detected area.
    if frame is not None and type(frame) == np.ndarray:
        cv2.imshow("Stream", frame)
        if cv2.waitKey(1) == 27 or cv2.waitKey(1) == ord("q"):
            break
    if frame2 is not None and type(frame2) == np.ndarray:
        cv2.imshow("QR", frame2)
        if cv2.waitKey(1) == 27 or cv2.waitKey(1) == ord("q"):
            break

cap.release()
cv2.destroyAllWindows()
print("end")


"""
[ 79.72906  295.32443 ]
  [168.       287.      ]
  [178.44711  370.92462 ]
  [ 88.370895 380.6626  ]
"""
