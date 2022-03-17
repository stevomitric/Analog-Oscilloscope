from tkinter import *
from tkinter.ttk import *
from PIL import ImageTk, Image

import math

class Button1:
    def __init__(self, root, size, offset=1):
        self.size = size
        self.offset = offset
        self.root = root

        self.basePos = (-1,-1)
        self.baseAngle = 0
        self.curAngle = 0
        self.moving = 0

        self.img_org = Image.open("data/knob1.png")
        self.img_org = self.img_org.resize((size,size))
        self.imgx = ImageTk.PhotoImage(self.img_org)

        self.label = Label(self.root, image=self.imgx)

        self.label.bind("<B1-Motion>", self.drag)
        self.label.bind("<ButtonPress>", self.press)
        self.label.bind("<ButtonRelease>", self.release)

    def get(self):
        return self.curAngle * self.offset

    def recalcRotate(self, x,y):
        angle = 270- math.atan2(y,x)/math.pi*180
        angle = angle - self.baseAngle
        if (abs(360-abs(angle)) < abs(angle)): angle = abs(360-abs(angle)) * ( 1 if angle < 0 else -1 )

        self.curAngle += angle
        self.baseAngle = 270- math.atan2(y,x)/math.pi*180

        self.img1 = self.img_org.rotate(self.curAngle)
        self.imgx = ImageTk.PhotoImage(self.img1)
        self.label.configure(image = self.imgx)


    def isMoving(self):
        return self.moving

    def press(self, ev):
        self.moving = 1
        if (ev.num == 1):
            self.basePos = (ev.x, ev.y)
            self.baseAngle = 270- math.atan2(ev.y-self.size//2,ev.x-self.size//2)/math.pi*180

    def drag(self, ev):
        self.recalcRotate(ev.x-self.size//2, ev.y-self.size//2)

    def release(self, ev):
        self.moving = 0
        if (ev.num == 1):
            self.basePos = (-1,-1)

    def place(self, x,y):
        self.label.place(x=x-self.size/2,y=y-self.size/2)