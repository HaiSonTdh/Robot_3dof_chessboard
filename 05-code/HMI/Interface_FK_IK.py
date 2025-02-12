from ctypes import sizeof #gọi các hàm từ các thư viện khác không thuộc về python
from tkinter import * # thư viện GUI tiêu chuẩn cho Python
import tkinter
from tkinter import font
from tkinter import *
from tkinter import filedialog
from typing import Mapping, Sized #thư viện mảng kich thuoc
import numpy as np #thư viện toán học
from PIL import Image, ImageTk

from serial.serialutil import Timeout #thu vien serial, timeout: limit the max time for calling a function
import serial # cong serial
import KinematicRobot #thu vien dong hoc
import time # thoi gian

import threading #luồng thực thi riêng biệt

def switching_interface():
    global switch_state
    if switch_state == 0:
        top.withdraw()
        GiaoDien.deiconify()
        switch_state = 1
    else:
        top.deiconify()
        GiaoDien.withdraw()
        switch_state = 0

GiaoDien = Tk() #tao man hinh giao dien
top=Toplevel()  # màn hình hiện thị đầu tiên
top.title("GIAO DIỆN ROBOT 3 DOF") #tên
top.geometry('797x521') #kích  thước 

image_path = r"E:\HaiSon\Nam_IV_HK1\ProjectROBOT\gioithieu_tmson.png"
img = Image.open(image_path)
MC = ImageTk.PhotoImage(img)

Label(top,image=MC).place(x=0,y=0)  # vi tri
#MC=PhotoImage(file="VSP.png") # hình
# Label(top,image=MC).grid() # vị trí
Button(top,text="CONTROL INTERFACE",font='Times 15 bold', bg='#6666ff',fg='white',command=lambda:switching_interface()).place(x=400,y=450) # nút nhấn fg mau vien bg mau nen

GiaoDien.withdraw() # de chi hien thi 1 giao dien TOP ban dau
ser = serial.Serial(port='COM3',baudrate=9600,timeout=1)
time.sleep(2)

x_axis = 15
y_axis = 30
y_lable_IK = 250
value1 = 0
value2 = 0
value3 = 0
x=0

# L1 = 156.67
# L2 = 120
# L3 = 140
L1 = 156.67
L2 = 120
L3 = 145

switch_state = 0

background_color = '#FFFAF0' # mã TLP RGB xem ở https://htlit.maytinhhtl.com/lam-web/bang-ma-mau-css-html-code-thet-ke-design.html

GiaoDien.geometry('1300x600')
GiaoDien.title("CONTROL INTERFACE")
GiaoDien.configure(bg=background_color)

#------------------------------- VIẾT HÀM CON ------------------------------------
def slider_theta1_value(x):
    value1 = slider_theta1.get()
    txb_slider_theta1.delete(0,END) # Xóa dữ liệu trước đó
    txb_slider_theta1.insert(0,value1) # hiển thị dữ liệu mới
    return value1

def slider_theta2_value(x):
    txb_slider_theta2.delete(0,END)
    value2 = slider_theta2.get()
    txb_slider_theta2.insert(0,value2)
    return value2

def slider_theta3_value(x):
    txb_slider_theta3.delete(0,END)
    value3 = slider_theta3.get()
    txb_slider_theta3.insert(0,value3)  
    return value3

def FK(x):
    txb_Px_FK.delete(0,END) # Xóa dữ liệu trước đó
    txb_Py_FK.delete(0,END) # Xóa dữ liệu trước đó
    txb_Pz_FK.delete(0,END) # Xóa dữ liệu trước đó
    value1 = slider_theta1_value(x)
    value2 = slider_theta2_value(x)
    value3 = slider_theta3_value(x)
    Px = KinematicRobot.Forward_Kinematic(value1,value2,value3,L1,L2,L3)[0]
    Py = KinematicRobot.Forward_Kinematic(value1,value2,value3,L1,L2,L3)[1]
    Pz = KinematicRobot.Forward_Kinematic(value1,value2,value3,L1,L2,L3)[2]
    txb_Px_FK.insert(0,Px) # hiển thị dữ liệu mới vao PX PY PZ
    txb_Py_FK.insert(0,Py) # hiển thị dữ liệu mới
    txb_Pz_FK.insert(0,Pz) # hiển thị dữ liệu mới
    mang = str(value1)+'A'+str(value2)+'B'+str(value3)+'C'
    ser.write(mang.encode()) 
    time.sleep(0.01)

