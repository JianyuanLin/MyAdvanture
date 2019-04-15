#coding:utf-8
#角色类
from State import State
class Role:
    def __init__(self, role):
        self.key = role["key"]
        self.name = role["name"]
        self.text = role["text"]
        self.maxHp = role["maxHp"]
        self.hp = role["maxHp"]
        self.maxMp = role["maxMp"]
        self.mp = role["maxMp"]
        self.gongJi = role["gongJi"]
        self.fangYu = role["fangYu"]
        self.moGong = role["moGong"]
        self.pic = role["pic"]
        self.wuQi = -1
        self.fangJu = -1
        self.skill = role["skill"][:]
        self.canStudySkill = role["canStudySkill"]
        self.state = State()