from tkinter import *
from tkinter.ttk import *
from PIL import ImageTk, Image

import math

class Button2:
    def __init__(self, root, l1, l2, v):
        self.root = root

        self.curOption = 0
        self.x, self.y = 0,0
        self.v = v

        self.img_org = Image.open("data/button1.png")
        self.imgx = ImageTk.PhotoImage(self.img_org)

        self.label = Label(self.root, image=self.imgx)
        self.l1 = Label(self.root, text='-'+l1, font=("Courier", 8))
        self.l2 = Label(self.root, text=l2, font=("Courier", 8))

        self.t1 = l1
        self.t2 = l2

        self.label.bind("<Button-1>", self.press)

    def get(self):
        return self.v[self.curOption]

    def press(self, ev):
        self.curOption = 1-self.curOption
        if (self.curOption == 0):
            self.l1.configure(text='-'+self.t1)
            self.l2.configure(text=self.t2)
            self.l1.place(x=self.x+8,y=self.y-30)
            self.l2.place(x=self.x+15,y=self.y-15)
        else:
            self.l1.configure(text=self.t1)
            self.l2.configure(text='-'+self.t2)
            self.l1.place(x=self.x+15,y=self.y-30)
            self.l2.place(x=self.x+8,y=self.y-15)
            

    def place(self, x,y):
        self.x = x
        self.y = y
        self.label.place(x=x,y=y)
        self.curOption = 1
        self.press(None)