def IK():
    txb_theta1_IK.delete(0,END)
    txb_theta2_IK.delete(0,END)
    txb_theta3_IK.delete(0,END)
    Px = float(txb_Px_IK.get())
    Py = float(txb_Py_IK.get())
    Pz = float(txb_Pz_IK.get())
    theta1 = KinematicRobot.Inverse_Kinematic(Px,Py,Pz,L1,L2,L3)[0]
    theta2 = KinematicRobot.Inverse_Kinematic(Px,Py,Pz,L1,L2,L3)[1]
    theta3 = KinematicRobot.Inverse_Kinematic(Px,Py,Pz,L1,L2,L3)[2]
    txb_theta1_IK.insert(0,theta1)
    txb_theta2_IK.insert(0,theta2)
    txb_theta3_IK.insert(0,theta3)
    mang = f'F{theta1}A{theta2}B{theta3}C'
    print(mang)
    ser.write(mang.encode()) 
    time.sleep(0.01)  #để thêm độ trễ trong quá trình thực thi chương trình. 
    #txb_Px_IK.delete(0,END)
    #txb_Py_IK.delete(0,END)
    #txb_Pz_IK.delete(0,END)
    #txb_Theta.delete(0,END)

def Reset_Slider():
    txb_slider_theta1.delete(0,END)
    txb_slider_theta2.delete(0,END)
    txb_slider_theta3.delete(0,END) 
    txb_slider_theta1.insert(0,value1)
    txb_slider_theta2.insert(0,value2)
    txb_slider_theta3.insert(0,value3)    
    slider_theta1.set('0') #đặt lại vị trí thanh slider tương ứng với giá trị lấy từ textbox
    slider_theta2.set('0')
    slider_theta3.set('0')

def Reset_lable_Slider():
    Reset_Slider()
    Px = KinematicRobot.Forward_Kinematic(0,0,0,L1,L2,L3)[0]
    Py = KinematicRobot.Forward_Kinematic(0,0,0,L1,L2,L3)[1]
    Pz = KinematicRobot.Forward_Kinematic(0,0,0,L1,L2,L3)[2] 

    txb_Px_FK.delete(0,END) # hiển thị dữ liệu mới
    txb_Py_FK.delete(0,END) # hiển thị dữ liệu mới
    txb_Pz_FK.delete(0,END) # hiển thị dữ liệu mới 
    txb_Px_FK.insert(0,Px) # hiển thị dữ liệu mới
    txb_Py_FK.insert(0,Py) # hiển thị dữ liệu mới
    txb_Pz_FK.insert(0,Pz) # hiển thị dữ liệu mới    

def ReSet_btn():
    new_thread = threading.Thread(target=Reset_lable_Slider) # Thread là các hàm hay thủ tục chạy độc lập đối với chương trình chính
    new_thread.start()
    mang = f'F0A0B0C'
    print(mang,type(mang))
    ser.write(mang.encode())
    time.sleep(0.01)

def theta1_set_btn():
    slider_theta1.set(txb_slider_theta1.get())
    value1 = slider_theta1_value(x) # lấy giá trị hiện tại của thanh slider 
    value2 = slider_theta2_value(x)
    value3 = slider_theta3_value(x)
    txb_Px_FK.delete(0,END) # Xóa dữ liệu trước đó
    txb_Py_FK.delete(0,END) # Xóa dữ liệu trước đó
    txb_Pz_FK.delete(0,END) # Xóa dữ liệu trước đó
    Px = KinematicRobot.Forward_Kinematic(value1,value2,value3,L1,L2,L3)[0]
    Py = KinematicRobot.Forward_Kinematic(value1,value2,value3,L1,L2,L3)[1]
    Pz = KinematicRobot.Forward_Kinematic(value1,value2,value3,L1,L2,L3)[2]
    txb_Px_FK.insert(0,Px) # hiển thị dữ liệu mới
    txb_Py_FK.insert(0,Py) # hiển thị dữ liệu mới
    txb_Pz_FK.insert(0,Pz) # hiển thị dữ liệu mới
    mang = f'F{value1}A{value2}B{value3}C'
    print(mang,type(mang))
    ser.write(mang.encode())
    time.sleep(0.1)


