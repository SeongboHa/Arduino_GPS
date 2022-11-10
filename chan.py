import serial
import cv2
import numpy as np
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import time

# 블루투스 세팅
ser = serial.Serial(
        port='COM7',
        baudrate=9600,
)


def emergency(trigger):
    window =  np.zeros((200,400,3), np.uint8)
    if not (trigger):
        win = cv2.putText(window, "Safe", (10, 100), 5, 2, (255,120,120), 2, cv2.LINE_AA)
    else:
        win = cv2.putText(window, "Emergency", (10, 100), 5, 2, (110,110,255), 2, cv2.LINE_AA)
    cv2.imshow("window", win)
    cv2.waitKey(1)
        
if __name__ == "__main__":

    emergency_trigger = 0
    
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)
    
    driver.get('https://www.google.co.kr/maps/?hl=ko')
    time.sleep(3)
    search_box = driver.find_element_by_xpath('//*[@id="searchboxinput"]')
    
    while True:

        if ser.in_waiting != 0:
            content = ser.readline()        # 들어온 메시지 읽어서 content 변수에 저장
            content = content[:-1].decode() # 전송된 원본 데이터 형식을 우리가 쓸 수 있는 형식으로 변환
            print(content)
            latitude, longitude = content.split(',')

            msg = str(latitude) + " " + str(longitude)

            if emergency_trigger == 0:
                search_box.send_keys(msg)
                search_box.send_keys(Keys.RETURN)
            emergency_trigger = 1

        emergency(emergency_trigger)
    


        
