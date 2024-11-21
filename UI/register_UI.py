import tkinter as tk
from Database.login_register_user import personal_detail, account

class Register(tk.Frame):
    
    def check(self):
        fullName = " ".join((self.fname.get(),self.mname.get(), self.lname.get()))
        res = personal_detail( fullName, self.address.get(), self.phone.get(), self.email.get())
        
        if type(res) != tuple : 
            tk.Message(self, test=res).grid(row=8, column=2)
        else: 
            self.controller.show_frame(Page=Account(self.parent, self.controller, res))
     
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        text = tk.Label(self, text="Register", font="TimesNewRoman 28")
        text.grid(row=0, column=2,pady=10)
        self.controller = controller
        self.parent= parent

        fL = tk.Label(self, text="First Name", font='TimesNewRoman')
        fL.grid(row=1, column=1,pady=10, padx=10)
        mL = tk.Label(self, text="Middle Name", font='TimesNewRoman')
        mL.grid(row=1, column=2,padx=10, pady=10)
        lL = tk.Label(self, text="Last Name", font='TimesNewRoman')
        lL.grid(row=1, column=3,padx=10,pady=10)
        self.fname = tk.Entry(self)
        self.mname = tk.Entry(self)
        self.lname = tk.Entry(self)
        self.fname.grid(row=2, column=1,padx=10)
        self.mname.grid(row=2, column=2,padx=10)
        self.lname.grid(row=2, column=3,padx=10)

        phoneL = tk.Label(self, text="Phone Number", font='TimesNewRoman')
        phoneL.grid(row=3, column=1,pady=10)
        emailL = tk.Label(self, text="Email", font='TimesNewRoman')
        emailL.grid(row=3, column=3,pady=10)
        self.phone = tk.Entry(self)
        self.email = tk.Entry(self)
        self.phone.grid(row=4, column=1,padx=10)
        self.email.grid(row=4, column=3,padx=10)

        addL = tk.Label(self, text="Address", font='TimesNewRoman')
        addL.grid(row=5, column=1,pady=10)
        self.address = tk.Entry(self)
        self.address.grid(row=6, column=1,padx=10)
        # tk.Label(self, text='Gender', font='TimesNewRoman').grid(row=9, column=1,pady=10)
        # radioMale = tk.Radiobutton(self, text='Male', value='male')
        # radioMale.grid(row=9, column=2)
        # radioFemale = tk.Radiobutton(self, text='Female', value='female')
        # radioFemale.grid(row=9, column=3)


        detail = tk.Button(self, text='Continue', command=self.check)
        detail.grid(row=7, column= 2)

        button1 = tk.Button(self, text ="StartPage", command = lambda : controller.show_frame(cont= 'StartPage'))
        button1.grid(row = 7, column = 1, padx = 10, pady = 10)  
        res = (0,0)
        button2 = tk.Button(self, text='test', command= lambda: controller.show_frame(Page=Account(self.parent, self.controller, res)))
        button2.grid(row = 7, column=3)



class Account(tk.Frame):
    def store(self):
        res = account(self.userName.get(), self.password.get(),self.personal)
        tk.Message(self,text=res).grid(row=3, column=2)        


    def __init__(self, parent, controller, personal: tuple):

        tk.Frame.__init__(self, parent)    
        self.controller = controller
        self.personal = personal
        userL = tk.Label(self, text="User Name", font='TimesNewRoman')
        userL.grid(row=1, column=1,pady=10)
        passL= tk.Label(self, text="Password", font='TimesNewRoman')
        passL.grid(row=1, column=3,pady=10)
        self.userName = tk.Entry(self)
        self.password = tk.Entry(self, show='*')
        self.userName.grid(row=2, column=1,padx=10)
        self.password.grid(row=2, column=3,padx=10)

        store = tk.Button(self, text='Continue', command=self.store)
        store.grid(row=3, column= 2)

        back = tk.Button(self, text='Start Page', command=self.gotoStart)
        back.grid(row=4, column= 2)

    def gotoStart(self):
        self.destroy()
        return self.controller.show_frame(cont = 'StartPage')
        # print('destroied')
        
    