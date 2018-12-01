#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from spi_fun import SPI_FUN
from oled_display import OLED
from run import RUN
import RPi.GPIO as GPIO
import threading
import json
import time
import sys
import os
import serial

GPIO.setmode(GPIO.BCM)
GPIO.setup(4,GPIO.IN,pull_up_down=GPIO.PUD_UP)


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

goods_data = ["ZJGXDS01","ZJGXDS03","ZJGXDS04","ZJGXDS06","ZJGXDS07","ZJGXDS09"]
goods_place_info = ["ZJGXDS10","ZJGXDS05","ZJGXDS09","ZJGXDS04","ZJGXDS08","ZJGXDS03","ZJGXDS07","ZJGXDS02","ZJGXDS06","ZJGXDS01"]
goods_place_data = [0,0,0,0,0]
goods_place_count = 1

par_run_flag = False            #程序运行标志

camera_data = None

def restart_program():
    python = sys.executable
    os.execl(python,python, * sys.argv)

def button_fun():
    if(GPIO.input(4) == 1):
        if par_run_flag == True:
            spi_fun.set_motor(0)         
            print("复位程序")
            restart_program()
    else:
        pass
        #print("未触发复位")
    #time.sleep(3)
print("程序运行")
#button_thread = threading.Thread(target=button_fun)
#button_thread.start()

def camera_use():
    global camera_data
    str_data = []
    for i in range(0,8):
        str_data.append(0)
    ser = serial.Serial("/dev/ttyAMA0",115200)
    while True:
        #print("条形码识别")
        #data = ser.read()
        if(str(ser.read(),encoding="utf8") == 'Z'):
            str_data[0] = 'Z'
            for i in range(1,8):
                data = str(ser.read(),encoding="utf8")
                str_data[i] = data
            camera_data = ''.join(str_data)
            print(camera_data)          
        """try:
            data = str(data, encoding = "utf8") 
        except UnicodeDecodeError:
            pass
        print(str_data)
        if len(data) > 5:
            camera_data = data[0:8]
            print(camera_data)
        else:
            camera_data = None
"""

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
            button_fun()
        else:
            while((time.time()-time_last) > 0.02):
                break
        #print(time.time())
def code_fun():
    global camera_data
    temp = camera_data
    camera_data = None
    return temp 

def steer_catch_code():         #抓物料前扫码
    global camera_data
    spi_fun.set_steer_time_3(2,500,3,-400,4,-570,20)
    spi_fun.set_steer_time_1(1,0,10)
    spi_fun.set_steer_time_1(6,1000,10)
    spi_fun.set_steer_time_1(5,900,5)
    spi_fun.set_steer_time_1(2,550,5)
    camera_data = None

def steer_catch_goods():        #从取物台抓物料
    spi_fun.set_steer_time_3(2,470,3,-440,4,-830,30)
    spi_fun.set_steer_time_1(2,420,10)
    spi_fun.set_steer_time_1(6,100,5)
    spi_fun.set_steer_time_3(2,550,3,-400,4,-750,20)
    #spi_fun.set_steer_time_3(2,500,3,-900,4,-900,20)
def steer_catch_place_m1():     #放到右侧第一个载物台
    print("放到右侧第一个")
    spi_fun.set_steer_time_3(1,250,2,-200,3,800,20)
    spi_fun.set_steer_time_1(5,-400,5)
    spi_fun.set_steer_time_1(4,0,20)
    spi_fun.set_steer_time_1(6,1000,5)
def steer_catch_place_m2():     #放到右侧第二个载物台
    print("放到右侧第二个")
    spi_fun.set_steer_time_3(1,-50,2,-200,3,1000,20)
    spi_fun.set_steer_time_1(5,-400,5)
    spi_fun.set_steer_time_1(4,-300,20)
    spi_fun.set_steer_time_1(6,1000,5)

def steer_catch_place_m3():     #放到右侧第三个载物台
    print("放到右侧第三个")
    spi_fun.set_steer_time_3(1,-380,2,-250,3,800,20)
    spi_fun.set_steer_time_1(5,-400,5)
    spi_fun.set_steer_time_1(4,0,20)
    spi_fun.set_steer_time_1(6,1000,5)


