import tkinter as tk
from tkinter import ttk
from UI.register_UI import Register
from UI.login_UI import Login
from UI.query_test_UI import Query


class tkinterApp(tk.Tk):

    def __init__(self, frames,  *args, **kwargs): 
         
        
        tk.Tk.__init__(self, *args, **kwargs)
         
        # creating a container
        mainframe = ttk.Frame(self, padding='3 3 12 12')  
        mainframe.grid(column=0, row=0, sticky=tk.N + tk.W + tk.E + tk.S) 
        
  
        self.grid_columnconfigure(0, weight = 1)
        self.grid_rowconfigure(0, weight = 1)
        mainframe.grid_columnconfigure(0, weight = 1)
        mainframe.grid_rowconfigure(0, weight = 1)

  
        
        self.frames = {}
        # iterating through a tuple consisting of the different page layouts
        for F in frames:
            frame = F(mainframe, self)
            self.frames[F.__name__] = frame
            frame.grid(row = 0, column = 0,sticky =(tk.N, tk.S, tk.E, tk.W))

  
        self.show_frame(cont='StartPage')
  
    def show_frame(self, Page = None, cont: str | None = None ):

        if Page != None:
            frame = Page
            frame.grid(row = 0, column = 0, sticky =(tk.N, tk.S, tk.E, tk.W))
        else:
            frame = self.frames[cont]
        
        frame.tkraise()

class StartPage(ttk.Frame):
    def __init__(self, mainframe, root): 
        ttk.Frame.__init__(self, mainframe)

        self.columnconfigure(0, weight=1)
        self.rowconfigure([0,1,2,3], weight=1)


        label = ttk.Label(self, text ="Startpage", anchor='center')
        label.grid(row = 0, column = 0,  pady = 10, padx=5) 

        button1 = ttk.Button(self, text ="Login", command = lambda : root.show_frame(cont='Login'))
        button1.grid(row = 1, column = 0,  pady = 10)
  
        button2 = ttk.Button(self, text ="Register", command = lambda : root.show_frame(cont='Register'))
        button2.grid(row = 2, column = 0,  pady = 10)

        button3 = ttk.Button(self, text ="Query Test", command = lambda : root.show_frame(cont='Query'))
        button3.grid(row = 3, column = 0,  pady = 10)




frames = (StartPage, Login, Register, Query)

if __name__ == '__main__':

    app = tkinterApp(frames)
    # app.geometry('800x500')

    app.mainloop()
