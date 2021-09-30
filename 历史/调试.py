import tkinter.filedialog
from tkinter import filedialog
Filepath = filedialog.askopenfilename(title=u'多个地址',filetype=[("TXT",".txt")])#创建新窗口用于获取文件
if Filepath == '':
    break
else:
    print(File)
    
print("runed")