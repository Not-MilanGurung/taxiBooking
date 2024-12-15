from tkinter import ttk, N,E,S,W, Tk, StringVar, IntVar, messagebox
from tkcalendar import Calendar
from datetime import date, timedelta, datetime, time
from threading import Thread

BOOK = 'BOOK'
CURRENT_RIDE = 'CURRENT_RIDE'
HISTORY = 'HISTORY'

class SideNavigationMenu(ttk.Frame):

    def __init__(self, parent, root):


        super().__init__(parent, style='SideBar.TFrame')

        ttk.Label(self, text=f'Welcome ', width=20, justify='center').grid(row=0, column=0, sticky='ew', pady=(40,20), padx=10)
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
        self.root = root
        self.parent = parent
        super().__init__(parent, style='MainBar.TFrame')
        ttk.Label(self, text='Booking').grid(row=0, column=0, sticky='')

        pickup =ttk.Label(self, style='Secondary_Frame.TLabel')
        pickup.grid(row=1, column=0, sticky='ew', padx=20, pady=20, ipady=10)
        pickup.rowconfigure(0, weight=1)
        ttk.Label(pickup, text='Pickup Location', style='Secondary_Frame.TLabel').grid(row=0, column=0, padx=20)
        self.pickup = StringVar()
        ttk.Entry(pickup, textvariable=self.pickup).grid(row=0, column=1, padx=20)

        dropoff = ttk.Label(self, style='Secondary_Frame.TLabel')
        dropoff.grid(row=2, column=0, sticky='ew', padx=20, pady=20, ipady=10)
        dropoff.rowconfigure(0, weight=1)
        ttk.Label(dropoff, text='Dropoff Location',style='Secondary_Frame.TLabel').grid(row=0, column=0, padx=20, sticky='we')
        self.dropoff = StringVar()
        ttk.Entry(dropoff, textvariable=self.dropoff).grid(row=0, column=1, padx=20, sticky='we')

        dateLabel = ttk.Label(self, style='Secondary_Frame.TLabel')
        dateLabel.grid(row=1, column=1, rowspan=3, sticky='ew', padx=20, pady=20, ipady=10, ipadx=10)
        dateLabel.rowconfigure((0,1), weight=1)
        dateLabel.columnconfigure(0, weight=1)
        ttk.Label(dateLabel, text='Date', style='Secondary_Frame.TLabel').grid(row=0, column=0, padx=20, pady=10, sticky='we')
        self.cal = Calendar(dateLabel, mindate=date.today(), maxdate=(date.today()+ timedelta(days=30)))
        self.cal.grid(row=1, column=0)

        timeLabel = ttk.Label(self, style='Secondary_Frame.TLabel')
        timeLabel.grid(row=3, column=0, padx=20, pady = 20, sticky='we', ipadx=20, ipady=20)
        timeLabel.rowconfigure((0,1), weight=1)
        timeLabel.columnconfigure((0,1), weight=1)
        ttk.Label(timeLabel, text='Hour', style='Secondary_Frame.TLabel').grid(row=0, column=0, padx=20)
        self.timeHour = IntVar(value=datetime.now().time().hour)
        ttk.Spinbox(timeLabel, from_=0, to=23, textvariable=self.timeHour).grid(row=0, column=1, padx=20)
        ttk.Label(timeLabel, text='Minuate', style='Secondary_Frame.TLabel').grid(row=1, column=0, padx=20)
        self.timeMin = IntVar(value=datetime.now().time().minute)
        ttk.Spinbox(timeLabel, from_=0, to=59, textvariable=self.timeMin).grid(row=1, column=1, padx=20)

        ttk.Button(self, command=self.book, text='Book').grid(row=5, column=0, columnspan=2)
    

    def book(self):
        pickup = self.pickup.get()
        if pickup == '':
            messagebox.showerror('Incomplete Data', 'Pickup location can not be empty')
            return
        dropoff = self.dropoff.get()
        if dropoff == '':
            messagebox.showerror('Incomplete Data', 'Pickup location can not be empty')
            return
        date = self.cal.get_date()
        date = date.split('/')
        date = f'20{date[2]}-{date[0]}-{date[1]}'

        hour = self.timeHour.get()
        min = self.timeMin.get()
        time = f'{hour}:{min}:00'
        self.res = ['Did not recive any data',]

        data = [BOOK, pickup, dropoff, date, time]
        self.root.send_to_server(data)
        thread = Thread(target=self.recive_thread)
        thread.start()

    def recive_thread(self):
        self.res = self.root.recive_from_server()
        self.recive()

    def recive(self):
        if self.res[0] == 'Sucess':
            messagebox.showinfo('Sucessful','Booked sucessfully')
            self.parent.starting_data_current()
        else:
            messagebox.showerror('Error', self.res[0])


        

