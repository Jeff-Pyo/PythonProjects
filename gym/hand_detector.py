import math
import cv2
import mediapipe as mp
import time

class handDetector():
    def __init__(self, mode=False, maxHands=2, modelComplexity=1, detectionCon=0.5, trackCon=0.5):
        # handDetector 클래스의 생성자 메서드
        # 인스턴스 변수 초기화
        self.lmList = []  # 손의 랜드마크 좌표를 저장하는 리스트
        self.results = None  # 손 인식 결과를 저장하는 변수
        self.mode = mode  # 손 인식 모드
        self.maxHands = maxHands  # 인식할 최대 손의 개수
        self.modelComplex = modelComplexity  # 손 인식 모델의 복잡도
        self.detectionCon = detectionCon  # 손 인식의 신뢰도 임계값
        self.trackCon = trackCon  # 손 추적의 신뢰도 임계값

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modelComplex, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]  # 각 손가락의 끝 지점 인덱스

    def findHands(self, img, draw=True):
        # 이미지에서 손을 검색하고 필요에 따라 그림을 그림
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(rgb_img)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)

        return img

    def findPosition(self, img, handNo=0, draw=True):
        # 이미지에서 손의 위치를 찾아 손가락 끝 지점의 좌표와 바운딩 박스를 반환
        xList = []
        yList = []
        bbox = []
        self.lmList = []

        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]

            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                xList.append(cx)
                yList.append(cy)
                self.lmList.append([id, cx, cy])

                if draw:
                    cv2.circle(img, (cx, cy), 6, (0, 0, 255), cv2.FILLED)

            xmin, xmax = min(xList), max(xList)
            ymin, ymax = min(yList), max(yList)
            bbox = xmin, ymin, xmax, ymax

            if draw:
                cv2.rectangle(img, (bbox[0]-20, bbox[1]-20), (bbox[2]+20, bbox[3]+20), (0, 255, 0), 2)

        return self.lmList, bbox

    def fingersUp(self):
        # 손가락의 상태(펴짐 또는 접힘)를 반환
        fingers = []
        # 엄지 손가락
        if self.lmList[self.tipIds[0]][1] < self.lmList[self.tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        # 나머지 손가락
        for id in range(1, 5):
            if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers




    def findDistance(self, p1, p2, img, draw=True):
        # 두 지점 사이의 거리를 계산하고, 필요에 따라 그림을 그림
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (0, 255, 255), 3)
            cv2.circle(img, (x1, y1), 6, (0, 255, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 6, (0, 255, 255), cv2.FILLED)
            cv2.circle(img, (cx, cy), 6, (0, 255, 255), cv2.FILLED)

        length = math.hypot(x2 - x1, y2 - y1)

        return length, img, [x1, y1, x2, y2, cx, cy]




    def findAngle(self, p1, p2, p3, img, draw=True):
        # 세 지점을 이용하여 각도를 계산하고, 필요에 따라 그림을 그림
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        x3, y3 = self.lmList[p3][1:]
        angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
        if angle < 0:
            angle += 360

        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 3)
            cv2.line(img, (x3, y3), (x2, y2), (255, 255, 255), 3)
            cv2.circle(img, (x1, y1), 15, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x1, y1), 15, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (0, 0, 255), cv2.FILLED)

        return angle
