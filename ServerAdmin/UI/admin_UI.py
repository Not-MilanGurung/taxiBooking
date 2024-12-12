from tkinter import ttk, N,E,S,W, Tk, StringVar, messagebox
import Database.sqlite_mid as Query  




class SideNavigationMenu(ttk.Frame):

    def __init__(self, parent, root):


        super().__init__(parent, style='SideBar.TFrame')

        ttk.Label(self, text=f'Welcome {parent.username}', width=20, justify='center').grid(row=0, column=0, sticky='ew', pady=(40,20), padx=10)

        current = ttk.Button(self, text='Current Rides', command=lambda :parent.show_page('currentRide'))
        current.grid(row=2, sticky='ew', pady=20, padx=10)

        history = ttk.Button(self, text='Unassigined Rides', command=lambda :parent.show_page('unassiginedRide'))
        history.grid(row=3, sticky='ew', pady=20, padx=10)

        history = ttk.Button(self, text='Double Booked Rides', command=lambda :parent.show_page('doubleBookedRide'))
        history.grid(row=4, sticky='ew', pady=20, padx=10)

        profile = ttk.Button(self, text='Profile', command=lambda :parent.show_page('profile'))
        profile.grid(row=5, sticky='ew', pady=20, padx=10)
    


class CurrentRide(ttk.Frame):
    def __init__(self, parent, root):
        super().__init__(parent, style='MainBar.TFrame')

        ttk.Label(self, text='Current Ride').grid(row=0, column=0, sticky='')
        columns= list(range(7))
        self.tree = ttk.Treeview(self, columns=columns, show='headings', height=20, selectmode='browse')
        self.tree.grid(row=3, column=0)
        scrollbar = ttk.Scrollbar(self, orient='vertical', command=self.tree.yview)
        scrollbar.grid(row=3, column=1, sticky='ns')

        self.tree.configure(yscrollcommand= scrollbar.set)
        self.treeInitlise()
        self.refresh()
        ttk.Button(self, text='Refresh', command=self.refresh).grid(row=1, column=0)
        ttk.Button(self, text='Select', command=self.selection).grid(row=4, column=0)

        
    def treeInitlise(self):
        self.tree.heading(0, text='ID')
        self.tree.column(0, width=60)

        self.tree.heading(1, text='Pickup Location')
        self.tree.heading(2, text='Dropoff Location')

        self.tree.heading(3, text='Date')
        self.tree.column(3, width=80)

        self.tree.heading(4, text='Time')
        self.tree.column(4, width=60)

        self.tree.heading(5, text='CustomerID')
        self.tree.column(5, width=60)
        self.tree.heading(6, text='DriverID')
        self.tree.column(6, width=60)
        #test
    def refresh(self):
        self.tree.delete(*self.tree.get_children())
        cur = Query.current_rides()
        res = cur.fetchall()
        for data in res:

            self.tree.insert('', 'end', values=data)
    
    def selection(self):
        print(self.tree.selection())

class UnassiginedRide(ttk.Frame):
    def __init__(self, parent, root):
        self.parent = parent
        super().__init__(parent, style='MainBar.TFrame')
        ttk.Label(self, text='UnassiginedRide').grid(row=0, column=0, sticky='')

        columns= list(range(7))
        self.tree = ttk.Treeview(self, columns=columns, show='headings', height=20)
        self.tree.grid(row=3, column=0)
        scrollbar = ttk.Scrollbar(self, orient='vertical', command=self.tree.yview)
        scrollbar.grid(row=3, column=1, sticky='ns')

        self.tree.configure(yscrollcommand= scrollbar.set)
        self.treeInitlise()
        self.refresh()
        ttk.Button(self, text='Refresh', command=self.refresh).grid(row=1, column=0)
        ttk.Button(self, text='Select', command=self.select).grid(row=4, column=0)

        
    def treeInitlise(self):
        self.tree.heading(0, text='ID')
        self.tree.column(0, width=60)

        self.tree.heading(1, text='Pickup Location')
        self.tree.heading(2, text='Dropoff Location')

        self.tree.heading(3, text='Date')
        self.tree.column(3, width=80)

        self.tree.heading(4, text='Time')
        self.tree.column(4, width=60)

        self.tree.heading(5, text='CustomerID')
        self.tree.column(5, width=60)
        self.tree.heading(6, text='DriverID')
        self.tree.column(6, width=60)

    def refresh(self):
        self.tree.delete(*self.tree.get_children())
        cur = Query.unassigined_rides()
        res = cur.fetchall()
        for data in res:

            self.tree.insert('', 'end', values=data)
    
    def select(self):
        res = self.tree.selection()

        row = self.tree.item(res[0])
        record = row['values']
        selectionPage = self.parent.__dict__['select']
        selectionPage.__dict__['booking'] = record
        selectionPage.bookingGet()
        selectionPage.tkraise()

