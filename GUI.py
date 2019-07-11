#!/usr/bin/python3

import tkinter # note that module name has changed from Tkinter in Python 2 to tkinter in Python 3
from tkinter import *

from tkinter import messagebox

#define window
window = Tk()
#window.geometry("100x100")

#define button functions
def helloCallBack():
   msg = messagebox.showinfo( "Hello Python", "Hello World")
   
def closeWindow():
   window.destroy()
   window.quit()
   
#define Buttons
B = Button(window, text = "Hello", command = helloCallBack)
A = Button(window, text = "Close", command = closeWindow)

#place buttons
B.place(x = 25,y = 50)
A.place(x = 75, y = 50)

#run the GUI
window.mainloop()