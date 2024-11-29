import tkinter as tk
from tkinter import ttk
from UI.register_UI import Register
from UI.login_UI import Login
from UI.query_test_UI import Query
from UI.style import TaxiAppStyle


class tkinterApp(tk.Tk):

    def __init__(self, frames,  *args, **kwargs): 
         
        
        tk.Tk.__init__(self, *args, **kwargs)
         
        # creating a container
        mainframe = ttk.Frame(self)  
        mainframe.grid(column=0, row=0, sticky=tk.N + tk.W + tk.E + tk.S) 

        s = TaxiAppStyle(mainframe)
        
  
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

        login = Login(self, root)
        login.grid_propagate(0)
        login.grid(row=0, column=0, sticky='')

        register = Register(self, root)
        register.grid_propagate(0)
        register.grid(row=0, column=0, sticky='')

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)


        '''
        label = ttk.Label(self, text ="Startpage", anchor='center')
        label.grid(row = 0, column = 0,  pady = 10, padx=5) 




        button3 = ttk.Button(self, text ="Customer Test", command = lambda : root.show_frame(Page=Customer(mainframe, root, 'Test')))
        button3.grid(row = 3, column = 0,  pady = 10)
        '''




frames = (StartPage,)

if __name__ == '__main__':

    app = tkinterApp(frames)
    app.geometry('1200x600+100+0')

    app.mainloop()
