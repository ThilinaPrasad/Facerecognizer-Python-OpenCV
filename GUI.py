import sys,os
from tkinter import *
from PIL import ImageTk, Image
import tkinter.messagebox

mainUI = Tk()                        #Create frame
mainUI.geometry('450x400+500+300')
mainUI.title("Face Recognizer")

def reg():                          #Register user method
    result = tkinter.messagebox.askquestion("Recognizer Info", "Please enter your data and wait untill scan successful!\nDo you want to continue.")
    if(result == 'yes'):
        os.system('dataset.py') 
def rec():                          #User recognize method
    confirm = tkinter.messagebox.askquestion("Recognizer Info", "Press Q to leave the camera window!\nYou want to open camera?")
    if(confirm=='yes'):
        os.system('detector.py')
def train():                        #System training function
    os.system('trainer.py')

img = ImageTk.PhotoImage(Image.open("icon.png"))
panel = Label(mainUI, image = img)
panel.pack(side = "top", fill = "both", expand = "no")

#Button event handeling
reg=Button(mainUI,text="Register New User",command=reg,fg="white",bg="#1de9b6").pack(side="left",expand="yes")
rec=Button(mainUI,text="Recognize User",command=rec,fg="white",bg="#1de9b6").pack(side="right",expand="yes")
rec=Button(mainUI,text="Train System",command=train,fg="white",bg="#1de9b6").pack(side="right",expand="yes")

mainUI.mainloop()
