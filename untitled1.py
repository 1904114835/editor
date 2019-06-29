from tkinter import *
# 导入ttk
from tkinter import ttk
# 导入messagebox
from tkinter import messagebox as msgbox
class App:
    def __init__(self, master):
        self.master = master
        self.initWidgets()
    def initWidgets(self):
        #-----------创建第1个Labelframe，用于选择图标类型-----------
        topF = Frame(self.master)
        topF.pack(fill=BOTH)
        lf1 = ttk.Labelframe(topF, text='请选择图标类型')
        lf1.pack(side=LEFT, fill=BOTH, expand=YES, padx=10, pady=5)
        i = 0
        self.iconVar = IntVar()
        self.icons = [None, "error", "info", "question", "warning"]
        # 使用循环创建多个Radiobutton，并放入Labelframe中
        for icon in self.icons:
            Radiobutton(lf1, text = icon if icon is not None else '默认',
            value=i,
            variable=self.iconVar).pack(side=TOP, anchor=W)
            i += 1
        self.iconVar.set(0)
        #-----------创建第二个Labelframe，用于选择按钮类型-----------
        lf2 = ttk.Labelframe(topF, text='请选择按钮类型')
        lf2.pack(side=LEFT,fill=BOTH, expand=YES, padx=10, pady=5)
        i = 0
        self.typeVar = IntVar()
        # 定义所有按钮类型
        self.types = [None, "abortretryignore", "ok", "okcancel",
            "retrycancel", "yesno", "yesnocancel"]
        # 使用循环创建多个Radiobutton，并放入Labelframe中
        for tp in self.types:
            Radiobutton(lf2, text= tp if tp is not None else '默认',
            value=i,
            variable=self.typeVar).pack(side=TOP, anchor=W)
            i += 1
        self.typeVar.set(0)
        #-----------创建Frame,用于包含多个按钮来生成不同的消息框-----------
        bottomF = Frame(self.master)
        bottomF.pack(fill=BOTH)
        # 创建8个按钮，并为之绑定事件处理函数
        btn1 = ttk.Button(bottomF, text="showinfo",
            command=self.showinfo_clicked)
        btn1.pack(side=LEFT, fill=X, ipadx=5, ipady=5,
            pady=5, padx=5)
        btn2 = ttk.Button(bottomF, text="showwarning",
            command=self.showwarning_clicked)
        btn2.pack(side=LEFT, fill=X, ipadx=5, ipady=5,
            pady=5, padx=5)
        btn3 = ttk.Button(bottomF, text="showerror",
            command=self.showerror_clicked)
        btn3.pack(side=LEFT, fill=X, ipadx=5, ipady=5,
            pady=5, padx=5)
        btn4 = ttk.Button(bottomF, text="askquestion",
            command=self.askquestion_clicked)
        btn4.pack(side=LEFT, fill=X, ipadx=5, ipady=5,
            pady=5, padx=5)
        btn5 = ttk.Button(bottomF, text="askokcancel",
            command=self.askokcancel_clicked)
        btn5.pack(side=LEFT, fill=X, ipadx=5, ipady=5,
            pady=5, padx=5)
        btn6 = ttk.Button(bottomF, text="askyesno",
            command=self.askyesno_clicked)
        btn6.pack(side=LEFT, fill=X, ipadx=5, ipady=5,
            pady=5, padx=5)
        btn7 = ttk.Button(bottomF, text="askyesnocancel",
            command=self.askyesnocancel_clicked)
        btn7.pack(side=LEFT, fill=X, ipadx=5, ipady=5,
            pady=5, padx=5)
        btn8 = ttk.Button(bottomF, text="askretrycancel",
            command=self.askretrycancel_clicked)
        btn8.pack(side=LEFT, fill=X, ipadx=5, ipady=5,
            pady=5, padx=5)
    def showinfo_clicked(self):
        print(msgbox.showinfo("Info", "showinfo测试.",
            icon=self.icons[self.iconVar.get()],
            type=self.types[self.typeVar.get()]))
    def showwarning_clicked(self):
        print(msgbox.showwarning("Warning", "showwarning测试.",
            icon=self.icons[self.iconVar.get()],
            type=self.types[self.typeVar.get()]))
    def showerror_clicked(self):
        print(msgbox.showerror("Error", "showerror测试.",
            icon=self.icons[self.iconVar.get()],
            type=self.types[self.typeVar.get()]))
    def askquestion_clicked(self):
        print(msgbox.askquestion("Question", "askquestion测试.",
            icon=self.icons[self.iconVar.get()],
            type=self.types[self.typeVar.get()]))
    def askokcancel_clicked(self):
        print(msgbox.askokcancel("OkCancel", "askokcancel测试.",
            icon=self.icons[self.iconVar.get()],
            type=self.types[self.typeVar.get()]))
    def askyesno_clicked(self):
        print(msgbox.askyesno("YesNo", "askyesno测试.",
            icon=self.icons[self.iconVar.get()],
            type=self.types[self.typeVar.get()]))
    def askyesnocancel_clicked(self):
        print(msgbox.askyesnocancel("YesNoCancel", "askyesnocancel测试.",
            icon=self.icons[self.iconVar.get()],
            type=self.types[self.typeVar.get()]))
    def askretrycancel_clicked(self):
        print(msgbox.askretrycancel("RetryCancel", "askretrycancel测试.",
            icon=self.icons[self.iconVar.get()],
            type=self.types[self.typeVar.get()]))
root = Tk()
root.title("消息框测试")
App(root)
root.mainloop()