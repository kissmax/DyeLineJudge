from imutils.video.pivideostream import PiVideoStream
import argparse
import detectLines
import imutils
import time
import cv2
import numpy as np
import math

def sideOfLine(point0x, point0y, point1x, point1y, point2x, point2y):
    return (point1x - point0x)*(point2y-point0y) - (point2x - point0x)*(point1y - point0y)

def distanceBtw(point0x, point0y, point1x, point1y):
    return math.sqrt((point0x - point1x)**2 + (point0y - point1y)**2)

vs = PiVideoStream().start()
time.sleep(2)
#vs = cv2.VideoCapture('/home/pi/Desktop/output7.mp4')
baseFrame = None
prevPoints = []
centerLine = [[96,225,155,35],[202,225,164,35]]
while True:
    frame = vs.read()
    #if ret != True:
        #break

    #if frame is not None:
#        leftLine = centerLine[0]
#        print(leftLine)
#        cv2.line(frame, (leftLine[0], leftLine[1]), (leftLine[2], leftLine[3]), (255,0,255), 2)
#         for i in centerLine:
#            cv2.line(frame, (i[0], i[1]), (i[2], i[3]), (255,0,255), 2)

    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    #blurred = cv2.GaussianBlur(gray, (1, 1), 0) 
    if baseFrame is None:
        #centerLine = detectLines.centerLine(gray)
#         while len(centerLine) != 2:
#             frame = vs.read()
#             gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
#             centerLine = detectLines.centerLine(gray)
        baseFrame = gray
        resetFrame = time.time()

    # compute the absolute difference between the current frame and
    # first frame
    frameDelta = cv2.absdiff(baseFrame, gray)
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

    # dilate the thresholded image to fill in holes, then find contours
    # on thresholded image
    thresh = cv2.dilate(thresh, None, iterations=2)
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

#         for i in centerLine:
#             cv2.line(frame, (i[0], i[1]), (i[2], i[3]), (255,0,255), 2)
    if (len(cnts) == 0 and time.time()-resetFrame > 3) or time.time() - resetFrame > 8:
        print("New frame")
        prevPoints = []
        baseFrame = gray
        resetFrame = time.time()
    min1 = min(centerLine[0][0],centerLine[0][2])
    min2 = min(centerLine[1][0],centerLine[1][2])
    if min1 < min2:
        leftLine = centerLine[0]
        rightLine = centerLine[1]
    else:
        leftLine = centerLine[1]
        rightLine = centerLine[0]

    for c in cnts:
        # if the contour is too small, ignore it
        if cv2.contourArea(c) < 100:
            continue
        if cv2.contourArea(c) > 500:
            continue
      
        # compute the center of the contour
        M = cv2.moments(c)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        print(cY)
        if len(prevPoints) > 1:
            lastPoint = len(prevPoints) -1
            prevX = prevPoints[lastPoint][0]
            prevY = prevPoints[lastPoint][1]
            if distanceBtw(cX, cY, prevX, prevY) < 50:
                prevPoints.append([cX,cY])
        else:
            prevPoints.append([cX,cY])
        
        cv2.circle(frame, (cX, cY), 7, (255, 255, 255), -1)
 
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
#             else:
#                 cv2.line(frame, (i[0], i[1]), (xprev, yprev), (255,0,255), 2)
#                 xprev = i[0]
#                 yprev = i[1]
        cv2.line(frame, (i[0], i[1]), (xprev, yprev), (255,0,255), 2)
        #print(lastdif - (yprev - i[1]))
        if lastdif - (yprev - i[1]) < -10:
            impacty = yprev
            impactx = xprev
            cv2.circle(frame, (impactx, impacty), 10, (0, 255, 0), -1)
            break
        else:
            lastdif = yprev - i[1]
            xprev = i[0]
            yprev = i[1]
        

#     if time.time() - ledInd > 3:
#         GPIO.output(left,0)
#         GPIO.output(right,0)
#         GPIO.output(line,0)
    #Draw leftLine
    cv2.line(frame, (leftLine[0], leftLine[1]), (leftLine[2], leftLine[3]), (255,0,255), 2)
    #Draw rightLine
    cv2.line(frame, (rightLine[0], rightLine[1]), (rightLine[2], rightLine[3]), (0,0,255), 2)
    if impactx != 0 and impacty != 0:
#             print("left: ",sideOfLine(leftLine[0],leftLine[1],leftLine[2],leftLine[3],impactx,impacty))
#             print("right: ",sideOfLine(rightLine[0],rightLine[1],rightLine[2],rightLine[3],impactx,impacty))
        if sideOfLine(leftLine[0],leftLine[1],leftLine[2],leftLine[3],impactx,impacty) < 0:
            print("left")
#                 GPIO.output(left,1)
#                 ledInd = time.time()
        elif sideOfLine(rightLine[0],rightLine[1],rightLine[2],rightLine[3],impactx,impacty) < 0:
            print("right")
#                 GPIO.output(right,1)
#                 ledInd = time.time()
        else:
            print("line")
#                 GPIO.output(line,1)
#                 ledInd = time.time()

    cv2.imshow("frame",frame)
    key = cv2.waitKey(1) & 0xFF
    
    if key == ord("q"):
        break
        
#     else:
#         break

    
    
vs.stop()
#vs.release()
cv2.destroyAllWindows()


