#全部优化
import tkinter
import os
import time
import re
import tkinter.messagebox
import tkinter.filedialog
from tkinter import filedialog,scrolledtext,END
import sys


AllIp = []
AllErrorIp = []
AllTestIpText = ''
Filepath = ''
ErrorIpText = ''
TipEntryText = ''
AllErrorIpText = ''
allresult = '本次检测结果：'
tip = ''


def Initialization():
    global AllIp,AllErrorIp,AllTestIpText,Filepath,ErrorIpText,TipEntryText,Start
    AllIp = []
    AllErrorIp = []
    AllTestIpText = ''
    ErrorIpText = ''
    TipEntryText = ''
    Update()

def StartSelfTest():
    global OpenFileLogo
    try:
        OpenFileLogo = tkinter.PhotoImage(file = 'OpenFileLogo.gif')
    except:
        tkinter.messagebox.showerror("常见错误","软件文件缺失")
        sys.exit(0)
        

def CmdPing():
    global cmdread,AllTestIpText,AllErrorIpText,AllErrorIp
    for i in AllIp:
        AllTestIpText=("%s\n%s"%(AllTestIpText,i))
    for _i in AllIp:
        ip=_i.strip('-t')
        ip=_i.strip('/t')
        ip=_i.replace(' ','')
        cmd = os.popen('ping %s'%ip)
        cmdread = cmd.read()
        Judge(cmdread,ip)

def Judge(cmdread,ip):
    global AllErrorIp,AllErrorIpText,allresult,tip
    state = re.findall(r'回复:(.*)。', cmdread)
    tip = ''
    if state == []:
        speed = re.findall(r'平均 = (.*)ms', cmdread)
        if speed == []:
            tip = ("检测的地址：%s,存在异常"%(ip))
            AllErrorIp.append(ip)
            AllErrorIpText=("%s\n%s"%(AllErrorIpText,ip))
        else:
            speed = int(speed[0])
            if speed < 100:
                tip = ("检测的地址：%s,连接耗时：%d毫秒,速度较快"%(ip,speed))
            if speed > 100:
                tip = ("检测的地址：%s,连接耗时：%d毫秒,速度较慢"%(ip,speed))
    else:
        AllErrorIp.append(ip)
        print("检测的地址：%s,无法连接"%(ip))
        AllErrorIpText=("%s\n%s"%(AllErrorIpText,ip))
    print(tip)
    allresult = ('%s\n%s'%(allresult,tip))
    Update()

def GetFile():
    global Filepath
    Filepath = filedialog.askopenfilename(title=u'多个地址',filetype=[("TXT",".txt")])
    if Filepath == '':
        tkinter.messagebox.showinfo( "提示", "你需要选择正确的文件")
    else:
        with open("%s"%Filepath,"r")as f:
            IpListText = f.readlines()
        while len(IpListText) == 0:
            tkinter.messagebox.showinfo( "提示", "你需要选择正确的文件")
            GetFile()

def StratCmd():
    global Start,Filepath,AllTestIpText,TipEntryText,win,AllIp,AllIpText,AllErrorIpText,IPPing
    Initialization()
    AllTestIpText=("计划中：")
    AllErrorIpText=("错误的：")
    IPPing.delete(1.0, END)
    if PatternMultiple['state']=='normal':
        i = str(IpEntry.get())
        I=i.split(',')
        if len(I) < 3:
            for _i in I:
                i=_i.strip('-t')
                i=_i.strip('/t')
                i=_i.replace(' ','')
                AllIp.append(i)
            AllIpText=("%s\n%s"%(AllTestIpText,i))
            Start['text'] = "稍等"
            Start['state']='disable'
            Update()
            tkinter.messagebox.showinfo( "提示", "好了，您需要稍等片刻")
            time.sleep(1)
            CmdPing()
            time.sleep(2)
            tkinter.messagebox.showinfo( "提示", "测试完成，请查看")
            Start["text"] = "开始"
            Start['state']='normal'
        else:
            tkinter.messagebox.showwarning('提示','检测多个地址时建议使用“多个测试”模式')
    
        
    elif PatternSingle['state']=='normal':
        if Filepath != '':
            Start['text'] = "稍等"
            Start['state']='disable'
            tkinter.messagebox.showinfo( "提示", "为避免堵塞，将关闭窗口\n测试结束时会提醒你")
            win.withdraw()
            MakeList()
        else:
            tkinter.messagebox.showinfo( "提示", "你需要选择正确的文件")
            GetFile()
    if PatternSingle['state']=='normal' and Filepath != '':
        win.deiconify()
        time.sleep(2)
        tkinter.messagebox.showinfo( "提示", "测试完成，请查看")
        Start["text"] = "开始"
        Start['state']='normal'

def Update():
    global IPWillBeTested,AllIpText,IPPing,AllIp,AllErrorIpText,AllTestIpText,tip
    IPWillBeTested.delete(1.0, END)
    IPWillBeTested.insert('end',AllTestIpText)
    IPPingText = ("%s\n"%tip)
    IPPing.insert('end',IPPingText)
    ErrorIpLable.delete(1.0, END)
    ErrorIpLable.insert('end',AllErrorIpText)  

