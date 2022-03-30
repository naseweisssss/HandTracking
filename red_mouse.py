import cv2.cv2 as cv2
import numpy as np
import time
import pyautogui

#######################
wCam, hCam = 640, 480
wScr, hScr = pyautogui.size()
frameReduction = 100
smoothen = 4
#######################

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(3,wCam)
cap.set(4,hCam)

pTime = 0
coolingTime = 0

px,py = pyautogui.position()
cx,cy = pyautogui.position()

c = [148,117,115,173,236,239]

myColorValues = [[153,51,255],
                 [102,255,255],
                 [128,255,0]]

myPoints = []

def getContours(img):
    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    x,y,w,h = 0,0,0,0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 250:
            # cv2.drawContours(imgResult, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)
            x,y,w,h = cv2.boundingRect(approx)
            break
    return x+w//2, y


while True:
    # find landmark
    success, img = cap.read()
    img = cv2.flip(img,1)
    imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    lower = np.array(c[0:3])
    upper = np.array(c[3:6])
    mask = cv2.inRange(imgHSV, lower, upper)
    # cv2.imshow(str(c[0]), mask)  # testing
    x,y = getContours(mask)
 
    # convert coordinate
    x3 = np.interp(x,(frameReduction,wCam-frameReduction),(0,wScr-1))
    y3 = np.interp(y,(frameReduction,hCam-frameReduction),(0,hScr-1))
    # smoothen values
    cx = px + (x3-px)/smoothen
    cy = py + (y3-py)/smoothen
    # move mouse
    if pyautogui.onScreen(cx,cy):
        pyautogui.moveTo(cx, cy)
    px,py = cx,cy


    # fps
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f"FPS: {int(fps)}", (20,50), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,0), 2)

    # display
    cv2.imshow("Display", img)
    if cv2.waitKey(1)&0xFF == ord("q"):
        cv2.destroyAllWindows()
        break


