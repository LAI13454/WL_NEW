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
gray_data_two = []              #灰度侧面数据
g_speed_set = 0                 #当前速度设置值
speed_set_status = 0            #速度设置状态控制位，设置为0停止

speed_setH = 0
speed_setM = 0
speed_setL = 0

def run_fun():
    global gray_data
    global gray_data_two
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
    speed_ratio_B = setting["Speed"]["Ratio_B"]
    speed_ratio_S = setting["Speed"]["Ratio_S"]
    g_speed_set = speed_setH
    time_last = 0
    print("速度设置高速:%d,中速:%d,低速:%d"%(speed_setH,speed_setM,speed_setL))
    print("speed_ratio_B:%d"%speed_ratio_B)
    while True:
        gray_data = spi_fun.get_gray()      #获取寻线传感器的数据
        gray_data_two = spi_fun.get_gray_two()      #获取侧面传感器的数据
        if(((time.time()-time_last) > 0.02) and (speed_set_status != 0)):   #20ms进行一次PID运算
            time_last = time.time()
            #print(gray_data)
            if speed_set_status == 1:
                dif = run.gray_dif(gray_data,0)         #全白时，偏移量为0
            elif speed_set_status == 2:
                dif = run.gray_dif(gray_data,1)         #全白时，偏移向左
            elif speed_set_status == 3:
                dif = run.gray_dif(gray_data,2)         #全白时，偏移向右
            else:
                dif = run.gray_dif(gray_data,0)         #全白时，偏移量为0
            turn_out = run.turn_pid(dif)
            if speed_set_status != 4:
                spi_fun.set_motor_left(int(g_speed_set+turn_out*speed_ratio_S))
                spi_fun.set_motor_right(int(g_speed_set-turn_out*speed_ratio_S))
                spi_fun.set_steer_turn(turn_out)
            else:
                spi_fun.set_motor_left(int(g_speed_set+turn_out*speed_ratio_B))
                spi_fun.set_motor_right(int(g_speed_set-turn_out*speed_ratio_B))
                spi_fun.set_steer_turn(0)
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
        while True:             #当走到终点时退出循环
            print("STEP:"+str("直线行驶"))
            speed_set_status = 0    #关闭PID寻线控制
            print(speed_setM)
            spi_fun.set_motor(speed_setM)         
            spi_fun.set_steer_turn(0)
            time.sleep(1)
            speed_set_status = 2    #切换到第二种寻线模式

            print("STEP:"+str("上坡第一次停车准备"))
            while(not((gray_data_two[1] and gray_data_two[2]) and (gray_data_two[9] and gray_data_two[10]) and (not(gray_data_two[4] or gray_data_two[6] or gray_data_two[5])))):
                pass
            speed_set_status = 0    #停车
            spi_fun.set_motor(0)
            spi_fun.set_steer_turn(0)
            time.sleep(1)

            print("STEP:"+str("倒车"))
            spi_fun.set_motor(int(-speed_setL))
            spi_fun.set_steer_turn(0)
            count = 0    #当右边传感器检测到第0个点为黑线时并且整条只有一个黑点时，停车
            while(not((gray_data_two[0] == 1) and count == 1)):
                count = 0
                for i in gray_data_two:
                    if(i == 1):
                        count = count + 1
            spi_fun.set_motor(0)
            spi_fun.set_steer_turn(0)
            
            print("STEP:"+str("扫第一个物料"))
            spi_fun.set_steer_time_3(2,500,3,-400,4,-530,20)
            spi_fun.set_steer_time_1(1,0,10)

            spi_fun.set_steer_time_1(6,1000,10)
            print("STEP:"+str("抓第一个物料"))
            spi_fun.set_steer_time_3(2,400,3,-1000,4,-1000,30)
            
            spi_fun.set_steer_time_1(6,200,5)
            spi_fun.set_steer_time_3(2,500,3,-900,4,-900,20)
            
            spi_fun.set_steer_time_3(1,250,2,-100,3,400,20)
            spi_fun.set_steer_time_1(4,1000,10)
            time.sleep(2)
            spi_fun.set_steer_time_1(6,1000,5)

            print("STEP:"+str("第二个抓取点"))
            g_speed_set = speed_setL
            speed_set_status = 4
            while(not((gray_data_two[6] == 1) and (gray_data_two[7] == 1))):
                pass
            speed_set_status = 0
            spi_fun.set_motor(0)
            spi_fun.set_steer_turn(0)
            time.sleep(5)
            
            spi_fun.set_steer_time_3(2,500,3,-400,4,-530,20)
            spi_fun.set_steer_time_1(1,0,10)


            spi_fun.set_steer_time_3(2,400,3,-1000,4,-1000,20)
            spi_fun.set_steer_time_1(6,200,5)
            time.sleep(2)

            spi_fun.set_steer_time_3(2,500,3,-900,4,-900,20)

            spi_fun.set_steer_time_3(1,-50,2,-150,3,500,20)
            spi_fun.set_steer_time_1(4,900,10)
            time.sleep(2)
            spi_fun.set_steer_time_1(6,1000,5)
            print("STEP:"+str("第三个抓取点"))
            g_speed_set = speed_setL
            speed_set_status = 4
            count = 0    
            time.sleep(1)
            while(not((gray_data_two[5] == 1) or (not(gray_data_two[6])))):
                count = 0
                for i in gray_data_two:
                    if(i == 1):
                        count = count + 1

            speed_set_status = 0
            spi_fun.set_motor(0)
            spi_fun.set_steer_turn(0)
            time.sleep(5)

            spi_fun.set_steer_time_3(2,500,3,-400,4,-530,20)
            spi_fun.set_steer_time_1(1,0,10)


            spi_fun.set_steer_time_3(2,400,3,-1000,4,-1000,20)
            spi_fun.set_steer_time_1(6,200,5)

            spi_fun.set_steer_time_3(2,500,3,-900,4,-900,20)

            spi_fun.set_steer_time_3(1,-350,2,-150,3,500,20)
            spi_fun.set_steer_time_1(4,1000,10)
            time.sleep(2)
            spi_fun.set_steer_time_1(6,1000,5)

            print("STEP:"+str("第四个抓取点"))
            g_speed_set = speed_setL
            speed_set_status = 4
            time.sleep(0.5)
            while(not((gray_data_two[4]) and (gray_data_two[5]))):
                count = 0
                for i in gray_data_two:
                    if(i == 1):
                        count = count + 1

            speed_set_status = 0
            spi_fun.set_motor(0)
            spi_fun.set_steer_turn(0)
            time.sleep(5)

            print("STEP:"+str("第五个抓取点"))
            g_speed_set = speed_setL
            speed_set_status = 0
            spi_fun.set_motor(int(speed_setL))
            spi_fun.set_steer_turn(0)
            time.sleep(0.5)
            while(not((gray_data_two[11]) and (gray_data_two[10]) and (count == 2))):
                count = 0
                for i in gray_data_two:
                    if(i == 1):
                        count = count + 1

            speed_set_status = 0
            spi_fun.set_motor(0)
            spi_fun.set_steer_turn(0)
            time.sleep(5)
            
            print("STEP:"+str("下坡"))
            g_speed_set = speed_setM
            speed_set_status = 1
            time.sleep(5)

            while True:
                pass
    except KeyboardInterrupt:
        speed_set_status = 0
        spi_fun.set_steer_turn(0)
        spi_fun.set_motor(0)
        sys.exit()
