#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from spi_fun import SPI_FUN
from oled_display import OLED
from run import RUN
import threading
import json
import time

spi_fun = SPI_FUN(0)            #SPI通讯类初始化
oled = OLED()                   #OLED类初始化
run = RUN()                     #RUN类初始化，包括PID，灰度数据转偏移量

gray_data = []                  #灰度数据
g_speed_set = 0                 #当前速度设置值
speed_set_status = 1            #速度设置状态控制位，设置为0停止

def run_fun():
    global gray_data
    global g_speed_set
    global speed_set_status
    f = open("config.json",encoding='utf-8')
    setting = json.load(f)
    speed_setH = setting["Speed"]["SetH"]
    speed_setM = setting["Speed"]["SetM"]
    speed_setL = setting["Speed"]["SetL"]
    speed_ratio = setting["Speed"]["Ratio"]
    g_speed_set = speed_setH
    time_last = 0
    print("速度设置高速:%d,中速:%d,低速:%d"%(speed_setH,speed_setM,speed_setL))
    
    while True:
        gray_data = spi_fun.get_gray()      #获取寻线传感器的数据
        if(((time.time()-time_last) > 0.02) and (speed_set_status != 0)):   #20ms进行一次PID运算
            time_last = time.time()
            #print(gray_data)
            dif = run.gray_dif(gray_data)
            turn_out = run.turn_pid(dif)
            spi_fun.set_motor_left(int(g_speed_set+turn_out*speed_ratio))
            spi_fun.set_motor_right(int(g_speed_set-turn_out*speed_ratio))
            spi_fun.set_steer_turn(turn_out)
        else:
            while((time.time()-time_last) > 0.02):
                break
        #print(time.time())



oled_thread = threading.Thread(target=oled.display)
oled_thread.start()
run_thread = threading.Thread(target=run_fun)
print(spi_fun.get_gray())

run_thread.start()              #PID运算开启
while True:
   pass 