def theta2_set_btn():
    slider_theta2.set(txb_slider_theta2.get())
    value1 = slider_theta1_value(x) # lấy giá trị hiện tại của thanh slider 
    value2 = slider_theta2_value(x)
    value3 = slider_theta3_value(x)
    txb_Px_FK.delete(0,END) # Xóa dữ liệu trước đó
    txb_Py_FK.delete(0,END) # Xóa dữ liệu trước đó
    txb_Pz_FK.delete(0,END) # Xóa dữ liệu trước đó
    Px = KinematicRobot.Forward_Kinematic(value1,value2,value3,L1,L2,L3)[0]
    Py = KinematicRobot.Forward_Kinematic(value1,value2,value3,L1,L2,L3)[1]
    Pz = KinematicRobot.Forward_Kinematic(value1,value2,value3,L1,L2,L3)[2]
    txb_Px_FK.insert(0,Px) # hiển thị dữ liệu mới
    txb_Py_FK.insert(0,Py) # hiển thị dữ liệu mới
    txb_Pz_FK.insert(0,Pz) # hiển thị dữ liệu mới
    mang = f'F{value1}A{value2}B{value3}C'
    print(mang,type(mang))
    ser.write(mang.encode())
    time.sleep(0.01)

def theta3_set_btn():
    slider_theta3.set(txb_slider_theta3.get())
    value1 = slider_theta1_value(x) # lấy giá trị hiện tại của thanh slider 
    value2 = slider_theta2_value(x)
    value3 = slider_theta3_value(x)
    txb_Px_FK.delete(0,END) # Xóa dữ liệu trước đó
    txb_Py_FK.delete(0,END) # Xóa dữ liệu trước đó
    txb_Pz_FK.delete(0,END) # Xóa dữ liệu trước đó
    Px = KinematicRobot.Forward_Kinematic(value1,value2,value3,L1,L2,L3)[0]
    Py = KinematicRobot.Forward_Kinematic(value1,value2,value3,L1,L2,L3)[1]
    Pz = KinematicRobot.Forward_Kinematic(value1,value2,value3,L1,L2,L3)[2]
    txb_Px_FK.insert(0,Px) # hiển thị dữ liệu mới
    txb_Py_FK.insert(0,Py) # hiển thị dữ liệu mới
    txb_Pz_FK.insert(0,Pz) # hiển thị dữ liệu mới
    mang = f'F{value1}A{value2}B{value3}C'
    print(mang,type(mang))
    ser.write(mang.encode())
    time.sleep(0.01)

def Start_btn():
    mang = 'S'
    print(mang,type(mang))
    ser.write(mang.encode())
    time.sleep(0.1)

def Stop_btn():
    mang = 'T'
    ser.write(mang.encode())
    time.sleep(0.01)

def hut_btn():
    mang = 'H'
    ser.write(mang.encode())
    time.sleep(0.01)
def tha_btn():
    mang = "N"
    print(mang,type(mang))
    ser.write(mang.encode())
    time.sleep(0.01)

def A2_btn():
    value1 = -28
    value2 = 11
    value3 = 64
    mang = f'F{value1}A{value3}C{value2}BHON'
    print(mang, type(mang))
    ser.write(mang.encode())
    time.sleep(0.01)
def A3_btn():
    value1 = -17
    value2 = 9
    value3 = 73
    mang = f'F{value1}A{value3}C{value2}BHON'
    print(mang, type(mang))
    ser.write(mang.encode())
    time.sleep(0.01)
def A4_btn():
    value1 = -5
    value2 = 8
    value3 = 75
    mang = f'F{value1}A{value3}C{value2}BHON'
    print(mang, type(mang))
    ser.write(mang.encode())
    time.sleep(0.01)
def A5_btn():
    value1 = 8
    value2 = 7
    value3 = 78
    mang = f'F{value1}A{value3}C{value2}BHON'
    print(mang, type(mang))
    ser.write(mang.encode())
    time.sleep(0.01)
def A6_btn():
    value1 = 19
    value2 = 11
    value3 = 72
    mang = f'F{value1}A{value3}C{value2}BHON'
    print(mang, type(mang))
    ser.write(mang.encode())
    time.sleep(0.01)
def A7_btn():
    value1 = 30
    value2 = 11
    value3 = 67
    mang = f'F{value1}A{value3}C{value2}BHON'
    print(mang, type(mang))
    ser.write(mang.encode())
    time.sleep(0.01)

