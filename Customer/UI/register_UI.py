from tkinter import ttk, messagebox
from threading import Thread
REGISTER = ['CUSTOMER','REGISTER']

class Register(ttk.Frame):
    
     
    def __init__(self, parent, root):

        super().__init__( parent)

        
        self.root = root
        self.parent = parent

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        frame = ttk.Frame(self, style='LoginRegister.TFrame')
        frame.grid(column=0, row=0, sticky='')

        text = ttk.Label(frame, text="Register", style='mainBgText.TLabel')
        text.grid(row=0, column=2,pady=10)
        fL = ttk.Label(frame, text="First Name", style='mainBgText.TLabel')
        fL.grid(row=1, column=1,pady=10, padx=10)
        mL = ttk.Label(frame, text="Middle Name", style='mainBgText.TLabel')
        mL.grid(row=1, column=2,padx=10, pady=10)
        lL = ttk.Label(frame, text="Last Name", style='mainBgText.TLabel')
        lL.grid(row=1, column=3,padx=10,pady=10)
        self.fname = ttk.Entry(frame)
        self.mname = ttk.Entry(frame)
        self.lname = ttk.Entry(frame)
        self.fname.grid(row=2, column=1,padx=10)
        self.mname.grid(row=2, column=2,padx=10)
        self.lname.grid(row=2, column=3,padx=10)

        phoneL = ttk.Label(frame, text="Phone Number", style='mainBgText.TLabel')
        phoneL.grid(row=3, column=1,pady=10)
        emailL = ttk.Label(frame, text="Email", style='mainBgText.TLabel')
        emailL.grid(row=3, column=3,pady=10)
        self.phone = ttk.Entry(frame)
        self.email = ttk.Entry(frame)
        self.phone.grid(row=4, column=1,padx=10)
        self.email.grid(row=4, column=3,padx=10)

        addL = ttk.Label(frame, text="Address", style='mainBgText.TLabel')
        addL.grid(row=5, column=1,pady=10)
        self.address = ttk.Entry(frame)
        self.address.grid(row=6, column=1,padx=10)

        userL = ttk.Label(frame, text="User Name", style='mainBgText.TLabel')
        userL.grid(row=7, column=1,pady=10)
        passL= ttk.Label(frame, text="Password", style='mainBgText.TLabel')
        passL.grid(row=7, column=2,pady=10)
        passLC= ttk.Label(frame, text="Confirm Password", style='mainBgText.TLabel')
        passLC.grid(row=7, column=3,pady=10)
        self.userName = ttk.Entry(frame)
        self.password = ttk.Entry(frame, show='*')
        self.passwordC = ttk.Entry(frame, show='*')
        self.userName.grid(row=8, column=1,padx=10)
        self.password.grid(row=8, column=2,padx=10)
        self.passwordC.grid(row=8, column=3,padx=10)

        detail = ttk.Button(frame, text='Continue', command=self.check)
        detail.grid(row=9, column= 2)

        button1 = ttk.Button(frame, text ="Login Page", command = lambda : parent.show_frame('loginFrame'))
        button1.grid(row = 9, column = 1, padx = 10, pady = 10)  
    
    def check(self):
        fname = self.fname.get()
        if fname == '':
            messagebox.showerror('Incomplete data', 'First Name can not be empty')
            return

        lname = self.lname.get()
        if lname == '':
            messagebox.showerror('Incomplete data', 'Last Name can not be empty')
            return

        mname = self.mname.get()
        fullName = ' '.join((fname, mname, lname))

        address = self.address.get()
        if address == '':
            messagebox.showerror('Incomplete data', 'Address can not be empty')
            return

        phone = self.phone.get()
        if phone == '':
            messagebox.showerror('Incomplete data', 'Phone Number can not be empty')
            return

        email = self.email.get()
        if email == '':
            messagebox.showerror('Incomplete data', 'Email can not be empty')
            return

        userName = self.userName.get()
        if userName == '':
            messagebox.showerror('Incomplete data', 'Username can not be empty')
            return
        
        password = self.password.get()
        if password == '':
            messagebox.showerror('Incomplete data', 'Password can not be empty')
            return
        if len(password) < 8 :
            messagebox.showerror('Incomplete data', 'Password can not be less than 8 characters')
            return
        
        confPass = self.passwordC.get()
        if confPass != password:
            messagebox.showerror('Error', 'Password does not match')
            return
        
        data = [userName, password, fullName,  phone, email, address]
        self.store(data)

    def recive_thread(self):
        self.res = self.root.recive_from_server()
        self.recive()

    def recive(self): 
        if self.res == 'Sucess':
            messagebox.showinfo('Successfull', 'Account created, go to login page')       
        else:
            messagebox.showerror('Error', self.res)

    def store(self, data):
        self.res = 'Did not recive any data'
        data = REGISTER + data
        self.root.send_to_server(data)
        thread = Thread(target=self.recive_thread)
        thread.start()

        
    