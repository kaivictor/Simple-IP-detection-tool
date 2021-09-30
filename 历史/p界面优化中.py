import tkinter
import os
import time
#import subprocess
import re
import tkinter.messagebox
import tkinter.filedialog
from PIL import Image, ImageTk
from tkinter import filedialog

global Pattern
global AllErrorIp
AllErrorIp = ['错误的IP']
global Filepath
Filepath = ''

def ping(ip):
    global allIp
    AllIpText=("计划中：")
    if PatternMultiple['state']=='normal':
        AllIpText=("%s\n%s"%(AllIpText,allIp))
    elif PatternSingle['state']=='normal':
        for e in range(0,len(allIp)):
            AllIpText=("%s\n%s"%(AllIpText,allIp[e]))
    print(AllIpText)
    stateL1['text']=AllIpText
    cmd = os.popen('ping %s'%ip)
    cmdread = cmd.read()
    state = re.findall(r'回复:(.*)。', cmdread)
    if state == []:
        speed = re.findall(r'平均 = (.*)ms', cmdread)
        if speed != []:
            print("%s可连接，速度：%s ms"%(ip,speed))
        else:
            print("断开") 
            AllErrorIp.append(ip)
    else:
        print("断开")
      
        AllErrorIp.append(ip)
    print(AllErrorIp)

    
def GetFile():
    global Filepath
    FileWin = tkinter.Tk() 
    FileWin.withdraw()
    Filepath = filedialog.askopenfilename(title=u'多个地址',filetype=[("TXT",".txt")])
    print(Filepath)

def stratcmd():#开始命令
    start['text'] = "稍等"
    start['state']='disable'
    #i = '192.168.33.1'#用于调试的ip地址
    ip1['textvariable']=''
    if PatternMultiple['state']=='normal':
        i = ip1.get()
        global allIp
        allIp=i
        ipping = ("即将连接的ip为%s"%i)
        print(ipping)
        iping['text']=ipping

        tkinter.messagebox.showinfo( "提示", "您需要稍等片刻")
        ping(i)
    elif PatternSingle['state']=='normal':
        if Filepath != '':
            tkinter.messagebox.showinfo( "提示", "为避免堵塞，测试结束时会提醒你")
            win.withdraw()
            getip()
        else:
            tkinter.messagebox.showinfo( "提示", "你需要选择正确的文件")
        print(Filepath)
        
    if PatternSingle['state']=='normal' and Filepath != '':
        #win.update()
        win.deiconify()
    time.sleep(1)
    tkinter.messagebox.showinfo( "提示", "测试完成，请查看")
    start["text"] = "开始"
    start['state']='normal'
    iping['text']=""
    
    global AllErrorIpText,AllErrorIp
    AllErrorIpText=''
    for d in range(0,len(AllErrorIp)):
        print(AllErrorIp)
        #错误的IP
        AllErrorIpText=("%s\n%s"%(AllErrorIpText,AllErrorIp[d]))
    print(AllErrorIpText) 
    errorIp['text']=AllErrorIpText
    AllErrorIp = []
    if PatternMultiple['state']=='normal':
        allIp = []

def getip():
    print("可以启动格式处理")
    with open("%s"%Filepath,"r")as f:
        Iplist = f.readlines()

    global allIp,AllErrorIp
    allIp = []
    if len(Iplist) == 1:
        iplist=Iplist[0].strip('\n')
        Iplist=iplist.split(',')
        for i in Iplist:
            ping(i)
            allIp.append(i)
    elif len(Iplist) > 1:
        iplist=Iplist
        for a in range(0,len(iplist)):
            Iplist[a]=iplist[a].strip('\n')
        for b in range(0,len(iplist)): 
            Ipku=iplist[b].split('-')
            ip_3 = Ipku[0].split('.')
            for c in range((int(ip_3[3])+1),(int(Ipku[1])+2)):
                i = ('%s.%s.%s.%d'%(ip_3[0],ip_3[1],ip_3[2],(c-1)))
                print("使用得:%s"%i)
                ping(i)
                allIp.append(i)
        
    print(Iplist)
    print(len(Iplist))
    print(allIp)
    
        

def pattern():
    if PatternMultiple['state']=='normal':
        pattern = 2
        PatternMultiple['state']='disable'
        PatternSingle['state']='normal'
        ip1 = tkinter.Button(win,image=OpenFileLogo,command=GetFile)
        ip1.place(width = 200,height = 40,x=50,y=70)
        print(pattern)
    elif PatternSingle['state']=='normal':
        pattern = 1
        PatternSingle['state']='disable'
        PatternMultiple['state']='normal'
        ip1 = tkinter.Entry(win,text="这是一个输入框",show=None,highlightthickness=3)
        ip1.place(width = 200,height = 40,x=50,y=70)
        print(pattern)
    
def page():#创建界面
    global win
    win = tkinter.Tk()
    win.title("一个界面")
    winwidth = 600
    winheight  = 400
    screenwidth = int((win.winfo_screenwidth()-winwidth)/2)
    screenheight = int((win.winfo_screenheight()-winheight)/2)
    win.geometry("%dx%d+%d+%d" %(winwidth,winheight,screenwidth,screenheight))
    win.resizable(0,0)
    
    global PatternSingle,PatternMultiple,ip1,start,iping,img,OpenFileLogo,errorIp,stateL1
    PatternSingle = tkinter.Button(win,text="单个测试",command = pattern,state='disable')
    PatternSingle.place(width = 100,height = 20,x=50,y=50)
    PatternMultiple = tkinter.Button(win,text="多个测试",command = pattern,state='normal')
    PatternMultiple.place(width = 100,height = 20,x=150,y=50)
    
    tip1 = tkinter.Label(win,text="网络设备检测",font=('华文行楷', 20))
    tip1.place(x=50,y=10)
    warn = tkinter.StringVar()
    ip1 = tkinter.Entry(win,textvariable=warn,show=None,highlightthickness=3)
    warn.set('请输入正确的网络地址以确保可以测试')
    ip1.place(width = 200,height = 40,x=50,y=70)
    
    img = Image.open("OpenFileLogo.jpg")
    OpenFileLogo = ImageTk.PhotoImage(img)
    #OpenFile = tkinter.Button(win,image=OpenFileLogo)
    #OpenFile.place(width = 200,height = 40,x=50,y=50)

    start = tkinter.Button(win,text = "开始",command=stratcmd,activebackground="#000000")
    start.place(width = 200,height = 40,x=50,y=110)
    
    stateLtip = tkinter.Label(win,text="将会检测的地址：")
    stateLtip.place(x=50,y=180)
    stateL1 = tkinter.Label(win,text="",highlightthickness=3)
    stateL1.place(width = 200,height = 200,x=50,y=200)
    
    pingip1 = tkinter.Label(win,text="正在检测的地址")
    pingip1.place(x=400,y=50)
    
    iping = tkinter.Label(win,text="")
    iping.place(x=400,y=70)
    errorIp = tkinter.Label(win,text="")
    errorIp.place(x=400,y=200)
    
    #win.after(1000,pagemain)
    


#ping('192.168.100.59')
page()
#win.loop()