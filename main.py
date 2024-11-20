import tkinter as tk
from UI.register_UI import Register, Account
from UI.login_UI import Login
class tkinterApp(tk.Tk):
    # __init__ function for class tkinterApp 
    def __init__(self, frames,  *args, **kwargs): 
         
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)
         
        # creating a container
        self.container = tk.Frame(self)  
        self.container.pack(side = "top", fill = "both", expand = True) 
        
  
        self.container.grid_rowconfigure(0, weight = 1)
        self.container.grid_columnconfigure(0, weight = 1)
  
        # initializing frames to an empty array

        self.frames = {}
        # iterating through a tuple consisting
        # of the different page layouts
        for F in frames:
            frame = F(self.container, self)
            self.frames[F.__name__] = frame
            frame.grid(row = 0, column = 0, sticky ="nsew")
            # initializing frame of that object from
            # startpage, page1, page2 respectively with 
            # for loop
  
        self.show_frame(cont='StartPage')
  
    # to display the current frame passed as
    # parameter
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
         
        # label of frame Layout 2
        label = tk.Label(self, text ="Startpage")
         
        # putting the grid in its place by using
        # grid
        label.grid(row = 0, column = 0, padx = 100, pady = 10) 

        button1 = tk.Button(self, text ="Login",
        command = lambda : controller.show_frame(cont='Login'))
     
        # putting the button in its place by
        # using grid
        button1.grid(row = 1, column = 0, padx = 350, pady = 10)
  
        ## button to show frame 2 with text layout2
        button2 = tk.Button(self, text ="Register",
        command = lambda : controller.show_frame(cont='Register'))
     
        # putting the button in its place by
        # using grid
        button2.grid(row = 2, column = 0, padx = 100, pady = 10)
frames = (StartPage, Login, Register)
app = tkinterApp(frames)
app.geometry('800x500')



app.mainloop()
