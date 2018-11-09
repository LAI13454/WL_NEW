import time

import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import subprocess

class OLED:
    def __init__(self):
        self.disp = Adafruit_SSD1306.SSD1306_128_64(rst=None)
        self.disp.begin()
        self.disp.clear()
        self.disp.display()
        self.width = self.disp.width
        self.height = self.disp.height
        self.image = Image.new('1', (self.width, self.height))
        self.draw = ImageDraw.Draw(self.image)
        self.draw.rectangle((0,0,self.width,self.height), outline=0, fill=0)
        padding = -2
        self.top = padding
        self.bottom = self.height-padding
        self.font = ImageFont.load_default()

    def sys_info(self):
        cmd = "hostname -I | cut -d\' \' -f1"
        IP = subprocess.check_output(cmd, shell = True)
        cmd = "top -bn1 | grep load | awk '{printf \"CPU:%.2f\", $(NF-2)}'"
        CPU = subprocess.check_output(cmd, shell = True )
        cmd = "free -m | awk 'NR==2{printf \"Mem:%.2f%%\",$3*100/$2 }'"
        MemUsage = subprocess.check_output(cmd, shell = True )
        self.draw.rectangle((0,0,self.width,self.height), outline=0, fill=0)
        self.draw.text((0,self.top),       "IP: "+str(IP,encoding='utf-8'),  font=self.font, fill=255)
        self.draw.text((0,self.top+8),     str(CPU,encoding='utf-8'), font=self.font, fill=255)
        self.draw.text((64,self.top+8),    str(MemUsage,encoding='utf-8'),  font=self.font, fill=255)

        self.disp.image(self.image)
        self.disp.display()
    def display(self):
        while True:
            self.sys_info()
            time.sleep(1)