def steer_catch_place():        #放物料到物料架
    global goods_place_count
    print("放%d位"%goods_place_count)
    if(goods_place_count == 1):
        steer_catch_place_m1()
    elif(goods_place_count == 2):
        steer_catch_place_m2()
    elif(goods_place_count == 3):
        steer_catch_place_m3()
    goods_place_count = goods_place_count + 1

def steer_place_code_bottom():
    print("放下层物料")
    spi_fun.set_steer_time_3(2,750,3,-700,4,-260,20)
    spi_fun.set_steer_time_3(5,900,1,50,6,1000,20)
def steer_place_code_top():
    print("放上层物料")
    spi_fun.set_steer_time_3(2,500,3,-700,4,320,20)
    spi_fun.set_steer_time_3(5,900,1,50,6,1000,20)
def steer_place_catch_m1():
    steer_place_code_bottom()
    print("抓第一个" )
    spi_fun.set_steer_time_1(1,250,10)
    spi_fun.set_steer_time_2(2,200,3,50,20)
    spi_fun.set_steer_time_1(4,650,10)
    spi_fun.set_steer_time_1(6,100,10)
    spi_fun.set_steer_time_1(2,0,10)
    spi_fun.set_steer_time_1(5,-400,10)
def steer_place_catch_m2():
    steer_place_code_bottom()
    spi_fun.set_steer_time_3(1,-40,2,100,3,270,20)
    spi_fun.set_steer_time_1(4,500,10)
    spi_fun.set_steer_time_1(6,100,10)
    spi_fun.set_steer_time_1(2,-100,10)
    spi_fun.set_steer_time_1(5,-400,10)
def steer_place_catch_m3():
    steer_place_code_bottom()
    print("抓第三个")
    spi_fun.set_steer_time_1(1,-380,10)
    spi_fun.set_steer_time_2(2,-100,3,550,20)
    spi_fun.set_steer_time_1(4,400,20)
    spi_fun.set_steer_time_1(6,100,10)
    spi_fun.set_steer_time_1(2,-300,10)
    spi_fun.set_steer_time_1(5,-400,10)

def steer_place_goods_bottom():
    spi_fun.set_steer_time_3(2,800,3,-500,4,-868,20)
    spi_fun.set_steer_time_1(1,0,10)
    spi_fun.set_steer_time_2(2,400,3,-500,20)
    spi_fun.set_steer_time_1(6,1000,10)
    spi_fun.set_steer_time_3(2,800,3,-500,4,-850,20)      #-850
    spi_fun.set_steer_time_1(1,-700,10)
def steer_place_goods_top():
    spi_fun.set_steer_time_3(2,500,3,0,4,-868,20)
    spi_fun.set_steer_time_1(1,0,10)
    spi_fun.set_steer_time_1(2,300,10)
    spi_fun.set_steer_time_1(4,-850,10)
    spi_fun.set_steer_time_1(6,1000,10)
    spi_fun.set_steer_time_1(2,500,10)
#主函数开始
oled_thread = threading.Thread(target=oled.display)
#oled_thread.start()
run_thread = threading.Thread(target=run_fun)
print(spi_fun.get_gray())
camera_thread = threading.Thread(target=camera_use)
camera_thread.start()


run_thread.start()              #PID运算开启
spi_fun.set_steer_turn(0)   
time.sleep(1)
while GPIO.input(4):
    pass
