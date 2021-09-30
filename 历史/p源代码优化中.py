import tkinter
import os
import time
#import subprocess
import re
import tkinter.messagebox
import tkinter.filedialog
#from PIL import Image, ImageTk
from tkinter import filedialog

global Pattern
global AllErrorIp
AllErrorIp = ['']
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
    IPWillBeTested['text']=AllIpText
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
    Start['text'] = "稍等"
    Start['state']='disable'
    #i = '192.168.33.1'#用于调试的ip地址
    IpEntry['textvariable']=''
    if PatternMultiple['state']=='normal':
        i = IpEntry.get()
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
    time.sleep(2)
    tkinter.messagebox.showinfo( "提示", "测试完成，请查看")
    Start["text"] = "开始"
    Start['state']='normal'
    iping['text']=""
    
    global AllErrorIpText,AllErrorIp
    AllErrorIpText='错误的IP'
    for d in range(0,len(AllErrorIp)):
        print(AllErrorIp)
        #错误的IP
        AllErrorIpText=("%s\n%s"%(AllErrorIpText,AllErrorIp[d]))
    #AllErrorIpText=("错误的地址%s"%(AllErrorIpText))
    print(AllErrorIpText) 
    ErrorIpLable['text']=AllErrorIpText
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
        IpEntry = tkinter.Button(win,image=OpenFileLogo,command=GetFile)
        IpEntry.place(width = 200,height = 40,x=50,y=70)
        print(pattern)
    elif PatternSingle['state']=='normal':
        pattern = 1
        PatternSingle['state']='disable'
        PatternMultiple['state']='normal'
        IpEntry = tkinter.Entry(win,show=None,highlightthickness=3)
        IpEntry.place(width = 200,height = 40,x=50,y=70)
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
    
    global PatternSingle,PatternMultiple,IpEntry,Start,iping,img,OpenFileLogo,ErrorIpLable,IPWillBeTested
    PatternSingle = tkinter.Button(win,text="单个测试",command = pattern,state='disable')
    PatternSingle.place(width = 100,height = 20,x=50,y=50)
    PatternMultiple = tkinter.Button(win,text="多个测试",command = pattern,state='normal')
    PatternMultiple.place(width = 100,height = 20,x=150,y=50)
    
    SoftwareName = tkinter.Label(win,text="网络设备检测",font=('华文行楷', 20))
    SoftwareName.place(x=50,y=10)
    warn = tkinter.StringVar()
    IpEntry = tkinter.Entry(win,textvariable=warn,show=None,highlightthickness=3)
    warn.set('请输入正确的网络地址以确保可以测试')
    IpEntry.place(width = 200,height = 40,x=50,y=70)
    
    #img = Image.open("OpenFileLogo.jpg")
    #OpenFileLogo = ImageTk.PhotoImage(img)
    OpenFileLogo = tkinter.PhotoImage(file = 'OpenFileLogo.gif')
    #OpenFile = tkinter.Button(win,image=OpenFileLogo)
    #OpenFile.place(width = 200,height = 40,x=50,y=50)

    Start = tkinter.Button(win,text = "开始",command=stratcmd,activebackground="#000000")
    Start.place(width = 200,height = 40,x=50,y=110)
    
    WillBeTested = tkinter.Label(win,text="将会检测的地址：")
    WillBeTested.place(x=50,y=180)
    IPWillBeTested = tkinter.Label(win,text="这里会显示被计划检测的地址",highlightthickness=3,anchor='n')
    IPWillBeTested.place(width = 200,height = 200,x=50,y=200)
    IPPing = tkinter.Label(win,text="正在检测的地址")
    IPPing.place(x=400,y=50)
    ErrorIpLable = tkinter.Label(win,text="这里会显示错误的地址")
    ErrorIpLable.place(x=400,y=200)
    
    win.mainloop()
    #win.after(1000,pagemain)
    


#ping('192.168.100.59')
page()
#win.loop()
