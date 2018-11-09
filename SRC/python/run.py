import json
class RUN:
    def __init__(self):
        self.dif_last = 0
        f = open("config.json",encoding='utf-8')
        setting = json.load(f)
        self.KP = setting["PID_turn"]["P"]
        self.KI = setting["PID_turn"]["I"]
        self.KD = setting["PID_turn"]["D"]
    def gray_dif(self,gray,status=0):     #status = 0 当白色时，偏移量为0，status = 1，偏移量使其左转，status = 2，偏移量使其右转
        left = 0        #左边第一个黑点位置
        right = 0       #右边第一个黑点位置
        l1 = list(range(12))
        del l1[-1]
        for i in l1:
            if((not gray[i]) and gray[i+1]):
                left = i+1
                break
        l2 = list(gray)
        l2.reverse()
        for i in l1:
            if((not l2[i]) and (l2[i+1])):
                right = i+1
                break
        if((left == 0) and (right == 0)):
            if status == 1:
                right = 15
            elif status == 2:
                left == 15
        elif left == 0:
            left = right
        elif right == 0:
            right = left
        #print(left,right)
        return (left - right)
    def turn_pid(self,dif):
        out = self.KP * dif + self.KD * (dif - self.dif_last)
        #print("PO:",self.KP * dif,"DO:",self.KD * (dif - self.dif_last))
        self.dif_last = dif
        return out
