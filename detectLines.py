from imutils.video.pivideostream import PiVideoStream
import argparse
import imutils
import time
import cv2
import numpy as np
import math

def centerLine(frame):
    colorInt = 0
    centerLine = []
    tableEdge = []
    frame = cv2.GaussianBlur(frame,(99,99),cv2.BORDER_DEFAULT)
    edges = cv2.Canny(frame,150,300,apertureSize = 5) 
    lines = cv2.HoughLinesP(edges,1,np.pi/180,55,minLineLength = 80, maxLineGap = 25)
    if lines is not None:
            for line in lines:
                for x1,y1,x2,y2 in line:
                    #cv2.line(frame, (x1, y1), (x2, y2), (255,colorInt,255), 1)
                    colorInt += 50
                    yDif = y2-y1
                    xDif = x2-x1
                    if abs(yDif) > 50:
                        cv2.line(frame, (x1, y1), (x2, y2), (255,colorInt,255), 1)
                        centerLine.append([x1,y1,x2,y2])
#                     if abs(yDif) < 10 and abs(xDif) > 250:
#                         cv2.line(frame, (x1, y1), (x2, y2), (255,colorInt,255), 1)
#                    if abs(yDif) < 5:
#tableEdge.append([x1,y1,x2,y2])
   # cv2.imshow("edges",edges)
    return centerLine