def B2_btn():
    value1 = -33
    value2 = 8
    value3 = 77
    mang = f'F{value1}A{value3}C{value2}BHON'
    print(mang, type(mang))
    ser.write(mang.encode())
    time.sleep(0.01)
def B3_btn():
    value1 = -22
    value2 = 6
    value3 = 86
    mang = f'F{value1}A{value3}C{value2}BHON'
    print(mang, type(mang))
    ser.write(mang.encode())
    time.sleep(0.01)
def B4_btn():
    value1 = -7
    value2 = 4
    value3 = 90
    mang = f'F{value1}A{value3}C{value2}BHON'
    print(mang, type(mang))
    ser.write(mang.encode())
    time.sleep(0.01)
def B5_btn():
    value1 = 8
    value2 = 4
    value3 = 90
    mang = f'F{value1}A{value3}C{value2}BHON'
    print(mang, type(mang))
    ser.write(mang.encode())
    time.sleep(0.01)
def B6_btn():
    value1 = 21
    value2 = 5
    value3 = 87
    mang = f'F{value1}A{value3}C{value2}BHON'
    print(mang, type(mang))
    ser.write(mang.encode())
    time.sleep(0.01)
def B7_btn():
    value1 = 34
    value2 = 8
    value3 = 77
    mang = f'F{value1}A{value3}C{value2}BHON'
    print(mang, type(mang))
    ser.write(mang.encode())
    time.sleep(0.01)

def C1_btn():
    value1 = -47
    value2 = 9
    value3 = 74
    mang = f'F{value1}A{value3}C{value2}BHON'
    print(mang, type(mang))
    ser.write(mang.encode())
    time.sleep(0.01)
def C2_btn():
    value1 = -37
    value2 = 5
    value3 = 87
    mang = f'F{value1}A{value3}C{value2}BHON'
    print(mang, type(mang))
    ser.write(mang.encode())
    time.sleep(0.01)
def C3_btn():
    value1 = -22
    value2 = 4
    value3 = 96
    mang = f'F{value1}A{value3}C{value2}BHON'
    print(mang, type(mang))
    ser.write(mang.encode())
    time.sleep(0.01)
def C4_btn():
    value1 = -8
    value2 = 5
    value3 = 101.5
    mang = f'F{value1}A{value3}C{value2}BHON'
    print(mang, type(mang))
    ser.write(mang.encode())
    time.sleep(0.01)
def C5_btn():
    value1 = 10
    value2 = 5
    value3 = 100
    mang = f'F{value1}A{value3}C{value2}BHON'
    print(mang, type(mang))
    ser.write(mang.encode())
    time.sleep(0.01)
def C6_btn():
    value1 = 28
    value2 = 5
    value3 = 97
    mang = f'F{value1}A{value3}C{value2}BHON'
    print(mang, type(mang))
    ser.write(mang.encode())
    time.sleep(0.01)
def C7_btn():
    value1 = 40
    value2 = 5
    value3 = 89
    mang = f'F{value1}A{value3}C{value2}BHON'
    print(mang, type(mang))
    ser.write(mang.encode())
    time.sleep(0.01)
def C8_btn():
    value1 = 47
    value2 = 6
    value3 = 78
    mang = f'F{value1}A{value3}C{value2}BHON'
    print(mang, type(mang))
    ser.write(mang.encode())
    time.sleep(0.01)    
    
def D1_btn():
    value1 = -54
    value2 = 7
    value3 = 83
    mang = f'F{value1}A{value3}C{value2}BHON'
    print(mang, type(mang))
    ser.write(mang.encode())
    time.sleep(0.01)
def D2_btn():
    value1 = -44
    value2 = 4.5
    value3 = 95
    mang = f'F{value1}A{value3}C{value2}BHON'
    print(mang, type(mang))
    ser.write(mang.encode())
    time.sleep(0.01)
def D3_btn():
    value1 = -30
    value2 = 5
    value3 = 104
    mang = f'F{value1}A{value3}C{value2}BHON'
    print(mang, type(mang))
    ser.write(mang.encode())
    time.sleep(0.01)
def D4_btn():
    value1 = -8
    value2 = 6.5
    value3 = 110
    mang = f'F{value1}A{value3}C{value2}BHON'
    print(mang, type(mang))
    ser.write(mang.encode())
    time.sleep(0.01)
def D5_btn():
    value1 = 12
    value2 = 6
    value3 = 109
    mang = f'F{value1}A{value3}C{value2}BHON'
    print(mang, type(mang))
    ser.write(mang.encode())
    time.sleep(0.01)
