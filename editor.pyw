# -*- coding: utf-8 -*-
"""
Created on Thu Jun 24 20:01:33 2019

@author: 19041
"""
from editor_style import theme_color, ICONS
try :
    from tkinter import *#引用tkinter下的所有方法
except:
    from Tkinter import *
try:
    from tkinter import filedialog, messagebox
except:
    from Tkinter import filedialog, messagebox
try:
    from tkinter.ttk import Scrollbar, Checkbutton, Label, Button
except:
    from Tkinter.ttk import Scrollbar, Checkbutton, Label, Button
import os
import string

class easyEditor(Tk):#继承Tk类
    icon_res = []#icon的集合
    file_name = None#文件名，暂命名为none，若此时保存文件，则无反应

    def __init__(self):#初始化
        super().__init__()
        self._set_window_()#底框
        self._create_menu_bar_()#上方菜单栏
        self._create_shortcut_bar_()#小工具栏
        self._create_body_()#文本输入框主体
        self._create_right_popup_menu()#右键菜单

    # 设置初始窗口的属性
    def _set_window_(self):
        self.title("easyEditor")#头名称
        scn_width, scn_height = self.maxsize()
        wm_val = '750x450+%d+%d' % ((scn_width - 750) / 2, (scn_height - 450) / 2)
        #高减450除以2，宽减750除以2
        self.resizable(width=True, height=True)
        self.geometry(wm_val)#设置窗口大小
        self.iconbitmap("img/editor.ico")
        self.protocol('WM_DELETE_WINDOW', self.exit_editor)#用于关闭的协议

    # 创建整个菜单栏
    def _create_menu_bar_(self):
        menu_bar = Menu(self)
        # 创建文件的联级菜单
        file_menu = Menu(menu_bar, tearoff=0)#文件栏
        file_menu.add_command(label='新建', accelerator='Ctrl+N', command=self.new_file)#accelerator只是显示字符，不用做键盘监听
        file_menu.add_command(label='打开', accelerator='Ctrl+O', command=self.open_file)
        file_menu.add_command(label='保存', accelerator='Ctrl+S', command=self.save)
        file_menu.add_command(label='另存为', accelerator='Shift+Ctrl+S', command=self.save_as)
        file_menu.add_separator()#添加分割线
        file_menu.add_command(label='退出', accelerator='Alt+F4', command=self.exit_editor)

        # 在菜单栏上添加菜单标签，并将该标签与相应的联级菜单关联起来
        menu_bar.add_cascade(label='文件', menu=file_menu)

        # 创建编辑的联级菜单
        edit_menu = Menu(menu_bar, tearoff=0)#编辑栏
        edit_menu.add_command(label='撤销', accelerator='Ctrl+Z', command=lambda: self.handle_menu_action('撤销'))
        edit_menu.add_command(label='恢复', accelerator='Ctrl+Y', command=lambda: self.handle_menu_action('恢复'))
        edit_menu.add_separator()
        edit_menu.add_command(label='剪切', accelerator='Ctrl+X', command=lambda: self.handle_menu_action('剪切'))
        edit_menu.add_command(label='复制', accelerator='Ctrl+C', command=lambda: self.handle_menu_action('复制'))
        edit_menu.add_command(label='粘贴', accelerator='Ctrl+V', command=lambda: self.handle_menu_action('粘贴'))
        edit_menu.add_separator()
        edit_menu.add_command(label='查找', accelerator='Ctrl+F', command=self.find_text)
        edit_menu.add_separator()
        edit_menu.add_command(label='全选', accelerator='Ctrl+A', command=self.select_all)
        menu_bar.add_cascade(label='编辑', menu=edit_menu)

        # 视图菜单
        view_menu = Menu(menu_bar, tearoff=0)
        self.is_show_line_num = IntVar()
        self.is_show_line_num.set(1)
        view_menu.add_checkbutton(label='显示行号', variable=self.is_show_line_num,
                                  command=self._update_line_num)

        self.is_highlight_line = IntVar()
        view_menu.add_checkbutton(label='高亮当前行', onvalue=1, offvalue=0,
                                  variable=self.is_highlight_line, command=self._toggle_highlight)
        
        # 在主题菜单中再添加一个子菜单列表
        themes_menu = Menu(menu_bar, tearoff=0)
        view_menu.add_cascade(label='主题', menu=themes_menu)

        self.theme_choice = StringVar()
        self.theme_choice.set('Default')#标准主题
        for k in sorted(theme_color):
            themes_menu.add_radiobutton(label=k, variable=self.theme_choice,
                                        command=self.change_theme)
        menu_bar.add_cascade(label='视图', menu=view_menu)


        #关于栏
        about_menu = Menu(menu_bar, tearoff=0)
        about_menu.add_command(label='关于', command=lambda: self.show_messagebox('关于'))
        about_menu.add_command(label='帮助', command=lambda: self.show_messagebox('帮助'))
        menu_bar.add_cascade(label='关于', menu=about_menu)
        
        #工具菜单
        tools = Menu(menu_bar, tearoff=0)
        tools.add_command(label='字数统计',command=lambda:self.world_num())
        tools.add_command(label='HTML标签匹配',command=lambda: self.show_messagebox('HTML标签匹配'))
        tools.add_command(label='查找', command=lambda: self.find_text() )
        menu_bar.add_cascade(label='工具', menu=tools)
        
        self["menu"] = menu_bar

    # 创建快捷菜单栏,横向的body上方那个
    def _create_shortcut_bar_(self):
        self.shortcut_bar = Frame(self, height=25, background='#20b2aa')
        self.shortcut_bar.pack(fill='x')

        for i, icon in enumerate(ICONS):
            tool_icon = PhotoImage(file='img/%s.gif' % (icon,))
            tool_btn = Button(self.shortcut_bar, image=tool_icon,
                              command=self._shortcut_action(icon))

            tool_btn.pack(side='left')
            self.icon_res.append(tool_icon)

    # 创建程序主体
    def _create_body_(self):
        # 创建行号栏 （takefocus=0 屏蔽焦点）
        self.line_number_bar = Text(self, width=4, padx=3, takefocus=0, border=0,
                                    background='#F0E68C', state='disabled')
        self.line_number_bar.pack(side='left', fill='y')
        # 创建文本输入框(undo是否启用撤销机制)
        self.content_text = Text(self, wrap='word', undo=True)
        self.content_text.pack(expand='yes', fill='both')
        self.content_text.bind('<Control-N>', self.new_file)
        self.content_text.bind('<Control-n>', self.new_file)
        self.content_text.bind('<Control-O>', self.open_file)
        self.content_text.bind('<Control-o>', self.open_file)
        self.content_text.bind('<Control-S>', self.save)
        self.content_text.bind('<Control-s>', self.save)
        self.content_text.bind('<Control-A>', self.select_all)
        self.content_text.bind('<Control-a>', self.select_all)
        self.content_text.bind('<Control-f>', self.find_text)
        self.content_text.bind('<Control-F>', self.find_text)
        self.content_text.bind('<Any-KeyPress>', lambda e: self._update_line_num())
        self.bind_all('<KeyPress-F1>', lambda e: self.show_messagebox("帮助"))
        self.content_text.tag_configure('active_line', background='#EEEEE0')

        # 创建滚动条
        scroll_bar = Scrollbar(self.content_text)
        scroll_bar["command"] = self.content_text.yview
        self.content_text["yscrollcommand"] = scroll_bar.set
        scroll_bar.pack(side='right', fill='y')

    # 鼠标右键弹出菜单
    def _create_right_popup_menu(self):
        popup_menu = Menu(self.content_text, tearoff=0)
        for it1, it2 in zip(['剪切', '复制', '粘贴', '撤销', '恢复'],
                            ['cut', 'copy', 'paste', 'undo', 'redo']):
            popup_menu.add_command(label=it1, compound='left',
                                   command=self._shortcut_action(it2))
        popup_menu.add_separator()
        popup_menu.add_command(label='全选', command=self.select_all)
        self.content_text.bind('<Button-3>',
                               lambda event: popup_menu.tk_popup(event.x_root, event.y_root))

    def _update_line_num(self):#用于显示行号
        if self.is_show_line_num.get() == 1:
            row, col = self.content_text.index("end").split('.')#采用自带的划分方法将所有文本分行列
            line_num_content = "\n".join([str(i) for i in range(1, int(row))])
            #print(line_num_content)
            self.line_number_bar.config(state='normal')
            self.line_number_bar.delete('1.0', 'end')
            self.line_number_bar.insert('1.0', line_num_content)
            self.line_number_bar.config(state='disabled')
        else:
            self.line_number_bar.config(state='normal')
            self.line_number_bar.delete('1.0', 'end')
            self.line_number_bar.config(state='disabled')

    def _toggle_highlight(self):#用于高亮一行
        if self.is_highlight_line.get():
            self.content_text.tag_remove("active_line", 1.0, "end")
            self.content_text.tag_add("active_line", "insert linestart", "insert lineend+1c")
            self.content_text.after(200, self._toggle_highlight)
        else:
            self.content_text.tag_remove("active_line", 1.0, "end")

    def change_theme(self):#背景主题
        selected_theme = self.theme_choice.get()
        fg_bg = theme_color.get(selected_theme)
        fg_color, bg_color, col_color, row_color = fg_bg.split('.')
        self.content_text.config(bg=bg_color)
        self.content_text.config(fg=fg_color)
        self.line_number_bar.config(background=col_color)
        self.shortcut_bar.config( background = row_color )
        
    # 处理菜单响应，返回break，使事件不在传递
    def handle_menu_action(self, action_type):
        if action_type == "撤销":
            self.content_text.event_generate("<<Undo>>")
        elif action_type == "恢复":
            self.content_text.event_generate("<<Redo>>")
        elif action_type == "剪切":
            self.content_text.event_generate("<<Cut>>")
        elif action_type == "复制":
            self.content_text.event_generate("<<Copy>>")
        elif action_type == "粘贴":
            self.content_text.event_generate("<<Paste>>")

        if action_type != "复制":
            self._update_line_num()

        return "break"

    #信息显示栏
    def show_messagebox(self, type):
        if type == "帮助":
            student_message="电计1701吴瑞林201785072\n"
            github_message="具体信息请访问我的github：\n"
            github_message_1="https://github.com/1904114835\n"
            all_message=student_message+github_message+ github_message_1
            messagebox.showinfo("帮助",all_message , icon='question')
        elif type == "关于":
            messagebox.showinfo("关于", "程序设计训练大作业")
        elif type == "HTML标签匹配":
            messagebox.showinfo("HTML标签匹配", "功能开发中",detail="")
