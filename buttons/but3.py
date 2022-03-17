from tkinter import *
from tkinter.ttk import *
from PIL import ImageTk, Image

import math

class Button3:
    ALLOWED_ANGLES = [131.3, 109.4, 77.7, 45.6, 16.4, -22.3, -47.5, -75.8, -107.3, -133.7]
    VALUES = [5,2,1,.5,.2,.1,.05,.02,.01,.005]

    @staticmethod
    def closestAngle(angle):
        ''' vracam najblizi ugao '''
        dif, res = 99999, 0
        for item in Button3.ALLOWED_ANGLES:
            if (abs(item-angle) < dif):
                dif = abs(item-angle)
                res = item
        return res

    def __init__(self, root):
        self.root = root

        self.basePos = [(-1,-1), (-1,-1)]
        self.baseAngle = [0,0]
        self.curAngle = [77.7,0]
        self.curId = 0

        self.canvas = Canvas(self.root, width=90, height=90)

        self.img_base = Image.open("data/button3-1.png")
        self.img_base = ImageTk.PhotoImage(self.img_base)
        self.canvas.create_image(45,45+1, image=self.img_base)

        self.img_1 = Image.open("data/button3-2.png")
        self.img_1_x = self.img_1.rotate(self.curAngle[0])
        self.img_1_p = ImageTk.PhotoImage(self.img_1_x)
        self.img_1_id = self.canvas.create_image(45-1,45+1, image=self.img_1_p)

        self.img_2 = Image.open("data/button3-3.png")
        self.img_2_p = ImageTk.PhotoImage(self.img_2)
        self.img_2_id = self.canvas.create_image(45-1,45+1, image=self.img_2_p)

        self.canvas.bind("<B1-Motion>", self.drag)
        self.canvas.bind("<ButtonPress>", self.press)

    def get(self, id):
        if (id == 0):
            return Button3.VALUES[ Button3.ALLOWED_ANGLES.index(self.curAngle[0]) ]

    def recalcRotate(self, x,y, id):
        angle = 270- math.atan2(y,x)/math.pi*180
        angle = angle - self.baseAngle[id]
        if (abs(360-abs(angle)) < abs(angle)): angle = abs(360-abs(angle)) * ( 1 if angle < 0 else -1 )
        if (id == 0):
            if (Button3.closestAngle(self.curAngle[id]+angle) == self.curAngle[id]): return
            self.curAngle[id] = Button3.closestAngle(self.curAngle[id]+angle)
        else:
            self.curAngle[id] += angle
        
        self.baseAngle[id] = 270- math.atan2(y,x)/math.pi*180


        self.canvas.delete(self.img_1_id)
        self.img_1_x = self.img_1.rotate(self.curAngle[0])
        self.img_1_x = ImageTk.PhotoImage(self.img_1_x)
        self.img_1_id = self.canvas.create_image(45-1,45+1, image=self.img_1_x)

        self.canvas.delete(self.img_2_id)
        self.img_2_x = self.img_2.rotate(self.curAngle[1])
        self.img_2_x = ImageTk.PhotoImage(self.img_2_x)
        self.img_2_id = self.canvas.create_image(45-1,45+1, image=self.img_2_x)


    def press(self, ev):
        d = (ev.x-45)**2 + (ev.y-45)**2
        self.curId = 0 if d > 350 else 1
        if (ev.num == 1):
            self.basePos[self.curId] = (ev.x, ev.y)
            self.baseAngle[self.curId] = 270- math.atan2(ev.y-45,ev.x-45)/math.pi*180

    def drag(self, ev):
        self.recalcRotate(ev.x-45, ev.y-45, self.curId)

    def place(self, x,y):
        self.canvas.place(x=x-45,y=y-45)