from tkinter import *
from tkinter.ttk import *
from PIL import ImageTk, Image

import math

class Mode2:
    def __init__(self, root):
        self.root = root

        self.curOption = 3

        self.img_org = Image.open("data/mode_h3.png")
        self.imgx = ImageTk.PhotoImage(self.img_org)

        self.label = Label(self.root, image=self.imgx)

        self.label.bind("<Button-1>", self.press)

    def get(self):
        return self.curOption

    def press(self, ev):
        if (ev.num == 1):
            if (ev.x <= 20): self.curOption = 1
            elif (ev.x <= 35): self.curOption = 2
            else: self.curOption = 3

        self.img_org = Image.open(f"data/mode_h{self.curOption}.png")
        self.imgx = ImageTk.PhotoImage(self.img_org)
        self.label.configure(image=self.imgx)

    def place(self, x,y):
        self.label.place(x=x,y=y)