#        elif type == "字数统计":
#            messagebox.showinfo("字数统计", "开发中")
        else:
            pass

    # 快捷菜单的响应程序
    def _shortcut_action(self, type):
        def handle():
            if type == "new_file":
                self.new_file()
            elif type == "open_file":
                self.open_file()
            elif type == "save":
                self.save()
            elif type == "cut":
                self.handle_menu_action("剪切")
            elif type == "copy":
                self.handle_menu_action("复制")
            elif type == "paste":
                self.handle_menu_action("粘贴")
            elif type == "undo":
                self.handle_menu_action("撤销")
            elif type == "redo":
                self.handle_menu_action("恢复")
            elif type == "find_text":
                self.find_text()

            if type != "copy" and type != "save":
                self._update_line_num()

        return handle
    
    #全选功能
    def select_all(self, event=None):
        self.content_text.tag_add('sel', '1.0', 'end')
        return "break"
    
    #新文件
    def new_file(self, event=None):
        self.title("New - easyEditor")#设置题头
        self.content_text.delete(1.0, END)#删除所有文本
        self.file_name = None

    #打开文件
    def open_file(self, event=None):
        input_file = filedialog.askopenfilename(
            filetypes=[("所有文件", "*.*"), ("文本文档", "*.txt")])#询问打开文件的名字
        if input_file:#若存在该名字
            name=os.path.basename(input_file)+"easyEditor"
            self.title(name)#设置
            self.file_name = input_file
            self.content_text.delete(1.0, END)
            with open(input_file, 'r') as _file:
                self.content_text.insert(1.0, _file.read())

    def save(self, event=None):
        if not self.file_name:
            self.save_as()
        else:
            self._write_to_file(self.file_name)

    def save_as(self, event=None):
        input_file = filedialog.asksaveasfilename(filetypes=[("All Files", "*.*"), ("文本文档", "*.txt")])
        if input_file == "All Files":
            self.file_name = input_file
            self.file_name = self.file_name
            self._write_to_file(self.file_name)
        else :
            self.file_name = input_file
            self.file_name = self.file_name+".txt"
            self._write_to_file(self.file_name)

    def _write_to_file(self, file_name):
        try:
            content = self.content_text.get(1.0, 'end')
            with open(file_name, 'w') as the_file:
                the_file.write(content)
            self.title("%s - easyEditor" % os.path.basename(file_name))
        except IOError:
            messagebox.showwarning("保存", "保存失败！")

    # 查找对话框
    def find_text(self, event=None):
        search_toplevel = Toplevel(self)
        search_toplevel.title('查找文本')
        search_toplevel.transient(self)  # 总是让搜索框显示在其父窗体之上
        search_toplevel.resizable(False, False)
        Label(search_toplevel, text="查找全部:").grid(row=0, column=0, sticky='e')
        search_entry_widget = Entry(search_toplevel, width=25)
        search_entry_widget.grid(row=0, column=1, padx=2, pady=2, sticky='we')
        search_entry_widget.focus_set()
        ignore_case_value = IntVar()
        Checkbutton(search_toplevel, text='忽略大小写', variable=ignore_case_value).grid(
            row=1, column=1, sticky='e', padx=2, pady=2)

        Button(search_toplevel, text="查找", command=lambda: self.search_result(
            search_entry_widget.get(), ignore_case_value.get(), search_toplevel, search_entry_widget)
               ).grid(row=0, column=2, sticky='e' + 'w', padx=2, pady=2)

        def close_search_window():
            self.content_text.tag_remove('match', '1.0', "end")
            search_toplevel.destroy()

        search_toplevel.protocol('WM_DELETE_WINDOW', close_search_window)
        return "break"

    def search_result(self, key, ignore_case, search_toplevel, search_box):
        self.content_text.tag_remove('match', '1.0', "end")
        matches_found = 0
        if key:
            start_pos = '1.0'
            while True:
                # search返回第一个匹配上的结果的开始索引，返回空则没有匹配的（nocase：忽略大小写）
                start_pos = self.content_text.search(key, start_pos, nocase=ignore_case, stopindex="end")
                if not start_pos:
                    break
                end_pos = start_pos+"+"+str(len(key))+"c"
                self.content_text.tag_add('match', start_pos, end_pos)
                matches_found += 1
                start_pos = end_pos
                #print(start_pos)
                #printf(end_pos)
            self.content_text.tag_config('match', foreground='red', background='yellow')
        search_box.focus_set()
        matches_found_str=str(matches_found)
        matches_found_temp='发现'+matches_found_str+'个匹配的'
        search_toplevel.title(matches_found_temp)
            
    def world_num(self,event=None):#字数统计，计算部分
        str_0=self.content_text.get(1.0,'end')
        '''找出字符串中的中英文、空格、数字、标点符号个数'''
        count_en = count_dg = count_sp = count_zh = count_pu = 0
        temp=[]
        for s in str_0:
            # 英文
            if s in string.ascii_letters:
                count_en += 1
                temp.append(s)
            # 数字
            elif s.isdigit():
                count_dg += 1
            # 空格
            elif s.isspace():
                count_sp += 1
                temp.append(" ")
            # 中文
            elif s.isalpha():
                count_zh += 1
                temp.append(" ")
            # 特殊字符
            else:
                count_pu += 1
        count_ew=self.english_world_num(temp)
        #print('英文字符：', count_en)
        #print("英文单词数量：",count_ew)
        #print('数字：', count_dg)
        #print('空格：', count_sp)
        #print('中文：', count_zh)
        #print('特殊字符：', count_pu)
        #print('temp:',temp)
        str_count_en=str(count_en)
        str_count_ew=str(count_ew)
        str_count_dg=str(count_dg)
        str_count_sp=str(count_sp)
        str_count_zh=str(count_zh)
        str_count_pu=str(count_pu)
        
        str_count_en='英文字符：'+str_count_en
        str_count_ew='英文单词：'+str_count_ew
        str_count_dg='数字：    '+str_count_dg
        str_count_sp='空格：    '+str_count_sp
        str_count_zh='中文：    '+str_count_zh
        str_count_pu='特殊字符：'+str_count_pu
        
        all_message='\n\n'+str_count_en+'\n'+str_count_ew+'\n'+str_count_dg+'\n'+str_count_sp+'\n'+str_count_zh+'\n'+str_count_pu
        
        messagebox.showinfo("字数统计",all_message)

    def show_num(self, count_en,count_ew,count_dg,count_sp,count_zh,count_pu):
        pass
        
    def english_world_num(self,temp):
        k=0
        for i in range(len(temp)):
            if temp[i] != " ":
                if temp[i+1]==" ":
                    k+=1
        return k




    def exit_editor(self):
        if messagebox.askokcancel("退出?", "确定退出吗?"):
            self.destroy()

if "__main__" == __name__:
    app = easyEditor()
    app.mainloop()

    
