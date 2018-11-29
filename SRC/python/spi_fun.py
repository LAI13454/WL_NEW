from spi_com import SPI_COM
import json
import time
class SPI_FUN:
    def __init__(self,val):         #val = 1 从stm32读取舵机值，val = 0 从config读取舵机值
        self.spi_com = SPI_COM()
        f = open("config.json",encoding='utf-8')
        setting = json.load(f)
        self.steer_val = []
        self.steer_val_def = []
        for i in range(0,7):
            self.steer_val.append(0)
            self.steer_val_def.append(0)
        print(self.steer_val)
        if val == 0:
            self.steer_val[1] = setting["Steer_DEF"]["1"]
            self.steer_val[2] = setting["Steer_DEF"]["2"]
            self.steer_val[3] = setting["Steer_DEF"]["3"]
            self.steer_val[4] = setting["Steer_DEF"]["4"]
            self.steer_val[5] = setting["Steer_DEF"]["5"]
            self.steer_val[6] = setting["Steer_DEF"]["6"]
            self.steer_speed = setting["Steer_DEF"]["Speed"]
            for i in range(1,7):
                self.steer_val_def[i] = self.steer_val[i]
        else:
            pass
        for i in range(1,6):
            self.spi_com.steer(i,self.steer_val[i])
        print(self.steer_val)
    def steer_init(self):
        self.set_steer_time_3(2,self.steer_val_def[2],3,self.steer_val_def[3],4,self.steer_val_def[4],20) 
        self.set_steer_time_1(1,self.steer_val_def[1],10)
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
        if val == 0:
            time.sleep(0.02)
            self.spi_com.motor(5,val)
    def get_steer_val(self,num_1):
        return self.steer_val[num_1]
    def set_steer_time_1(self,num_1,val_1,time_val):     
        if(val_1 < self.steer_val[num_1]):  #控制一个舵机运行
            l = list(range(self.steer_val[num_1],val_1,-10))
            l.append(val_1)
        else:
            l = list(range(self.steer_val[num_1],val_1,10))
            l.append(val_1)
        for i in l:
            self.spi_com.steer(num_1,i)
            time.sleep(time_val * self.steer_speed)
        self.steer_val[num_1] = val_1
    def set_steer_time_2(self,num_1,val_1,num_2,val_2,time_val):
        temp_time = []
        num = []
        val = []
        num.append(num_1)
        num.append(num_2)
        val.append(val_1)
        val.append(val_2)
        for i in range(0,2):
            temp_time.append(abs(val[i]-self.steer_val[num[i]]))    #找出每个数偏差
        #print(temp_time)
        temp_max_num = temp_time.index(max(temp_time))              #找出差距最大的索引号
        #print(temp_max_num)
        l = []
        for i in range(0,2):
            l.append([])
        if val[temp_max_num] < self.steer_val[num[temp_max_num]]:
            l[temp_max_num] = list(range(self.steer_val[num[temp_max_num]],val[temp_max_num],-10))
            l[temp_max_num].append(val[temp_max_num])
        elif val[temp_max_num] > self.steer_val[num[temp_max_num]]:
            l[temp_max_num] = list(range(self.steer_val[num[temp_max_num]],val[temp_max_num],10))
            l[temp_max_num].append(val[temp_max_num])
        else:
            l[temp_max_num].append(val[temp_max_num])
        for i in range(0,2):
            if i != temp_max_num:
                temp_1 = int((abs(val[i]-self.steer_val[num[i]]))/len(l[temp_max_num]))
                #print(temp_1)
                if val[i] < self.steer_val[num[i]]:
                    l[i] = list(range(self.steer_val[num[i]],val[i],-temp_1))
                    l[i].append(val[i])
                elif val[i] > self.steer_val[num[i]]:
                    if((val[i] != self.steer_val[num[i]]) and (temp_1 != 0)):
                        l[i] = list(range(self.steer_val[num[i]],val[i],temp_1))
                if(val[i] != self.steer_val[num[i]]):
                    for j in range(len(l[i])-1,len(l[temp_max_num])-2,-1):
                        l[i].pop(j)
                    l[i].append(val[i])
                    if len(l[i]) < len(l[temp_max_num]):
                        for j in range(len(l[i]),len(l[temp_max_num]),1):
                            l[i].append(val[i])
                else:
                    l[i] = []
                    l[i].append(val[i])
        #print(len(l[temp_max_num]),len(l[1]))
        #print(val)
        for i in range(0,len(l[temp_max_num])):
            #print(l[0])
            for k in range(0,2):
                if(val[k] != self.steer_val[num[k]]):
                    self.spi_com.steer(num[k],l[k][i])
            time.sleep(time_val * self.steer_speed)
        for i in range(0,2):
            self.steer_val[num[i]] = val[i]
        #print(l)
        #print(len(l[temp_max_num]),len(l[1]))


    def set_steer_time_3(self,num_1,val_1,num_2,val_2,num_3,val_3,time_val):
        temp_time = []
        num = []
        val = []
        num.append(num_1)
        num.append(num_2)
        num.append(num_3)
        val.append(val_1)
        val.append(val_2)
        val.append(val_3)
        for i in range(0,3):
            temp_time.append(abs(val[i]-self.steer_val[num[i]]))    #找出每个数偏差
        #print(temp_time)
        temp_max_num = temp_time.index(max(temp_time))              #找出差距最大的索引号
        #print(temp_max_num)
        l = []
        for i in range(0,3):
            l.append([])
        if val[temp_max_num] < self.steer_val[num[temp_max_num]]:
            l[temp_max_num] = list(range(self.steer_val[num[temp_max_num]],val[temp_max_num],-10))
            l[temp_max_num].append(val[temp_max_num])
        elif val[temp_max_num] > self.steer_val[num[temp_max_num]]:
            l[temp_max_num] = list(range(self.steer_val[num[temp_max_num]],val[temp_max_num],10))
            l[temp_max_num].append(val[temp_max_num])
        else:
            l[temp_max_num].append(val[temp_max_num])
        for i in range(0,3):
            if i != temp_max_num:
                temp_1 = int((abs(val[i]-self.steer_val[num[i]]))/len(l[temp_max_num]))
                #print(temp_1)
                if val[i] < self.steer_val[num[i]]:
                    if temp_1 != 0:
                        l[i] = list(range(self.steer_val[num[i]],val[i],-temp_1))
                    l[i].append(val[i])
                elif val[i] > self.steer_val[num[i]]:
                    if((val[i] != self.steer_val[num[i]]) and (temp_1 != 0)):
                        l[i] = list(range(self.steer_val[num[i]],val[i],temp_1))
                if(val[i] != self.steer_val[num[i]]):
                    for j in range(len(l[i])-1,len(l[temp_max_num])-2,-1):
                        l[i].pop(j)
                    l[i].append(val[i])
                    if len(l[i]) < len(l[temp_max_num]):
                        for j in range(len(l[i]),len(l[temp_max_num]),1):
                            l[i].append(val[i])
                else:
                    l[i] = []
                    l[i].append(val[i])
        #print(len(l[0]),len(l[1]),len(l[2]))
        #print(val)
        for i in range(0,len(l[temp_max_num])):
            #print(l[0])
            for k in range(0,3):
                if(val[k] != self.steer_val[num[k]]):
                    self.spi_com.steer(num[k],l[k][i])
            time.sleep(time_val * self.steer_speed)
        for i in range(0,3):
            self.steer_val[num[i]] = val[i]
        #print(l)
        #print(len(l[temp_max_num]),len(l[1]))
       
    def set_steer_time_4(self,num_1,val_1,num_2,val_2,num_3,val_3,num_4,val_4):
        pass
    def get_red_data(self):
        return self.spi_com.get_red()
#spi_fun = SPI_FUN(0)
#spi_fun.set_steer_time_2(5,-100,6,0,10)
#spi_fun.set_steer_time_2(5,1000,6,1000,10)
