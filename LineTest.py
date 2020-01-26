from imutils.video.pivideostream import PiVideoStream
import detectLines
import imutils
import time
import cv2
import numpy as np

#vs = cv2.VideoCapture('/home/pi/Desktop/output5.mp4')
vs = PiVideoStream().start()
time.sleep(2)
i = 0

while i <= 1:
    frame = vs.read()
    
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    centerLine = detectLines.centerLine(gray)
    print(centerLine)
    for i in centerLine:
            cv2.line(frame, (i[0], i[1]), (i[2], i[3]), (255,0,255), 2)
    cv2.imshow("frame",frame)
    key = cv2.waitKey(50000) & 0xFF
    i += 1
    if key == ord("q"):
        break
    
vs.release()
cv2.destroyAllWindows()