def D6_btn():
    value1 = 30
    value2 = 5
    value3 = 107
    mang = f'F{value1}A{value3}C{value2}BHON'
    print(mang, type(mang))
    ser.write(mang.encode())
    time.sleep(0.01)
def D7_btn():
    value1 = 47
    value2 = 6
    value3 = 95
    mang = f'F{value1}A{value3}C{value2}BHON'
    print(mang, type(mang))
    ser.write(mang.encode())
    time.sleep(0.01)
def D8_btn():
    value1 = 55
    value2 = 5
    value3 = 85
    mang = f'F{value1}A{value3}C{value2}BHON'
    print(mang, type(mang))
    ser.write(mang.encode())
    time.sleep(0.01)    

def Box_btn():
    value1 = -87
    value2 = -30
    value3 = 115
    mang = f'F{value2}B{value1}A{value3}C'
    print(mang, type(mang))
    ser.write(mang.encode())
    time.sleep(0.01)

#--------------------------------------------------------------------------

lbl_tieude = Label(GiaoDien,text="                                                                    CONTROL INTERFACE",font=("Arial",17,font.BOLD),bg=background_color)
lbl_FK = Label(GiaoDien,text="FORWARD KINEMATIC",fg="blue",font=("Arial",14,font.BOLD),bg=background_color)
lbl_IK = Label(GiaoDien,text="INVERSE KINEMATIC",fg="blue",font=("Arial",14,font.BOLD),bg=background_color)
lbl_theta1_FK = Label(GiaoDien,text="Theta1",fg="black",font=("Arial",12,font.BOLD),bg=background_color)
lbl_theta2_FK = Label(GiaoDien,text="Theta2",fg="black",font=("Arial",12,font.BOLD),bg=background_color)
lbl_theta3_FK = Label(GiaoDien,text="Theta3",fg="black",font=("Arial",12,font.BOLD),bg=background_color)
lbl_theta1_IK = Label(GiaoDien,text="Theta1",fg="black",font=("Arial",12,font.BOLD),bg=background_color)
lbl_theta2_IK = Label(GiaoDien,text="Theta2",fg="black",font=("Arial",12,font.BOLD),bg=background_color)
lbl_theta3_IK = Label(GiaoDien,text="Theta3",fg="black",font=("Arial",12,font.BOLD),bg=background_color)
lbl_Px_IK = Label(GiaoDien,text="Px",fg="black",font=("Arial",12,font.BOLD),bg=background_color)
lbl_Py_IK = Label(GiaoDien,text="Py",fg="black",font=("Arial",12,font.BOLD),bg=background_color)
lbl_Pz_IK = Label(GiaoDien,text="Pz",fg="black",font=("Arial",12,font.BOLD),bg=background_color)
lbl_Px_FK = Label(GiaoDien,text="Px",fg="black",font=("Arial",12,font.BOLD),bg=background_color)
lbl_Py_FK = Label(GiaoDien,text="Py",fg="black",font=("Arial",12,font.BOLD),bg=background_color)
lbl_Pz_FK = Label(GiaoDien,text="Pz",fg="black",font=("Arial",12,font.BOLD),bg=background_color)
# lbl_Theta = Label(GiaoDien,text="Theta",fg="black",font=("Arial",12,font.BOLD),bg=background_color)


txb_slider_theta1 = Entry(GiaoDien,width=6,font=("Arial",12,font.BOLD)) #tao o hien thi goc ben canh slider
txb_slider_theta1.insert(0,value1)

txb_slider_theta2 = Entry(GiaoDien,width=6,font=("Arial",12,font.BOLD))
txb_slider_theta2.insert(0,value2)

txb_slider_theta3 = Entry(GiaoDien,width=6,font=("Arial",12,font.BOLD))
txb_slider_theta3.insert(0,value3)