class CurrentRide(ttk.Frame):
    def __init__(self, parent, root):
        super().__init__(parent, style='MainBar.TFrame')
        ttk.Label(self, text='Current Ride').grid(row=0, column=0, sticky='')
        self.root = root

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

        driverDetail = ttk.Label(self, style='Secondary_Frame.TLabel')
        driverDetail.grid(row=2, column=0, sticky='ew', padx=20, pady=20, ipady=20)
        driverDetail.rowconfigure((0,1), weight=1)
        driverDetail.columnconfigure(1, minsize=200)
        
        ttk.Label(driverDetail, text="Driver's Name:",style='Secondary_Frame.TLabel').grid(row=0, column=0, padx=20)
        self.driverName = StringVar()
        ttk.Label(driverDetail, textvariable=self.driverName, style='Secondary_Frame.TLabel').grid(row=0, column=1, padx=20)

        ttk.Label(driverDetail, text='Phone Number: ',style='Secondary_Frame.TLabel').grid(row=1, column=0, padx=20)
        self.driverPhone = StringVar()
        ttk.Label(driverDetail, textvariable=self.driverPhone, style='Secondary_Frame.TLabel').grid(row=1, column=1, padx=20)

        ttk.Button(driverDetail, text='Cancel', command=self.cancel).grid(row=2, column=1, pady=20)
        ttk.Button(driverDetail, text='Refresh', command=parent.starting_data_current).grid(row=2, column=2, pady=20)

    def cancel(self):
        res = messagebox.askquestion('Cancel', 'Do you want to cancel the booking?')
        if res == 'yes':
            self.root.send_to_server(['CANCEL',None])
            thread = Thread(target=self.recive_thread)
            thread.start()

    # The thread that awaits for server's reply 
    def recive_thread(self):
        self.ans = self.root.recive_from_server()
        self.recive()
    
    # Method after reciving a reply from the server
    def recive(self):
        if self.ans == 'CANCELLED':
            messagebox.showinfo('Cancelled', 'Booking cancelled') 
            # Clearing the labels
            self.date.set('')   
            self.pickup.set('')   
            self.dropoff.set('')   
            self.time.set('')   
            self.driverPhone.set('')   
            self.driverName.set('') 
        else:
            messagebox.showerror('Error', self.ans)  


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
        self.tree.heading(0, text='Driver Name')

        self.tree.heading(1, text='Pickup Location')
        self.tree.heading(2, text='Dropoff Location')

        self.tree.heading(3, text='Date')
        self.tree.column(3, width=80)

        self.tree.heading(4, text='Time')
        self.tree.column(4, width=60)

        self.tree.heading(5, text='Status')
        self.tree.column(5, width=150)

    def get_data(self):
        self.tree.delete(*self.tree.get_children())
        self.root.send_to_server([HISTORY,None])
        thread = Thread(target=self.recive_thread)
        thread.start()

    def recive_thread(self):
        self.res = self.root.recive_from_server()
        self.recive()
    
    def recive(self):
        if self.res[0] == HISTORY:
            for row in self.res[1:]:
                self.tree.insert('', 'end', values=row)

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

       



class Customer(ttk.Frame):

    def __init__(self, mainframe, root):


        ttk.Frame.__init__(self, mainframe)

        self.columnconfigure(1, weight=1,minsize=500)
        self.rowconfigure(0, weight=1)
        self.root = root


        side_navigation = SideNavigationMenu(self, root)
        side_navigation.grid(row=0,column=0, sticky='nsew', padx=(20,0), pady=20)

        self.booking = Booking(self, root)
        self.booking.grid(row=0, column=1, sticky='nsew', padx=(0, 20), pady=20)


        self.rideHistory = RideHistory(self, root)
        self.rideHistory.grid(row=0, column=1, sticky='nsew', padx=(0, 20), pady=20)

        self.profile = Profile(self, root)
        self.profile.grid(row=0, column=1, sticky='nsew', padx=(0, 20), pady=20)

        self.currentRide = CurrentRide(self, root)
        self.currentRide.grid(row=0, column=1, sticky='nsew', padx=(0, 20), pady=20)
        self.booking.tkraise()
        self.starting_data_profile()
        self.starting_data_current()

    
    def show_page(self, pageName):
        self.__dict__[pageName].tkraise()

    def recive_thread_current(self):
        self.res = self.root.recive_from_server()
        self.recive_current()

    def starting_data_current(self):
        self.res = ['No data recived',]
        self.root.send_to_server([CURRENT_RIDE, None])
        thread = Thread(target=self.recive_thread_current)
        thread.start()

    def recive_current(self):
        current = self.res
        if current[0] == CURRENT_RIDE and current[1] is not None:
            self.currentRide.__dict__['pickup'].set(current[1]) 
            self.currentRide.__dict__['dropoff'].set(current[2]) 
            self.currentRide.__dict__['date'].set(current[3]) 
            self.currentRide.__dict__['time'].set(current[4]) 
            try:
                self.currentRide.__dict__['driverName'].set(current[5])
                self.currentRide.__dict__['driverPhone'].set(current[6])
            except:
                pass
        else: 
            self.currentRide.__dict__['pickup'].set("") 
            self.currentRide.__dict__['dropoff'].set('') 
            self.currentRide.__dict__['date'].set('') 
            self.currentRide.__dict__['time'].set('') 
            self.currentRide.__dict__['driverName'].set('')
            self.currentRide.__dict__['driverPhone'].set('')


    def starting_data_profile(self):
        self.res = ['No data recived']
    
        profile = self.root.recive_from_server()
        self.profile.__dict__['name'].set(profile[2])
        self.profile.__dict__['address'].set(profile[5])
        self.profile.__dict__['email'].set(profile[4])
        self.profile.__dict__['phone'].set(profile[3])



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