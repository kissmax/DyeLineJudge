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


# construct the argument parser and parse the arguments
# GPIO.setmode(GPIO.BCM)
# GPIO.setwarnings(False)
# ap = argparse.ArgumentParser()
# ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
# args = vars(ap.parse_args())
# 
# right = 2
# line = 4
# left = 17
# #Initialize your pin
# GPIO.setup(left,GPIO.OUT)
# GPIO.setup(line,GPIO.OUT)
# GPIO.setup(right,GPIO.OUT)

vs = PiVideoStream().start()
time.sleep(2.0)
fps = FPS().start()

# initialize the first frame in the video stream
firstFrame = None
resetFrame = time.time()
prevPoints = []
goodContours = []

def sideOfLine(point0x, point0y, point1x, point1y, point2x, point2y):
    return (point1x - point0x)*(point2y-point0y) - (point2x - point0x)*(point1y - point0y)

def distanceBtw(point0x, point0y, point1x, point1y):
    return math.sqrt((point0x - point1x)**2 + (point0y - point1y)**2)

while True:
    frame = vs.read()

    if frame is None:
        break

    centerLine = detectLines.centerLine(frame)

    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0) 
    # if the first frame is None, initialize it
    if firstFrame is None:
        firstFrame = blurred
        resetFrame = time.time()
        continue

    # compute the absolute difference between the current frame and
    # first frame
    frameDelta = cv2.absdiff(firstFrame, blurred)
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

    # dilate the thresholded image to fill in holes, then find contours
    # on thresholded image
    thresh = cv2.dilate(thresh, None, iterations=2)
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    if (len(cnts) == 0 and time.time()-resetFrame > 3) or time.time() - resetFrame > 8:
        print("new frame")
        prevPoints = []
        goodContours = []
        firstFrame = blurred
        resetFrame = time.time()
        continue
    yOld = 0
#     for i in centerLine:
#          cv2.line(frame, (i[0], i[1]), (i[2], i[3]), (255,0,255), 2)
    # loop over the contours
    for c in cnts:
        # if the contour is too small, ignore it
        if cv2.contourArea(c) < 50:
            continue

        # compute the bounding box for the contour, draw it on the frame,
        # and update the text
        (x, y, w, h) = cv2.boundingRect(c)
#         
#         if y < 75 and yOld - y < 0:
#             continue
#         if abs(xOld - x < 100) or abs(yOld - y < 100):
#             continue
#         yOld = y
#         #print("cv2.rectangle(frame, (",x,",",y,"),(", x+w,",", y+h,"), (0, 255, 0), 2)")
#         
        # compute the center of the contour
        M = cv2.moments(c)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        if len(prevPoints) > 1:
            lastPoint = len(prevPoints) -1
            prevX = prevPoints[lastPoint][0]
            prevY = prevPoints[lastPoint][1]
            if distanceBtw(cX, cY, prevX, prevY) < 100:
                prevPoints.append([cX,cY])
                goodContours.append(c)
        else:
            prevPoints.append([cX,cY])
#  
        # draw the contour and center of the shape on the image
        
            
        #cv2.drawContours(frame, [c], -1, (0, 255, 0), 2)
        cv2.circle(frame, (cX, cY), 7, (255, 255, 255), -1)
 
        
        #cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    #frame,linePoints = detectLines.returnLines(frame)
#     for i in linePoints:
#         cv2.circle(frame, (i[0], i[1]), 4, (255,0,255), -1)
    xprev = 0
    yprev = 0
    lastdif = 0
    impacty = 0
    impactx = 0
    for i in prevPoints:
        if i == len(prevPoints)-1:
            break
        if xprev == 0 and yprev == 0:
            xprev = i[0]
            yprev = i[1]
        else:
            cv2.line(frame, (i[0], i[1]), (xprev, yprev), (255,0,255), 2)
            xprev = i[0]
            yprev = i[1]
        print(lastdif - (yprev - i[1]))
        if lastdif - (yprev - i[1]) > 10:
            impacty = yprev
            impactx = xprev
            break
        else:
            lastdif = yprev -i[1]
            xprev = i[0]
            yprev = i[1]
    #for j in goodContours:
#         cv2.drawContours(frame, [j], -1, (0, 255, 0), 2)
    cv2.circle(frame, (impactx, impacty), 10, (0, 255, 0), -1)
    
#     if time.time() - ledInd > 3:
#         GPIO.output(left,0)
#         GPIO.output(right,0)
#         GPIO.output(line,0)
#     if impactx != 0 and impacty != 0:
#         cv2.circle(frame, (impactx, impacty), 10, (0, 255, 0), -1)
#         if sideOfLine(130,85,100,250,impactx,impacty) > 0:
#             print("left")
#             GPIO.output(left,1)
#             ledInd = time.time()
#         elif sideOfLine(135,85, 175,250,impactx,impacty) < 0:
#             print("right")
#             GPIO.output(right,1)
#             ledInd = time.time()
#         else:
#             print("line")
#             GPIO.output(line,1)
#             ledInd = time.time()

    # if the `q` key is pressed, break from the loop

    cv2.imshow("frame",frame)
    key = cv2.waitKey(1) & 0xFF
    fps.update()
    
    if key == ord("q"):
        break


# cleanup the camera and close any open windows
GPIO.output(right,0)
GPIO.output(left,0)
GPIO.output(line,0)

fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
vs.stop()
cv2.destroyAllWindows()
