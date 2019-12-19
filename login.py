import threading
import tkinter as tk
import tkinter.messagebox
from tkinter.filedialog import *
import pygame
import mainWin
import mysql
from PIL import Image, ImageTk

def get_image(filename, width, height):
    im = Image.open(filename).resize((width,height))
    return ImageTk.PhotoImage(im)

top = Tk()
top.title("监控视频的前景目标提取")
top.geometry('300x200')
top.resizable(False, False)

canvas_root = tk.Canvas(top)
im_root = get_image('img/img.jpg', 300, 200)
canvas_root.create_image(150,100,image=im_root)
canvas_root.pack()

label_title = tk.Label(top,text ='请登录系统')
label_title.place(x=120,y=5,anchor=NW)
entry_name = tk.Entry(top,show=None)
entry_pwd = tk.Entry(top,show='*')
label_name = tk.Label(top,text='用户名')
label_pwd = tk.Label(top,text='密码')
label_name.place(x=30,y=55,anchor=NW)
entry_name.place(x=120,y=55,anchor=NW)
label_pwd.place(x=30,y=85,anchor=NW)
entry_pwd.place(x=120,y=85,anchor=NW)

pygame.mixer.init()
track = pygame.mixer.music.load('music/music.mp3')
is_play = 0



def play_music():
    global is_play
    if is_play == 0:
        pygame.mixer.music.play()
        is_play  = 1
    else :
        is_play = 0
        pygame.mixer.music.stop()


def login():
    usr_name = entry_name.get()
    usr_pwd = entry_pwd.get()

    if bool(1-mysql.loginByUserName(usr_name)):
        tk.messagebox.showerror(title='wrong pwd', message='用户名不存在')
        return
    if mysql.loginByUserAndPW(usr_name,usr_pwd):
        tk.messagebox.showinfo(title  ='welcome',message='欢迎,'+str(usr_name))
        top.destroy()
        t = threading.Thread(target=mainWin.run())
        t.start()
        t.join()
    else:
        tk.messagebox.showerror(title='wrong pwd',message='密码或用户名错误')
        play_music()


def register():
    usr_name = entry_name.get()
    usr_pwd = entry_pwd.get()
    if mysql.loginByUserName(usr_name):
        tk.messagebox._show(title='register wrong', message='账户已存在 请更换用户名')
        return
    mysql.addUser(usr_name,usr_pwd)
    tk.messagebox.showinfo(title='register success', message='账号注册成功')

im_button = get_image('img/login.jpg',30,30)
btn_login = tk.Button(top,text = '登录',image=im_button,command = login)
btn_login.place(x=200,y=125,anchor=N,width=30,height=30)

im_button1 = get_image('img/register.jpg',30,30)
btn_register = tk.Button(top,text = '注册',image=im_button1,command = register)
btn_register.place(x=100,y=125,anchor=N,width=30,height=30)
top.mainloop()
