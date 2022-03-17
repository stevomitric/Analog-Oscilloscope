from tkinter import *
from tkinter.ttk import *
from PIL import ImageTk, Image

import numpy as np, time, random
from math import *

from buttons.but1 import Button1
from buttons.but2 import Button2
from buttons.mod1 import Mode1
from buttons.mod2 import Mode2
from buttons.but3 import Button3
from buttons.but4 import Button4

from componenets.bnc_sig import BNC_Connect

class Main:

    def __init__(self):
        self.TIME = time.time()
        self.REFRESH_LIS = 10 # skiciraj lisazua svaki 10-ti frame (jer se ne menja)
        self.cur_lis = 0

        #self.sig1 = lambda t: int(t*1000)%5-2
        self.sig1 = 0
        self.sig2 = 0
        
        self.mid1 = 0
        self.mid2 = 0

        self.setSignal(lambda t: 0, 0)
        self.setSignal(lambda t: 0, 1)

    def setSignal(self, sig, id):
        # izracunaj srednju vrednost
        val, N = 0, 10000
        for i in range(N):
            guess = random.randint(-1000000000000,1000000000000) / random.randint(0,100000000000)
            val += sig(guess)
        val = val/N

        if (id ==0):
            self.sig1 = sig
            self.mid1 = val
        else:
            self.sig2 = sig
            self.mid2 = val

    def drawCanvasBase(self):
        self.canvas.create_rectangle(0,0,1000,1000, fill='#006ec8')

        for i in range(0,10):
            self.canvas.create_line(i*30,0,i*30,1000)
            self.canvas.create_line(0,i*30,1000,i*30)
        for i in range(0,300,6):
            self.canvas.create_line(i,120-2,i,120+2)
            self.canvas.create_line(150-2,i,150+2,i)

    def drawLisazue(self):
        self.cur_lis = (self.cur_lis+1)%self.REFRESH_LIS
        if (self.cur_lis != 0):
            return

        self.canvas.delete('lines')

        voltsDIV = self.b5.get(0)
        voltsDIV2 = self.b6.get(0)
        lines = []
        for tm in np.linspace(0, 10, 300):
            y1 = self.sig1(tm) * self.b3.get()
            y2 = self.sig2(tm) * self.b4.get()

            y2 *= -1
            # calc value to pixels
            y1 = y1/voltsDIV * 30
            y2 = y2/voltsDIV2 * 30
            y2 += 120
            y1 += 150

            lines.append(y1)
            lines.append(y2)
        
        self.canvas.create_line(*lines, tags="lines", width=3, fill="#00a1e6", smooth=True,capstyle='round')

    def drawSignal(self):
        timeDIV = self.b7.get()
        if (timeDIV == -1):
            return self.drawLisazue()
        
        self.canvas.delete('lines')

        voltsDIV = self.b5.get(0)
        voltsDIV2 = self.b6.get(0)
        i, curtm, = 0,  time.time()

        lines1, lines2, lines3, lines4 = [], [], [], []

        # nadji triger
        trigger, trigger_val = self.b8.get()*(-1) + 120, -1
        prev_val = -9999
        for tm in np.linspace(curtm, curtm+10*timeDIV, 600):
            y = self.sig1(tm) * (-1)
            y = y/voltsDIV * 30 + 120 + self.b1.get()
            if (y > trigger and (prev_val != -9999 and prev_val <= trigger ) ):
                trigger_val = tm
                break
            prev_val = y

        # ako postoji trigger, podesi vreme od njega
        if (trigger_val != -1):
            curtm = trigger_val

        mod1, mod2 = self.mod2.get(), self.mod3.get()
        for tm in np.linspace(curtm, curtm+10*timeDIV, 300):
            x = i
            y1 = self.sig1(tm) * self.b3.get()
            if (mod1 == 2): y1=0
            if (mod1 == 1): y1 -= self.mid1
            y2 = self.sig2(tm) * self.b4.get()
            if (mod2 == 2): y2=0
            if (mod2 == 1): y2 -= self.mid2
            y3 = y1+y2

            # invert because of canvas
            y1 *= -1
            y2 *= -1
            y3 *= -1
            # calc value to pixels
            y1 = y1/voltsDIV * 30
            y2 = y2/voltsDIV2 * 30
            y3 = y3/voltsDIV * 30
            # add canvas offset
            y1 += 120
            y2 += 120
            y3 += 120
            # add gnd
            y1 += self.b1.get()
            y2 += self.b2.get()
            y3 += self.b2.get() + self.b1.get()

            lines1.append(x)
            lines2.append(x)
            lines3.append(x)
            lines1.append(y1)
            lines2.append(y2)
            lines3.append(y3)

            lines4.append(y1)
            lines4.append(y2)
            i += 1


        if (self.b7.get() != -1):
            if (self.mod1.get() == 1 or self.mod1.get() == 3):
                self.canvas.create_line(*lines1, tags="lines", width=3, fill="#00a1e6", smooth=True,capstyle='round')
            if (self.mod1.get() == 2 or self.mod1.get() == 3):    
                self.canvas.create_line(*lines2, tags="lines", width=3, fill="#00a1e6", smooth=True,capstyle='round')
            if (self.mod1.get() == 4):    
                self.canvas.create_line(*lines3, tags="lines", width=3, fill="#00a1e6", smooth=True,capstyle='round')
        else:
            # lisazuova fig
            self.canvas.create_line(*lines4, tags="lines", width=3, fill="#00a1e6", smooth=True,capstyle='round')

    def drawTrigger(self):
        self.canvas.delete('trigger')

        if (self.b8.isMoving()):
            self.canvas.create_line(0, self.b8.get()*(-1)+120, 300, self.b8.get()*(-1)+120, tags="trigger", width=3, fill="#AA0000")


    def mainLoop(self):
        self.drawTrigger()
        self.drawSignal()

        self.root.after(50, self.mainLoop)

    def drawGui(self):
        self.root = Tk()
        self.root.geometry('700x350')
        self.root.title('Analogni osciloskop')
        self.root.resizable(0,0)

        self.s1 = Style()
        self.s1.configure('Frame1.TFrame', background='#AAAAAA')

        self.canvas = Canvas(self.root, width=10*30, height=8*30)
        self.canvas.place(x=20,y=20)

        self.img1 = Image.open("data/footer.png")
        self.img1 = ImageTk.PhotoImage(self.img1)
        self.l1 = Label(self.root, image=self.img1)
        self.l1.place(x=-2,y=290)
        self.l1.bind("<ButtonPress>", self.footer_click)

        self.i1 = Image.open("data/arrows.png")
        self.i1 = self.i1.resize((15,15))
        self.i1 = ImageTk.PhotoImage(self.i1)
        self.l2 = Label(self.root, image=self.i1)
        self.l3 = Label(self.root, image=self.i1)
        self.l4 = Label(self.root, text="POSITION")
        self.b1 = Button1(self.root, 35, offset=.1)
        self.b2 = Button1(self.root, 35, offset=.1)
        self.l2.place(x=370,y=20)
        self.l3.place(x=490,y=20)
        self.l4.place(x=413,y=20)
        self.b1.place(378,65)
        self.b2.place(498,65)
        Label(self.root, text = '[Y]').place(x=520,y=55)

        self.mod1 = Mode1(self.root)
        self.mod1.place(x=403,y=75)

        self.b3 = Button2(self.root, 'X1', 'X5', [1,5])
        self.b3.place(360,130)
        self.b4 = Button2(self.root, 'NOR', 'INV', [1,-1])
        self.b4.place(478,130)

        self.b5 = Button3(self.root)
        self.b5.place(380,210)
        self.mod2 = Mode2(self.root)
        self.mod2.place(350,250)
        self.b6 = Button3(self.root)
        self.b6.place(505,210)
        self.mod3 = Mode2(self.root)
        self.mod3.place(475,250)
        Label(self.root, text = 'VOLTS/DIV').place(x=413,y=150)
        Label(self.root, text = 'mV',  font=("Courier", 8)).place(x=432,y=180)
        Label(self.root, text = 'CAL',  font=("Courier", 7)).place(x=420,y=220)

        self.b7 = Button4(self.root)
        self.b7.place(625,240)
        Label(self.root, text = 'TIME/DIV').place(x=600,y=170)
        Label(self.root, text = 'ms',  font=("Courier", 7)).place(x=580,y=196)
        Label(self.root, text = 's',  font=("Courier", 7)).place(x=580,y=266)
        Label(self.root, text = 'us',  font=("Courier", 7)).place(x=660,y=196)

        Label(self.root, text="TRIGGER").place(x=605,y=20)
        Label(self.root, text="[0]", font=("Courier", 7)).place(x=618,y=35)
        self.b8 = Button1(self.root, 35, offset=.1)
        self.b8.place(625,65)

        self.drawCanvasBase()

        self.mainLoop()

        self.root.mainloop()

    def footer_click(self, ev):
        if (ev.x >= 400 and ev.x <= 445):
            BNC_Connect(self.root, id=0, callback=self.setSignal)
        elif (ev.x >= 515 and ev.x <= 560):
            BNC_Connect(self.root, id=1, callback=self.setSignal)


if __name__ == "__main__":
    main = Main()
    main.drawGui()