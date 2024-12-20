from tkinter import ttk, N,E,S,W, Tk, StringVar, messagebox

CURRENT_RIDE = 'CURRENT_RIDE'
PROFILE = 'PROFILE'
HISTORY = 'HISTORY'
ASSIGINED = 'ASSIGINED'

class SideNavigationMenu(ttk.Frame):

    def __init__(self, parent, root):

        self.root = root
        super().__init__(parent, style='SideBar.TFrame')

        ttk.Label(self, text=f'Welcome {parent.username}', width=20, justify='center').grid(row=0, column=0, sticky='ew', pady=(40,20), padx=10)
        current = ttk.Button(self, text='Current ride', command=lambda :parent.show_page('currentRide'))
        current.grid(row=2, sticky='ew', pady=20, padx=10)
        current = ttk.Button(self, text='Assigined Rides', command=lambda :parent.show_page('assiginedRides'))
        current.grid(row=3, sticky='ew', pady=20, padx=10)
        history = ttk.Button(self, text='Ride history', command=lambda :parent.show_page('rideHistory'))
        history.grid(row=4, sticky='ew', pady=20, padx=10)
        profile = ttk.Button(self, text='Profile', command=lambda :parent.show_page('profile'))
        profile.grid(row=5, sticky='ew', pady=20, padx=10)

        self.cur_status = StringVar()
        statuses = ['AVAILABLE', 'BUSY', 'OFFLINE']
        self.status = ttk.Combobox(self, textvariable=self.cur_status, values=statuses, state='readonly')
        self.status.grid(row=6, sticky='ew', pady=20, padx=10)

        self.status.bind('<<ComboboxSelected>>', func=self.status_update)
    
    
    def status_update(self, event):
        cur_status = self.cur_status.get()
        self.root.send_to_server(['DRIVER_STATUS', cur_status])
        res = self.root.recive_from_server()
        self.recive(res)
            

    def recive(self, res):
        if res[0] == 'DRIVER_STATUS':
            match res[1]:
                case 'AVAILABLE':
                    i =  0
                case 'BUSY':
                    i =  1
                case 'OFFLINE':
                    i = 2
                case _:
                    i = -1
            self.status.current(newindex=i)
            messagebox.showinfo('Status set', f'Status set to {res[1]}')


    

class CurrentRide(ttk.Frame):
    def __init__(self, parent, root):
        self.root = root
        super().__init__(parent, style='MainBar.TFrame')
        ttk.Label(self, text='Current Ride').grid(row=0, column=0, sticky='')

        pickup= ttk.Label(self, style='Secondary_Frame.TLabel')
        pickup.grid(row=1, column=0, sticky='ew', padx=20, pady=20, ipady=20)
        pickup.rowconfigure((0,1), weight=1)
        pickup.columnconfigure(1, minsize=200)
        ttk.Label(pickup, text='Pickup Location: ', style='Secondary_Frame.TLabel').grid(row=0, column=0, padx=20)
        self.pickup = StringVar(value='')
        ttk.Label(pickup, textvariable=self.pickup, style='Secondary_Frame.TLabel').grid(row=0, column=1, padx=20)
        ttk.Label(pickup, text='Dropoff Location:',style='Secondary_Frame.TLabel').grid(row=1, column=0, padx=20)
        self.dropoff = StringVar()
        ttk.Label(pickup, textvariable=self.dropoff, style='Secondary_Frame.TLabel').grid(row=1, column=1, padx=20)
        
        date = ttk.Label(self, style='Secondary_Frame.TLabel')
        date.grid(row=1, column=1, sticky='ew', padx=20, pady=20, ipady=20)
        date.rowconfigure((0,1), weight=1)
        date.columnconfigure(1, minsize=50)
        ttk.Label(date, text='Date:',style='Secondary_Frame.TLabel').grid(row=0, column=0, padx=20)
        self.date = StringVar()
        ttk.Label(date, textvariable=self.date, style='Secondary_Frame.TLabel').grid(row=0, column=1, padx=20)
        ttk.Label(date, text='Time: ',style='Secondary_Frame.TLabel').grid(row=1, column=0, padx=20)
        self.time = StringVar()
        ttk.Label(date, textvariable=self.time, style='Secondary_Frame.TLabel').grid(row=1, column=1, padx=20)

        customerDetail = ttk.Label(self, style='Secondary_Frame.TLabel')
        customerDetail.grid(row=2, column=0, sticky='ew', padx=20, pady=20, ipady=20)
        customerDetail.rowconfigure((0,1), weight=1)
        customerDetail.columnconfigure(1, minsize=200)
        
        ttk.Label(customerDetail, text="Customer's Name:",style='Secondary_Frame.TLabel').grid(row=0, column=0, padx=20)
        self.customerName = StringVar()
        ttk.Label(customerDetail, textvariable=self.customerName, style='Secondary_Frame.TLabel').grid(row=0, column=1, padx=20)

        ttk.Label(customerDetail, text='Phone Number: ',style='Secondary_Frame.TLabel').grid(row=1, column=0, padx=20)
        self.customerPhone = StringVar()
        ttk.Label(customerDetail, textvariable=self.customerPhone, style='Secondary_Frame.TLabel').grid(row=1, column=1, padx=20)
        
        self.get_info()

        ttk.Button(self, text='Refresh', command=self.get_info).grid(row=3, padx=20, pady=20)
        ttk.Button(self, text='Mark completed', command=self.complete).grid(row=3, column=1, padx=20, pady=20)
        ttk.Button(self, text='Change Ride', command=self.change).grid(row=4, column=0, padx=20, pady=20)
        
    def complete(self):
        yn = messagebox.askquestion('Confirm', 'Do you want to mark the ride completed')
        if yn == 'yes':
            self.root.send_to_server(['COMPLETED',None])
            res = self.root.recive_from_server()
            if res[0] == 'COMPLETED':
                if res[1] is None:
                    self.get_info()
                    messagebox.showinfo('Success', 'Completed the ride')
                else:
                    messagebox.showerror('Error', res[1])
            
    def change(self):
        yn = messagebox.askquestion('Confirm', 'Do you want to change the current ride')
        if yn == 'yes':
            self.root.send_to_server(['CHANGE',None])
            res = self.root.recive_from_server()
            if res[0] == 'CHANGE':
                if res[1] is None:
                    self.get_info()
                    messagebox.showinfo('Success', 'Now you can select another assigined ride')
                else:
                    messagebox.showerror('Error', res[1])
            

    def get_info(self):
        self.res = [''] * 10
        self.root.send_to_server([CURRENT_RIDE, None])
        self.res = self.root.recive_from_server()
        self.recive()
    # Read then Load data after reciving from server
    def recive(self):

        if self.res[0] == 'CURRENT_RIDE':
            if self.res[1] is None:
                self.res = ['']*7
            self.pickup.set(self.res[1])
            self.dropoff.set(self.res[2])
            self.date.set(self.res[3])
            self.time.set(self.res[4])

            self.customerName.set(self.res[5])
            self.customerPhone.set(self.res[6])

