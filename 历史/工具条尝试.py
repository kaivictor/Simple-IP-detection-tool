import tkinter as tk

window = tk.Tk()
# 设置窗口大小
winWidth = 600
winHeight = 400
# 获取屏幕分辨率
screenWidth = window.winfo_screenwidth()
screenHeight = window.winfo_screenheight()

x = int((screenWidth - winWidth) / 2)
y = int((screenHeight - winHeight) / 2)

# 设置主窗口标题
window.title("ScrollBar参数说明")
# 设置窗口初始位置在屏幕居中
window.geometry("%sx%s+%s+%s" % (winWidth, winHeight, x, y))
# 设置窗口图标
#window.iconbitmap("./image/icon.ico")
# 设置窗口宽高固定
window.resizable(0, 0)

"""scrollbar 参数.

        Valid resource names: activebackground, activerelief,
        background, bd, bg, borderwidth, command, cursor,
        elementborderwidth, highlightbackground,
        highlightcolor, highlightthickness, jump, orient,
        relief, repeatdelay, repeatinterval, takefocus,
        troughcolor, width."""
scroll_bar = tk.Scrollbar(window)
scroll_bar.pack()

list_box = tk.Listbox(window)

for i in range(1000):
    list_box.insert(tk.END, i)
list_box.config(yscrollcommand = scroll_bar.set)
list_box.pack()

scroll_bar.config(command = list_box.yview, width = 16)

window.mainloop()