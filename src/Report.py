import tkinter as tk
import pymysql
import sys
import os
import gc
from html.parser import HTMLParser
from tkinter.filedialog import askopenfile
from subprocess import Popen
from tkinter import messagebox
import urllib.request

        
mydb=pymysql.connect(host="localhost",user="root",password="",database="emotionanalyst")
mycursor=mydb.cursor()
top1=tk.Tk()
top1.title("Admin Dashboard")

error1=tk.StringVar()
url= tk.StringVar()

width = 500
height = 350
screen_width = top1.winfo_screenwidth()
screen_height = top1.winfo_screenheight()
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)
top1.geometry("%dx%d+%d+%d" % (width, height, x, y))
top1.config(bg="grey")




Lb1 = tk.Listbox(top1,width=50,bd=3,font=("arial",12))

fearcount=0
angrycount=0
disgustedcount=0
happycount=0
nuetralcount=0
sadcount=0
surprised=0


mycursor.execute("select * from uanswer")
myresult = mycursor.fetchall()
k=1
for x in myresult:
    data="Question : "+x[3]+" | Cat : "+x[2]+" | Answer : "+x[3]
    Lb1.insert(k, data)

#Lb1.grid(row=12, column=1)




def search():
    os.system("AdminDashboard.py")
    top1.destroy()
    
          
L= tk.Label(top1, width=30, font=('arial', 20),bg="black",fg="green", text = "   Emotion Analyst    ",bd=5)
L.grid(row=1,column=1)

L1= tk.Label(top1, width=30,bg="grey",font=('arial', 20),fg="green", text = "Happy Count :")
L1.grid(row=2,column=1)

L2= tk.Label(top1, width=30,bg="grey",font=('arial', 20),fg="green", text = "Sad Count :")
L2.grid(row=3,column=1)





top1.mainloop()
