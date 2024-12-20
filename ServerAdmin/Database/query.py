from sqlite3 import connect, IntegrityError, OperationalError

# Selects the table according to the user
def select_table(user):
    table, idcolumn = ' ' , ' '

    match user:
        case 'CUSTOMER':
            table, idcolumn = 'customers' , 'CustomerID'
        case 'DRIVER':
            table, idcolumn = 'drivers' , 'DriverID'
        case 'ADMIN':
            table, idcolumn = 'admins' , 'AdminID'
    return table, idcolumn


def ride_history(user: str, id: int):
    table, idcolumn = select_table(user)
    con = connect("file:Database/database.db?mode=ro", uri=True)
    # Defining the table and column to get data from
    if table == 'customers': 
        opptable = 'drivers'
        oppidcolumn = 'DriverID'
    elif table == 'drivers': 
        opptable = 'customers'
        oppidcolumn = 'CustomerID'
    cur = con.cursor()
    # Gettign the information
    query = f'''SELECT {opptable}.FullName, bookings.PickupLocation, bookings.DropoffLocation, bookings.Date, bookings.Time, bookings.Status FROM {opptable} 
                JOIN bookings WHERE {opptable}.{oppidcolumn} = bookings.{oppidcolumn} AND bookings.{idcolumn} = {id} ORDER BY Date, Time'''
    res = cur.execute(query).fetchall()
    return ['HISTORY'] + res


def login(user, msg_arr):
    table, idcolumn = select_table(user)
    # Error handeling
    if table == ' ':
        return 'Incorrect message'
    # Password hashing module
    from hashlib import pbkdf2_hmac
    username = msg_arr[1]
    password = msg_arr[2]
    # Open database in readonly mode
    con = connect("file:Database/database.db?mode=ro", uri=True)
    cur = con.cursor()
    # Get the id, salt, hash from the table matching the username
    query = f"select {idcolumn}, Salt, Hash from {table} where Username = '{username}'"
    data = cur.execute(query).fetchone()
    con.close()
    # User not in database
    if data is None:
        return 'UserName is not registered'
    # Assigining the query results to variables
    id = data[0]
    salt = data[1]
    true_hash = data[2]
    # Hashing the input password
    hash = pbkdf2_hmac('sha256', password.encode() , salt, 10_000) 

    # Check if the hash matches
    if true_hash != hash:
        return 'Incorrect password'

    # Login if the requirements are met
    return id

def register(user, msg_arr):
    table, idcolumn = select_table(user)
    # Database in read and write mode
    con = connect("file:Database/database.db?mode=rw", uri=True)
    cur = con.cursor()
    # Checking if the phone is already registeried
    res = cur.execute(f"SELECT * FROM {table} where Phone ='{msg_arr[4]}' ").fetchone()
    if res is not None:
        return 'The phone no. is already registered'
    
    # Checking if the username is unique
    res = cur.execute(f"SELECT * FROM {table} where Username ='{msg_arr[1]}' ").fetchone()
    if res is not None:
        return 'The username is taken.\nTry another one'
    
    username = msg_arr[1]

    from hashlib import pbkdf2_hmac
    from os import urandom
    salt = urandom(16)  # Generating a salt
    password = msg_arr[2]
    hash = pbkdf2_hmac('sha256', password.encode(), salt, 10_000)   # Getting the hash from the password and salt

    fullname = msg_arr[3]
    phone = msg_arr[4]
    email = msg_arr[5]
    address = msg_arr[6]

    try:
        if table == 'drivers':
            licenseNo = msg_arr[7]
            vehicleNo = msg_arr[8]
            vehicleType = msg_arr[9]
            vehicleDes = msg_arr[10]
            status = msg_arr[11]
            # Storing the data into the table
            query = f'''INSERT INTO {table}(Username, Salt, Hash, FullName, Phone, Email, Address,
                        LicenceNo, VehicleNo, VehicleType, VehicleDes, Status) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)'''
            cur.execute(query, (username, salt, hash, fullname, phone, email, address, licenseNo,
                                vehicleNo, vehicleType, vehicleDes, status))
            con.commit()
            con.close()
            return 'Sucess'


        else:
            # Storing the data into the table
            query = f'INSERT INTO {table}(Username, Salt, Hash, FullName, Phone, Email, Address) VALUES(?,?,?,?,?,?,?)'
            cur.execute(query, (username, salt, hash, fullname, phone, email, address))
            con.commit()
            con.close()
            return 'Sucess'
    except IntegrityError as error :
        con.close()
        return error

def current_ride(user, id):
    table, idcolumn = select_table(user)
    column = 'FullName, Phone' # Column to get when a driver is assigined
    # Differenting between columns and table according to the user
    if idcolumn == 'CustomerID': 
        idget = 'DriverID'
        tableGet = 'drivers'
        column += ', VehicleNo, VehicleType'    # Extra column of driver whose data is given to the user
        status = ('ASSIGINED', 'ONGOING', 'REQUESTED')  # The rides classified as current ride for customer

    elif idcolumn == 'DriverID': 
        idget = 'CustomerID'
        tableGet = 'customers'
        status = ('ONGOING', 'PLACEHOLDER') # The rides classified as current ride for driver

    # Database in readonly mode
    con = connect("file:Database/database.db?mode=ro", uri=True)
    cur = con.cursor()
    # Get the booking details when no driver is assigined
    res = cur.execute(f"SELECT PickupLocation, DropoffLocation, Date, Time, {idget} FROM bookings where {idcolumn} = {id} and Status IN {status}").fetchone()

    if res is None: return ['CURRENT_RIDE', None]
    out = [res[0], res[1], res[2], res[3]]

    # Get the details when a driver is assigined
    if res[4] is not None:
        res = cur.execute(f'SELECT {column} FROM {tableGet} where {idget} = {res[4]}').fetchone()
        out += list(res)
    # Close database
    con.close()
    # Add keyword infront to declare the type of message
    out = ['CURRENT_RIDE'] + out
    return out