txb_Px_IK = Entry(GiaoDien,width=10,font=("Arial",12,font.BOLD)) # tao o hien thi Px Invert
txb_Py_IK = Entry(GiaoDien,width=10,font=("Arial",12,font.BOLD))
txb_Pz_IK = Entry(GiaoDien,width=10,font=("Arial",12,font.BOLD))
txb_Px_FK = Entry(GiaoDien,width=7,font=("Arial",12,font.BOLD))
txb_Py_FK = Entry(GiaoDien,width=7,font=("Arial",12,font.BOLD))
txb_Pz_FK = Entry(GiaoDien,width=7,font=("Arial",12,font.BOLD))
# txb_Theta = Entry(GiaoDien,width=9,font=("Arial",12,font.BOLD))
txb_theta1_IK = Entry(GiaoDien,width=9,font=("Arial",12,font.BOLD)) #tao o hien thi goc invert
txb_theta2_IK = Entry(GiaoDien,width=9,font=("Arial",12,font.BOLD))
txb_theta3_IK = Entry(GiaoDien,width=9,font=("Arial",12,font.BOLD))

slider_theta1 = Scale(GiaoDien,from_=-90, to_= 90,orient=HORIZONTAL,width=15,resolution=0.5,length=350,command=FK) # gioi han thanh slider
slider_theta1.set(value1)
slider_theta2 = Scale(GiaoDien,from_=-90, to_= 20,orient=HORIZONTAL,width=15,resolution=0.5,length=350,command=FK)
slider_theta2.set(value2)
slider_theta3 = Scale(GiaoDien,from_=-150, to_= 110,orient=HORIZONTAL,width=15,resolution=0.5,length=350,command=FK)
slider_theta3.set(value3)

btn_Start = Button(GiaoDien,text="Set Home",font=("Arial",12,font.BOLD),width=10,height=2,bg='#ECAB53',command=Start_btn)
btn_Stop = Button(GiaoDien,text="Stop",font=("Arial",12,font.BOLD),width=10,height=2,bg='#FF0000',command=Stop_btn)
btn_Solve = Button(GiaoDien,text="Solve",font=("Arial",12,font.BOLD),width=10,height=2,bg='#98FB98',command=IK)
btn_ReSet = Button(GiaoDien,text="Reset",font=("Arial",12,font.BOLD),width=10,height=2,bg='#98FB98',command=ReSet_btn)
btn_Set_Theta1 = Button(GiaoDien,text="Set Theta1",font=("Arial",10,font.BOLD),width=8,height=2,bg='#98FB98',command=theta1_set_btn)
btn_Set_Theta2 = Button(GiaoDien,text="Set Theta2",font=("Arial",10,font.BOLD),width=8,height=2,bg='#98FB98',command=theta2_set_btn)
btn_Set_Theta3 = Button(GiaoDien,text="Set Theta3",font=("Arial",10,font.BOLD),width=8,height=2,bg='#98FB98',command=theta3_set_btn)

btn_hut = Button(GiaoDien,text="Hut",font=("Arial",10,font.BOLD),width=8,height=2,bg='#98FB98',command=hut_btn)
btn_tha = Button(GiaoDien,text="Tha",font=("Arial",10,font.BOLD),width=8,height=2,bg='#98FB98',command=tha_btn)

btn_A2 = Button(GiaoDien, text="A2", font=("Arial", 10, font.BOLD), width=8, height=2, bg='gray', fg='white',
                  command=A2_btn)
btn_A3 = Button(GiaoDien, text="A3", font=("Arial", 10, font.BOLD), width=8, height=2, bg='gray', fg='white',
                  command=A3_btn)
btn_A4 = Button(GiaoDien, text="A4", font=("Arial", 10, font.BOLD), width=8, height=2, bg='gray', fg='white',
                  command=A4_btn)
btn_A5 = Button(GiaoDien, text="A5", font=("Arial", 10, font.BOLD), width=8, height=2, bg='gray', fg='white',
                  command=A5_btn)
btn_A6 = Button(GiaoDien, text="A6", font=("Arial", 10, font.BOLD), width=8, height=2, bg='gray', fg='white',
                  command=A6_btn)
btn_A7 = Button(GiaoDien, text="A7", font=("Arial", 10, font.BOLD), width=8, height=2, bg='gray', fg='white',
                  command=A7_btn)
btn_B2 = Button(GiaoDien, text="B2", font=("Arial", 10, font.BOLD), width=8, height=2, bg='gray', fg='white',
                  command=B2_btn)
btn_B3 = Button(GiaoDien, text="B3", font=("Arial", 10, font.BOLD), width=8, height=2, bg='gray', fg='white',
                  command=B3_btn)
btn_B4 = Button(GiaoDien, text="B4", font=("Arial", 10, font.BOLD), width=8, height=2, bg='gray', fg='white',
                  command=B4_btn)