class AssiginedRides(ttk.Frame):
    def __init__(self, parent, root):
        self.root = root
        super().__init__(parent, style='MainBar.TFrame')

        ttk.Label(self, text='Assigined Rides').grid(row=0, column=0, sticky='')
        # Assigined rides tree
        columns= list(range(7))
        self.tree = ttk.Treeview(self, columns=columns, show='headings', selectmode='browse')
        self.tree.grid(row=3, column=0)
        self.treeInitlise()

        scroll = ttk.Scrollbar(self, command=self.tree.yview)
        scroll.grid(row=3, column=1, sticky='ns')
        self.tree.configure(yscrollcommand=scroll.set)

        ttk.Button(self, text='Refreash', command=self.get_data).grid(row=1, column=0, pady = 20)
        ttk.Button(self, text='Select', command=self.select).grid(row=2, column=0, pady = 20)

        
    def treeInitlise(self):
        self.tree.heading(0, text='Customer Name')

        self.tree.heading(1, text='Pickup Location')
        self.tree.heading(2, text='Dropoff Location')

        self.tree.heading(3, text='Date')
        self.tree.column(3, width=80)

        self.tree.heading(4, text='Time')
        self.tree.column(4, width=60)

        self.tree.heading(5, text='Status')
        self.tree.column(5, width=150)

        self.tree.heading(6, text='ID')
        self.tree.column(6, width=20)

    def get_data(self):
        self.tree.delete(*self.tree.get_children())
        self.root.send_to_server([ASSIGINED,None])

        self.res = self.root.recive_from_server()
        self.recive()

    def select(self):
        sel = self.tree.selection()
        row = self.tree.item(sel[0])
        record = row['values']
        self.root.send_to_server(['SELECT',record[6]])
        res = self.root.recive_from_server()
        if res[0] == 'SELECT':
            if res[1] is None:
                self.get_data()
                messagebox.showinfo('Succesfully', 'Selected the ride to be the current ride')
            else:
                messagebox.showerror('Error', res[1])

    def recive(self):
        if self.res[0] == ASSIGINED:
            for row in self.res[1:]:
                self.tree.insert('', 'end', values=row)

