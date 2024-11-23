import tkinter as tk
from Database.query import *

class Query(tk.Frame):

    def __init__(self, mainframe, root):

        tk.Frame.__init__(self, mainframe)

        self.columnconfigure([0,1], weight=1)
        self.rowconfigure([0,1,2], weight=1)

        column_Label = tk.Label(self, text='Column')
        para_Label = tk.Label(self, text='Parameter')
        column_Label.grid(row=0, column=0, padx=50, pady=10)
        para_Label.grid(row=0, column=1, padx=50)

        self.column_Entry = tk.Entry(self)
        self.para_Entry = tk.Entry(self)
        self.column_Entry.grid(row=1, column=0, padx=50, pady=10)
        self.para_Entry.grid(row=1, column=1, padx=50)

        button_StartPage = tk.Button(self, text='Start Page', command=lambda: root.show_frame(cont='StartPage'))
        button_StartPage.grid(row=2, column=0, pady=10)

        button_Query = tk.Button(self, text='Query', command=self.show)
        button_Query.grid(row=2, column=1, pady=10)

    
    def show(self):
        try:
            res = select_from('login', self.column_Entry.get(), self.para_Entry.get())
            tk.Message(self, text=res).grid(row=3, column=0, columnspan=2)
        except:
            pass