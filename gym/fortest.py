from brm2 import GestureDetector
import cv2
import virt2

#gesture_detector = GestureDetector()
#gesture_detector.run()
virt2.main()

while True:

    if cv2.waitKey(1) == ord('q'): 
        break

cv2.destroyAllWindows()
