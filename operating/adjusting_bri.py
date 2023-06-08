import wmi

def set_brightness(level):
    wmi_interface = wmi.WMI(namespace='wmi')     # WMI 인터페이스 초기화
    brightness_instance = wmi_interface.WmiMonitorBrightnessMethods()[0]   # 모니터 설정 변경을 위한 인스턴스 가져오기
    brightness_instance.WmiSetBrightness(level, 0)     # 밝기 레벨 설정