class SelectionPage(ttk.Frame):
    def __init__(self, parent, root):
        self.parent = parent
        super().__init__(parent, style='MainBar.TFrame')
        ttk.Label(self, text='Selected Booking').grid(row=0, column=0, sticky='')

        columns= list(range(7))
        self.tree = ttk.Treeview(self, columns=columns, show='headings', height=1)
        self.tree.grid(row=3, column=0, sticky='ew')
        self.treeInitlise()

        ttk.Button(self, text='Refresh', command=self.refresh).grid(row=4, column=0)

        columns= list(range(4))
        self.drivers = ttk.Treeview(self, columns=columns, show='headings', height=15, selectmode='browse')
        self.drivers.grid(row=5, column=0)
        
        scrollbar1 = ttk.Scrollbar(self, orient='vertical', command=self.drivers.yview)
        scrollbar1.grid(row=5, column=1, sticky='ns')

        self.drivers.configure(yscrollcommand= scrollbar1.set)

        # Placeholder value from booking
        self.booking = [0, 'Blank', 'Blank', 'XXXX-XX-XX', 'XX:XX:XX', 0, 0]
        self.bookingGet()
        self.driverListInitlise()
        self.refresh()

        ttk.Button(self, text='Assign', command=self.assign).grid(row=6, column=0)


    def bookingGet(self):
        self.tree.delete(*self.tree.get_children())
        self.tree.insert('', 'end', values=self.booking) 
    
    def assign(self):
        sel = self.drivers.selection()
        row = self.drivers.item(sel[0])
        record = row['values']
        res = Query.assign_driver(self.booking[0], record[0])
        if res == 'Assigined':
            messagebox.showinfo('Assigined', 'Driver was assigined')
            self.lower()
        else:
            messagebox.showerror('Error', 'Could not assign')
    
    def driverListInitlise(self):
        self.drivers.heading(0, text='Driver ID')
        self.drivers.heading(1, text='Driver Name')
        self.drivers.heading(2, text='Vehicle Type')
        self.drivers.heading(3, text='Status')

    def treeInitlise(self):
        self.tree.heading(0, text='ID')
        self.tree.column(0, width=60)

        self.tree.heading(1, text='Pickup Location')
        self.tree.heading(2, text='Dropoff Location')

        self.tree.heading(3, text='Date')
        self.tree.column(3, width=80)

        self.tree.heading(4, text='Time')
        self.tree.column(4, width=60)

        self.tree.heading(5, text='CustomerID')
        self.tree.column(5, width=60)
        self.tree.heading(6, text='DriverID')
        self.tree.column(6, width=60)

    def refresh(self):
        self.drivers.delete(*self.drivers.get_children())
        data = Query.driver_list()
        for row in data:
            self.drivers.insert('', 'end', values=row)
    



