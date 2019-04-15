#coding:utf-8
import pygame as pg
pg.init()
from Button import Button
from AI import AI
from getCommand import getCommand
from Data import Data
import time
import random
from draw import drawText, drawPic, drawPic43, SysTip
from Window import *
from GlobalValue import GlobalValue
from GameData import GameData
from Role import Role
from Item import Item
from State import State

#主函数
def main():   
    pg.display.set_caption("我的冒险")
    while True:
        if gv.state == "Title":
            Title()
        elif gv.state == "Run":
            Run()
    
#标题函数        
def Title():
    #初始化
    beginButton = Button((gv.width / 2 - 2 * gv.meta, gv.height / 2 - 1.5 * gv.meta), u"开始游戏")
    continueButton = Button((gv.width / 2 - 2 * gv.meta, gv.height / 2 - 0.5 * gv.meta), u"继续游戏")
    exitButton = Button((gv.width / 2 - 2 * gv.meta, gv.height / 2 + 0.5 * gv.meta), u"离开游戏")
    beiJing = pg.image.load("./pic/BeiJing.jpg").convert()
    bgm = pg.mixer.music.load("./music/title.ogg")
    pg.mixer.music.play(-1)
    #进入循环
    while gv.state == "Title":
        #监听系统事件
        mouseButtonDown = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                mouseButtonDown = True
        #监听按钮
        beginButton.isMouseOn()
        continueButton.isMouseOn()
        exitButton.isMouseOn()
        #按下鼠标左键
        if mouseButtonDown:
            #游戏开始
            if beginButton.mouseOn:
                gv.state = "Run"
                gv.gd = GameData()
                return
            #继续游戏
            elif continueButton.mouseOn:
                Read()
            #离开游戏
            elif exitButton.mouseOn:
                exit()
        #绘制屏幕
        gv.win.blit(beiJing, (0,0))
        beginButton.display(gv.win)
        continueButton.display(gv.win)
        exitButton.display(gv.win)
        pg.display.update()
        time.sleep(0.03)
        
#游戏函数
def Run():
    while gv.state == "Run":
        if gv.gd._in == "Begin":#开场剧情
            Begin()
        elif gv.gd._in == "ChooseRole":#选择角色
            ChooseRole()
        elif gv.gd._in == "BigMap":#大地图
            BigMap()
        elif gv.gd._in == "City":#城镇
            City()
        elif gv.gd._in == "FengZhiGu":#风之谷
            FengZhiGu()
        elif gv.gd._in == "HaiDiShiJie":#海底世界
            HaiDiShiJie()
        elif gv.gd._in == "HuoYanShan":#火焰山
            HuoYanShan()
        elif gv.gd._in == "TongTianTa":#通天塔
            TongTianTa()
        elif gv.gd._in == "DiXiaCheng":#地下城
            DiXiaCheng()

#开场剧情
def Begin():
    #初始化
    story = pg.image.load("./pic/story.png")
    #循环
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                gv.gd._in = "ChooseRole"
                return
        #绘制屏幕
        gv.win.blit(story,(0,0))
        pg.display.update()
        time.sleep(0.03)
    
#选择角色
def ChooseRole():
    #初始化
    roleButtonList = []
    nameList = [u"战士",u"骑士",u"法师",u"牧师",u"射手",u"刺客",]
    picNameList = ["./pic/ZhanShi.png","./pic/QiShi.png","./pic/FaShi.png",
                   "./pic/MuShi.png","./pic/SheShou.png","./pic/CiKe.png",]
    for i in range(6):
        roleButton = Button((0,25 + i * 25), nameList[i], i)
        roleButtonList.append(roleButton)
    #循环
    while True:
        mouseButtonDown = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                mouseButtonDown = True
        #监听按钮
        pic = None
        text = None
        for b in roleButtonList:
            b.isMouseOn()
            if b.mouseOn:
                pic = picNameList[b.key]
                text = gv.data.roleList[b.key]["text"]
                if mouseButtonDown:
                    gv.gd.team.append(Role(gv.data.roleList[b.key]))
                    #gv.gd = testData()
                    index = 0
                    for r in gv.gd.bigMapRole:
                        if r == b.key:
                            gv.gd.bigMapRole.pop(index)
                    gv.gd._in = "BigMap"
                    return
        #按下鼠标左键
        #绘制屏幕
        gv.win.fill((255,255,255))
        
        drawText(gv.win, u"选择角色", (0,0))
        for b in roleButtonList:
            b.display(gv.win)
        if pic != None:
            drawPic(gv.win, pic, (100,0))
            drawText(gv.win, text, (0,240))
        pg.display.update()
        time.sleep(0.03)

