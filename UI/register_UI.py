from tkinter import ttk
from Database.login_register_user import personal_detail, account

class Register(ttk.Frame):
    
    def check(self):
        try:
            fullName = " ".join((self.fname.get(),self.mname.get(), self.lname.get()))
            res = personal_detail( fullName, self.address.get(), self.phone.get(), self.email.get())
            
            if type(res) != tuple : 
                ttk.Message(self, test=res).grid(row=8, column=2)
            else: 
                self.root.show_frame(Page=Account(self.mainframe, self.root, res))
        except ValueError:
            pass
     
    def __init__(self, mainframe, root):

        ttk.Frame.__init__(self, mainframe)
        self.rowconfigure([0,1,2,3,4,5,6,7], weight=1)
        self.columnconfigure([0,1,2,3], weight=1)

        text = ttk.Label(self, text="Register", font="TimesNewRoman 28")
        
        text.grid(row=0, column=2,pady=10)
        self.root = root
        self.mainframe= mainframe

        fL = ttk.Label(self, text="First Name", font='TimesNewRoman')
        fL.grid(row=1, column=1,pady=10, padx=10)
        mL = ttk.Label(self, text="Middle Name", font='TimesNewRoman')
        mL.grid(row=1, column=2,padx=10, pady=10)
        lL = ttk.Label(self, text="Last Name", font='TimesNewRoman')
        lL.grid(row=1, column=3,padx=10,pady=10)
        self.fname = ttk.Entry(self)
        self.mname = ttk.Entry(self)
        self.lname = ttk.Entry(self)
        self.fname.grid(row=2, column=1,padx=10)
        self.mname.grid(row=2, column=2,padx=10)
        self.lname.grid(row=2, column=3,padx=10)

        phoneL = ttk.Label(self, text="Phone Number", font='TimesNewRoman')
        phoneL.grid(row=3, column=1,pady=10)
        emailL = ttk.Label(self, text="Email", font='TimesNewRoman')
        emailL.grid(row=3, column=3,pady=10)
        self.phone = ttk.Entry(self)
        self.email = ttk.Entry(self)
        self.phone.grid(row=4, column=1,padx=10)
        self.email.grid(row=4, column=3,padx=10)

        addL = ttk.Label(self, text="Address", font='TimesNewRoman')
        addL.grid(row=5, column=1,pady=10)
        self.address = ttk.Entry(self)
        self.address.grid(row=6, column=1,padx=10)
        # ttk.Label(self, text='Gender', font='TimesNewRoman').grid(row=9, column=1,pady=10)
        # radioMale = ttk.Radiobutton(self, text='Male', value='male')
        # radioMale.grid(row=9, column=2)
        # radioFemale = ttk.Radiobutton(self, text='Female', value='female')
        # radioFemale.grid(row=9, column=3)


        detail = ttk.Button(self, text='Continue', command=self.check)
        detail.grid(row=7, column= 2)

        button1 = ttk.Button(self, text ="StartPage", command = lambda : root.show_frame(cont= 'StartPage'))
        button1.grid(row = 7, column = 1, padx = 10, pady = 10)  
        res = (0,0)
        button2 = ttk.Button(self, text='test', command= lambda: root.show_frame(Page=Account(self.mainframe, self.root, res)))
        button2.grid(row = 7, column=3)



class Account(ttk.Frame):
    def store(self):
        try:
            res = account(self.userName.get(), self.password.get(),self.personal)
            ttk.Message(self,text=res).grid(row=3, column=2)        
        except ValueError:
            pass

    def __init__(self, mainframe, root, personal: tuple):

        ttk.Frame.__init__(self, mainframe) 

        self.root = root
        self.personal = personal

        self.columnconfigure([0,1,2,3], weight=1)
        self.rowconfigure([0,1,2,3,4], weight=1)
        userL = ttk.Label(self, text="User Name", font='TimesNewRoman')
        userL.grid(row=1, column=1,pady=10)
        passL= ttk.Label(self, text="Password", font='TimesNewRoman')
        passL.grid(row=1, column=3,pady=10)
        self.userName = ttk.Entry(self)
        self.password = ttk.Entry(self, show='*')
        self.userName.grid(row=2, column=1,padx=10)
        self.password.grid(row=2, column=3,padx=10)

        store = ttk.Button(self, text='Continue', command=self.store)
        store.grid(row=3, column= 2)

        back = ttk.Button(self, text='Start Page', command=self.gotoStart)
        back.grid(row=4, column= 2)

    def gotoStart(self):
        self.destroy()
        return self.root.show_frame(cont = 'StartPage')
        # print('destroied')
        
    