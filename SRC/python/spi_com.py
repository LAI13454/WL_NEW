import spidev
class SPI_COM:      #树莓派与STM32通信类
    def __init__(self):
        self.steer_place = [3,1,2,4,5,6,7,8]   #舵机口对应关系，方便操作
        self.spi = spidev.SpiDev()
        self.spi.open(0,0)
        self.spi.max_speed_hz = 1000000
        pass
    def motor(self,direction,val):      #direction == 5:左右电机控制 1:左侧电机 2:右侧电机i
        
        #print("Test:"+str(direction)+"val:"+str(val))
        if((direction != 5) and (direction != 1) and (direction != 2)):
            while True:
                print("电机设置错误")
        l = []
        l.append(0xaa)
        l.append(0x00 + direction)
        if val > 1000:
            val = 1000
        elif val < -1000:
            val = -1000
        l.append((val>>8)&0xff)
        l.append(val&0xff)
        l.append(0x00)
        l.append(0x00)
        temp = 0
        for i in range(6):
            temp = temp + l[i]
        l.append(temp&0xff)         #检验位
        l.append(0x55)
        while_flag = True
        while while_flag:
            r_l = self.spi.xfer(l)
            if(r_l[7] != 1):
                #print(l)
                #print(r_l)
                #print("SPI通信错误--电机")
                while_flag = True
            else:
                #print("SPI通信正确--电机")
                while_flag = False
        #print(l)
        #print(r_l)

    def steer(self,steer_num,val):      
        if((steer_num < 0) or (steer_num > 7)):
            while True:
                print("舵机设置错误")
        l = []
        l.append(0xaa)
        l.append(0x10 + self.steer_place[steer_num])
        if val > 1000:
            val = 1000
        elif val < -1000:
            val = -1000
        l.append((val>>8)&0xff)
        l.append(val&0xff)
        l.append(0x00)
        l.append(0x00)
        temp = 0
        for i in range(6):
            temp = temp + l[i]
        l.append(temp&0xff)         #检验位
        l.append(0x55)
        while_flag = True
        while while_flag:
            r_l = self.spi.xfer(l)
            if(r_l[7] != 1):
                #print(l)
                #print(r_l)
                #print("SPI通信错误--舵机")
                while_flag = True
            else:
                while_flag = False
        #print(l)
        #print(r_l)
    def steer_turn(self,val):
        #print("Test:"+str(val))
        if val <= 0:
            #Left Turn
            if val <= -650:
                self.steer(0,-650)  #left
            else:
                self.steer(0,val)
            if val <= -650:
                self.steer(7,-650) #right
            else:
                self.steer(7,val-35)
        else:
            #Right Turn
            if val > 550:
                self.steer(0,550)
            else:
                self.steer(0,val)
            if val > 550:
                self.steer(7,550)
            else:
                self.steer(7,val-35)
    def gray(self):
        l = []
        l.append(0xaa)
        l.append(0x21)
        l.append(0x00)
        l.append(0x00)
        l.append(0xff)
        l.append(0xff)
        temp = 0
        for i in range(6):
            temp = temp + l[i]
        l.append(temp&0xff)         #检验位
        l.append(0x55)
        while_flag = True
        while while_flag:
            r_l = self.spi.xfer(l)
            if(((r_l[4] + r_l[5]) & 0xff) != r_l[6]):
                #print(l)
                #print(r_l)
                #print("SPI通信错误")
                while_flag = True
            else:
                while_flag = False
        temp = ((r_l[4]<<8)|r_l[5])&0x0fff
        val = []
        for i in range(12):
            if temp & (0x01<<i):
                val.append(1)
            else:
                val.append(0)
        #print(l)
        #print(r_l)
        #print(val)
        return val
    def gray_two(self):
        l = []
        l.append(0xaa)
        l.append(0x22)
        l.append(0x00)
        l.append(0x00)
        l.append(0xff)
        l.append(0xff)
        temp = 0
        for i in range(6):
            temp = temp + l[i]
        l.append(temp&0xff)         #检验位
        l.append(0x55)
        while_flag = True
        while while_flag:
            r_l = self.spi.xfer(l)
            if(((r_l[4] + r_l[5]) & 0xff) != r_l[6]):
                #print(l)
                #print(r_l)
                #print("SPI通信错误")
                while_flag = True
            else:
                while_flag = False
        temp = ((r_l[4]<<8)|r_l[5])&0x0fff
        val = []
        for i in range(12):
            if temp & (0x01<<i):
                val.append(1)
            else:
                val.append(0)
        #print(l)
        #print(r_l)
        val.reverse()
        #print(val)
        return val

#spi_com = SPI_COM()
#spi_com.motor(5,200)
