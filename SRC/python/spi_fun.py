#from spi_com import SPI_COM
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

        
