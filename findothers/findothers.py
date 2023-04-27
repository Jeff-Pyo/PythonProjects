import pyautogui
from PIL import Image
import numpy as np
import cv2


def preprocessing():
    img = Image.open("test.jpg")
    img = np.array(img)
    img = cv2.GaussianBlur(img, (3, 3), 0) # 가우시안 블러
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    coefficients = (0.001, 0, 1.2) # (h, s, v)
    scr = Image.fromarray(img)
    scr = scr.convert('L')
    scr.save('return.jpg')
    return scr

preprocessing()


##산업현장에서 모두 일치할 순 없다. 그래서 전처리 과정을 거쳐야 함
# 전처리 과정을 거친 이미지를 티칭 머신으로 학습하여 딥러닝 알고리즘 채택
      










####### 틀린그림찾기 ########
# import pyautogui
# from PIL import ImageChops
# import os
# import time
# import cv2
#
# print(pyautogui.position())
# # 좌측 이미지 좌상단 356, 221 우하단 955, 720
# # 우측 이미지 좌상단 967, 221 우하단 1567, 720
# # width = 611 height 509
# width = 611
# height = 509
# y_pos = 221
#
# src = pyautogui.screenshot(region=(356, y_pos, width, height))
# src.save('src.jpg')
#
# dest = pyautogui.screenshot(region=(967, y_pos, width, height))
# dest.save('dest.jpg')
#
# diff = ImageChops.difference(src, dest)
# diff.save('diff.jpg')
#
# while not os.path.exists('diff.jpg'):
#     time.sleep(1)
#
# src_img = cv2.imread('src.jpg')
# dest_img = cv2.imread('dest.jpg')
# diff_img = cv2.imread('diff.jpg')
#
# gray = cv2.cvtColor(diff_img, cv2.COLOR_BGR2GRAY)
# gray = (gray > 25) * gray
# contours, _ = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
#
# COLOR = (0, 200, 0)
# for cnt in contours:
#     if cv2.contourArea(cnt) > 25:
#         x, y, width, height = cv2.boundingRect(cnt)
#         cv2.rectangle(src_img, (x, y), (x + width, y + height), COLOR, 2)
#         cv2.rectangle(dest_img, (x, y), (x + width, y + height), COLOR, 2)
#         cv2.rectangle(diff_img, (x, y), (x + width, y + height), COLOR, 2)
#
#         to_x = x + (width // 2) + 356
#         to_y = y + (height // 2) + y_pos
#         pyautogui.click(to_x, to_y)
#
#
#
# #    cv2.imshow('src', src_img)
# #    cv2.imshow('dest', dest_img)
# #    cv2.imshow('diff', diff_img)
