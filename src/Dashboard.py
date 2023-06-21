import tkinter as tk
import pymysql
import sys
import os
import gc
from tkinter.filedialog import askopenfile
from subprocess import Popen
from tkinter import messagebox
from subprocess import call
top1=tk.Tk()
top1.title("Admin Dashboard")
width = 1300
height = 700
screen_width = top1.winfo_screenwidth()
screen_height = top1.winfo_screenheight()
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)
top1.geometry("%dx%d+%d+%d" % (width, height, x, y))
top1.config(bg="grey")
def viewresponses():
    call('python ViewResponses.py', shell=True)
    #os.system("ViewUsers.py")
def mysearches():
    call('python emotions.py', shell=True)
    #os.system("ViewAllSearches.py")
def addquestion():
    call('python AddQuestion.py', shell=True)
    #os.system("AddWordDictionary.py")
def blacklink():
    call('python Report.py', shell=True)
    #os.system("BlackListedLink.py")
def logout():
    top1.destroy()
    call('python index.py', shell=True)
    #os.system("index.py")
    
        



    
L= tk.Label(top1, width=30, font=('arial', 20),bg="black",fg="green", text = "   Emotion Analyst",bd=5)
L.grid(row=1,column=1)
L= tk.Label(top1, width=30, font=('arial', 20),bg="black",fg="red", text = "--Welcome to Emotions Detection",bd=5)
L.grid(row=1,column=2)
L= tk.Label(top1, width=30, font=('arial', 20),bg="black",fg="green", text = "",bd=5)
L.grid(row=1,column=3)

photo = tk.PhotoImage(file = r"E:\Gayatri\Fegusson College\project\Final Code\Emotion Detection Live Code\images\viewuser.png")
photoimage = photo.subsample(4, 4) 
b2= tk.Button(top1,bg="white",fg="green",text="View Dataset",bd=8,command=viewresponses,image = photoimage,compound ="top")  
b2.config(width="100")
b2.config(height="100")
b2.grid(row=2,column=1,padx=30,pady=30)


photo2 = tk.PhotoImage(file = r"E:\Gayatri\Fegusson College\project\Final Code\Emotion Detection Live Code\images\searches.png")
photoimage2 = photo2.subsample(4, 4) 
b3= tk.Button(top1,bg="white",fg="green",text="Start Bot",bd=8,command=mysearches,image = photoimage2,compound ="top" )
b3.config(width="100")
b3.config(height="100")  
b3.grid(row=2,column=2)

photo5 = tk.PhotoImage(file = r"E:\Gayatri\Fegusson College\project\Final Code\Emotion Detection Live Code\images\showword.png")
photoimage5 = photo5.subsample(4, 4)
b6= tk.Button(top1,bg="white",fg="green",text="Reports",bd=8,command=blacklink,image = photoimage5,compound ="top"  )
b6.config(width="100")
b6.config(height="100")  
b6.grid(row=2,column=3)


top1.mainloop()