class RideHistory(ttk.Frame):
    def __init__(self, parent, root):
        self.root = root
        super().__init__(parent, style='MainBar.TFrame')
        ttk.Label(self, text='RideHistory').grid(row=0, column=0, sticky='')
        # Ride history tree
        columns= list(range(6))
        self.tree = ttk.Treeview(self, columns=columns, show='headings', selectmode='browse')
        self.tree.grid(row=3, column=0)
        self.treeInitlise()

        scroll = ttk.Scrollbar(self, command=self.tree.yview)
        scroll.grid(row=3, column=1, sticky='ns')
        self.tree.configure(yscrollcommand=scroll.set)

        ttk.Button(self, text='Refreash', command=self.get_data).grid(row=1, column=0, pady = 20)

        
    def treeInitlise(self):
        self.tree.heading(0, text='Customer Name')

        self.tree.heading(1, text='Pickup Location')
        self.tree.heading(2, text='Dropoff Location')

        self.tree.heading(3, text='Date')
        self.tree.column(3, width=80)

        self.tree.heading(4, text='Time')
        self.tree.column(4, width=60)

        self.tree.heading(5, text='Status')
        self.tree.column(5, width=150)
        #test
    def get_data(self):
        self.tree.delete(*self.tree.get_children())
        self.root.send_to_server([HISTORY,None])

        self.res = self.root.recive_from_server()
        self.recive()
    
    def recive(self):

        if self.res[0] == HISTORY:
            for row in self.res[1:]:
                self.tree.insert('', 'end', values=row)

class Profile(ttk.Frame):
    def __init__(self, parent, root):
        self.root = root
        super().__init__(parent, style='MainBar.TFrame')
        self.columnconfigure(0, weight=1)
        ttk.Label(self, text='Profile').grid(row=0, column=0, sticky='')

        personal= ttk.Label(self, style='Secondary_Frame.TLabel')
        personal.grid(row=1, column=0, sticky='ew', padx=20, pady=20, ipady=20)
        personal.rowconfigure((0,1,2,3), weight=1)
        personal.columnconfigure(1, minsize=200)
        # Name Labels
        ttk.Label(personal, text='Name: ', style='Secondary_Frame.TLabel').grid(row=0, column=0, padx=20)
        self.name = StringVar()
        ttk.Label(personal, textvariable=self.name, style='Secondary_Frame.TLabel').grid(row=0, column=1, padx=20)
        # Address Labels
        ttk.Label(personal, text='Address:',style='Secondary_Frame.TLabel').grid(row=1, column=0, padx=20)
        self.address = StringVar()
        ttk.Label(personal, textvariable=self.address, style='Secondary_Frame.TLabel').grid(row=1, column=1, padx=20)
        # Email Labels
        ttk.Label(personal, text='Email:',style='Secondary_Frame.TLabel').grid(row=2, column=0, padx=20)
        self.email = StringVar()
        ttk.Label(personal, textvariable=self.email, style='Secondary_Frame.TLabel').grid(row=2, column=1, padx=20)
        # Phone Labels
        ttk.Label(personal, text='Phone No.: ',style='Secondary_Frame.TLabel').grid(row=3, column=0, padx=20)
        self.phone = StringVar()
        ttk.Label(personal, textvariable=self.phone, style='Secondary_Frame.TLabel').grid(row=3, column=1, padx=20)
        
        ttk.Label(personal, text='Status: ',style='Secondary_Frame.TLabel').grid(row=4, column=0, padx=20)
        self.status = StringVar()
        ttk.Label(personal, textvariable=self.status, style='Secondary_Frame.TLabel').grid(row=4, column=1, padx=20)
        self.get_info()

    def get_info(self):
        self.root.send_to_server(['PROFILE',None])
        res = self.root.recive_from_server()
        if res[0] == PROFILE:
            self.name.set(res[2])
            self.phone.set(res[3])
            self.email.set(res[4])
            self.address.set(res[5])
            self.status.set(res[6])
        else:
            messagebox.showerror('Error', 'Could not get profile info')



class Driver(ttk.Frame):

    def __init__(self, mainframe, root, username):


        ttk.Frame.__init__(self, mainframe)
        self.username = username

        self.columnconfigure(1, weight=1,minsize=500)
        self.rowconfigure(0, weight=1)
        


        side_navigation = SideNavigationMenu(self, root)
        side_navigation.grid(row=0,column=0, sticky='nsew', padx=(20,0), pady=20)

        self.profile = Profile(self, root)
        self.profile.grid(row=0, column=1, sticky='nsew', padx=(0, 20), pady=20)

        self.currentRide = CurrentRide(self, root)
        self.currentRide.grid(row=0, column=1, sticky='nsew', padx=(0, 20), pady=20)

        self.assiginedRides = AssiginedRides(self, root)
        self.assiginedRides.grid(row=0, column=1, sticky='nsew', padx=(0, 20), pady=20)

        self.rideHistory = RideHistory(self, root)
        self.rideHistory.grid(row=0, column=1, sticky='nsew', padx=(0, 20), pady=20)


        self.currentRide.tkraise()
    
    def show_page(self, pageName):
        self.__dict__[pageName].tkraise()



# For test purposes only
if __name__ == '__main__':
    from style import TaxiAppStyle

    root = Tk()
    style = TaxiAppStyle(root)

    mainframe = ttk.Frame(root)  
    mainframe.grid(column=0, row=0, sticky='nsew')

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    mainframe.columnconfigure(0, weight=1)
    mainframe.rowconfigure(0,weight=1)

    test = Driver(mainframe, root, 'test')
    test.grid(row=0, column=0, sticky='nsew')

    root.mainloop()