from tkinter import *
from tkinter.ttk import *
from PIL import ImageTk, Image

import math

class Button4:
    ALLOWED_ANGLES = [142.2, 129.3, 114.9, 100.2, 84.1, 70.8, 58, 45.5, 30.6, 15.5, 3.8, -15.1, -33.3, -43.9, -58.4, -70.2, -86, -100, -117, -132]
    VALUES = [0.2, 0.1, 0.05, 0.02, 0.01, 0.005, 0.002, 0.001, 0.0005, 0.0002, 0.0001, 5e-05, 2e-05, 1e-05, 5e-06, 2e-06, 1e-06, 5e-07, 2e-07 ,-1]

    @staticmethod
    def closestAngle(angle):
        ''' vracam najblizi ugao '''
        dif, res = 99999, 0
        for item in Button4.ALLOWED_ANGLES:
            if (abs(item-angle) < dif):
                dif = abs(item-angle)
                res = item
        return res

    def __init__(self, root):
        self.root = root

        self.basePos = (-1,-1)
        self.baseAngle = 0
        self.curAngle = 45.5

        self.canvas = Canvas(self.root, width=90, height=90)

        self.img_base = Image.open("data/button3-4.png")
        self.img_base = ImageTk.PhotoImage(self.img_base)
        self.canvas.create_image(45,45+1, image=self.img_base)

        self.img_1 = Image.open("data/button3-2.png")
        self.img_1 = self.img_1.resize((85,85))
        self.img_1_x = self.img_1.rotate(self.curAngle)
        self.img_1_p = ImageTk.PhotoImage(self.img_1_x)
        self.img_1_id = self.canvas.create_image(45-1,45+1, image=self.img_1_p)

        self.canvas.bind("<B1-Motion>", self.drag)
        self.canvas.bind("<ButtonPress>", self.press)

    def get(self):
        return Button4.VALUES[ Button4.ALLOWED_ANGLES.index(self.curAngle) ]

    def recalcRotate(self, x,y):
        angle = 270- math.atan2(y,x)/math.pi*180

        angle = angle - self.baseAngle
        if (abs(360-abs(angle)) < abs(angle)): angle = abs(360-abs(angle)) * ( 1 if angle < 0 else -1 )

        if (Button4.closestAngle(self.curAngle+angle) == self.curAngle): return
        self.curAngle = Button4.closestAngle(self.curAngle+angle)

        self.baseAngle = 270- math.atan2(y,x)/math.pi*180

        self.canvas.delete(self.img_1_id)
        self.img_1_x = self.img_1.rotate(self.curAngle)
        self.img_1_x = ImageTk.PhotoImage(self.img_1_x)
        self.img_1_id = self.canvas.create_image(45-1,45+1, image=self.img_1_x)

    def press(self, ev):
        if (ev.num == 1):
            self.basePos = (ev.x, ev.y)
            self.baseAngle = 270- math.atan2(ev.y-45,ev.x-45)/math.pi*180

    def drag(self, ev):
        self.recalcRotate(ev.x-45, ev.y-45)

    def place(self, x,y):
        self.canvas.place(x=x-45,y=y-45)