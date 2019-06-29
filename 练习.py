from tkinter import *
import webbrowser

import re
root = Tk()

text = Text(root,width=30,height=5)
text.pack()

text.insert(INSERT,'Its after 12 noon, do you know where your rooftops are?\n http://tinyurl.com/aaaaaaa, aaaaa\naaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa  http://tinyurl.com/aaaaaaa ')

start_link='1.0'
end_link='end'

str1=text.get(1.0,'end')


pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')    # 匹配模式
string = text.get(1.0,'end')
#print(string)
url = re.findall(pattern,string)

a=''
for temp in url:
    a=a+temp+'\n'
#print(a)
row, col = text.index("end").split('.')#采用自带的划分方法将所有文本分行列
for i in range(0,int(row)):
    i=i*1.0
    string1= text.get(i,'end')
    string2=text.get(i+1,'end')
    print(string1)
    print(string2)




text.tag_add('link',start_link,end_link)
text.tag_config('link',foreground='blue',underline=True)

def show_arrow_cursor(event):
     text.config(cursor='arrow')

def show_xterm_cursor(event):
     text.config(cursor='xterm')
def click(event):
     webbrowser.open('http://baidu.com')

text.tag_bind('link','<Enter>',show_arrow_cursor)
text.tag_bind('link','<Leave>',show_xterm_cursor)
text.tag_bind('link','<Button-1>',click)

mainloop()