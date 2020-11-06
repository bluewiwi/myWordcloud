import tkinter as tk
from tkinter import filedialog
import tkinter.messagebox

from wordcloud import WordCloud,ImageColorGenerator
import jieba
import jieba.analyse

import numpy as np
from PIL import Image,ImageTk
import matplotlib.pyplot as plt
import string


#主窗口
window = tk.Tk()
window.title('my wordcloud')
window.geometry('800x600')
window.resizable(width=False, height=False)

tk.Label(window, text='欢迎使用词云系统').pack()


#导入文本文件弹窗
def open_txt():
    txt_path = ''
    root = tk.Tk()
    root.withdraw()
    txt_path = filedialog.askopenfilename()  # 获得选择好的文件
    if txt_path == '':
        tk.messagebox.showinfo(title='温馨提示',message='选取失败！')
    else :
        with open(txt_path,"r",encoding='UTF-8') as file:
            data = file.read()
            text_.insert('insert',data)
            file.close()

#导入背景图片弹窗
mask_counter = 0              #判断是否自定义词云形状
image_path = ''
def open_image():
    global mask_counter
    tk.messagebox.showinfo(title='温馨提示', message='为达到最好的展示效果，推荐选择白色背景图片')
    root = tk.Tk()
    root.withdraw()
    global image_path
    image_path = filedialog.askopenfilename()  # 获得选择好的文件
    if image_path == '':
        tk.messagebox.showinfo(title='温馨提示',message='选取失败！')
    else :
        selfdisplay()
        mask_counter = 1

###菜单
menubar = tk.Menu(window)
filemenu = tk.Menu(menubar,tearoff=0)
menubar.add_cascade(label='项目',menu = filemenu)
filemenu.add_command(label='导入文本文件',comman=open_txt)
filemenu.add_command(label='导入背景图片',comman=open_image)

'''def open_font():
    root = tk.Tk()
    root.withdraw()
    font_path = filedialog.askopenfilename()  # 获得选择好的文件
    print(font_path)

###设置
settingmenu = tk.Menu(menubar,tearoff=0)
menubar.add_cascade(label='设置',menu = settingmenu)

fontmenu = tk.Menu(settingmenu,tearoff=0)
settingmenu.add_command(label='字体',comman=open_font)

colormenu = tk.Menu(settingmenu,tearoff=0)
settingmenu.add_cascade(label='颜色',menu=colormenu)
'''
window.config(menu=menubar)

#面板
frame = tk.Frame(window)
frame.pack()
frame_left = tk.Frame(frame)
frame_right = tk.Frame(frame)
frame_left.pack(side='left')
frame_right.pack(side='right')

tk.Label(frame_left,text='请输入内容：').pack()
tk.Label(frame_left,text='只支持英文和中文输入，不支持数字').pack()
show = tk.Label(frame_right,text='图片展示')
label_img = tk.Label(frame_right,bg='lightblue',width=450,height=350)

text_=tk.Text(frame_left,height=30,width=45)
text_.pack()

#信息保存提示
def save_message():
    tk.messagebox.showinfo(title='温馨提示',message='图片wordcloud'+str(counter)+'.png已保存在当前目录下')

counter = 0
#图片预览功能实现
def display():
    global counter
    global image_file
    image_open = Image.open('wordcloud'+str(counter)+'.png')
    image_resize = image_open.resize((450, 350))
    image_file = ImageTk.PhotoImage(image_resize)
    label_img.config(image=image_file)
    if counter == 1 :
        show.pack()
        label_img.pack()
    elif counter == 0:
        show.pack()
        label_img.pack()

    save_message()
    counter=counter+1

#重置面板
def nodisplay():
    global image_file
    image_open = Image.open('wordcloud.png')
    image_resize = image_open.resize((450,350))
    image_file = ImageTk.PhotoImage(image_resize)
    label_img.config(image=image_file)

#自定义形状
def selfdisplay():
    global counter
    global image_file
    image_open = Image.open(image_path)
    image_resize = image_open.resize((450, 350))
    image_file = ImageTk.PhotoImage(image_resize)
    label_img.config(image=image_file)
    if (counter== 0):
        show.pack()
        label_img.pack()
        counter = counter+1


#词云生成实现
def commit():
    global counter
    global image_path
    global mask_counter
    var = text_.get(0.0,tk.END)
    #输入判断
    if var.strip() !='' :

        if mask_counter == 0 :         #默认图形
            wc = WordCloud(
                background_color='white',
                font_path="C:\windows\Fonts\simsun.ttc",
                width=450,
                height=350,
            )
        else:  #自定义图形
            mask_ = np.array(Image.open(image_path))
            wc = WordCloud(
                background_color='white',
                font_path="C:\windows\Fonts\simsun.ttc",
                width=450,
                height=350,
                mask=mask_,
                max_font_size=40,
                random_state=42
            )
            mask_counter = 0

        if choose_.get() == 'B':  # 中文分词
            var = ' '.join(jieba.cut(var))
        wc.generate(var)
        wc.to_file('wordcloud' + str(counter) + '.png')
        display()
    else:
        tk.messagebox.showinfo(title='温馨提示', message='输入不能为空！')

def reset():
    text_.delete(0.0,tk.END)
    nodisplay()



#单选按钮
choose_ = tk.StringVar()
r1 = tk.Radiobutton(window, text='英文',
            variable=choose_, value='A')
r1.pack()

r2 = tk.Radiobutton(window, text='中文',
            variable=choose_, value='B')
r2.pack()

#功能按钮
button_yes = tk.Button(window,text='确认',width=15,height=0,command=commit).pack()
button_no = tk.Button(window,text='重置',width=15,height=0,command=reset).pack()

window.mainloop()
