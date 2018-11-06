#import spidev
class SPI_COM:      #树莓派与STM32通信类
    def __init__(self):
        #self.spi = spidev.SpiDev()
        #self.spi.open(0,0)
        #self.spi.max_speed_hz = 100000
        pass
    def motor(self,direction,val):      #direction == 0:左右电机控制 1:左侧电机 2:右侧电机
        if((direction != 0) and (direction != 1) and (direction != 2)):
            while True:
                print("电机设置错误")
        l = []
        l.append(0xaa)
        l.append(direction)
        l.append((val>>8)&0xff)
        l.append(val&0xff)
        l.append(0x00)
        l.append(0x00)
        temp = 0
        for i in range(6):
            temp = temp + l[i]
        l.append(temp&0xff)         #检验位
        l.append(0x55)
        print(l)
spi_com = SPI_COM()
spi_com.motor(0,500)
