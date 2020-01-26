from imutils.video import VideoStream
from imutils.video.pivideostream import PiVideoStream
import detectLines
from imutils.video import FPS
import argparse
import imutils
import time
import cv2
import numpy as np
import RPi.GPIO as GPIO
import math


vs = PiVideoStream().start()
time.sleep(1.0)
#out = cv2.VideoWriter('/home/pi/Desktop/output11.mp4', cv2.VideoWriter_fourcc('M','P','4','V'), 200, (320,240))

while True:
    frame = vs.read()
    cv2.imshow("frame",frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
         break

#   out.write(frame)
    
#    if time.time() - timer > 30:
#        break
#out.release()
cv2.destroyAllWindows()

