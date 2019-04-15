#coding:utf-8
from draw import drawPic43, drawPic, drawText
import pygame as pg
from Button import Button

#战斗窗口
class BattleWin:

    def __init__(self, win, bg="./pic/Battle.png"):
        self.win = win
        self.bg = pg.transform.smoothscale(pg.image.load(bg).convert(), (640, 480))
        self.state = "chooseBasic"
        self.command = []

    def run(self, gv, mobTeam, moveQueue, state):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()

        #绘制背景
        self.win.blit(self.bg, (0, 0))
        #绘制我方角色信息
        for i, r in enumerate(gv.gd.team):
            drawPic43(self.win, r.pic, (0, 80 * i))
            drawText(self.win, "HP:" + str(r.hp) + "/" + str(r.maxHp), (60, 80 * i))
            drawText(self.win, "MP:" + str(r.mp) + "/" + str(r.maxMp), (60, 25 + 80 * i))
        #绘制敌方角色信息
        for i, r in enumerate(mobTeam):
            drawPic43(self.win, r.pic, (460, 80 * i))
            drawText(self.win, "HP:" + str(r.hp) + "/" + str(r.maxHp), (360, 80 * i))
            drawText(self.win, "MP:" + str(r.mp) + "/" + str(r.maxMp), (360, 25 + 80 * i))
        #绘制队列信息
        drawText(self.win, u"行动顺序", (520, 0))
        for i, key in enumerate(moveQueue):
            if key < 10:
                drawText(self.win, gv.gd.team[key].name, (520, 25 + i * 25))
            else:
                drawText(self.win, mobTeam[key - 10].name, (520, 25 + i * 25))