class DoubleBookedRides(ttk.Frame):
    def __init__(self, parent, root):
        super().__init__(parent, style='MainBar.TFrame')
        ttk.Label(self, text='Double Booked Rides').grid(row=0, column=0, sticky='')

        columns= list(range(7))
        self.tree = ttk.Treeview(self, columns=columns, show='headings', height=20, selectmode='browse')
        self.tree.grid(row=3, column=0)
        scrollbar = ttk.Scrollbar(self, orient='vertical', command=self.tree.yview)
        scrollbar.grid(row=3, column=1, sticky='ns')

        self.tree.configure(yscrollcommand= scrollbar.set)
        self.treeInitlise()
        self.refresh()
        ttk.Button(self, text='Refresh', command=self.refresh).grid(row=1, column=0)
        ttk.Button(self, text='Select', command=self.select).grid(row=4, column=0)

        
    def treeInitlise(self):
        self.tree.heading(0, text='ID')
        self.tree.column(0, width=60)

        self.tree.heading(1, text='Pickup Location')
        self.tree.heading(2, text='Dropoff Location')

        self.tree.heading(3, text='Date')
        self.tree.column(3, width=80)

        self.tree.heading(4, text='Time')
        self.tree.column(4, width=60)

        self.tree.heading(5, text='CustomerID')
        self.tree.column(5, width=60)
        self.tree.heading(6, text='DriverID')
        self.tree.column(6, width=60)

    def refresh(self):
        self.tree.delete(*self.tree.get_children())
        cur = Query.double_booked_rides()
        res = cur.fetchall()
        for data in res:

            self.tree.insert('', 'end', values=data)
            
    def select(self):
            res = self.tree.selection()

            row = self.tree.item(res[0])
            record = row['values']
            selectionPage = self.parent.__dict__['select']
            selectionPage.__dict__['booking'] = record
            selectionPage.bookingGet()
            selectionPage.tkraise()

class Profile(ttk.Frame):
    def __init__(self, parent, root):
        self.parent= parent
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
        # Email Labels
        ttk.Label(personal, text='Email:',style='Secondary_Frame.TLabel').grid(row=2, column=0, padx=20)
        self.email = StringVar()
        ttk.Label(personal, textvariable=self.email, style='Secondary_Frame.TLabel').grid(row=2, column=1, padx=20)
        # Phone Labels
        ttk.Label(personal, text='Phone No.: ',style='Secondary_Frame.TLabel').grid(row=3, column=0, padx=20)
        self.phone = StringVar()
        ttk.Label(personal, textvariable=self.phone, style='Secondary_Frame.TLabel').grid(row=3, column=1, padx=20)
        # Username Labels
        ttk.Label(personal, text='Username: ',style='Secondary_Frame.TLabel').grid(row=4, column=0, padx=20)
        self.username = StringVar()
        ttk.Label(personal, textvariable=self.username, style='Secondary_Frame.TLabel').grid(row=4, column=1, padx=20)
        self.get_info()

    def get_info(self):
        res = Query.profile(self.parent.__dict__['username'])
        
        self.username.set(res[0])
        self.name.set(res[1])
        self.phone.set(res[2])
        self.email.set(res[3])


class Admin(ttk.Frame):

    def __init__(self, mainframe, root, username):


        ttk.Frame.__init__(self, mainframe)
        self.username = username

        self.columnconfigure(1, weight=1,minsize=500)
        self.rowconfigure(0, weight=1)
        


        side_navigation = SideNavigationMenu(self, root)
        side_navigation.grid(row=0,column=0, sticky='nsew', padx=(20,0), pady=20)

        self.currentRide = CurrentRide(self, root)
        self.currentRide.grid(row=0, column=1, sticky='nsew', padx=(0, 20), pady=20)

        self.doubleBookedRide = DoubleBookedRides(self, root)
        self.doubleBookedRide.grid(row=0, column=1, sticky='nsew', padx=(0, 20), pady=20)

        self.unassiginedRide = UnassiginedRide(self, root)
        self.unassiginedRide.grid(row=0, column=1, sticky='nsew', padx=(0, 20), pady=20)

        self.profile = Profile(self, root)
        self.profile.grid(row=0, column=1, sticky='nsew', padx=(0, 20), pady=20)

        self.select = SelectionPage(self, root)
        self.select.grid(row=0, column=1, sticky='nsew', padx=(0, 20), pady=20)

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

    test = Admin(mainframe, root, 'test')
    test.grid(row=0, column=0, sticky='nsew')

    root.mainloop()