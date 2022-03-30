import cv2.cv2 as cv2
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
cap.set(10,150)

# myColors = [[154,164,125,179,238,255],
#             [15,54,81,32,255,255],
#             [41,55,48,86,255,255]]

myColors = [[148,117,115,173,236,239]]

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

def findColor(img):
    imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    count=0
    newPoints = []
    for c in myColors:
        lower = np.array(c[0:3])
        upper = np.array(c[3:6])
        mask = cv2.inRange(imgHSV, lower, upper)
        # cv2.imshow(str(c[0]), mask)  # testing
        x,y = getContours(mask)
        print(x,y)
        cv2.circle(imgResult, (x,y), 8, myColorValues[count],cv2.FILLED)
        if x!=0 and y!=0:
            newPoints.append([x,y,count])
        count+=1
    return newPoints

def drawOnCanvas():
    for p in myPoints:
        cv2.circle(imgResult, (p[0],p[1]), 8, myColorValues[p[2]],cv2.FILLED)



while True:
    success, img = cap.read()
    img = cv2.flip(img,1)
    imgResult = img.copy()
    newPoints = findColor(img)
    if len(newPoints) != 0:
        for p in newPoints:
            myPoints.append(p)
    if len(myPoints) != 0:
        drawOnCanvas()
    cv2.imshow("video display", imgResult)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('r'):
        myPoints=[]
