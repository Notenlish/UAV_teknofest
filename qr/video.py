import cv2
import numpy as np

from im_contrast import contrast

detector = cv2.QRCodeDetector()


def qr(frame):
    retval, decoded_info, points, straight_qrcode = detector.detectAndDecodeMulti(frame)

    if retval:
        frame = cv2.polylines(frame, points.astype(int), True, (0, 255, 0), 3)

        for s, p in zip(decoded_info, points):
            frame = cv2.putText(
                frame,
                s,
                p[0].astype(int),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                2,
                cv2.LINE_AA,
            )
    else:
        retval = None
        decoded_info = None
    return retval, decoded_info, frame


def qrdetect(frame):
    retval, points = detector.detect(frame)
    print(retval, points)
    if retval:
        frame = cv2.polylines(frame, points.astype(int), True, (255, 0, 0), 3)
    return retval, frame


cap = cv2.VideoCapture(0)

ret, frame = cap.read()
while ret:
    ret, frame = cap.read()
    frame = contrast(frame)

    retval, decoded, frame = qr(frame)
    retval2, frame = qrdetect(frame)

    # it can detect at far distances but actually decoding is a problem,
    # we might need to scale up the detected area.

    if frame is not None and type(frame) == np.ndarray:
        cv2.imshow("Stream", frame)
        if cv2.waitKey(1) == 27 or cv2.waitKey(1) == ord("q"):
            break

cap.release()
cv2.destroyAllWindows()
print("end")