par_run_flag = True 
while True:
    try:
        while True:             #当走到终点时退出循环
            print("STEP:"+str("直线行驶"))
            speed_set_status = 0    #关闭PID寻线控制
            print(speed_setM)
            spi_fun.set_motor(speed_setM)         
            spi_fun.set_steer_turn(0)
            time.sleep(2)
            speed_set_status = 4    #切换到第二种寻线模式
        
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
            while(not((gray_data_two[0] == 1 and gray_data_two[1]) and count == 2)):
                count = 0
                for i in gray_data_two:
                    if(i == 1):
                        count = count + 1
            spi_fun.set_motor(0)
            spi_fun.set_steer_turn(0)
            
            print("STEP:"+str("扫第一个物料"))
            steer_catch_code()
            time_last = time.time()
            while (time.time()-time_last) < 10:
                code_temp = code_fun()
                if code_temp != None:
                    if code_temp[0:6] == "ZJGXDS":
                        break
            for i in goods_data:
                if(code_temp == i):
                    print("STEP:"+str("抓第一个物料")+str(code_temp))
                    goods_place_data[goods_place_count] = i 
                    steer_catch_goods()
                    steer_catch_place()
                    break
            code_temp = None

            print("STEP:"+str("第二个抓取点"))
            g_speed_set = speed_setL
            speed_set_status = 4
            while(not((gray_data_two[6] == 1) and (gray_data_two[7] == 1) and (gray_data_two[0]))):
                pass
            time.sleep(0.1)
            speed_set_status = 0
            spi_fun.set_motor(0)
            spi_fun.set_steer_turn(0)
            print("STEP:"+str("扫第二个物料"))
            steer_catch_code()
            time_last = time.time()
            while (time.time()-time_last) < 10:
                code_temp = code_fun()
                if code_temp != None:
                    if code_temp[0:6] == "ZJGXDS":
                        break

            for i in goods_data:
                if(code_temp == i):
                    print("STEP:"+str("抓第二个物料")+str(code_temp))
                    goods_place_data[goods_place_count] = i 
                    steer_catch_goods()
                    steer_catch_place()
                    break
            code_temp = None

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
            time.sleep(0.1)
            speed_set_status = 0
            spi_fun.set_motor(0)
            spi_fun.set_steer_turn(0)
            print("STEP:"+str("扫第三个物料"))
            steer_catch_code()
            time_last = time.time()
            while (time.time()-time_last) < 10:
                code_temp = code_fun()
                if code_temp != None:
                    if code_temp[0:6] == "ZJGXDS":
                        break

            for i in goods_data:
                if(code_temp == i):
                    print("STEP:"+str("抓第三个物料")+str(code_temp))
                    goods_place_data[goods_place_count] = i 
                    steer_catch_goods()
                    steer_catch_place()
                    break
            code_temp = None

            if goods_place_count != 4:
                print("STEP:"+str("第四个抓取点"))
                g_speed_set = speed_setL
                speed_set_status = 4
                time.sleep(0.2)
                while(not((gray_data_two[4]) and (gray_data_two[5]))):
                    count = 0
                    for i in gray_data_two:
                        if(i == 1):
                            count = count + 1

                speed_set_status = 0
                spi_fun.set_motor(0)
                spi_fun.set_steer_turn(0)
                print("STEP:"+str("扫第四个物料"))
                steer_catch_code()
                time_last = time.time()
                while (time.time()-time_last) < 10:
                    code_temp = code_fun()
                    if code_temp != None:
                        if code_temp[0:6] == "ZJGXDS":
                            break

                for i in goods_data:
                    if(code_temp == i):
                        print("STEP:"+str("抓第四个物料")+str(code_temp))
                        goods_place_data[goods_place_count] = i 
                        steer_catch_goods()
                        steer_catch_place()
                        break
                code_temp = None


            if goods_place_count != 4:
                print("STEP:"+str("第五个抓取点"))
                g_speed_set = speed_setL
                speed_set_status = 0
                spi_fun.set_motor(int(speed_setL))
                spi_fun.set_steer_turn(0)
                time.sleep(0.3)
                while(not((gray_data_two[11]) and (count == 1))):
                    count = 0
                    for i in gray_data_two:
                        if(i == 1):
                            count = count + 1

                speed_set_status = 0
                spi_fun.    set_motor(0)
                spi_fun.set_steer_turn(0)
                print("STEP:"+str("扫第五个物料"))
                steer_catch_code()
                spi_fun.set_steer_time_1(1,-50,5)
                #spi_fun.set_steer_time_1(4,-580,5)
                time_last = time.time()
                while (time.time()-time_last) < 10:
                    code_temp = code_fun()
                    if code_temp != None:
                        if code_temp[0:6] == "ZJGXDS":
                            break

                for i in goods_data:
                    if(code_temp == i):
                        print("STEP:"+str("抓第五个物料")+str(code_temp))
                        goods_place_data[goods_place_count] = i 
                        steer_catch_goods()
                        steer_catch_place()
                        break
                code_temp = None

            spi_fun.steer_init()
            
            print("STEP:"+str("下坡"))
            g_speed_set = speed_setM
            speed_set_status = 1

            time.sleep(5)

            """while spi_fun.get_red_data():
                pass
            while spi_fun.get_red_data():
                pass """
    
            """print("STEP:"+str("避障1"))
            speed_set_status = 0
            spi_fun.set_motor(0)
            spi_fun.set_steer_turn(0)
            time.sleep(0.5)
            spi_fun.set_steer_turn(0)
            spi_fun.set_motor_left(-400)
            spi_fun.set_motor_right(400)
            time.sleep(2)
            spi_fun.set_motor_left(400)
            spi_fun.set_motor_right(400)
            spi_fun.set_steer_turn(0)
            time.sleep(2.5)
            spi_fun.set_motor_left(400)
            spi_fun.set_motor_right(-400)
            spi_fun.set_steer_turn(0)
            time.sleep(2)
            spi_fun.set_motor_left(400)
            spi_fun.set_motor_right(400)
            spi_fun.set_steer_turn(300)"""
        
            """print("STEP:"+str("避障2"))
            speed_set_status = 0
            spi_fun.set_motor(0)
            spi_fun.set_steer_turn(0)
            time.sleep(0.5)
            spi_fun.set_steer_turn(0)
            spi_fun.set_motor_left(-400)
            spi_fun.set_motor_right(400)
            time.sleep(3)
            spi_fun.set_motor_left(400)
            spi_fun.set_motor_right(400)
            spi_fun.set_steer_turn(0)
            time.sleep(2.8)
            spi_fun.set_motor_left(400)
            spi_fun.set_motor_right(-400)
            spi_fun.set_steer_turn(0)
            time.sleep(2)
            spi_fun.set_motor_left(400)
            spi_fun.set_motor_right(400)
            spi_fun.set_steer_turn(300)

            while(not(gray_data_two[1] and gray_data_two[2])):
                pass
            """
            g_speed_set = speed_setH
            speed_set_status = 2

            time.sleep(3)
            

            
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
            #steer_place_code_bottom()
            code_temp = goods_place_info[0] 
            print(goods_place_data)
            count_temp = 0
            count_temp_1 = 0
            for i in goods_data:
                count_temp = count_temp + 1
                if(code_temp == i):
                    print("STEP:"+str("放第一个物料"))
                    for j in goods_place_data :
                        count_temp_1 = count_temp_1 + 1
                        if code_temp == j:
                            break
                    if count_temp_1 == 2:
                        steer_place_catch_m1()
                    elif count_temp_1 == 3:
                        steer_place_catch_m2()
                    elif count_temp_1 == 4:
                        steer_place_catch_m3()
                    steer_place_goods_bottom()
                    break
            #steer_place_code_top()
            code_temp = goods_place_info[1] 
            print(goods_place_data)
            count_temp = 0
            count_temp_1 = 0
            for i in goods_data:
                count_temp = count_temp + 1
                if(code_temp == i):
                    print("STEP:"+str("放第一个物料"))
                    for j in goods_place_data :
                        count_temp_1 = count_temp_1 + 1
                        if code_temp == j:
                            break
                    print(count_temp_1)
                    if count_temp_1 == 2:
                        steer_place_catch_m1()
                    elif count_temp_1 == 3:
                        steer_place_catch_m2()
                    elif count_temp_1 == 4:
                        steer_place_catch_m3()
                    steer_place_goods_top()
                    break

            
            print("STEP:"+str("第二个抓取点"))
            g_speed_set = speed_setL
            speed_set_status = 4
            while(not((gray_data_two[7] == 1) and (gray_data_two[8] == 1))):
                pass
            speed_set_status = 0
            spi_fun.set_motor(0)
            spi_fun.set_steer_turn(0)
            #steer_place_code_bottom()
            code_temp = goods_place_info[2] 
            print(goods_place_data)
            count_temp = 0
            count_temp_1 = 0
            for i in goods_data:
                count_temp = count_temp + 1
                if(code_temp == i):
                    print("STEP:"+str("放第一个物料"))
                    for j in goods_place_data :
                        count_temp_1 = count_temp_1 + 1
                        if code_temp == j:
                            break
                    print(count_temp_1)
                    if count_temp_1 == 2:
                        steer_place_catch_m1()
                    elif count_temp_1 == 3:
                        steer_place_catch_m2()
                    elif count_temp_1 == 4:
                        steer_place_catch_m3()
                    steer_place_goods_bottom()
                    break
            #steer_place_code_top()
            code_temp = goods_place_info[3] 
            print(goods_place_data)
            count_temp = 0
            count_temp_1 = 0
            for i in goods_data:
                count_temp = count_temp + 1
                if(code_temp == i):
                    print("STEP:"+str("放第一个物料"))
                    for j in goods_place_data :
                        count_temp_1 = count_temp_1 + 1
                        if code_temp == j:
                            break
                    print(count_temp_1)
                    if count_temp_1 == 2:
                        steer_place_catch_m1()
                    elif count_temp_1 == 3:
                        steer_place_catch_m2()
                    elif count_temp_1 == 4:
                        steer_place_catch_m3()
                    steer_place_goods_top()
                    break



            print("STEP:"+str("第三个抓取点"))
            g_speed_set = speed_setL
            speed_set_status = 4
            count = 0    
            time.sleep(1)
            while(not((gray_data_two[6] == 1) or (not(gray_data_two[7])))):
                count = 0
                for i in gray_data_two:
                    if(i == 1):
                        count = count + 1
            time.sleep(0.3)
            speed_set_status = 0
            spi_fun.set_motor(0)
            spi_fun.set_steer_turn(0) 
            #steer_place_code_bottom()
            code_temp = goods_place_info[4] 
            print(goods_place_data)
            count_temp = 0
            count_temp_1 = 0
            for i in goods_data:
                count_temp = count_temp + 1
                if(code_temp == i):
                    print("STEP:"+str("放第一个物料"))
                    for j in goods_place_data :
                        count_temp_1 = count_temp_1 + 1
                        if code_temp == j:
                            break
                    print(count_temp_1)
                    if count_temp_1 == 2:
                        steer_place_catch_m1()
                    elif count_temp_1 == 3:
                        steer_place_catch_m2()
                    elif count_temp_1 == 4:
                        steer_place_catch_m3()
                    steer_place_goods_bottom()
                    break
            #steer_place_code_top()
            code_temp = goods_place_info[5] 
            print(goods_place_data)
            count_temp = 0
            count_temp_1 = 0
            for i in goods_data:
                count_temp = count_temp + 1
                if(code_temp == i):
                    print("STEP:"+str("放第一个物料"))
                    for j in goods_place_data :
                        count_temp_1 = count_temp_1 + 1
                        if code_temp == j:
                            break
                    print(count_temp_1)
                    if count_temp_1 == 2:
                        steer_place_catch_m1()
                    elif count_temp_1 == 3:
                        steer_place_catch_m2()
                    elif count_temp_1 == 4:
                        steer_place_catch_m3()
                    steer_place_goods_top()
                    break


            print("STEP:"+str("第四个抓取点"))
            g_speed_set = speed_setL
            speed_set_status = 4
            time.sleep(0.5)
            while(not((gray_data_two[5]) and (gray_data_two[6]))):
                count = 0
                for i in gray_data_two:
                    if(i == 1):
                        count = count + 1

            speed_set_status = 0
            spi_fun.set_motor(0)
            spi_fun.set_steer_turn(0)
            #steer_place_code_bottom()
            code_temp = goods_place_info[6] 
            print(goods_place_data)
            count_temp = 0
            count_temp_1 = 0
            for i in goods_data:
                count_temp = count_temp + 1
                if(code_temp == i):
                    print("STEP:"+str("放第一个物料"))
                    for j in goods_place_data :
                        count_temp_1 = count_temp_1 + 1
                        if code_temp == j:
                            break
                    print(count_temp_1)
                    if count_temp_1 == 2:
                        steer_place_catch_m1()
                    elif count_temp_1 == 3:
                        steer_place_catch_m2()
                    elif count_temp_1 == 4:
                        steer_place_catch_m3()
                    steer_place_goods_bottom()
                    break
            #steer_place_code_top()
            code_temp = goods_place_info[7] 
            print(goods_place_data)
            count_temp = 0
            count_temp_1 = 0
            for i in goods_data:
                count_temp = count_temp + 1
                if(code_temp == i):
                    print("STEP:"+str("放第一个物料"))
                    for j in goods_place_data :
                        count_temp_1 = count_temp_1 + 1
                        if code_temp == j:
                            break
                    if count_temp_1 == 2:
                        steer_place_catch_m1()
                    elif count_temp_1 == 3:
                        steer_place_catch_m2()
                    elif count_temp_1 == 4:
                        steer_place_catch_m3()
                    steer_place_goods_top()
                    break

            
            print("STEP:"+str("第五个抓取点"))
            g_speed_set = speed_setL
            speed_set_status = 0
            spi_fun.set_motor(int(speed_setL))
            spi_fun.set_steer_turn(0)
            time.sleep(0.5)
            while(not((gray_data_two[11])  and (count == 1))):
                count = 0
                for i in gray_data_two:
                    if(i == 1):
                        count = count + 1

            speed_set_status = 0
            spi_fun.set_motor(0)
            spi_fun.set_steer_turn(0)
            #steer_place_code_bottom()
            code_temp = goods_place_info[8] 
            print(goods_place_data)
            count_temp = 0
            count_temp_1 = 0
            for i in goods_data:
                count_temp = count_temp + 1
                if(code_temp == i):
                    print("STEP:"+str("放第一个物料"))
                    for j in goods_place_data :
                        count_temp_1 = count_temp_1 + 1
                        if code_temp == j:
                            break
                    print(count_temp_1)
                    if count_temp_1 == 2:
                        steer_place_catch_m1()
                    elif count_temp_1 == 3:
                        steer_place_catch_m2()
                    elif count_temp_1 == 4:
                        steer_place_catch_m3()
                    steer_place_goods_bottom()
                    break
            #steer_place_code_top()
            code_temp = goods_place_info[9] 
            print(goods_place_data)
            count_temp = 0
            count_temp_1 = 0
            for i in goods_data:
                count_temp = count_temp + 1
                if(code_temp == i):
                    print("STEP:"+str("放第一个物料"))
                    for j in goods_place_data :
                        count_temp_1 = count_temp_1 + 1
                        if code_temp == j:
                            break
                    if count_temp_1 == 2:
                        steer_place_catch_m1()
                    elif count_temp_1 == 3:
                        steer_place_catch_m2()
                    elif count_temp_1 == 4:
                        steer_place_catch_m3()
                    steer_place_goods_top()
                    break
            
            spi_fun.steer_init()
            g_speed_set = speed_setH
            speed_set_status = 2    #切换到第一种寻线模式
            time.sleep(3.5)
            speed_set_status = 0    #切换到第一种寻线模式
            spi_fun.set_motor(speed_setH)
            while(not((gray_data_two[10] or gray_data_two[11]))):
                pass
            time.sleep(0.4)
            spi_fun.set_motor(0)
    
            while True:
                time.sleep(2)

    except KeyboardInterrupt:
        speed_set_status = 0
        spi_fun.set_steer_turn(0)
        spi_fun.set_motor(0)
        sys.exit()