#大地图
def BigMap():
    #初始化
    equipButton = Button((80,60), u"装备")
    skillButton = Button((80,85), u"技能")
    bagButton = Button((80,110), u"背包")
    saveButton = Button((80,135), u"存档")
    readButton = Button((80,160), u"读档")
    titleButton = Button((80,185), u"标题")
    exitButton = Button((80,210), u"退出")
    moveButton = Button((295,228), u"移动")
    BM = pg.image.load("./pic/BigMap.png")
    pg.mixer.music.load("./music/BigMap.ogg")
    pg.mixer.music.play(-1)
    playerPosList = [(0,0),(80,0),(160,0),(240,0),(320,0),(400,0),(480,0),
                     (560,0),(560,60),(560,120),(560,180),(560,240),(560,300),(560,360),
                     (560,420),(480,420),(400,420),(320,420),(240,420),(160,420),(80,420),
                     (0,420),(0,360),(0,300),(0,240),(0,180),(0,120),(0,60),]
    roleSurface = pg.image.load(gv.gd.team[0].pic).convert_alpha()
    roleSurface = pg.transform.smoothscale(roleSurface, (45,60))
    step = 0
    times = 0
    #循环
    while True:
        if step != 0:
            times+=1
            if times >= 10:
                gv.gd.pos += 1
                if gv.gd.pos >= 28:
                    gv.gd.pos -= 28
                step -= 1
                times = 0
                #根据停留的位置进入不同的地方
                if step == 0:
                    #gv.gd.pos = 1
                    if gv.gd.pos in [0,7,14,21]:
                        gv.gd._in = "City"
                        return
                    elif gv.gd.pos in [1,4,5,8,9,13,15,17,20,22,25,26]:#野外
                        Battle()
                        pg.mixer.music.load("./music/BigMap.ogg")
                        pg.mixer.music.play(-1)                        
                    elif gv.gd.pos in [6,12,18,24]:#神秘之地
                        Unknown()
                    elif gv.gd.pos == 2:#酒馆
                        JiuGuan([0,1,2,3,4,5])
                    elif gv.gd.pos == 10:#神秘商店
                        Shop([9,11,13,15,17,19,21,23,25,27])
                    elif gv.gd.pos == 16:#学习技能
                        LearnSkill([3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
                    elif gv.gd.pos == 3:#风之谷
                        gv.gd._in = "FengZhiGu"
                        return
                    elif gv.gd.pos == 11:#海底世界
                        gv.gd._in = "HaiDiShiJie"
                        return
                    elif gv.gd.pos == 19:#火焰山
                        gv.gd._in = "HuoYanShan"
                        return
                    elif gv.gd.pos == 23:#通天塔
                        gv.gd._in = "TongTianTa"
                        return
                    elif gv.gd.pos == 27:#地下城
                        gv.gd._in = "DiXiaCheng"
                        return
        for event in pg.event.get():
            mouseButtonDown = False
            if event.type == pg.QUIT:
                exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                mouseButtonDown = True
        #监听按钮
        if step == 0:
            equipButton.isMouseOn()
            if equipButton.mouseOn and mouseButtonDown:
                Equip()
            skillButton.isMouseOn()
            if skillButton.mouseOn and mouseButtonDown:
                Skill()
            bagButton.isMouseOn()
            if bagButton.mouseOn and mouseButtonDown:
                Bag()
            saveButton.isMouseOn()
            if saveButton.mouseOn and mouseButtonDown:
                Save()
            readButton.isMouseOn()
            if readButton.mouseOn and mouseButtonDown:
                Read()
            titleButton.isMouseOn()
            if titleButton.mouseOn and mouseButtonDown:
                gv.state = "Title"
                return 
            exitButton.isMouseOn()
            if exitButton.mouseOn and mouseButtonDown:
                exit()            
            
            moveButton.isMouseOn()
            if moveButton.mouseOn:
                if mouseButtonDown:
                    step = random.randint(1,6)
        #绘制屏幕
        gv.win.fill((255,255,255))
        gv.win.blit(BM,(0,0))
        gv.win.blit(roleSurface, playerPosList[gv.gd.pos])
        drawText(gv.win, str(step), (345,228))
        equipButton.display(gv.win)
        skillButton.display(gv.win)
        bagButton.display(gv.win)
        saveButton.display(gv.win)
        readButton.display(gv.win)
        titleButton.display(gv.win)
        exitButton.display(gv.win)
        moveButton.display(gv.win)
        pg.display.update()
        time.sleep(0.03)

#城镇
def City():
    #初始化
    returnButton = Button((590, 455), u"返回")
    BM = pg.image.load("./pic/City.png").convert()
    pg.mixer.music.load("./music/City.ogg")
    pg.mixer.music.play(-1)
    shopButton = Button((295, 215), u"商店")
    hotelButton = Button((295, 240), u"旅馆")
    equipButton = Button((80,60), u"装备")
    skillButton = Button((80,85), u"技能")
    bagButton = Button((80,110), u"背包")
    saveButton = Button((80,135), u"存档")
    readButton = Button((80,160), u"读档")
    titleButton = Button((80,185), u"标题")
    exitButton = Button((80,210), u"退出")
    #循环
    while True:
        mouseButtonDown = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                mouseButtonDown = True
        #监听按钮
        returnButton.isMouseOn()
        if returnButton.mouseOn and mouseButtonDown:
            gv.gd._in = "BigMap"
            return 
        shopButton.isMouseOn()
        if shopButton.mouseOn and mouseButtonDown:
            Shop([0,1,2,3,4,5,6,7,8,10,12,14,16,18,20,22,24,26])
        hotelButton.isMouseOn()
        if hotelButton.mouseOn and mouseButtonDown:
            Hotel()
        equipButton.isMouseOn()
        if equipButton.mouseOn and mouseButtonDown:
            Equip()
        skillButton.isMouseOn()
        if skillButton.mouseOn and mouseButtonDown:
            Skill()
        bagButton.isMouseOn()
        if bagButton.mouseOn and mouseButtonDown:
            Bag()
        saveButton.isMouseOn()
        if saveButton.mouseOn and mouseButtonDown:
            Save()
        readButton.isMouseOn()
        if readButton.mouseOn and mouseButtonDown:
            Read()
        titleButton.isMouseOn()
        if titleButton.mouseOn and mouseButtonDown:
            gv.state = "Title"
            return 
        exitButton.isMouseOn()
        if exitButton.mouseOn and mouseButtonDown:
            exit()
        #绘制屏幕
        gv.win.blit(BM,(0,0))
        equipButton.display(gv.win)
        skillButton.display(gv.win)
        bagButton.display(gv.win)
        saveButton.display(gv.win)
        readButton.display(gv.win)
        titleButton.display(gv.win)
        exitButton.display(gv.win)
        shopButton.display(gv.win)
        hotelButton.display(gv.win)
        returnButton.display(gv.win)
        pg.display.update()
        time.sleep(0.03)

#风之谷
def FengZhiGu():
    #初始化
    battleButton = Button((380,60), u"挑战副本")
    returnButton = Button((380, 85), u"放弃副本")
    BM = pg.image.load("./pic/FengZhiGu.png").convert()
    BM = pg.transform.smoothscale(BM, (640,480))
    pg.mixer.music.load("./music/FengZhiGu.ogg")
    pg.mixer.music.play(-1)
    equipButton = Button((80,60), u"装备")
    skillButton = Button((80,85), u"技能")
    bagButton = Button((80,110), u"背包")
    saveButton = Button((80,135), u"存档")
    readButton = Button((80,160), u"读档")
    titleButton = Button((80,185), u"标题")
    exitButton =     Button((80,210), u"退出")
    #循环
    while True:
        mouseButtonDown = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                mouseButtonDown = True
        #监听按钮
        battleButton.isMouseOn()
        if battleButton.mouseOn and mouseButtonDown:
            Battle()
            gv.gd._in = "BigMap"
            return 
        returnButton.isMouseOn()
        if returnButton.mouseOn and mouseButtonDown:
            gv.gd._in = "BigMap"
            return 
        equipButton.isMouseOn()
        if equipButton.mouseOn and mouseButtonDown:
            Equip()
        skillButton.isMouseOn()
        if skillButton.mouseOn and mouseButtonDown:
            Skill()
        bagButton.isMouseOn()
        if bagButton.mouseOn and mouseButtonDown:
            Bag()
        saveButton.isMouseOn()
        if saveButton.mouseOn and mouseButtonDown:
            Save()
        readButton.isMouseOn()
        if readButton.mouseOn and mouseButtonDown:
            Read()
        titleButton.isMouseOn()
        if titleButton.mouseOn and mouseButtonDown:
            gv.state = "Title"
            return 
        exitButton.isMouseOn()
        if exitButton.mouseOn and mouseButtonDown:
            exit()
    
        #绘制屏幕
        gv.win.blit(BM,(0,0))
        battleButton.display(gv.win)
        drawText(gv.win, u"宁静祥和的风之谷，此时正面临着巨大的危机。", (155,0), length=19)
        equipButton.display(gv.win)
        skillButton.display(gv.win)
        bagButton.display(gv.win)
        saveButton.display(gv.win)
        readButton.display(gv.win)
        titleButton.display(gv.win)
        exitButton.display(gv.win)
        returnButton.display(gv.win)
        pg.display.update()
        time.sleep(0.03)

#海底世界
def HaiDiShiJie():
    #初始化
    battleButton = Button((380,60), u"挑战副本")
    returnButton = Button((380, 85), u"放弃副本")
    BM = pg.image.load("./pic/HaiDiShiJie.png").convert()
    BM = pg.transform.smoothscale(BM, (640,480))
    pg.mixer.music.load("./music/HaiDiShiJie.ogg")
    pg.mixer.music.play(-1)
    equipButton = Button((80,60), u"装备")
    skillButton = Button((80,85), u"技能")
    bagButton = Button((80,110), u"背包")
    saveButton = Button((80,135), u"存档")
    readButton = Button((80,160), u"读档")
    titleButton = Button((80,185), u"标题")
    exitButton =     Button((80,210), u"退出")
    #循环
    while True:
        mouseButtonDown = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                mouseButtonDown = True
        #监听按钮
        battleButton.isMouseOn()
        if battleButton.mouseOn and mouseButtonDown:
            Battle()
            gv.gd._in = "BigMap"
            return 
        returnButton.isMouseOn()
        if returnButton.mouseOn and mouseButtonDown:
            gv.gd._in = "BigMap"
            return 
        equipButton.isMouseOn()
        if equipButton.mouseOn and mouseButtonDown:
            Equip()
        skillButton.isMouseOn()
        if skillButton.mouseOn and mouseButtonDown:
            Skill()
        bagButton.isMouseOn()
        if bagButton.mouseOn and mouseButtonDown:
            Bag()
        saveButton.isMouseOn()
        if saveButton.mouseOn and mouseButtonDown:
            Save()
        readButton.isMouseOn()
        if readButton.mouseOn and mouseButtonDown:
            Read()
        titleButton.isMouseOn()
        if titleButton.mouseOn and mouseButtonDown:
            gv.state = "Title"
            return 
        exitButton.isMouseOn()
        if exitButton.mouseOn and mouseButtonDown:
            exit()
        #绘制屏幕
        gv.win.blit(BM,(0,0))
        battleButton.display(gv.win)
        drawText(gv.win, u"沉在海底的沉船，在海洋神秘力量的影响下，那些船员彻底变成了幽灵。", (155,0), length=19)
        equipButton.display(gv.win)
        skillButton.display(gv.win)
        bagButton.display(gv.win)
        saveButton.display(gv.win)
        readButton.display(gv.win)
        titleButton.display(gv.win)
        exitButton.display(gv.win)
        returnButton.display(gv.win)
        pg.display.update()
        time.sleep(0.03)

#火焰山
def HuoYanShan():
    #初始化
    battleButton = Button((380,60), u"挑战副本")
    returnButton = Button((380, 85), u"放弃副本")
    BM = pg.image.load("./pic/HuoYanShan.png").convert()
    BM = pg.transform.smoothscale(BM, (640,480))
    pg.mixer.music.load("./music/HuoYanShan.ogg")
    pg.mixer.music.play(-1)
    equipButton = Button((80,60), u"装备")
    skillButton = Button((80,85), u"技能")
    bagButton = Button((80,110), u"背包")
    saveButton = Button((80,135), u"存档")
    readButton = Button((80,160), u"读档")
    titleButton = Button((80,185), u"标题")
    exitButton =     Button((80,210), u"退出")
    #循环
    while True:
        mouseButtonDown = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                mouseButtonDown = True
        #监听按钮
        battleButton.isMouseOn()
        if battleButton.mouseOn and mouseButtonDown:
            Battle()
            gv.gd._in = "BigMap"
            return 
        returnButton.isMouseOn()
        if returnButton.mouseOn and mouseButtonDown:
            gv.gd._in = "BigMap"
            return 
        equipButton.isMouseOn()
        if equipButton.mouseOn and mouseButtonDown:
            Equip()
        skillButton.isMouseOn()
        if skillButton.mouseOn and mouseButtonDown:
            Skill()
        bagButton.isMouseOn()
        if bagButton.mouseOn and mouseButtonDown:
            Bag()
        saveButton.isMouseOn()
        if saveButton.mouseOn and mouseButtonDown:
            Save()
        readButton.isMouseOn()
        if readButton.mouseOn and mouseButtonDown:
            Read()
        titleButton.isMouseOn()
        if titleButton.mouseOn and mouseButtonDown:
            gv.state = "Title"
            return 
        exitButton.isMouseOn()
        if exitButton.mouseOn and mouseButtonDown:
            exit()
        
        #绘制屏幕
        gv.win.blit(BM,(0,0))
        battleButton.display(gv.win)
        drawText(gv.win, u"在炽热的火焰山周围，生活着一个神秘的民族，他们信仰着邪恶的美杜莎。", (155,0), length=19)
        equipButton.display(gv.win)
        skillButton.display(gv.win)
        bagButton.display(gv.win)
        saveButton.display(gv.win)
        readButton.display(gv.win)
        titleButton.display(gv.win)
        exitButton.display(gv.win)
        returnButton.display(gv.win)
        pg.display.update()
        time.sleep(0.03)

#通天塔
def TongTianTa():
    #初始化
    battleButton = Button((380,60), u"挑战副本")
    returnButton = Button((380, 85), u"放弃副本")
    BM = pg.image.load("./pic/TongTianTa.png").convert()
    BM = pg.transform.smoothscale(BM, (640,480))

    pg.mixer.music.load("./music/TongTianTa.ogg")
    pg.mixer.music.play(-1)  
    equipButton = Button((80,60), u"装备")
    skillButton = Button((80,85), u"技能")
    bagButton = Button((80,110), u"背包")
    saveButton = Button((80,135), u"存档")
    readButton = Button((80,160), u"读档")
    titleButton = Button((80,185), u"标题")
    exitButton =     Button((80,210), u"退出")
    #循环
    while True:
        mouseButtonDown = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                mouseButtonDown = True
        #监听按钮
        battleButton.isMouseOn()
        if battleButton.mouseOn and mouseButtonDown:
            Battle()
            gv.gd._in = "BigMap"
            return 
        returnButton.isMouseOn()
        if returnButton.mouseOn and mouseButtonDown:
            gv.gd._in = "BigMap"
            return 
        equipButton.isMouseOn()
        if equipButton.mouseOn and mouseButtonDown:
            Equip()
        skillButton.isMouseOn()
        if skillButton.mouseOn and mouseButtonDown:
            Skill()
        bagButton.isMouseOn()
        if bagButton.mouseOn and mouseButtonDown:
            Bag()
        saveButton.isMouseOn()
        if saveButton.mouseOn and mouseButtonDown:
            Save()
        readButton.isMouseOn()
        if readButton.mouseOn and mouseButtonDown:
            Read()
        titleButton.isMouseOn()
        if titleButton.mouseOn and mouseButtonDown:
            gv.state = "Title"
            return 
        exitButton.isMouseOn()
        if exitButton.mouseOn and mouseButtonDown:
            exit()
        
        #绘制屏幕
        gv.win.blit(BM,(0,0))
        battleButton.display(gv.win)
        drawText(gv.win, u"通天塔周围电闪雷鸣，要想到达天神的所在之处，必须通过闪电的考验。", (155,0), length=19)
        equipButton.display(gv.win)
        skillButton.display(gv.win)
        bagButton.display(gv.win)
        saveButton.display(gv.win)
        readButton.display(gv.win)
        titleButton.display(gv.win)
        exitButton.display(gv.win)
        returnButton.display(gv.win)
        pg.display.update()
        time.sleep(0.03)

#地下城
def DiXiaCheng():
    #初始化
    battleButton = Button((380,60), u"挑战副本")
    returnButton = Button((380, 85), u"放弃副本")
    BM = pg.image.load("./pic/DiXiaCheng.png").convert()
    BM = pg.transform.smoothscale(BM, (640,480))
    pg.mixer.music.load("./music/DiXiaCheng.ogg")
    pg.mixer.music.play(-1)
    equipButton = Button((80,60), u"装备")
    skillButton = Button((80,85), u"技能")
    bagButton = Button((80,110), u"背包")
    saveButton = Button((80,135), u"存档")
    readButton = Button((80,160), u"读档")
    titleButton = Button((80,185), u"标题")
    exitButton =     Button((80,210), u"退出")
    #循环
    while True:
        mouseButtonDown = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                mouseButtonDown = True
        #监听按钮
        battleButton.isMouseOn()
        if battleButton.mouseOn and mouseButtonDown:
            Battle()
            gv.gd._in = "BigMap"
            return 
        returnButton.isMouseOn()
        if returnButton.mouseOn and mouseButtonDown:
            gv.gd._in = "BigMap"
            return 
        equipButton.isMouseOn()
        if equipButton.mouseOn and mouseButtonDown:
            Equip()
        skillButton.isMouseOn()
        if skillButton.mouseOn and mouseButtonDown:
            Skill()
        bagButton.isMouseOn()
        if bagButton.mouseOn and mouseButtonDown:
            Bag()
        saveButton.isMouseOn()
        if saveButton.mouseOn and mouseButtonDown:
            Save()
        readButton.isMouseOn()
        if readButton.mouseOn and mouseButtonDown:
            Read()
        titleButton.isMouseOn()
        if titleButton.mouseOn and mouseButtonDown:
            gv.state = "Title"
            return 
        exitButton.isMouseOn()
        if exitButton.mouseOn and mouseButtonDown:
            exit()
        
        #绘制屏幕
        gv.win.blit(BM,(0,0))
        battleButton.display(gv.win)
        drawText(gv.win, u"不同于冒险家们居住的地方，这里充斥着恶魔、亡灵、罪犯，所到之处，都是邪恶与肮脏。", (155,0), length=19)
        equipButton.display(gv.win)
        skillButton.display(gv.win)
        bagButton.display(gv.win)
        saveButton.display(gv.win)
        readButton.display(gv.win)
        titleButton.display(gv.win)
        exitButton.display(gv.win)
        returnButton.display(gv.win)
        pg.display.update()
        time.sleep(0.03)

#装备界面
def Equip():
    #初始化
    returnButton = Button((590, 455), u"返回")
    currentRolePos = 0
    lastRoleButton = Button((60,0), u"上一个")
    nextRoleButton = Button((60,25), u"下一个")
    totalPage = len(gv.gd.bag) / 15 + 1
    currentPage = 0
    lastPageButton = Button((335,430), u"上一页")
    nextPageButton = Button((435,430), u"下一页")
    #更新装备按钮
    def updateEquipButton():
        wuQi = gv.gd.team[currentRolePos].wuQi
        fangJu = gv.gd.team[currentRolePos].fangJu
        if wuQi == -1:
            wuQiButton = Button((230,25), u"无", key = -1)
        else:
            wuQiButton = Button((230,25), gv.data.itemList[wuQi]["name"],key = wuQi)
        if fangJu == -1:
            fangJuButton = Button((230,50), u"无", key = -1)
        else:
            fangJuButton = Button((230, 50), gv.data.itemList[fangJu]["name"], key = fangJu)
        return wuQiButton, fangJuButton
    #更新角色
    def updataRole():
        rolePic = pg.image.load(gv.gd.team[currentRolePos].pic).convert_alpha()
        rolePic = pg.transform.smoothscale(rolePic, (60,80))
        wuQiButton, fangJuButton = updateEquipButton()
        return rolePic, wuQiButton, fangJuButton
    #更新道具按钮
    def updataItemButton():
        itemButtonList = []
        itemNumList = []
        for i in range(15):
            if 15 * currentPage + i >= len(gv.gd.bag):
                break
            item = gv.gd.bag[15 * currentPage + i]
            itemButtonList.append(Button((335,50 + i * 25), gv.data.itemList[item.key]["name"], key = item.key))
            itemNumList.append(item.num)
        return itemButtonList, itemNumList
    rolePic, wuQiButton, fangJuButton = updataRole()
    itemButtonList, itemNumList = updataItemButton()
     
    #循环
    while True:
        shuoMing = ""
        mouseButtonDown = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                mouseButtonDown = True
        #监听按钮
        returnButton.isMouseOn()#返回
        if returnButton.mouseOn and mouseButtonDown:
            return 
        lastRoleButton.isMouseOn()#上一个
        if lastRoleButton.mouseOn and mouseButtonDown:
            currentRolePos -= 1
            currentRolePos = currentRolePos % len(gv.gd.team)
            rolePic, wuQiButton, fangJuButton = updataRole()
        nextRoleButton.isMouseOn()#下一个
        if nextRoleButton.mouseOn and mouseButtonDown:
            currentRolePos += 1
            currentRolePos = currentRolePos % len(gv.gd.team)
            rolePic, wuQiButton, fangJuButton = updataRole()
        wuQiButton.isMouseOn()#武器
        if wuQiButton.mouseOn:
            shuoMing = gv.data.itemList[wuQiButton.key]["text"]
            if mouseButtonDown:
                UnEquip(wuQiButton.key, gv.gd.team[currentRolePos])
                wuQiButton, fangJuButton = updateEquipButton()
                itemButtonList, itemNumList = updataItemButton()
        fangJuButton.isMouseOn()#防具
        if fangJuButton.mouseOn:
            shuoMing = gv.data.itemList[fangJuButton.key]["text"]
            if mouseButtonDown:
                UnEquip(fangJuButton.key,gv.gd.team[currentRolePos])
                wuQiButton, fangJuButton = updateEquipButton()
                itemButtonList, itemNumList = updataItemButton()
        for b in itemButtonList:#道具键
            b.isMouseOn()
            if b.mouseOn:
                shuoMing = gv.data.itemList[b.key]["text"]
                if mouseButtonDown:
                    EnEquip(b.key, gv.gd.team[currentRolePos])
                    wuQiButton, fangJuButton = updateEquipButton()
                    itemButtonList, itemNumList = updataItemButton()
        lastPageButton.isMouseOn()#上一页
        if lastPageButton.mouseOn and mouseButtonDown:
            currentPage -= 1
            currentPage = currentPage % totalPage
            itemButtonList, itemNumList = updataItemButton()
        nextPageButton.isMouseOn()#下一页
        if nextPageButton.mouseOn and mouseButtonDown:
            currentPage += 1
            currentPage = currentPage % totalPage
            itemButtonList, itemNumList = updataItemButton()
        #等待绘制的变量
        hpText = "HP:" + str(gv.gd.team[currentRolePos].hp) + "/" + str(gv.gd.team[currentRolePos].maxHp)
        mpText = "MP:" + str(gv.gd.team[currentRolePos].mp) + "/" + str(gv.gd.team[currentRolePos].maxMp)
        gongJiText = u"攻击:" + unicode(gv.gd.team[currentRolePos].gongJi) 
        fangYuText = u"防御:" + unicode(gv.gd.team[currentRolePos].fangYu)
        moGongText = u"魔攻:" + unicode(gv.gd.team[currentRolePos].moGong)
        #绘制屏幕
        gv.win.fill((255,255,255))
        lastPageButton.display(gv.win)
        nextPageButton.display(gv.win)
        lastRoleButton.display(gv.win)
        nextRoleButton.display(gv.win)
        drawText(gv.win, hpText, (0,355))
        drawText(gv.win, mpText, (0,380))
        drawText(gv.win, gongJiText, (0,405))
        drawText(gv.win, fangYuText, (0,430))
        drawText(gv.win, moGongText, (0,455))
        drawText(gv.win, u"已装备的装备", (160, 0))
        drawText(gv.win, u"武器:", (160,25))
        wuQiButton.display(gv.win)
        fangJuButton.display(gv.win)
        drawText(gv.win, u"防具:", (160,50))
        drawText(gv.win, shuoMing, (0,105), length=13)
        drawText(gv.win, u"背包内道具", (335,0))
        for b in itemButtonList:
            b.display(gv.win)
        for i, n in enumerate(itemNumList):
            drawText(gv.win, str(n), (485, 50 + i * 25))
        drawText(gv.win, u"名称", (335,25))
        drawText(gv.win, u"数量", (485,25))
        gv.win.blit(rolePic, (0,0))
        returnButton.display(gv.win)
        pg.display.update()
        time.sleep(0.03)
        
#背包界面
def Bag():
    #初始化
    returnButton = Button((590, 455), u"返回")#按钮
    lastPageButton = Button((0,430), u"上一页")
    nextPageButton = Button((100,430), u"下一页")
    currentPage = 0
    totalPage = len(gv.gd.bag) / 15 + 1
    #更新道具按钮
    def updataItemButton():
        itemButtonList = []
        itemNumList = []
        for i in range(15):
            if 15 * currentPage + i >= len(gv.gd.bag):
                break
            item = gv.gd.bag[15 * currentPage + i]
            itemButtonList.append(Button((0,50 + i * 25), gv.data.itemList[item.key]["name"], key = item.key))
            itemNumList.append(item.num)
        return itemButtonList,itemNumList
    itemButtonList, itemNumList = updataItemButton()
    #循环
    while True:
        shuoMing = ""
        mouseButtonDown = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                mouseButtonDown = True
        #监听按钮
        returnButton.isMouseOn()
        if returnButton.mouseOn and mouseButtonDown:
            return 
        for b in itemButtonList:#道具键
            b.isMouseOn()
            if b.mouseOn:
                shuoMing = gv.data.itemList[b.key]["text"]
                if mouseButtonDown:
                    if b.key in [0,1,2,3,4,5,7]:
                        rPos = ChooseRoleWin([r.key for r in gv.gd.team])
                        if rPos != -1:
                            aimer = gv.gd.team[rPos]
                            UseItem(b.key, aimer)
                            itemButtonList, itemNumList = updataItemButton()
        lastPageButton.isMouseOn()
        if lastPageButton.mouseOn and mouseButtonDown:
            currentPage -= 1
            currentPage = currentPage % totalPage
            itemButtonList, itemNumList = updataItemButton()
        nextPageButton.isMouseOn()
        if nextPageButton.mouseOn and mouseButtonDown:
            currentPage += 1
            currentPage = currentPage % totalPage
            itemButtonList, itemNumList = updataItemButton()
        #待绘制的变量
        hpText = []
        mpText = []
        roleName = []
        for r in gv.gd.team:
            hpText.append("HP:" + str(r.hp) + "/" + str(r.maxHp))
            mpText.append("MP:" + str(r.mp) + "/" + str(r.maxMp))
            roleName.append(r.name)
        #绘制屏幕
        gv.win.fill((255,255,255))
        drawText(gv.win, u"背包内道具", (0,0))#显示道具按钮及数量
        drawText(gv.win, u"名称", (0,25))
        drawText(gv.win, u"数量", (125,25))
        for b in itemButtonList:
            b.display(gv.win)
        for i, n in enumerate(itemNumList):
            drawText(gv.win, str(n), (125,50+25*i))
        lastPageButton.display(gv.win)
        nextPageButton.display(gv.win)
        #绘制角色信息
        for i in range(len(roleName)):
            drawText(gv.win, roleName[i], (200 + i / 2 * 125, i % 2 * 100))
            drawText(gv.win, hpText[i], (200 + i / 2 * 125, 25 + i % 2 * 100))
            drawText(gv.win, mpText[i], (200 + i / 2 * 125, 50 + i % 2 * 100))
        drawText(gv.win, shuoMing, (200,200),length=17)#绘制说明
        drawText(gv.win, u"金钱:" + unicode(gv.gd.money), (515,430))
        returnButton.display(gv.win)
        pg.display.update()
        time.sleep(0.03)

#技能界面
def Skill():
    #初始化
    returnButton = Button((590, 455), u"返回")
    currentRolePos = 0
    lastRoleButton = Button((60,0), u"上一个")
    nextRoleButton = Button((60,25), u"下一个")
    #更新技能按钮
    def updataSkillButton():
        skillButtonList = []
        for i, s in enumerate(gv.gd.team[currentRolePos].skill):
            skillButtonList.append(Button((0, 130 + i * 25), gv.data.skillList[s]["name"], key = s))
        return skillButtonList
    #更新角色
    def updataRole():
        rolePic = pg.image.load(gv.gd.team[currentRolePos].pic).convert()
        rolePic = pg.transform.smoothscale(rolePic, (60,80))
        skillButtonList = updataSkillButton()
        return rolePic, skillButtonList
    rolePic, skillButtonList = updataRole()
    #循环
    while True:
        shuoMing = ""
        mouseButtonDown = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                mouseButtonDown = True
        #监听按钮
        returnButton.isMouseOn()
        if returnButton.mouseOn and mouseButtonDown:
            return 
        lastRoleButton.isMouseOn()
        if lastRoleButton.mouseOn and mouseButtonDown:
            currentRolePos -= 1
            currentRolePos = currentRolePos % len(gv.gd.team)
            rolePic, skillButtonList = updataRole()
        nextRoleButton.isMouseOn()
        if nextRoleButton.mouseOn and mouseButtonDown:
            currentRolePos += 1
            currentRolePos = currentRolePos % len(gv.gd.team)
            rolePic, skillButtonList = updataRole()
            
        for b in skillButtonList:#技能键
            b.isMouseOn()
            if b.mouseOn:
                shuoMing = gv.data.skillList[b.key]["text"]
                if mouseButtonDown:
                    if b.key in [1,12]:
                        rPos = ChooseRoleWin([r.key for r in gv.gd.team])
                        if rPos != -1:
                            aimer = gv.gd.team[rPos]
                            UseSkill(gv.gd.team[currentRolePos],b.key,aimer)
                    if b.key == 14:
                        UseSkill(b.key, gv.gd.team)
            pass
        #待绘制的变量
        hpText = []
        mpText = []
        roleName = []
        for r in gv.gd.team:
            hpText.append("HP:" + str(r.hp) + "/" + str(r.maxHp))
            mpText.append("MP:" + str(r.mp) + "/" + str(r.maxMp))
            roleName.append(r.name)
        #绘制屏幕
        gv.win.fill((255,255,255))
        gv.win.blit(rolePic, (0,0))#绘制角色
        lastRoleButton.display(gv.win)
        nextRoleButton.display(gv.win)
        #绘制角色信息
        for i in range(len(roleName)):
            drawText(gv.win, roleName[i], (200 + i / 2 * 125, i % 2 * 100))
            drawText(gv.win, hpText[i], (200 + i / 2 * 125, 25 + i % 2 * 100))
            drawText(gv.win, mpText[i], (200 + i / 2 * 125, 50 + i % 2 * 100))
        drawText(gv.win, u"拥有的技能", (0,105))
        for b in skillButtonList:#绘制技能按钮
            b.display(gv.win)
        drawText(gv.win, shuoMing, (0,240))#绘制技能说明
        returnButton.display(gv.win)
        pg.display.update()
        time.sleep(0.03)

#存档界面
def Save():
    #初始化
    returnButton = Button((590, 455), u"返回")
    #循环
    while True:
        mouseButtonDown = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                mouseButtonDown = True
        #监听按钮
        returnButton.isMouseOn()
        if returnButton.mouseOn and mouseButtonDown:
            return 
        
        #绘制屏幕
        gv.win.fill((255,255,255))
        returnButton.display(gv.win)
        pg.display.update()
        time.sleep(0.03)

#读档界面
def Read():
    #初始化
    returnButton = Button((590, 455), u"返回")
    #循环
    while True:
        mouseButtonDown = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                mouseButtonDown = True
        #监听按钮
        returnButton.isMouseOn()
        if returnButton.mouseOn and mouseButtonDown:
            return 
        
        #绘制屏幕
        gv.win.fill((255,255,255))
        returnButton.display(gv.win)
        pg.display.update()
        time.sleep(0.03)

#战斗逻辑
def Battle(mobList = [1,2,3,4], bgPath = "./pic/Battle.png"):
    #初始化战斗窗口
    w = BattleWin(gv.win)
    # 初始化怪物队列
    mobTeam = []
    for key in mobList:
        mobTeam.append(Role(gv.data.mobList[key]))
    # 初始化行动顺序
    moveQueue = range(len(gv.gd.team)) + [(index + 10) for index in range(len(mobTeam))]
    random.shuffle(moveQueue)
    #初始化战斗状态
    if moveQueue[0] < 10:
        state = "waitBasic"
        mw = MiniBasicWin(gv.win, mobTeam, gv, moveQueue[0])
    else:
        state = "AICommand"
    count = 0
    while True:
        w.run(gv, mobTeam, moveQueue, state)
        #我方行动时
        if state == "waitBasic":
            command = mw.run()
            if command[0] != "None":
                text = getCommand(command, moveQueue[0], gv, mobTeam)
                state = "donghua"
                count = 15
        #敌方行动时
        elif state == "AICommand":
            command = AI()
            text = getCommand(command, moveQueue[0], gv, mobTeam)
            state = "donghua"
            count = 15
        #演示动画
        elif state == "donghua":
            DonghuaWin(gv.win, text)
            count -= 1
            if count <= 0:
                moveQueue.pop(0)
                if moveQueue[0] < 9:
                    state = "waitBasic"
                    mw = MiniBasicWin(gv.win, mobTeam, gv, moveQueue[0])
                else:
                    state = "AICommand"
        #当行动队列数小于总人数，插入新行动者
        if len(moveQueue) <= len(gv.gd.team) + len(mobTeam):
            tempMoveQueue = range(len(gv.gd.team)) + [(index + 10) for index in range(len(mobTeam))]
            random.shuffle(tempMoveQueue)
            moveQueue += tempMoveQueue
        pg.display.update()

#神秘之地界面
def Unknown():
    #初始化
    returnButton = Button((590, 455), u"返回")
    textList = [u"遇见了一伙佣兵。",
                u"遇见了一个商人。",
                u"遇见了一个知名的冒险家。",
                u"遇见了一家旅馆。",
                u"遇见了一帮怪物。",
                u"什么事都没发生。",]
    num = random.randint(0,5)
    #循环
    while True:
        mouseButtonDown = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                mouseButtonDown = True
        #监听按钮
        returnButton.isMouseOn()
        if returnButton.mouseOn and mouseButtonDown:
            return 
        if mouseButtonDown:
            if num == 0:
                JiuGuan([0,1,2,3,4,5])
                return
            elif num == 1:
                l = []
                for i in range(5):
                    l.append(random.randint(0,27))
                Shop(l)
                return
            elif num == 2:
                l = []
                for i in range(5):
                    for i in range(5):
                        l.append(random.randint(0,20))
                LearnSkill(l)
                return
            elif num == 3:
                Hotel()
            elif num == 4:
                Battle()
                return
            elif num == 5:
                return
        
        #绘制屏幕
        gv.win.fill((255,255,255))
        drawText(gv.win, textList[num], (0,0))
        returnButton.display(gv.win)
        pg.display.update()
        time.sleep(0.03)

#酒馆界面
def JiuGuan(roleList = []):
    #初始化
    returnButton = Button((590, 455), u"返回")
    ourTeamRoleKeyList = [gv.gd.team[i].key for i in range(len(gv.gd.team))]
    #更新伙伴按钮
    def updateOurRoleButton():
        ourRoleButtonList = []
        for i, r in enumerate(gv.gd.team):
            ourRoleButtonList.append(Button((320,25 + i * 25), r.name, r.key))
        return ourRoleButtonList
    #更新佣兵按钮
    def updataShopRoleButton():
        shopRoleButtonList = []
        for i, r in enumerate(roleList):
            if r not in ourTeamRoleKeyList:
                shopRoleButtonList.append(Button((0, 25 + i *25), gv.data.roleList[r]["name"], r))
        return shopRoleButtonList
    ourRoleButtonList = updateOurRoleButton()
    shopRoleButtonList = updataShopRoleButton()
    #循环
    while True:
        shuoMing = ""
        mouseButtonDown = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                mouseButtonDown = True
        #监听按钮
        returnButton.isMouseOn()
        if returnButton.mouseOn and mouseButtonDown:#返回
            return 
        for b in ourRoleButtonList:#伙伴按钮
            b.isMouseOn()
            if b.mouseOn:
                shuoMing = gv.data.roleList[b.key]["text"]
                if mouseButtonDown:
                    SellRole(b.key)
                    ourTeamRoleKeyList = [gv.gd.team[i].key for i in range(len(gv.gd.team))]
                    shopRoleButtonList = updataShopRoleButton()
                    ourRoleButtonList = updateOurRoleButton()
                    
        for b in shopRoleButtonList:#佣兵按钮
            b.isMouseOn()
            if b.mouseOn:
                shuoMing = gv.data.roleList[b.key]["text"]
                if mouseButtonDown:
                    BuyRole(b.key)
                    ourTeamRoleKeyList = [gv.gd.team[i].key for i in range(len(gv.gd.team))]
                    shopRoleButtonList = updataShopRoleButton()
                    ourRoleButtonList = updateOurRoleButton()
        
        #绘制屏幕
        gv.win.fill((255,255,255))
        drawText(gv.win, u"可雇佣的佣兵(40金/位)", (0,0))#绘制佣兵按钮
        for b in shopRoleButtonList:
            b.display(gv.win)
        drawText(gv.win, u"可解雇的伙伴(返还20金/位)", (320,0))#绘制伙伴按钮
        for b in ourRoleButtonList:
            b.display(gv.win)
        #绘制说明
        drawText(gv.win, shuoMing, (0,240))
        drawText(gv.win, u"金钱:" + unicode(gv.gd.money), (515,430))
        returnButton.display(gv.win)
        pg.display.update()
        time.sleep(0.03)

#商店界面
def Shop(itemList = []):
    #初始化
    returnButton = Button((590, 455), u"返回")
    shopItemCurrentPage = 0
    bagItemCurrentPage = 0
    shopItemTotalPage = len(itemList) / 7 + 1
    bagItemTotalPage = len(gv.gd.bag) / 7 + 1
    shopItemLastPageButton = Button((0,240), u"上一页")
    shopItemNextPageButton = Button((100,240), u"下一页")
    bagItemLastPageButton = Button((320,240), u"上一页")
    bagItemNextPageButton = Button((420,240), u"下一页")
    
    #更新商店内道具
    def updataShopItem():
        shopItemButtonList = []
        shopItemMoney = []
        for i in range(7):
            if i + shopItemCurrentPage * 7 >= len(itemList):
                break
            key = itemList[i + shopItemCurrentPage * 7]
            shopItemButtonList.append(Button((0, 50 + i *25), gv.data.itemList[key]["name"], 
                                             key=key))
            shopItemMoney.append(gv.data.itemList[key]["money"])
        return shopItemButtonList, shopItemMoney
    shopItemButtonList, shopItemMoneyList = updataShopItem()
    #更新背包内道具
    def updataBagItem():
        bagItemButtonList = []
        bagItemNumList = []
        bagItemMoneyList = []
        for i in range(7):
            if i + bagItemCurrentPage * 7 >= len(gv.gd.bag):
                break
            key = gv.gd.bag[i + bagItemCurrentPage * 7].key
            bagItemButtonList.append(Button((320, 50 + i * 25), gv.data.itemList[key]["name"], key=key))
            bagItemNumList.append(gv.gd.bag[i + bagItemCurrentPage * 7].num)
            bagItemMoneyList.append(gv.data.itemList[key]["sellMoney"])
        return bagItemButtonList, bagItemNumList, bagItemMoneyList
    bagItemButtonList, bagItemNumList, bagItemMoneyList =  updataBagItem()
    #循环
    while True:
        shuoMing = ""
        mouseButtonDown = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                mouseButtonDown = True
        #监听按钮
        returnButton.isMouseOn()
        if returnButton.mouseOn and mouseButtonDown:
            return 
        for b in shopItemButtonList:#商店内道具
            b.isMouseOn()
            if b.mouseOn:
                shuoMing = gv.data.itemList[b.key]["text"]
                if mouseButtonDown:
                    BuyItem(b.key)
                    bagItemTotalPage = len(gv.gd.bag) / 7 + 1
                    bagItemButtonList, bagItemNumList, bagItemMoneyList =  updataBagItem()
        for b in bagItemButtonList:#背包内道具
            b.isMouseOn()
            if b.mouseOn:
                shuoMing = gv.data.itemList[b.key]["text"]
                if mouseButtonDown:
                    SellItem(b.key)
                    bagItemTotalPage = len(gv.gd.bag) / 7 + 1
                    bagItemButtonList, bagItemNumList, bagItemMoneyList =  updataBagItem()
        shopItemLastPageButton.isMouseOn()
        if shopItemLastPageButton.mouseOn and mouseButtonDown:
            shopItemCurrentPage -= 1
            shopItemCurrentPage = shopItemCurrentPage % shopItemTotalPage
            shopItemButtonList, shopItemMoneyList = updataShopItem()
        shopItemNextPageButton.isMouseOn()
        if shopItemNextPageButton.mouseOn and mouseButtonDown:
            shopItemCurrentPage += 1
            shopItemCurrentPage = shopItemCurrentPage % shopItemTotalPage
            shopItemButtonList, shopItemMoneyList = updataShopItem()
        bagItemLastPageButton.isMouseOn()
        if bagItemLastPageButton.mouseOn and mouseButtonDown:
            bagItemCurrentPage -= 1
            bagItemCurrentPage = bagItemCurrentPage % bagItemTotalPage
            bagItemButtonList, bagItemNumList, bagItemMoneyList =  updataBagItem()
        bagItemNextPageButton.isMouseOn()
        if bagItemNextPageButton.mouseOn and mouseButtonDown:
            bagItemCurrentPage += 1
            bagItemCurrentPage = bagItemCurrentPage % bagItemTotalPage
            bagItemButtonList, bagItemNumList, bagItemMoneyList =  updataBagItem()
        #绘制屏幕
        gv.win.fill((255,255,255))
        returnButton.display(gv.win)
        drawText(gv.win, u"可购买的道具", (0,0))#绘制商店内道具
        drawText(gv.win, u"名称", (0,25))
        drawText(gv.win, u"价格", (125,25))
        for b in shopItemButtonList:
            b.display(gv.win)
        for i, m in enumerate(shopItemMoneyList):
            drawText(gv.win, str(m), (125,50 + i * 25))
        shopItemLastPageButton.display(gv.win)
        shopItemNextPageButton.display(gv.win)
        drawText(gv.win, u"背包内的道具", (320,0))#绘制背包内道具
        drawText(gv.win, u"名称", (320,25))
        drawText(gv.win, u"数量", (445,25))
        drawText(gv.win, u"售价", (545,25))
        for b in bagItemButtonList:
            b.display(gv.win) 
        for i, n in enumerate(bagItemNumList):
            drawText(gv.win, str(n), (445,50 + i * 25))
        for i, m in enumerate(bagItemMoneyList):
            drawText(gv.win, str(m), (545,50 + i * 25))
        bagItemLastPageButton.display(gv.win)
        bagItemNextPageButton.display(gv.win)  
        drawText(gv.win, shuoMing, (0,265))#绘制说明
        drawText(gv.win, u"金钱:" + unicode(gv.gd.money) , (515, 430))
        pg.display.update()
        time.sleep(0.03)

#旅馆界面
def Hotel():
    #初始化
    returnButton = Button((590, 455), u"返回")
    restButton = Button((0,0), u"休息(10金)")
    #循环
    while True:
        mouseButtonDown = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                mouseButtonDown = True
        #监听按钮
        returnButton.isMouseOn()
        if returnButton.mouseOn and mouseButtonDown:
            return 
        restButton.isMouseOn()
        if restButton.mouseOn and mouseButtonDown:
            Rest()
        
        #绘制屏幕
        gv.win.fill((255,255,255))
        returnButton.display(gv.win)
        pg.display.update()
        time.sleep(0.03)

#学习技能界面
def LearnSkill(skillList = []):
    #初始化
    returnButton = Button((590, 455), u"返回")
    currentRolePos = 0
    lastRoleButton = Button((60,0), u"上一个")
    nextRoleButton = Button((60,25), u"下一个")
    def updataRole():
        rolePic = pg.image.load(gv.gd.team[currentRolePos].pic).convert_alpha()
        rolePic = pg.transform.smoothscale(rolePic, (60,80))
        return rolePic
    rolePic = updataRole()
    #更新已拥有技能
    def updataOurSkill():
        ourSkillButtonList = []
        for i, s in enumerate(gv.gd.team[currentRolePos].skill):
            ourSkillButtonList.append(Button((160,25 + i * 25), gv.data.skillList[s]["name"], key=s))
        return ourSkillButtonList
    ourSkillButtonList = updataOurSkill()
    #更新可学习技能
    def updataShopSkill():
        shopSkillButtonList = []
        for i, s in enumerate(gv.gd.team[currentRolePos].canStudySkill):
            if s not in gv.gd.team[currentRolePos].skill:
                shopSkillButtonList.append(Button((310,25 + i * 25), gv.data.skillList[s]["name"], key = s))
        return shopSkillButtonList
    shopSkillButtonList= updataShopSkill()
    #循环
    while True:
        shuoMing = ""
        mouseButtonDown = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                mouseButtonDown = True
        #监听按钮
        returnButton.isMouseOn()
        if returnButton.mouseOn and mouseButtonDown:
            return 
        
        lastRoleButton.isMouseOn()
        if lastRoleButton.mouseOn and mouseButtonDown:
            currentRolePos -= 1
            currentRolePos = currentRolePos % len(gv.gd.team)
            rolePic = updataRole()
            ourSkillButtonList = updataOurSkill()
            shopSkillButtonList = updataShopSkill()
        nextRoleButton.isMouseOn()
        if nextRoleButton.mouseOn and mouseButtonDown:
            currentRolePos += 1
            currentRolePos = currentRolePos % len(gv.gd.team)
            rolePic = updataRole()
            ourSkillButtonList = updataOurSkill()
            shopSkillButtonList = updataShopSkill()
        for b in ourSkillButtonList:
            b.isMouseOn()
            if b.mouseOn:
                shuoMing = gv.data.skillList[b.key]["text"]
        for b in shopSkillButtonList:
            b.isMouseOn()
            if b.mouseOn:
                shuoMing = gv.data.skillList[b.key]["text"]
                if mouseButtonDown:
                    StudySkill(b.key,gv.gd.team[currentRolePos])
                    ourSkillButtonList = updataOurSkill()
                    shopSkillButtonList = updataShopSkill()
        #绘制屏幕
        gv.win.fill((255,255,255))
        gv.win.blit(rolePic, (0,0))#绘制角色
        lastRoleButton.display(gv.win)
        nextRoleButton.display(gv.win)
        drawText(gv.win, u"已拥有技能", (160,0))#绘制已有技能
        for b in ourSkillButtonList:
            b.display(gv.win)
        drawText(gv.win, u"可学习技能(40金/个)", (310,0))#绘制可学习技能
        for b in shopSkillButtonList:
            b.display(gv.win)
        drawText(gv.win, shuoMing, (0,240))#绘制技能说明
        drawText(gv.win, u"金钱" + unicode(gv.gd.money), (515,430))
        returnButton.display(gv.win)
        pg.display.update()
        time.sleep(0.03)

#测试用实例
def testData():
    gd = GameData()
    gd.team = []
    gd.team.append(Role(gv.data.roleList[0]))
    gd.team.append(Role(gv.data.roleList[1]))
    gd.team.append(Role(gv.data.roleList[2]))
    gd.team.append(Role(gv.data.roleList[3]))
    for i in range(28):
        gd.bag.append(Item(i, 2))
    gd.money = 1000
    return gd
    
######################
###各种封装好的函数###
######################
#装备装备
def EnEquip(key, aimer):
    result = CheckEquip(key, aimer.key)#检查装备是否匹配
    if not result:
        return 
    if key in [8,10,12,14,16,18]:#装备木剑、木盾、法杖、法典、木弓、飞刀
        UnEquip(aimer.wuQi, aimer)
        aimer.gongJi += 2
        aimer.wuQi = key
    elif key in [9,11,13,15,17,19]:#装备铁剑、铁盾、魔杖、圣典、铁弓、利刃
        UnEquip(aimer.wuQi, aimer)
        aimer.gongJi += 4
        aimer.wuQi = key
    elif key in [20,22,24,26]:#装备铁甲、魔法长袍、狩猎之衣、紧身衣
        UnEquip(aimer.fangJu, aimer)
        aimer.fangYu += 2
        aimer.fangJu = key
    elif key in [21,23,25,27]:#装备铜甲、巫师长袍、守望之衣、黑暗之衣
        UnEquip(aimer.fangJu, aimer)
        aimer.fangYu += 4
        aimer.fangJu = key
    for i in range(len(gv.gd.bag)):
        if gv.gd.bag[i].key == key:
            gv.gd.bag[i].num -= 1
            if gv.gd.bag[i].num == 0:
                gv.gd.bag.pop(i)
            return
#卸下装备
def UnEquip(key, aimer):
    if key == -1:
        return
    if key == aimer.wuQi:
        aimer.wuQi = -1
    elif  key == aimer.fangJu:
        aimer.fangJu = -1
    if key in [8,10,12,14,16,18]:#卸下木剑、木盾、法杖、法典、木弓、飞刀
        aimer.gongJi -= 2
    elif key in [9,11,13,15,17,19]:#卸下铁剑、铁盾、魔杖、圣典、铁弓、利刃
        aimer.gongJi -= 4
    elif key in [20,22,24,26]:#卸下铁甲、魔法长袍、狩猎之衣、紧身衣
        aimer.fangYu -= 2
    elif key in [21,23,25,27]:#卸下铜甲、巫师长袍、守望之衣、黑暗之衣
        aimer.fangYu -= 4
    for i in range(len(gv.gd.bag)):
        if gv.gd.bag[i].key == key:
            gv.gd.bag[i].num += 1
            return
    gv.gd.bag.append(Item(key, 1))
    
#检查装备是否匹配
def CheckEquip(key, aimerKey):
    table = [[8,9,20,21],#战士可装备木剑、铁剑、铁甲、铜甲
             [10,11,20,21],#骑士
             [12,13,22,23],#法师
             [14,15,22,23],#牧师
             [16,17,24,25],#射手
             [18,19,26,27],#刺客
             ]
    if key in table[aimerKey]:
        return True
    else:
        return False
#使用道具
def UseItem(key, aimer):
    if key == 0:
        if not aimer.state.death:
            aimer.hp += (4 + random.randint(1,6))
            aimer.hp = min(aimer.hp, aimer.maxHp)
    elif key == 1:
        if not aimer.state.death:
            aimer.hp += (8 + random.randint(1,6))
            aimer.hp = min(aimer.hp, aimer.maxHp)
    if key == 2:
        if not aimer.state.death:
            aimer.hp += (16 + random.randint(1,6))
            aimer.hp = min(aimer.hp, aimer.maxHp)
    if key == 3:
        if not aimer.state.death:
            aimer.mp += (4 + random.randint(1,6))
            aimer.mp = min(aimer.mp, aimer.maxMp)
    if key == 4:
        if not aimer.state.death:
            aimer.hp += (8 + random.randint(1,6))
            aimer.mp = min(aimer.mp, aimer.maxMp)
        pass
    if key == 5:
        if not aimer.state.death:
            aimer.hp += (16 + random.randint(1,6))
            aimer.mp = min(aimer.mp, aimer.maxMp)
        pass
    if key == 7:
        aimer.state.death = False
        aimer.hp += ( 4 + random.randint(1,6))
        aimer.hp = min(aimer.mp, aimer.maxMp)        
    for i in range(len(gv.gd.bag)):
        if gv.gd.bag[i].key == key:
            gv.gd.bag[i].num -= 1
            if gv.gd.bag[i].num == 0:
                gv.gd.bag.pop(i)
        return
#使用技能
def UseSkill(user, key, aimer):
    if key == 1:#治疗术
        if user.mp < 4:
            drawText(gv.win, u"魔力不足！", (320,240))
            pg.display.update()
            return
        user.mp -= 4
        if not aimer.state.death:
            aimer.hp += user.moGong + 4 - random.randint(1,5)
            aimer.hp = min(aimer.hp, aimer.maxHp)
    elif key == 12:#复活术
        if user.mp < 8:
            drawText(gv.win, u"魔力不足", (320,240))
            pg.display.update()
            return
        user.mp -= 8
        aimer.state.death = False
        aimer.hp += user.moGong + 4 - random.randint(1,5)
        aimer.hp = min(aimer.hp, aimer.maxHp)
    elif key == 14:#圣光术
        if user.mp < 16:
            drawText(gv.win, u"魔力不足", (320,240))
            pg.display.update()
            return
        user.mp -= 16
        for r in aimer:
            if not r.state.death:
                r.hp += user.moGong + 4 - random.randint(1,5)
                r.maxHp = min(r.hp, r.maxHp)
#雇佣佣兵
def BuyRole(key):
    if gv.gd.money < 40:
        drawText(gv.win, u"钱不够！", (320,240))
        pg.display.update()
        time.sleep(1)
        return
    if len(gv.gd.team) == 4:
        drawText(gv.win, u"人满了！", (320,240))
        pg.display.update()
        time.sleep(1)
        return
    gv.gd.money -= 40
    gv.gd.team.append(Role(gv.data.roleList[key]))
        
#解雇佣兵
def SellRole(key):
    if len(gv.gd.team) == 1:
        drawText(gv.win, u"必须留下一个人", (320,240))
        pg.display.update()
        time.sleep(1)
        return 
    gv.gd.money += 25
    for i in range(len(gv.gd.team)):
        if gv.gd.team[i].key == key:
            gv.gd.team.pop(i)
            return
#购买道具
def BuyItem(key):
    if gv.gd.money < gv.data.itemList[key]["money"]:
        SysTip(gv.win, u"钱不够！")
        return
    gv.gd.money -= gv.data.itemList[key]["money"]
    for i in range(len(gv.gd.bag)):
        if gv.gd.bag[i].key == key:
            gv.gd.bag[i].num += 1
            return
    gv.gd.bag.append(Item(key, 1))
#贩卖道具
def SellItem(key):
    gv.gd.money += gv.data.itemList[key]["sellMoney"]
    for i in range(len(gv.gd.bag)):
        if gv.gd.bag[i].key == key:
            gv.gd.bag[i].num -= 1
            if gv.gd.bag[i].num == 0:
                gv.gd.bag.pop(i)
            return
#学习技能
def StudySkill(key, aimer):
    if gv.gd.money < 40:
        SysTip(gv.win, u"钱不够！")
        return
    gv.gd.money -= 40
    aimer.skill.append(key)
#休息
def Rest():
    if gv.gv.money < 10:
        SysTip(gv.win, u"钱不够")
        return
    for r in gv.gd.team:
        r.state.death = False
        r.hp = r.maxHp

#选择角色
def ChooseRoleWin(roleList):
    winPic = pg.transform.smoothscale(gv.winPic, (145,155))
    roleButton = []
    cancelButton = Button((320,290), u"取消", key = -1)
    for (i, r) in enumerate(roleList):
        roleButton.append(Button((320,190 + i * 25), gv.data.roleList[r]["name"], key=i))
    while True:
        mouseButtonDown = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                mouseButtonDown = True
        #监听按钮
        for b in roleButton:
            b.isMouseOn()
            if b.mouseOn and mouseButtonDown:
                return b.key
        cancelButton.isMouseOn()
        if cancelButton.mouseOn and mouseButtonDown:
            return -1
        #绘制窗口
        gv.win.blit(winPic, (300,170))
        for b in roleButton:
            b.display(gv.win)
        cancelButton.display(gv.win)
        pg.display.update()
        time.sleep(0.03)
    return

#全局变量
gv = GlobalValue()
main()