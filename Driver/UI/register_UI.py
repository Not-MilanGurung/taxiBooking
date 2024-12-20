from tkinter import ttk, messagebox, Text, StringVar

REGISTER = ['DRIVER','REGISTER']

class Register(ttk.Frame):
    
     
    def __init__(self, parent, root):

        super().__init__( parent)

        # Initilise variables
        self.root = root
        self.parent = parent
        # Allow row and column 0,0 to be scaled with the mainframe
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        frame = ttk.Frame(self, style='LoginRegister.TFrame')
        frame.grid(column=0, row=0, sticky='')

        ttk.Label(frame, text="Register", style='mainBgText.TLabel').grid(row=0, column=2,pady=10)

        ttk.Label(frame, text="First Name", style='mainBgText.TLabel').grid(row=1, column=1,pady=10, padx=10)
        ttk.Label(frame, text="Middle Name", style='mainBgText.TLabel').grid(row=1, column=2,padx=10, pady=10)
        ttk.Label(frame, text="Last Name", style='mainBgText.TLabel').grid(row=1, column=3,padx=10,pady=10)
        self.fname = ttk.Entry(frame)
        self.mname = ttk.Entry(frame)
        self.lname = ttk.Entry(frame)
        self.fname.grid(row=2, column=1,padx=10)
        self.mname.grid(row=2, column=2,padx=10)
        self.lname.grid(row=2, column=3,padx=10)

        ttk.Label(frame, text="Phone Number", style='mainBgText.TLabel').grid(row=3, column=1,pady=10)
        ttk.Label(frame, text="Email", style='mainBgText.TLabel').grid(row=3, column=3,pady=10)
        self.phone = ttk.Entry(frame)
        self.email = ttk.Entry(frame)
        self.phone.grid(row=4, column=1,padx=10)
        self.email.grid(row=4, column=3,padx=10)

        ttk.Label(frame, text="Address", style='mainBgText.TLabel').grid(row=5, column=1,pady=10)
        self.address = ttk.Entry(frame)
        self.address.grid(row=6, column=1,padx=10)

        ttk.Label(frame, text="User Name", style='mainBgText.TLabel').grid(row=7, column=1,pady=10)
        ttk.Label(frame, text="Password", style='mainBgText.TLabel').grid(row=7, column=2,pady=10)
        ttk.Label(frame, text="Confirm Password", style='mainBgText.TLabel').grid(row=7, column=3,pady=10)
        self.userName = ttk.Entry(frame)
        self.password = ttk.Entry(frame, show='*')
        self.passwordC = ttk.Entry(frame, show='*')
        self.userName.grid(row=8, column=1,padx=10)
        self.password.grid(row=8, column=2,padx=10)
        self.passwordC.grid(row=8, column=3,padx=10)

        ttk.Label(frame, text="License No", style='mainBgText.TLabel').grid(row=9, column=1,pady=10)
        ttk.Label(frame, text="Vehicle No", style='mainBgText.TLabel').grid(row=9, column=2,pady=10)
        ttk.Label(frame, text="Vehicle Type", style='mainBgText.TLabel').grid(row=9, column=3,pady=10)
        self.licenceNo = ttk.Entry(frame)
        self.vehicleNO = ttk.Entry(frame)
        self.licenceNo.grid(row=10, column=1,padx=10)
        self.vehicleNO.grid(row=10, column=2,padx=10)
        self.vehicleType = StringVar(value='')
        vehicles = ['MINICAB', 'COMFORT CAB', 'MULTI-PURPOSE VEHICLE']
        ttk.Combobox(frame, textvariable=self.vehicleType, state='readonly', values=vehicles).grid(row=10, column=3, padx=10)


        ttk.Label(frame, text="Vehicle Description", style='mainBgText.TLabel').grid(row=11, column=1,pady=10)
        ttk.Label(frame, text="Status", style='mainBgText.TLabel').grid(row=11, column=3,pady=10)
        self.vehicleDesc = Text(frame, height=5, width=40)
        self.vehicleDesc.grid(row=12, column=1, columnspan=2, padx=10)
        self.status = StringVar(value='')
        statuses = ['AVAILABLE', 'BUSY', 'OFFLINE']
        ttk.Combobox(frame, textvariable=self.status, values=statuses, state='readonly').grid(row=12, column=3, padx=10)


        ttk.Button(frame, text='Continue', command=self.check).grid(row=13, column= 2)

        ttk.Button(frame, text ="Login Page", command = self.lower).grid(row = 13, column = 1, padx = 10, pady = 10)  
    
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
        
        licenceNo = self.licenceNo.get()
        if licenceNo == '':
            messagebox.showerror('Incomplete data', 'Licence no. can not be empty')
            return
        
        vehicleNo = self.vehicleNO.get()
        if vehicleNo == '':
            messagebox.showerror('Incomplete data', 'Vehicle no. can not be empty')
            return
        
        vehicleType = self.vehicleType.get()
        if vehicleType == '':
            messagebox.showerror('Incomplete data', 'Vehicle type can not be empty')
            return
        
        vehicleDes = self.vehicleDesc.get('1.0', 'end')
        status = self.status.get()
        if status == '':
            messagebox.showerror('Incomplete data', 'Status can not be empty')
            return
        data = [userName, password, fullName,  phone, email, address, licenceNo, vehicleNo, vehicleType, vehicleDes, status]
        self.store(data)


    def store(self, data):
        data = REGISTER + data
        self.root.send_to_server(data)
        self.res = self.root.recive_from_server()
        if self.res == 'Sucess':
            messagebox.showinfo('Successfull', 'Account created, go to login page')       
        else:
            messagebox.showerror('Error', self.res)


        
    