def MakeList():
    global AllIp,AllIpText,Iplist
    with open("%s"%Filepath,"r")as f:
        IpListText = f.readlines()
    AllIp = []
    if len(IpListText) == 0:
        tkinter.messagebox.showinfo( "提示", "你需要选择正确的文件")
        GetFile()
    Iplist=IpListText
    if len(Iplist) == 1:
        iplist=Iplist[0].strip('\n')
        Iplist=iplist.split(',')
        for i in Iplist:
            AllIp.append(i)
    elif len(Iplist) > 1:
        iplist=Iplist
        if (Iplist[0]) == 'pass\n' or (Iplist[0]) == '\n':
            Iplist1=iplist[0].split(',')
            del(iplist[0])
        for a in range(0,len(iplist)):
            iplist[a]=iplist[a].strip('\n')
        for b in range(0,len(iplist)): 
            Ipku=iplist[b].split('-')
            ip_3 = Ipku[0].split('.')
            for c in range((int(ip_3[3])+1),(int(Ipku[1])+2)):
                i = ('%s.%s.%s.%d'%(ip_3[0],ip_3[1],ip_3[2],(c-1)))
                AllIp.append(i)
    _allip = AllIp
    AllIp = sorted(set(_allip),key=_allip.index)
    print(AllIp)
    for e in range(0,len(AllIp)):
        AllIpText=("%s\n%s"%(AllTestIpText,AllIp[e]))
    CmdPing()
    
def SaveResults():
    global AllErrorIpText,AllTestIpText,allresult
    file_save = filedialog.asksaveasfilename(title=u'保存文件',filetype=[("TXT",".txt")],initialfile="错误的地址.txt")
    localtime = time.asctime( time.localtime(time.time()) )
    if file_save != '':
        text_results = ("\n%s\n%s\n%s"%(localtime,AllTestIpText,AllErrorIpText))
        with open(file=file_save, mode='a+', encoding='utf-8') as file:
            file.write(text_results)
    with open(file='结果.txt', mode='w', encoding='utf-8') as file:
            file.write(allresult)
    os.system("结果.txt")
  
def Pattern():
    global PatternMultiple,PatternSingle,IpEntry,OpenFileLogo
    if PatternMultiple['state']=='normal':
        PatternMultiple['state']='disable'
        PatternSingle['state']='normal'
        IpEntry = tkinter.Button(win,image=OpenFileLogo,command=GetFile)
        IpEntry.place(width = 200,height = 40,x=50,y=70)
    elif PatternSingle['state']=='normal':
        PatternSingle['state']='disable'
        PatternMultiple['state']='normal'
        IpEntry = tkinter.Entry(win,show=None,highlightthickness=3)
        IpEntry.place(width = 200,height = 40,x=50,y=70)
    
win = tkinter.Tk()
win.title("地址检测工具")
winwidth = 600
winheight  = 400
screenwidth = int((win.winfo_screenwidth()-winwidth)/2)
screenheight = int((win.winfo_screenheight()-winheight)/2)
win.geometry("%dx%d+%d+%d" %(winwidth,winheight,screenwidth,screenheight))
win.resizable(0,0)

def page():
    global PatternSingle,PatternMultiple,IpEntry,TipEntryText,Start,IPWillBeTested,IPPing,ErrorIpLable
    PatternSingle = tkinter.Button(win,text="单个测试",command = Pattern,state='disable')
    PatternSingle.place(width = 100,height = 20,x=50,y=50)
    PatternMultiple = tkinter.Button(win,text="多个测试",command = Pattern,state='normal')
    PatternMultiple.place(width = 100,height = 20,x=150,y=50)
    
    SoftwareName = tkinter.Label(win,text="地址检测工具",font=('华文行楷', 18))
    SoftwareName.place(x=50,y=10)
    TipEntryText = tkinter.StringVar()
    IpEntry = tkinter.Entry(win,textvariable=TipEntryText,show=None,highlightthickness=3)
    TipEntryText.set('请输入正确的网络地址以确保可以测试')
    IpEntry.place(width = 200,height = 40,x=50,y=70)
    #TipEntryText=''
    IpEntry['textvariable']=''
    Start = tkinter.Button(win,text = "开始",command=StratCmd,activebackground="#000000")
    Start.place(width = 200,height = 40,x=50,y=110)
    WillBeTested = tkinter.Label(win,text="检测结果：")
    WillBeTested.place(x=50,y=180)
    IPWillBeTested = scrolledtext.ScrolledText(win)
    IPWillBeTested.place(width = 200,height = 150,x=50,y=200)
    IPWillBeTested.insert('end','这里会显示被计划检测的地址')
    IPPing = scrolledtext.ScrolledText(win)
    IPPing.place(width = 200,height = 100,x=350,y=50)
    IPPing.insert('end','正在检测的地址')
    ErrorIpLableTip = tkinter.Label(win,text="错误的地址：")
    ErrorIpLableTip.place(x=350,y=180)
    ErrorIpLable = scrolledtext.ScrolledText(win)
    ErrorIpLable.place(width = 200,height = 150,x=350,y=200)
    ErrorIpLable.insert('insert','这里会显示错误的地址')

    Save = tkinter.Button(win,text = "保存",command = SaveResults,state='normal')
    Save.place(width = 80,height = 20,x=400,y=350)
    
    Maker = tkinter.Label(win,text="制作：林楷")
    Maker.place(x=300,y=20)

StartSelfTest()
page()
Initialization()
win.mainloop()


#下一步支持中文地址：用encode等转化为网址
#将会被测得地址列表可以删除一些元素，已经知道不能用或不用测的地址