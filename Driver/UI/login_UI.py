from tkinter import ttk, StringVar, messagebox
from threading import Thread
from UI.driver_UI import Driver

LOGIN = 'LOGIN'
class Login(ttk.Frame):
            
     
    def __init__(self, parent, root):

        super().__init__(parent, height=500, width=400, style='LoginRegister.TFrame')
        # self.columnconfigure(0, weight=1)
        # self.rowconfigure([0,1,2], weight=1)
        self.parent = parent
        self.root = root
        self.columnconfigure(0, weight=1)
        ttk.Label(self, text='LOGIN', style='loginTitleLabel.TLabel').grid(row=0, column=0, pady=(10, 40))

        username_Frame = ttk.Frame(self, style='Username_Frame.TFrame')
        username_Frame.grid(row=1, column=0, sticky='ew', padx=10, pady=10)

        ttk.Label(username_Frame, text='Username').grid(row=0, column=0, padx=10, pady=10, sticky='ew')
        self.username = StringVar()
        user_entry = ttk.Entry(username_Frame, textvariable=self.username)
        user_entry.grid(row=0, column=1, padx=10, pady=10, sticky='ew')

        username_Frame.columnconfigure((0,1), weight=1)
        username_Frame.rowconfigure(0, weight=1)

        password_Frame = ttk.Frame(self, style='Username_Frame.TFrame')
        password_Frame.grid(row=2, column=0, sticky='ew', padx=10, pady=10)
        password_Frame.columnconfigure([0,1], weight=1)
        password_Frame.rowconfigure(0, weight=1)


        ttk.Label(password_Frame, text='Password').grid(row=0, column=0, padx=10, pady=10, sticky='ew')
        self.password = StringVar()
        password_entry = ttk.Entry(password_Frame, textvariable=self.password, show='*')
        password_entry.grid(row=0, column=1, padx=10, pady=10, sticky='ew')


        button1 = ttk.Button(self, text='Login', command=self.check)
        button1.grid(row=3, column=0, padx=10, pady=10)


    def login(self, username, password):
        self.res = 'No data recived'
        self.root.send_to_server(['DRIVER',LOGIN, username, password])
        self.res =  self.root.recive_from_server()
        self.recived()
   

    def check(self):
        username = self.username.get()
        password = self.password.get()
        if (username == ''):
            messagebox.showerror('Invalid Input', 'Username can not be empty')

        elif (password == ''): 
            messagebox.showerror('Invalid Input', 'Password cannot be empty')

        elif len(password) < 8: 
            messagebox.showerror('Invalid password', 'The password must be 8 characters long')
        else:     
            self.login(username, password)

    def recived(self):
        if self.res == 'Sucess':
            username = self.username.get()
            print(self.res)
            self.root.show_frame(frame=Driver(self.parent.mainframe, self.root, username))

        else:
            messagebox.showerror('Error', self.res)



