#coding:utf-8
import pygame as pg

# 按钮类
class Button():
    def __init__(self, pos, text, key=0):
        self.buttonPic = pg.image.load("./pic/Button.png").convert_alpha()
        self.font = pg.font.Font("simkai.ttf", 25)
        self.pos = pos
        self.text = text
        self.mouseOn = False
        self.choosed = False
        self.width = len(text) * 25
        self.height = 25
        self.key = key
        self.pic = pg.transform.smoothscale(self.buttonPic, (25 * len(text), 25))

    def isMouseOn(self):
        x, y = pg.mouse.get_pos()
        dx = x - self.pos[0]
        dy = y - self.pos[1]
        self.mouseOn = False
        if dx > 0 and dy > 0:
            if dx < self.width and dy < self.height:
                self.mouseOn = True

    def display(self, win):
        if self.mouseOn or self.choosed:
            color = (255, 0, 0)
        else:
            color = (0, 0, 255)
        surface = self.font.render(self.text, True, color)
        # win.blit(self.pic, self.pos)
        win.blit(surface, self.pos)
