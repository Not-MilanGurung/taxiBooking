from tkinter import ttk, N,E,S,W, Tk, StringVar, IntVar
from tkcalendar import Calendar
from datetime import date, timedelta, datetime




class SideNavigationMenu(ttk.Frame):

    def __init__(self, parent, root):


        super().__init__(parent, style='SideBar.TFrame')

        ttk.Label(self, text=f'Welcome {parent.username}', width=20, justify='center').grid(row=0, column=0, sticky='ew', pady=(40,20), padx=10)
        current = ttk.Button(self, text='Current ride', command=lambda :parent.show_page('currentRide'))
        current.grid(row=2, sticky='ew', pady=20, padx=10)
        history = ttk.Button(self, text='Ride history', command=lambda :parent.show_page('rideHistory'))
        history.grid(row=3, sticky='ew', pady=20, padx=10)
        profile = ttk.Button(self, text='Profile', command=lambda :parent.show_page('profile'))
        profile.grid(row=4, sticky='ew', pady=20, padx=10)
    

class CurrentRide(ttk.Frame):
    def __init__(self, parent, root):
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
        self.driverPhone = StringVar()
        ttk.Label(customerDetail, textvariable=self.driverPhone, style='Secondary_Frame.TLabel').grid(row=1, column=1, padx=20)

        # ttk.Label(time, text='Photo: ',style='Secondary_Frame.TLabel').grid(row=0, column=0, padx=20)
        # self.time = StringVar()
        # ttk.Label(time, textvariable=self.dropoff, style='Secondary_Frame.TLabel').grid(row=0, column=1, padx=20)

class RideHistory(ttk.Frame):
    def __init__(self, parent, root):
        super().__init__(parent, style='MainBar.TFrame')
        ttk.Label(self, text='RideHistory').grid(row=0, column=0, sticky='')
        columns= list(range(6))
        self.tree = ttk.Treeview(self, columns=columns, show='headings')
        self.tree.grid(row=3, column=0)
        self.treeInitlise()

        
    def treeInitlise(self):
        self.tree.heading(0, text='ID')
        self.tree.column(0, width=60)

        self.tree.heading(1, text='Pickup Location')
        self.tree.heading(2, text='Dropoff Location')

        self.tree.heading(3, text='Date')
        self.tree.column(3, width=80)

        self.tree.heading(4, text='Time')
        self.tree.column(4, width=60)

        self.tree.heading(5, text='Status')
        self.tree.column(5, width=60)
        #test
        data = (12, 'Kupondole', 'Hattiban', '11/11/24','13:45', 'Done')
        self.tree.insert('', 'end', values=data)

class Profile(ttk.Frame):
    def __init__(self, parent, root):
        super().__init__(parent, style='MainBar.TFrame')
        self.columnconfigure(0, weight=1)
        ttk.Label(self, text='Profile').grid(row=0, column=0, sticky='')

        personal= ttk.Label(self, style='Secondary_Frame.TLabel')
        personal.grid(row=1, column=0, sticky='ew', padx=20, pady=20, ipady=20)
        personal.rowconfigure((0,1,2,3), weight=1)
        personal.columnconfigure(1, minsize=200)
        # Name Labels
        ttk.Label(personal, text='Name: ', style='Secondary_Frame.TLabel').grid(row=0, column=0, padx=20)
        self.name = StringVar(value='Test')
        ttk.Label(personal, textvariable=self.name, style='Secondary_Frame.TLabel').grid(row=0, column=1, padx=20)
        # Address Labels
        ttk.Label(personal, text='Address:',style='Secondary_Frame.TLabel').grid(row=1, column=0, padx=20)
        self.address = StringVar(value='KTM')
        ttk.Label(personal, textvariable=self.address, style='Secondary_Frame.TLabel').grid(row=1, column=1, padx=20)
        # Email Labels
        ttk.Label(personal, text='Email:',style='Secondary_Frame.TLabel').grid(row=2, column=0, padx=20)
        self.email = StringVar(value='example@gmail.com')
        ttk.Label(personal, textvariable=self.email, style='Secondary_Frame.TLabel').grid(row=2, column=1, padx=20)
        # Phone Labels
        ttk.Label(personal, text='Phone No.: ',style='Secondary_Frame.TLabel').grid(row=3, column=0, padx=20)
        self.phone = StringVar(value=12345)
        ttk.Label(personal, textvariable=self.phone, style='Secondary_Frame.TLabel').grid(row=3, column=1, padx=20)

       



class Driver(ttk.Frame):

    def __init__(self, mainframe, root, username):


        ttk.Frame.__init__(self, mainframe)
        self.username = username

        self.columnconfigure(1, weight=1,minsize=500)
        self.rowconfigure(0, weight=1)
        


        side_navigation = SideNavigationMenu(self, root)
        side_navigation.grid(row=0,column=0, sticky='nsew', padx=(20,0), pady=20)

        self.currentRide = CurrentRide(self, root)
        self.currentRide.grid(row=0, column=1, sticky='nsew', padx=(0, 20), pady=20)

        self.rideHistory = RideHistory(self, root)
        self.rideHistory.grid(row=0, column=1, sticky='nsew', padx=(0, 20), pady=20)

        self.profile = Profile(self, root)
        self.profile.grid(row=0, column=1, sticky='nsew', padx=(0, 20), pady=20)

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