btn_B5 = Button(GiaoDien, text="B5", font=("Arial", 10, font.BOLD), width=8, height=2, bg='gray', fg='white',
                  command=B5_btn)
btn_B6 = Button(GiaoDien, text="B6", font=("Arial", 10, font.BOLD), width=8, height=2, bg='gray', fg='white',
                  command=B6_btn)
btn_B7 = Button(GiaoDien, text="B7", font=("Arial", 10, font.BOLD), width=8, height=2, bg='gray', fg='white',
                  command=B7_btn)

btn_C1 = Button(GiaoDien, text="C1", font=("Arial", 10, font.BOLD), width=8, height=2, bg='gray', fg='white',
                  command=C1_btn)
btn_C2 = Button(GiaoDien, text="C2", font=("Arial", 10, font.BOLD), width=8, height=2, bg='gray', fg='white',
                  command=C2_btn)
btn_C3 = Button(GiaoDien, text="C3", font=("Arial", 10, font.BOLD), width=8, height=2, bg='gray', fg='white',
                  command=C3_btn)
btn_C4 = Button(GiaoDien, text="C4", font=("Arial", 10, font.BOLD), width=8, height=2, bg='gray', fg='white',
                  command=C4_btn)
btn_C5 = Button(GiaoDien, text="C5", font=("Arial", 10, font.BOLD), width=8, height=2, bg='gray', fg='white',
                  command=C5_btn)
btn_C6 = Button(GiaoDien, text="C6", font=("Arial", 10, font.BOLD), width=8, height=2, bg='gray', fg='white',
                  command=C6_btn)
btn_C7 = Button(GiaoDien, text="C7", font=("Arial", 10, font.BOLD), width=8, height=2, bg='gray', fg='white',
                  command=C7_btn)
btn_C8 = Button(GiaoDien, text="C8", font=("Arial", 10, font.BOLD), width=8, height=2, bg='gray', fg='white',
                  command=C8_btn)
btn_D1 = Button(GiaoDien, text="D1", font=("Arial", 10, font.BOLD), width=8, height=2, bg='gray', fg='white',
                  command=D1_btn)
btn_D2 = Button(GiaoDien, text="D2", font=("Arial", 10, font.BOLD), width=8, height=2, bg='gray', fg='white',
                  command=D2_btn)
btn_D3 = Button(GiaoDien, text="D3", font=("Arial", 10, font.BOLD), width=8, height=2, bg='gray', fg='white',
                  command=D3_btn)
btn_D4 = Button(GiaoDien, text="D4", font=("Arial", 10, font.BOLD), width=8, height=2, bg='gray', fg='white',
                  command=D4_btn)
btn_D5 = Button(GiaoDien, text="D5", font=("Arial", 10, font.BOLD), width=8, height=2, bg='gray', fg='white',
                  command=D5_btn)
btn_D6 = Button(GiaoDien, text="D6", font=("Arial", 10, font.BOLD), width=8, height=2, bg='gray', fg='white',
                  command=D6_btn)
btn_D7 = Button(GiaoDien, text="D7", font=("Arial", 10, font.BOLD), width=8, height=2, bg='gray', fg='white',
                  command=D7_btn)
btn_D8 = Button(GiaoDien, text="D8", font=("Arial", 10, font.BOLD), width=8, height=2, bg='gray', fg='white',
                  command=D8_btn)
btn_Box = Button(GiaoDien, text="BOX", font=("Arial", 10, font.BOLD), width=8, height=2, bg='gray', fg='white',
                  command=Box_btn)


lbl_tieude.place(x=150,y=0)
lbl_FK.place(x=x_axis,y=y_axis)
lbl_IK.place(x=x_axis,y=y_axis+y_lable_IK)
lbl_theta1_FK.place(x=x_axis,y=y_axis+40)
lbl_theta2_FK.place(x=15,y=y_axis+85)
lbl_theta3_FK.place(x=15,y=y_axis+130)
lbl_theta1_IK.place(x=200,y=y_axis+y_lable_IK+53)
lbl_theta2_IK.place(x=200,y=y_axis+y_lable_IK+103)
lbl_theta3_IK.place(x=200,y=y_axis+y_lable_IK+153)
lbl_Px_FK.place(x=x_axis+40,y=y_axis+170)
lbl_Py_FK.place(x=x_axis+140,y=y_axis+170)
lbl_Pz_FK.place(x=x_axis+240,y=y_axis+170)
lbl_Px_IK.place(x=x_axis+20,y=y_axis+y_lable_IK+50)
lbl_Py_IK.place(x=x_axis+20,y=y_axis+y_lable_IK+100)
lbl_Pz_IK.place(x=x_axis+20,y=y_axis+y_lable_IK+150)
# lbl_Theta.place(x=x_axis,y=y_axis+y_lable_IK+200)
        
