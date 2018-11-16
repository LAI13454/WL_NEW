import sys
import readline
from spi_fun import SPI_FUN
steer_fun = SPI_FUN(0)
speed = input("请输入移动速度:")
try:
    speed = float(speed)
except ValueError:
    print("请重开软件")
    
 
while True:
    temp = input("控制机械臂位号:")
    try:
        temp = int(temp)
    except ValueError:
        print("请重试")
        continue
    if(temp == 0):
        for i in range(1,7):
            str_info = steer_fun.get_steer_val(i)
            print(str(i)+"的当前值:"+str(str_info))
    if(temp == 20):
        temp_num = []
        temp_val = []
        for i in range(0,2):
            temp_2 = input("控制机械臂位号"+str(i)+":")
            try:
                temp_2 = int(temp_2)
            except ValueError:
                print("请重试")
                continue
            temp_num.append(temp_2)
            temp_2 = input("请输入设定值"+str(i)+":")
            try:
                temp_2 = int(temp_2)
            except ValueError:
                print("请重试")
                continue
            temp_val.append(temp_2)

        steer_fun.set_steer_time_2(temp_num[0],temp_val[0],temp_num[1],temp_val[1],speed)
        #steer_fun.set_steer_time_2(5,1000,6,1000,10)
    elif((temp >= 1) and (temp <= 6)):
        str_info = steer_fun.get_steer_val(temp)
        print(str(temp)+"的当前值:"+str(str_info))
    val = input("请输入设定值:")
    try:
        val = int(val)
    except ValueError:
        print("请重试")
        continue
    if((temp >= 1) and (temp <= 6)):
       steer_fun.set_steer_time_1(temp,val,speed) 
    print(str(temp)+"号以达目标值"+str(val))






