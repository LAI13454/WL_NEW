#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from spi_fun import SPI_FUN
from oled_display import OLED
from run import RUN
import threading
import json
import time
import sys

spi_fun = SPI_FUN(0)            #SPI通讯类初始化
oled = OLED()                   #OLED类初始化
run = RUN()                     #RUN类初始化，包括PID，灰度数据转偏移量

gray_data = []                  #灰度数据
g_speed_set = 0                 #当前速度设置值
speed_set_status = 0            #速度设置状态控制位，设置为0停止

speed_setH = 0
speed_setM = 0
speed_setL = 0

def run_fun():
    global gray_data
    global g_speed_set
    global speed_set_status
    global speed_setH
    global speed_setM
    global speed_setL
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
            if speed_set_status == 1:
                dif = run.gray_dif(gray_data,0)         #全白时，偏移量为0
            elif speed_set_status == 2:
                dif = run.gray_dif(gray_data,1)         #全白时，偏移向左
            elif speed_set_status == 3:
                dif = run.gray_dif(gray_data,2)         #全白时，偏移向右
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
spi_fun.set_steer_turn(0)   
time.sleep(1)
while True:
    try:
        walk_path_count = 0     #行走点位计数，知道自己走到哪一步，流程控制
        while True:             #当走到终点时退出循环
            if walk_path_count == 0:  #开机固定一段时间往前走,结束流程控制转为正常寻线模式
                print("STEP:"+str(walk_path_count)+str("直线行驶"))
                speed_set_status = 0    #关闭PID寻线控制
                print(speed_setM)
                spi_fun.set_motor(speed_setM)         
                spi_fun.set_steer_turn(0)   
                time.sleep(1)
                speed_set_status = 2    #切换到第二种寻线模式
                walk_path_count = walk_path_count + 1
            else:
                while True:
                    pass
    except KeyboardInterrupt:
        speed_set_status = 0
        spi_fun.set_steer_turn(0)
        spi_fun.set_motor(0)
        sys.exit()
