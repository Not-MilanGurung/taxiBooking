import tkinter as tk
from UI.register_UI import Register
from UI.login_UI import Login
from UI.query_test_UI import Query


class tkinterApp(tk.Tk):

    def __init__(self, frames,  *args, **kwargs): 
         
        
        tk.Tk.__init__(self, *args, **kwargs)
         
        # creating a container
        container = tk.Frame(self)  
        container.pack(side = "top", fill = "both", expand = True) 
        
  
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
  
        
        self.frames = {}
        # iterating through a tuple consisting of the different page layouts
        for F in frames:
            frame = F(container, self)
            self.frames[F.__name__] = frame
            frame.grid(row = 0, column = 0, sticky ="nsew")

  
        self.show_frame(cont='StartPage')
  
    def show_frame(self, Page = None, cont: str | None = None ):

        if Page != None:
            frame = Page
            frame.grid(row = 0, column = 0, sticky ="nsew")
        else:
            frame = self.frames[cont]
        
        frame.tkraise()

class StartPage(tk.Frame):
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text ="Startpage")
        label.grid(row = 0, column = 0, padx = 100, pady = 10) 

        button1 = tk.Button(self, text ="Login", command = lambda : controller.show_frame(cont='Login'))
        button1.grid(row = 1, column = 0, padx = 350, pady = 10)
  
        button2 = tk.Button(self, text ="Register", command = lambda : controller.show_frame(cont='Register'))
        button2.grid(row = 2, column = 0, padx = 100, pady = 10)

        button3 = tk.Button(self, text ="Query Test", command = lambda : controller.show_frame(cont='Query'))
        button3.grid(row = 3, column = 0, padx = 100, pady = 10)


frames = (StartPage, Login, Register, Query)

if __name__ == '__main__':

    app = tkinterApp(frames)
    app.geometry('800x500')

    app.mainloop()
