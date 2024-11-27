from tkinter import ttk, N,E,S,W, Tk



class SideNavigationMenu(ttk.Frame):

    def __init__(self, parent, root):


        super().__init__(parent, style='SideBar.TFrame')

        ttk.Label(self, text=f'Welcome {parent.username}', width=20, justify='center').grid(row=0, column=0, sticky='ew', pady=(40,20), padx=10)
        book = ttk.Button(self, text='Book a ride', command=lambda :parent.show_page('booking'))
        book.grid(row=1, sticky='ew', pady=20, padx=10)
        current = ttk.Button(self, text='Current ride', command=lambda :parent.show_page('currentRide'))
        current.grid(row=2, sticky='ew', pady=20, padx=10)
        history = ttk.Button(self, text='Ride history', command=lambda :parent.show_page('rideHistory'))
        history.grid(row=3, sticky='ew', pady=20, padx=10)
        profile = ttk.Button(self, text='Profile', command=lambda :parent.show_page('profile'))
        profile.grid(row=4, sticky='ew', pady=20, padx=10)
    

class Booking(ttk.Frame):
    def __init__(self, parent, root):
        super().__init__(parent, style='MainBar.TFrame')
        ttk.Label(self, text='Booking').grid(row=0, column=0, sticky='')

class CurrentRide(ttk.Frame):
    def __init__(self, parent, root):
        super().__init__(parent, style='MainBar.TFrame')
        ttk.Label(self, text='Current Ride').grid(row=0, column=0, sticky='')

class RideHistory(ttk.Frame):
    def __init__(self, parent, root):
        super().__init__(parent, style='MainBar.TFrame')
        ttk.Label(self, text='RideHistory').grid(row=0, column=0, sticky='')

class Profile(ttk.Frame):
    def __init__(self, parent, root):
        super().__init__(parent, style='MainBar.TFrame')
        self.columnconfigure(0, weight=1)
        ttk.Label(self, text='Profile').grid(row=0, column=0, sticky='')



class Customer(ttk.Frame):

    def __init__(self, mainframe, root, username):


        ttk.Frame.__init__(self, mainframe)
        self.username = username

        self.columnconfigure(1, weight=1,minsize=500)
        self.rowconfigure(0, weight=1)
        


        side_navigation = SideNavigationMenu(self, root)
        side_navigation.grid(row=0,column=0, sticky='nsew', padx=(20,0), pady=20)

        self.booking = Booking(self, root)
        self.booking.grid(row=0, column=1, sticky='nsew', padx=(0, 20), pady=20)

        self.currentRide = CurrentRide(self, root)
        self.currentRide.grid(row=0, column=1, sticky='nsew', padx=(0, 20), pady=20)

        self.rideHistory = RideHistory(self, root)
        self.rideHistory.grid(row=0, column=1, sticky='nsew', padx=(0, 20), pady=20)

        self.profile = Profile(self, root)
        self.profile.grid(row=0, column=1, sticky='nsew', padx=(0, 20), pady=20)

        self.booking.tkraise()
    
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

    test = Customer(mainframe, root, 'test')
    test.grid(row=0, column=0, sticky='nsew')

    root.mainloop()