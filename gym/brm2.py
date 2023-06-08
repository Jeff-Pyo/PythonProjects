import cv2
import mediapipe as mp
import wmi

class GestureDetector:
    def __init__(self):
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_hands = mp.solutions.hands
        self.my_hands = self.mp_hands.Hands()
        self.cap = None

    def set_brightness(self, level):
        wmi_interface = wmi.WMI(namespace='wmi')
        brightness_instance = wmi_interface.WmiMonitorBrightnessMethods()[0]
        brightness_instance.WmiSetBrightness(level, 0)

    def run(self):
        self.cap = cv2.VideoCapture(0)

        with self.mp_hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as hands:
            while self.cap.isOpened():
                success, img = self.cap.read()
                h, w, c = img.shape

                if not success:
                    continue
                image = cv2.cvtColor(cv2.flip(img, 1), cv2.COLOR_BGR2RGB)

                results = self.my_hands.process(image)

                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        finger1 = int(hand_landmarks.landmark[4].x * 600)
                        finger2 = int(hand_landmarks.landmark[8].x * 600)

                        dist = int(abs(finger1 - finger2))
                        self.set_brightness(dist)

                        cv2.putText(
                            image, text='brightness=%d' % (dist), org=(10, 30),
                            fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1,
                            color=255, thickness=2)

                        self.mp_drawing.draw_landmarks(image, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                cv2.imshow('gesture detection', image)
        self.cap.release()
        cv2.destroyAllWindows()