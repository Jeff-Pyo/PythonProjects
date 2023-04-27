import pyautogui as pg
import keyboard
a = 0
b = 0
c = 1
array = ["EL203204", "LA034501", "LA031102", "BA002601", "EL501901"]
#pg.moveTo(590, 307, 2)
pg.sleep(3)
print(pg.position())
# pg.click(382, 15)  # 엑셀창


while c:
    # pg.press('winleft', presses=3)
    pg.hotkey('ctrl', 'v')
    pg.hotkey('enter')
    # key = input('press key: ')
    # if key == 'p':
    #     pg.hotkey('winleft', 'v')
    #     pg.hotkey('down')
    #     pg.hotkey('enter')



    c -= 1


while b:
   pg.doubleClick(217, 622)
   b -= 1


while a:
    key = keyboard.read_key()
    pg.click(371, 252) # 첫 행 ## 매 시도마다 최적화
    pg.sleep(1.3)
    pg.hotkey('ctrl', 'c')
    pg.click(366, 5) # 엑셀창 돌아오기
    pg.hotkey('ctrl', 'v')
    pg.click(944, 980) # 엑셀 한 칸 내리기
    a -= 1




