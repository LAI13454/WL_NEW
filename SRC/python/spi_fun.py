from spi_com import SPI_COM
import json
import time
class SPI_FUN:
    def __init__(self,val):         #val = 1 从stm32读取舵机值，val = 0 从config读取舵机值
        self.spi_com = SPI_COM()
        f = open("config.json",encoding='utf-8')
        setting = json.load(f)
        if val == 0:
            self.steer_val_1 = setting["Steer_DEF"]["1"]
            self.steer_val_2 = setting["Steer_DEF"]["2"]
            self.steer_val_3 = setting["Steer_DEF"]["3"]
            self.steer_val_4 = setting["Steer_DEF"]["4"]
            self.steer_val_5 = setting["Steer_DEF"]["5"]
            self.steer_val_6 = setting["Steer_DEF"]["6"]
            self.steer_speed = setting["Steer_DEF"]["Speed"]
        else:
            pass
    def get_gray(self):             #获取寻线灰度数据
        return self.spi_com.gray()
    def get_gray_two(self):
        return self.spi_com.gray_two()      #获取右侧灰度数据
    def set_steer_turn(self,val):
        return self.spi_com.steer_turn(val-40)    #设置舵机转向值
    def set_motor_left(self,val):           
        self.spi_com.motor(1,val)           #设置左侧电机值
    def set_motor_right(self,val):
        self.spi_com.motor(2,val)           #设置右侧电机值
    def set_motor(self,val):
        self.spi_com.motor(5,val)           #设置两个电机值
        
