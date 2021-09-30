import os
import re

def ping():
    ip= input("请输入需要检测的地址")
    cmd = os.popen('ping %s'%ip)
    cmdread = cmd.read()
    #print(cmdread)
    state = re.findall(r'回复:(.*)。', cmdread)
    tip = ''
    if state == []:
        speed = re.findall(r'平均 = (.*)ms', cmdread)
        if speed == []:
            tip = ("检测的地址：%s,存在异常"%(ip))
        else:
            speed = int(speed[0])
            if speed < 100:
                tip = ("检测的地址：%s,连接耗时：%d毫秒,速度较快"%(ip,speed))
            if speed > 100:
                tip = ("检测的地址：%s,连接耗时：%d毫秒,速度较慢"%(ip,speed))
    else:
        print("检测的地址：%s,无法连接"%(ip))
    print(tip)

    
while True:
    ping()
