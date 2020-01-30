from imutils.video.pivideostream import PiVideoStream
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

def mainLoop():
    vs = PiVideoStream().start()
    time.sleep(2)
    baseFrame = None
    frameTimer = time.time()
    while True:
        frame = vs.read()
        HSV = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        white_mask = cv2.inRange(HSV, np.array([0, 0, 40]), np.array([360, 111, 255]))
        whiteSmooth = cv2.GaussianBlur(white_mask, (3, 3), 0)
        if baseFrame is None:
            baseFrame = whiteSmooth
        frameDelta = cv2.absdiff(whiteSmooth, baseFrame)
        thresh = cv2.threshold(frameDelta, 150, 255, cv2.THRESH_BINARY)[1]
        cv2.imshow('white_mask', whiteSmooth)
        cv2.imshow('thresh', thresh)
        cv2.imshow('frameDelta',frameDelta)
        cv2.imshow('baseFrame', baseFrame)
        #cv2.imshow('frame',frame)
        _, cnts, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
        im = np.copy(frame)
        cv2.drawContours(im,cnts, -1, (0,255,0), 1)
        
        
        key = cv2.waitKey(1) & 0xFF
        
        if (len(cnts) == 0 and time.time()- frameTimer > 3) or time.time() - frameTimer > 8:
            baseFrame = whiteSmooth
            print("New reference frame")
            frameTimer = time.time()

        
        #contours = imutils.grab_contours(cnts)
        
        for c in cnts:
            if cv2.contourArea(c) < 50:
                 continue
            print(cv2.contourArea(c))
            M = cv2.moments(c)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            cv2.circle(im, (cX, cY), 7, (255, 255, 255), -1)
        
        cv2.imshow('im',im)
        
        if key == ord("q"):
            break
    
    vs.stop()
    cv2.destroyAllWindows()

mainLoop()
