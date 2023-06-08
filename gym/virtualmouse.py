import cv2
import time
import numpy as np
import hand_detector as hd
import pyautogui

wCam, hCam = 640, 480  # 카메라 화면의 가로와 세로 크기
frameR = 100  # 손을 감지할 프레임의 크기
smoothening = 1.3  # 움직임을 부드럽게 처리하기 위한 값

pTime = 0  # 이전 시간 초기화
plocX, plocY = 0, 0  # 이전 위치 초기화
clocX, clocY = 0, 0  # 현재 위치 초기화

cap = cv2.VideoCapture(0)  # 카메라 객체 생성
cap.set(3, wCam)  # 카메라 화면의 가로 크기 설정
cap.set(4, hCam)  # 카메라 화면의 세로 크기 설정
detector = hd.handDetector(detectionCon=0.7)  # 손 감지기 객체 생성
wScr, hScr = pyautogui.size()  # 화면의 가로와 세로 크기 가져오기
print(wScr, hScr)

while True:
    success, img = cap.read()  # 카메라로부터 영상 프레임 가져오기
    img = detector.findHands(img)  # 손 감지하기
    lmList, bbox = detector.findPosition(img)  # 손가락 위치 및 경계 상자 찾기
    output = img.copy()

    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]  # 검지 손가락 끝 위치
        x2, y2 = lmList[12][1:]  # 중지 손가락 끝 위치

        fingers = detector.fingersUp()  # 손가락 상태 가져오기
        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (205, 250, 255), -1)  # 사각형 그리기
        img = cv2.addWeighted(img, 0.5, output, 1 - .5, 0, output)  # 영상 합성

        # 검지 손가락만 펼쳐져 있는 경우: 이동 모드
        if fingers[1] == 1 and fingers[2] == 0:
            x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))  # 좌표 변환
            y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))  # 좌표 변환

            clocX = plocX + (x3 - plocX) / smoothening  # 값 부드럽게 처리
            clocY = plocY + (y3 - plocY) / smoothening  # 값 부드럽게 처리

            pyautogui.moveTo(wScr - clocX, clocY)  # 마우스 이동
            cv2.circle(img, (x1, y1), 6, (255, 28, 0), cv2.FILLED)  # 원 그리기
            plocX, plocY = clocX, clocY

        # 검지와 중지 손가락 모두 펼쳐져 있는 경우: 클릭 모드
        if fingers[1] == 1 and fingers[2] == 1: 
            length, img, lineInfo = detector.findDistance(8, 12, img)  # 손가락 사이의 거리 찾기

            if length < 40:  # 거리가 짧으면 클릭
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 6, (0, 255, 0), cv2.FILLED)  # 원 그리기
                pyautogui.click()

    if cv2.waitKey(1) & 0xFF == ord('q'):  # 'q' 키를 누르면 종료
        break

    cTime = time.time()  # 현재 시간
    fps = 1 / (cTime - pTime)  # 프레임 속도 계산
    pTime = cTime

    cv2.imshow("Virtual Mouse Monitor", cv2.flip(img, 1))  # 영상 출력
    cv2.setWindowProperty("Virtual Mouse Monitor", cv2.WND_PROP_TOPMOST, 1)  # 항상 위에 윈도우 유지
    cv2.waitKey(1)
