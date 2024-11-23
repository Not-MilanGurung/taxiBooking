import tkinter as tk
from tkinter import ttk

class Login(ttk.Frame):
     
    def __init__(self, mainframe, root):

        ttk.Frame.__init__(self, mainframe)
        self.columnconfigure([0,1], weight=1)
        self.rowconfigure([0,2,3,5], weight=1)
        

        userL = ttk.Label(self, text='Username')
        userL.grid(row=0, column=0, padx=10, pady=10)
        user = ttk.Entry(self)
        user.grid(row=0, column=1, padx=10, pady=10)



        gradeL = ttk.Label(self, text='Grade')
        gradeL.grid(row=2, column=0, padx=10, pady=10)
        grade_entry = ttk.Entry(self)
        grade_entry.grid(row=2, column=1, padx=10, pady=10)

        button1 = ttk.Button(self, text='Save', command=exit)
        button1.grid(row=3, column=0, padx=10,pady=20)

        button1 = ttk.Button(self, text ="StartPage", command = lambda : root.show_frame(cont='StartPage'))
        button1.grid(row = 5, column = 1, padx = 10, pady = 10)  
