import tkinter as tk
from tkinter import ttk, messagebox
from UI.admin_UI_login import Login
from UI.style import TaxiAppStyle


CUSTOMER = 'CUSTOMER'

class tkinterApp(tk.Tk):

    def __init__(self,  *args, **kwargs): 
        super().__init__(*args, **kwargs)
        self.geometry('1200x600+100+0')
        self.title('Taxi Booking System: [ADMINISTRATOR]')
         
        # creating a container
        mainframe = ttk.Frame(self)  
        mainframe.grid(column=0, row=0, sticky=tk.N + tk.W + tk.E + tk.S) 

        style = TaxiAppStyle(mainframe)
  
        self.grid_columnconfigure(0, weight = 1)
        self.grid_rowconfigure(0, weight = 1)
        mainframe.grid_columnconfigure(0, weight = 1)
        mainframe.grid_rowconfigure(0, weight = 1)

        self.show_frame(StartPage(mainframe, self))


    def show_frame(self, frame: ttk.Frame):
        frame.grid(row = 0, column = 0, sticky =(tk.N, tk.S, tk.E, tk.W))
        frame.tkraise()
    



class StartPage(ttk.Frame):
        
        def __init__(self, mainframe, root):
            super().__init__(mainframe)
            self.mainframe = mainframe
            self.root = root

            self.columnconfigure(0, weight=1)
            self.rowconfigure(0, weight=1)
             
            self.login = Login(self, root)
            self.login.grid_propagate(0)
            self.login.grid(row=0, column=0, sticky='')

            self.login.tkraise()


if __name__ == '__main__':

    app = tkinterApp()
    
    try:
        app.mainloop()
        app.disconnect_server()
        print('Disconnected from server')
    except: # If can not connect to the server
        pass