#基础选择窗口
class MiniBasicWin:

    def __init__(self, win, mobTeam, gv, userpos):
        self.win = win
        self.state = "Basic"
        self.returnButton = Button((170, 265), u"返回")
        #基础按钮
        self.gongjiButton = Button((170, 140), u"攻击")
        self.jinengButton = Button((170, 165), u"技能")
        self.wupinButton = Button((170, 190), u"物品")
        self.taopaoButton = Button((170, 215), u"逃跑")
        #技能按钮
        #此处从数据库中获取角色技能表中的技能key值对应的技能名
        self.jinengButtonList = [Button((170, 140 + 25 * i),
                                    gv.data.skillList[gv.gd.team[userpos].skill[i]]['name'],
                                        gv.gd.team[userpos].skill[i])
                                 for i in range(len(gv.gd.team[userpos].skill))]
        self.wupinPage = 0
        self.allPage = len(gv.gd.bag) / 4
        self.wupinButtonList = [Button((170, 140 + 25 * i),
                                    gv.data.itemList[gv.gd.bag[i].key]['name'],
                                        gv.gd.bag[i].key)
                                 for i in range(len(gv.gd.bag))]
        self.lastPageButton = Button((170, 240), u"上页")
        self.nextPageButton = Button((245, 240), u"下页")
        #队友按钮
        self.roleButtonList = [Button((170, 140 + 25 * i), gv.gd.team[i].name) for i in range(len(gv.gd.team))]
        #怪物按钮
        self.mobButtonList = [Button((170, 140 + 25 * i), mobTeam[i].name) for i in range(len(mobTeam))]
        self.commandList = []

    def run(self):
        if self.state == "Basic":
            result = self.run_basic()
        elif self.state == "jineng":
            result = self.run_jineng()
        elif self.state == "wupin":
            result = self.run_wupin()
        elif self.state == "role":
            result = self.run_role()
        elif self.state == "mob":
            result = self.run_mob()
        if result:
            return self.commandList
        else:
            return ["None"]
    #选择攻击、技能、物品、逃跑
    def run_basic(self):
        #监听按钮
        self.gongjiButton.isMouseOn()
        self.jinengButton.isMouseOn()
        self.wupinButton.isMouseOn()
        self.taopaoButton.isMouseOn()
        #监听事件
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if self.gongjiButton.mouseOn:
                    self.commandList.append("gongji")
                    self.state = "mob"
                    return False
                elif self.jinengButton.mouseOn:
                    self.commandList.append("jineng")
                    self.state = "jineng"
                    return False
                elif self.wupinButton.mouseOn:
                    self.commandList.append("wupin")
                    self.state = "wupin"
                    return False
                elif self.taopaoButton.mouseOn:
                    self.commandList.append("taopao")
                    return True

        self.gongjiButton.display(self.win)
        self.jinengButton.display(self.win)
        self.wupinButton.display(self.win)
        self.taopaoButton.display(self.win)
    #选择技能
    def run_jineng(self):
        for b in self.jinengButtonList:
            b.isMouseOn()
        self.returnButton.isMouseOn()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if self.returnButton.mouseOn:
                    self.state = "Basic"
                    self.commandList.pop(-1)
                    return False
                for i, b in enumerate(self.jinengButtonList):
                    if b.mouseOn:
                        print b.key
                        if b.key in [0]:#无需选择的技能
                            self.commandList.append(b.key)
                            return True
                        elif b.key in [1]:#需要选择队友的技能
                            self.commandList.append(b.key)
                            self.state = "role"
                            return False
                        elif b.key in [2]:#需要选择敌人的技能
                            self.commandList.append(b.key)
                            self.state = "mob"
                            return False

        for b in self.jinengButtonList:
            b.display(self.win)
        self.returnButton.display(self.win)

    #选择物品
    def run_wupin(self):
        for b in self.wupinButtonList:
            b.isMouseOn()
        self.returnButton.isMouseOn()
        self.nextPageButton.isMouseOn()
        self.lastPageButton.isMouseOn()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if self.returnButton.mouseOn:
                    self.state = "Basic"
                    self.commandList.pop(-1)
                    return False
        for b in self.wupinButtonList:
            b.display(self.win)
        self.returnButton.display(self.win)
        self.nextPageButton.display(self.win)
        self.lastPageButton.display(self.win)

    #选择我方角色
    def run_role(self):
        for b in self.roleButtonList:
            b.isMouseOn()
        self.returnButton.isMouseOn()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                for i, b in enumerate(self.roleButtonList):
                    if b.mouseOn:
                        self.commandList.append(i)
                        return True
                if self.returnButton.mouseOn:
                    if self.commandList[0] == "gongji":
                        self.state = "Basic"
                    elif self.commandList[0] == "jineng":
                        self.state = "jineng"
                    elif self.commandList[0] == "wupin":
                        self.state = "wupin"
                    self.commandList.pop(-1)
                    return False
        for b in self.roleButtonList:
            b.display(self.win)
        self.returnButton.display(self.win)
    #选择敌方角色
    def run_mob(self):
        for b in self.mobButtonList:
            b.isMouseOn()
        self.returnButton.isMouseOn()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                for i, b in enumerate(self.mobButtonList):
                    if b.mouseOn:
                        self.commandList.append(i)
                        return True
                if self.returnButton.mouseOn:
                    if self.commandList[0] == "gongji":
                        self.state = "Basic"
                    elif self.commandList[0] == "jineng":
                        self.state = "jineng"
                    elif self.commandList[0] == "wupin":
                        self.state = "wupin"
                    self.commandList.pop(-1)
                    return False
        for b in self.mobButtonList:
            b.display(self.win)
        self.returnButton.display(self.win)
        return False

#怪物选择窗口
class MiniMobWin:
    def __init__(self, win, mobTeam):
        self.win = win
        self.buttonList = [Button((270, 190 + i), mobTeam[i].name) for i in range(len(mobTeam))]
        self.returnButton = Button((270, 290), u"返回")

    def run(self):
        for b in self.buttonList:
            b.isMouseOn()
        self.returnButton.isMouseOn()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                for i, b in self.buttonList:
                    if b.mouseOn:
                        return i
                if self.returnButton.mouseOn:
                    return -2
        for b in self.buttonList:
            b.display(self.win)
        return -1

#动画窗口
def DonghuaWin(win, text):

    pg.draw.rect(win, [0, 255, 0], [0, 320, 640, 160], 0)
    for i, t in enumerate(text):
        drawText(win, t, (0, 320 + i * 25))
