import cv2

def putText(img, texts, colors):
    cv2.putText(
    img, text=texts,
    org=(10,30), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
    fontScale=1, color=colors, thickness=2)
    #putText의 함수의 인수로 img, texts, colors를 받아와 화면에 글자를 띄우는 함수
    #coded by Junho Pyo
