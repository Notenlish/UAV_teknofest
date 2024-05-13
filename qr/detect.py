import cv2
import numpy as np

detector = cv2.QRCodeDetector()


def detect(frame):
    retval, points = detector.detect(frame)

    if retval:
        frame = cv2.polylines(frame, points.astype(int), True, (0, 255, 0), 3)
        quad = points[0]
        print(quad)
        center = [0, 0]
        center[0] = (quad[0][0] + quad[1][0] + quad[2][0] + quad[3][0]) / 4
        center[1] = (quad[0][1] + quad[1][1] + quad[2][1] + quad[3][1]) / 4
        cv2.drawMarker(frame, np.array(center).astype(np.int32q), (0, 255, 0))
    else:
        retval = None
        decoded_info = None
    return retval, points, frame


cap = cv2.VideoCapture(0)

ret, frame = cap.read()
while ret:
    ret, frame = cap.read()
    # frame = contrast(frame)

    retval, points, frame = detect(frame)

    # it can detect at far distances but actually decoding is a problem,
    # we might need to scale up the detected area.
    if frame is not None and type(frame) == np.ndarray:
        cv2.imshow("Stream", frame)
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
