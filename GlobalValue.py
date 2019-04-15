#coding:utf-8
import pygame as pg
from Data import Data
#全局控制类
class GlobalValue:
    def __init__(self):
        self.state = "Title"
        self.width = 640
        self.height = 480
        self.meta = 25
        self.win = pg.display.set_mode((640, 480))
        self.font = pg.font.Font("simkai.ttf", 25)
        self.gd = None
        self.data = Data()
        self.buttonPic = pg.image.load("./pic/Button.png").convert_alpha()
        self.winPic = pg.image.load("./pic/win.png").convert_alpha()