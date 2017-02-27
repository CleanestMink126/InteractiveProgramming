""" Experiment with face detection and image filtering using OpenCV """

import cv2
import numpy as np

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print('not working')
#     cap.open()
# print(cap.isOpened())
while cap.isOpened():
    # Capture frame-by-frame

    ret, frame = cap.read()
    ret = cap.set(3, 320)
    ret = cap.set(4, 240)
    # Display the resulting frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    cv2.imshow('frame', gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
