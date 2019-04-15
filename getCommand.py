#coding:utf-8

def getCommand(command, userPos, gv, mobTeam):
    text = []
    if command[0] == "gongji":
        if userPos < 9:
            username = gv.gd.team[userPos].name
            aimername = mobTeam[command[1]].name
        else:
            username =mobTeam[userPos - 10].name
            aimername = gv.gd.team[command[1]].name
        text.append(username+u"攻击"+aimername)
    if command[0] == "jineng":
        if userPos < 9:
            username = gv.gd.team[userPos].name
        else:
            username =mobTeam[userPos - 10].name
        text.append(username+u"使用了"+gv.data.skillList[command[1]]['name'])
    return text