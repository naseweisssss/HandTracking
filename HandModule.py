import math
import cv2.cv2 as cv2
import mediapipe as mp
import time
# removed , modelComplex=0
class handDetector():
    def __init__(self, mode=False, maxHands = 2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        # self.modelComplex = modelComplex
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        # removed , self.modelComplex
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [[4,5,17],8,12,16,20]

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # print(results.multi_hand_landmarks)
        if self.results.multi_hand_landmarks:
            for handles in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img,handles,self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self,img,handNo=0,draw=True):
        self.lmList =[]
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                # print(id,lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmList.append([id,cx,cy])
                if draw:
                    cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)
        return self.lmList

    def findDistance(self, pos1, pos2, img):
        x1, y1 = self.lmList[pos1][1:]
        x2, y2 = self.lmList[pos2][1:]
        cx, cy = (x1+x2)//2 , (y1+y2)//2
        length = math.hypot(x2-x1, y2-y1)
        return length, [x1,y1,x2,y2,cx,cy]

    def fingersUp(self):
        ans = []
        if (self.lmList[self.tipIds[0][0]][1] < self.lmList[self.tipIds[0][1]][1]) ^ (self.lmList[self.tipIds[0][0]][1] < self.lmList[self.tipIds[0][2]][1]):
            ans.append(1)
        else:
            ans.append(0)

        for i in range(1,5):
            if self.lmList[self.tipIds[i]][2] < self.lmList[self.tipIds[i]-2][2]:
                ans.append(1)
            else:
                ans.append(0)

        return ans



def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector = handDetector()
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img)
        if len(lmList) != 0:
            print(lmList[4])

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 0, 0), 3)
        cv2.imshow("Display", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == "__main__":
    main()