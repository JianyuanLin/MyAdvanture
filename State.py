#coding:utf-8
#状态类
class State():
    def __init__(self):
        self.death = False
        self.gongJiUpRound = 0
        self.gongJiDownrRound = 0
        self.moGongUpRound = 0
        self.moGongDownRound = 0
        self.fangYuUpRound = 0
        self.fangYuDownRound = 0
        self.chaoFengRound = 0
        self.chaoFengZhePos = -1
        self.shouHuRound = 0
        self.shouHuZhePos = -1
        self.wuDiRound = 0
        self.zhuoShaoRound = 0
        self.xunYunRound = 0
        self.JuJiRound = 0
        self.gongSuUpRound = 0
        self.KeYinNum = 0
        self.shanBiRound = 0
        self.huiFuRound = 0