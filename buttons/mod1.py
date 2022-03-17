from tkinter import *
from tkinter.ttk import *
from PIL import ImageTk, Image

import math

class Mode1:
    def __init__(self, root):
        self.root = root

        self.curOption = 1

        self.img_org = Image.open("data/mode1.png")
        self.imgx = ImageTk.PhotoImage(self.img_org)

        self.label = Label(self.root, image=self.imgx)

        self.label.bind("<Button-1>", self.press)

    def get(self):
        return self.curOption

    def press(self, ev):
        if (ev.num == 1):
            if (ev.y <= 25): self.curOption = 1
            elif (ev.y <= 35): self.curOption = 2
            elif (ev.y <= 45): self.curOption = 3
            else: self.curOption = 4

        self.img_org = Image.open(f"data/mode{self.curOption}.png")
        self.imgx = ImageTk.PhotoImage(self.img_org)
        self.label.configure(image=self.imgx)

    def place(self, x,y):
        self.label.place(x=x,y=y)