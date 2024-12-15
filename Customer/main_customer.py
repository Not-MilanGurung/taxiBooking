
import tkinter as tk

from tkinter import ttk, messagebox
from Networking.client import Client
from UI.register_UI import Register
from UI.login_UI import Login
from UI.style import TaxiAppStyle




class tkinterApp(tk.Tk):

    def __init__(self,  *args, **kwargs): 
        super().__init__(*args, **kwargs)
        self.geometry('1200x600+100+0')
         
        # creating a container
        mainframe = ttk.Frame(self)  
        mainframe.grid(column=0, row=0, sticky=tk.N + tk.W + tk.E + tk.S) 

        style = TaxiAppStyle(mainframe)
  
        self.grid_columnconfigure(0, weight = 1)
        self.grid_rowconfigure(0, weight = 1)
        mainframe.grid_columnconfigure(0, weight = 1)
        mainframe.grid_rowconfigure(0, weight = 1)

        self.show_frame(StartPage(mainframe, self))
        self.connect_server()

    def connect_server(self):
        try:
            self.con = Client()
        except:
            # messagebox.showerror('Network Error', 'Can not connect to the server' )
            res = messagebox.askquestion('Network Error','Can not connect to server'+'\n'+'Try to reconnect?')
            if res == 'yes':
                self.connect_server()
            else:
                self.destroy()
  
    def show_frame(self, frame: ttk.Frame):
        frame.grid(row = 0, column = 0, sticky =(tk.N, tk.S, tk.E, tk.W))
        frame.tkraise()

    def send_to_server(self, msg: list[any]):
        try:
            self.con.sendToServer(msg)
        except BrokenPipeError:
            self.connect_server()
    
    def recive_from_server(self):

        return self.con.recive()

    def disconnect_server(self):
        self.con.disconnect()


class StartPage(ttk.Frame):
        
        def __init__(self, mainframe, root):
            super().__init__(mainframe)
            self.mainframe = mainframe
            self.root = root

            self.columnconfigure(0, weight=1)
            self.rowconfigure(0, weight=1)
             
            self.loginFrame = Login(self, root)
            self.loginFrame.grid_propagate(0)
            self.loginFrame.grid(row=0, column=0, sticky='nsew')

            self.registerFrame = Register(self, root)
            self.registerFrame.grid(row=0, column=0, sticky='nsew')
            
            self.loginFrame.tkraise()

        def show_frame(self, frame:str):
            frameObj = self.__dict__[frame]
            frameObj.tkraise()

if __name__ == '__main__':

    app = tkinterApp()
    
    try:
        app.mainloop()
        app.disconnect_server()
        print('Disconnected from server')
    except: # If can not connect to the server
        pass