def assigined_rides_driver(user, id):
    # Using variables in case this functions needs to be modified
    idcolumn = 'DriverID'
    tableGet = 'customers'
    idget = 'CustomerID'
    tableGet = 'customers'
    # Database in readonly mode
    con = connect("file:Database/database.db?mode=ro", uri=True)
    cur = con.cursor()
    # Getting Customer's Name, Pickup and DropoffLocation, Date, Time, Status and BookingId of 
    # all the rides assigined to the driver of the input ID
    query = f'''SELECT {tableGet}.FullName, bookings.PickupLocation, bookings.DropoffLocation, bookings.Date, 
                bookings.Time, bookings.Status, bookings.BookingID FROM {tableGet} 
                JOIN bookings WHERE {tableGet}.{idget} = bookings.{idget} AND bookings.{idcolumn} = {id} AND bookings.Status = "ASSIGINED"
                ORDER BY Date, Time'''
    out = cur.execute(query).fetchall()
    con.close()
    # Keyword for identification
    out = ['ASSIGINED'] + out
    return out

def profile_info(user, id):
    table, idcolumn = select_table(user)
    # Database in readonly mode
    con = connect("file:Database/database.db?mode=ro", uri=True)
    cur = con.cursor()
    # Blank for customer
    status = ''

    res = cur.execute(f'SELECT Username, FullName, Phone, Email, Address FROM {table} where {idcolumn} = {id}').fetchone()
    # Status info for driver
    if idcolumn == 'DriverID':
        status = cur.execute(f'SELECT Status FROM drivers WHERE {idcolumn} = {id}').fetchone()
    con.close()

    res = ['PROFILE'] + list(res) + [status]
    return res


def book(id: int, msg_arr):
    # Database in read and write mode
    con = connect("file:Database/database.db?mode=rw", uri=True)
    cur = con.cursor()

    pickup = msg_arr[1]
    dropoff = msg_arr[2]
    date = msg_arr[3]
    time = msg_arr[4]

    # Checking if the customer has already booked a ride
    res = cur.execute(f"SELECT BookingID FROM bookings WHERE CustomerID = {id} AND Status NOT IN ('CANCELLED','COMPLETED')").fetchone()
    if res is not None:
        return ['You have already booked a ride', None]
    
    try:
        # Store the booking details
        query = "INSERT INTO bookings(CustomerID, PickupLocation, DropoffLocation, Date, Time, Status) VALUES(?,?,?,?,?,?)"
        cur.execute(query, (id, pickup, dropoff, date, time, 'REQUESTED'))
        con.commit()
        # Getting the booking id and returning it
        res = cur.execute(f"SELECT BookingID FROM bookings WHERE CustomerID = {id} AND Status = 'REQUESTED'").fetchone()
        con.close
        return ['Sucess', res[0]]
    except:
        con.close()
        return ['Could not book', None]

def cancel_ride(user, id):
    # Database in read and write mode
    con = connect("file:Database/database.db?mode=rw", uri=True)
    cur = con.cursor()
    # Set the booking as cancelled
    cur.execute(f"UPDATE bookings SET status = 'CANCELLED' WHERE CustomerID = {id} AND Status NOT IN ('CANCELLED','COMPLETED')")
    con.commit()
    return 'CANCELLED'

def complete_ride(user, id):
    try:
        # Database in read and write mode
        con = connect("file:Database/database.db?mode=rw", uri=True)
        cur = con.cursor()
        # Mark the Ongoing ride status as COMPLETED
        cur.execute(f"UPDATE bookings SET Status = 'COMPLETED' WHERE DriverID = {id} AND Status = 'ONGOING'")
        con.commit()
        return ['COMPLETED', None]
    except:
        return ['COMPLETED', 'Error occured']

# Update driver's status
def driver_status(id, status):
    try:
        # Database in read and write mode
        con = connect("file:Database/database.db?mode=rw", uri=True)
        cur = con.cursor()

        cur.execute(f"UPDATE drivers SET Status = '{status}' WHERE DriverID = {id}")
        con.commit()
        con.close()
        return ['DRIVER_STATUS', status]
    except:
        return ['DRIVER_STATUS', 'Error']

# Select a ride and set it's status to be ONGOING
def select_ride_driver(bookingID: int, id: int):
    try:
        # Open the database in read and write mode.
        con = connect("file:Database/database.db?mode=rw", uri=True)
        cur = con.cursor()

        res = cur.execute(f"SELECT * FROM bookings WHERE DriverID = {id} AND Status = 'ONGOING'").fetchone()
        if res is not None:
            return ['SELECT', 'You have already have an ongoing ride']
        # Change the status to ONGOING of the selected booking
        cur.execute(f"UPDATE bookings SET Status = 'ONGOING' WHERE BookingID = {bookingID} AND DriverID = {id}")
        con.commit()
        con.close()
        # Send back successful message
        return ['SELECT', None]
    except OperationalError as error:
        return ['SELECT', error]

def change_current_ride(id: int):
    try:
        # Open the database in read and write mode.
        con = connect("file:Database/database.db?mode=rw", uri=True)
        cur = con.cursor()
        # Change the status to ASSIGINED of the selected booking
        cur.execute(f"UPDATE bookings SET Status = 'ASSIGINED' WHERE Status = 'ONGOING' AND DriverID = {id}")
        con.commit()
        con.close()
        # Send back successful message
        return ['CHANGE', None]
    except OperationalError as error:
        return ['CHANGE', error]




