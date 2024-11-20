import tkinter as tk

class Login(tk.Frame):
     
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        

        userL = tk.Label(self, text='Username')
        userL.grid(row=0, column=0, padx=10, pady=10)
        user = tk.Entry(self)
        user.grid(row=0, column=1, padx=10, pady=10)

        ageL = tk.Label(self, text='Age')
        ageL.grid(row=1, column=0, padx=10, pady=10)
        age_entry = tk.Entry(self)
        age_entry.grid(row=1, column=1, padx=10, pady=10)

        gradeL = tk.Label(self, text='Grade')
        gradeL.grid(row=2, column=0, padx=10, pady=10)
        grade_entry = tk.Entry(self)
        grade_entry.grid(row=2, column=1, padx=10, pady=10)

        button1 = tk.Button(self, text='Save', command=exit)
        button1.grid(row=3, column=0, padx=10,pady=20)

        button1 = tk.Button(self, text ="StartPage", command = lambda : controller.show_frame(cont='StartPage'))
        button1.grid(row = 5, column = 1, padx = 10, pady = 10)  