slider_theta1.place(x=x_axis+60,y=y_axis+30)
slider_theta2.place(x=x_axis+60,y=y_axis+75)
slider_theta3.place(x=x_axis+60,y=y_axis+120)

txb_slider_theta1.place(x=x_axis+420,y=y_axis+40)
txb_slider_theta2.place(x=x_axis+420,y=y_axis+80)
txb_slider_theta3.place(x=x_axis+420,y=y_axis+130)
txb_Px_FK.place(x=x_axis+20,y=y_axis+203)
txb_Py_FK.place(x=x_axis+120,y=y_axis+203)
txb_Pz_FK.place(x=x_axis+220,y=y_axis+203)
txb_Px_IK.place(x=x_axis+50,y=y_axis+y_lable_IK+53)
txb_Py_IK.place(x=x_axis+50,y=y_axis+y_lable_IK+103)
txb_Pz_IK.place(x=x_axis+50,y=y_axis+y_lable_IK+153)
# txb_Theta.place(x=x_axis+58,y=y_axis+y_lable_IK+203)
txb_theta1_IK.place(x=270,y=y_axis+y_lable_IK+53)
txb_theta2_IK.place(x=270,y=y_axis+y_lable_IK+103)
txb_theta3_IK.place(x=270,y=y_axis+y_lable_IK+153)

btn_Start.place(x=x_axis+60,y=y_axis+y_lable_IK+200)
btn_Stop.place(x=x_axis+370,y=y_axis+y_lable_IK+200)
btn_Solve.place(x=x_axis+370,y=y_axis+y_lable_IK+85)
btn_ReSet.place(x=x_axis+370,y=y_axis+190)
btn_Set_Theta1.place(x=x_axis+480,y=y_axis+26)
btn_Set_Theta2.place(x=x_axis+480,y=y_axis+74)
btn_Set_Theta3.place(x=x_axis+480,y=y_axis+120)

btn_hut.place(x=650,y=y_axis+y_lable_IK+203)
btn_tha.place(x=x_axis+730,y=y_axis+y_lable_IK+203)

btn_D1.place(x=650,y=190)
btn_D2.place(x=730,y=190)
btn_D3.place(x=810,y=190)
btn_D4.place(x=890,y=190)
btn_D5.place(x=970,y=190)
btn_D6.place(x=1050,y=190)
btn_D7.place(x=1130,y=190)
btn_D8.place(x=1210,y=190)

btn_C1.place(x=650,y=240)
btn_C2.place(x=730,y=240)
btn_C3.place(x=810,y=240)
btn_C4.place(x=890,y=240)
btn_C5.place(x=970,y=240)
btn_C6.place(x=1050,y=240)
btn_C7.place(x=1130,y=240)
btn_C8.place(x=1210,y=240)

btn_B2.place(x=730,y=290)
btn_B3.place(x=810,y=290)
btn_B4.place(x=890,y=290)
btn_B5.place(x=970,y=290)
btn_B6.place(x=1050,y=290)
btn_B7.place(x=1130,y=290)

btn_A2.place(x=730,y=340)
btn_A3.place(x=810,y=340)
btn_A4.place(x=890,y=340)
btn_A5.place(x=970,y=340)
btn_A6.place(x=1050,y=340)
btn_A7.place(x=1130,y=340)
btn_Box.place(x=650,y=420)


#------------------------------------ TRẠNG THÁI BAN ĐẦU --------------------------------------
Px = KinematicRobot.Forward_Kinematic(0,0,0,L1,L2,L3)[0]
Py = KinematicRobot.Forward_Kinematic(0,0,0,L1,L2,L3)[1]
Pz = KinematicRobot.Forward_Kinematic(0,0,0,L1,L2,L3)[2]
txb_Px_FK.insert(0,Px) # hiển thị dữ liệu mới
txb_Py_FK.insert(0,Py) # hiển thị dữ liệu mới
txb_Pz_FK.insert(0,Pz) # hiển thị dữ liệu mới


GiaoDien.mainloop() # vong lap