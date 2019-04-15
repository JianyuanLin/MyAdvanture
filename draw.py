# coding:utf-8
import pygame as pg
import time

# 绘制文本
def drawText(win, text, pos, length=25, font=pg.font.Font("simkai.ttf", 25)):
    nRow = len(text) / length
    if len(text) % length == 0:
        nRow -= 1
    for i in range(nRow):
        surface = font.render(text[i * length:(i + 1) * length], True, (0, 0, 0))
        win.blit(surface, (pos[0], pos[1] + i * 25))
    surface = font.render(text[(nRow) * length:], True, (0, 0, 0))
    win.blit(surface, (pos[0], pos[1] + nRow * 25))


# 绘制图片
def drawPic(win, pic, pos):
    surface = pg.image.load(pic).convert()
    win.blit(surface, pos)


# 绘制缩放为4:3的图
def drawPic43(win, pic, pos):
    try:
        surface = pg.transform.smoothscale(pg.image.load(pic).convert_alpha(), (60, 80))
        win.blit(surface, pos)
    except Exception:
        pass

#系统提示
def SysTip(win,text):
    drawText(win, text, (320,240))
    pg.display.update()
    time.sleep(1)

