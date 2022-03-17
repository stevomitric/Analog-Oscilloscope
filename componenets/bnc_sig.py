from tkinter import *
from tkinter.ttk import *
from PIL import ImageTk, Image

from math import *

class BNC_Connect(Toplevel):
    def __init__(self, master=None, id=0, callback=None, **kw):
        super().__init__(master=master, **kw)

        self.geometry('470x200')
        self.title('Izbor Signala')
        self.callback = callback
        self.id = id

        self.sig = IntVar()
        self.sig.set(1)


        lf1 = LabelFrame(self, text='Sinusoida', width=150,height=150)
        lf1.place(x=5,y=2)
        self.rb1 = Radiobutton(lf1, text='Kompleksni oblik', variable=self.sig, value=0)
        self.rb2 = Radiobutton(lf1, text='Sinusni oblik', variable=self.sig, value=1)
        Label(lf1, text=r'Re{x}=').place(x=5,y=30)
        Label(lf1, text=r'Im{x}=').place(x=70,y=30)
        self.se1 = Entry(lf1, width=3)
        self.se1.insert(0,'1')
        self.se2 = Entry(lf1, width=3)
        self.se2.insert(0,'1')
        self.se1.place(x=42,y=30)
        self.se2.place(x=107,y=30)
        self.rb1.place(x=5,y=5)
        self.rb2.place(x=5,y=70)
        Label(lf1, text=r'A=').place(x=5,y=95)
        Label(lf1, text=r'W=').place(x=50,y=95)
        Label(lf1, text=r'Fi=').place(x=99,y=95)
        self.se3 = Entry(lf1, width=3)
        self.se3.insert(0,'1')
        self.se4 = Entry(lf1, width=3)
        self.se4.insert(0,'10')
        self.se5 = Entry(lf1, width=3)
        self.se5.insert(0,'0')
        self.se3.place(x=22,y=95)
        self.se4.place(x=70,y=95)
        self.se5.place(x=117,y=95)

        lf2 = LabelFrame(self, text='Cetvrtka', width=150,height=150)
        lf2.place(x=160,y=2)
        self.rb3 = Radiobutton(lf2, text='Pravougaoni oblik', variable=self.sig, value=2)
        self.rb3.place(x=5,y=5)
        Label(lf2, text=r'Amplituda [V] = ').place(x=5,y=30)
        Label(lf2, text=r'Trajanje 1 [s] = ').place(x=5,y=55)
        Label(lf2, text=r'Trajanje 0 [s] = ').place(x=5,y=80)
        self.ce1 = Entry(lf2, width=6)
        self.ce1.place(x=95,y=30)
        self.ce1.insert(0,'1')
        self.ce2 = Entry(lf2, width=6)
        self.ce2.place(x=95,y=55)
        self.ce2.insert(0,'0.1')
        self.ce3 = Entry(lf2, width=6)
        self.ce3.place(x=95,y=80)
        self.ce3.insert(0,'0.1')

        lf3 = LabelFrame(self, text='Custom', width=150,height=150)
        lf3.place(x=160+150+5,y=2)
        self.rb4 = Radiobutton(lf3, text='Specijalni oblik', variable=self.sig, value=3)
        self.rb4.place(x=5,y=5)
        self.t1 = Text(lf3, width=16,height=5)
        self.t1.place(x=5,y=35)
        self.t1.insert('end', 'cos(2*pi*t)')

        Button(self, text='Izaberi signal', width=15, command = self.izabranSignal).place(x=200,y=160)



    def izabranSignal(self):
        if (self.sig.get() == 1):
            A = eval(self.se3.get())
            W = eval(self.se4.get())
            F = eval(self.se5.get())
            
            fun = lambda t: A*(sin(W*t+F))
            if (self.callback):
                self.callback(fun, self.id)
        
        if (self.sig.get() == 2):
            A = eval(self.ce1.get())
            T1 = eval(self.ce2.get())
            T0 = eval(self.ce3.get())

            fun = lambda t: A*( 1 if (t%(T1+T0) <= T1) else 0  )
            if (self.callback):
                self.callback(fun, self.id)

        if (self.sig.get() == 3):
            tmp = self.t1.get('1.0','end')
            
            fun = lambda t: eval(tmp)
            if (self.callback):
                self.callback(fun, self.id)

        self.destroy()