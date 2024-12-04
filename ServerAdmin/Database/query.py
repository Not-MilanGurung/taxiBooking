from sqlite3 import connect, Connection, IntegrityError


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

def login(user, msg_arr):
    table, idcolumn = select_table(user)
            
    if table == ' ':
        return 'Incorrect message'
    
    from hashlib import pbkdf2_hmac
    username = msg_arr[1]
    password = msg_arr[2]
    con = connect("file:Database/database.db?mode=ro", uri=True)
    cur = con.cursor()
    query = f"select {idcolumn}, Salt, Hash from {table} where Username = '{username}'"
    data = cur.execute(query).fetchone()
    con.close()
    if data is None:
        return 'UserName is not registered'
    
    id = data[0]
    salt = data[1]
    true_hash = data[2]
    hash = pbkdf2_hmac('sha256', password.encode() , salt, 10_000) 

    # Check if the hash matches
    if true_hash != hash:
        return 'Incorrect password'

    # Login if the requirements are met
    return id


def current_ride(user, id):
    table, idcolumn = select_table(user)

    con = connect("file:Database/database.db?mode=ro", uri=True)
    cur = con.cursor()

    res = cur.execute(f"SELECT PickupLocation, DropoffLocation, Date, Time, DriverID FROM bookings where {idcolumn} = {id} and Status NOT IN ('CANCELLED','COMPLETED')").fetchone()
    if res is None: return ['CURRENT_RIDE', None]

    out = [res[0], res[1], res[2], res[3]]
    if res[4] is not None:
        res = cur.execute(f'SELECT FullName, Phone, VehicleNo, VehicleType FROM drivers where DriverID = {res[4]}').fetchone()
        out += list(res)
    con.close()
    out = ['CURRENT_RIDE'] + out
    return out

def profile_info(user, id):
    table, idcolumn = select_table(user)
    con = connect("file:Database/database.db?mode=ro", uri=True)
    cur = con.cursor()

    res = cur.execute(f'SELECT Username, FullName, Phone, Email, Address FROM {table} where {idcolumn} = {id}').fetchone()
    con.close()
    res = ['PROFILE'] + list(res)
    return res

def register(user, msg_arr):
    table, idcolumn = select_table(user)
    con = connect("file:Database/database.db?mode=rw", uri=True)
    cur = con.cursor()
    res = cur.execute(f"SELECT * FROM {table} where Phone ='{msg_arr[4]}' ").fetchone()
    if res is not None:
        return 'The phone no. is already registered'
    
    res = cur.execute(f"SELECT * FROM {table} where Username ='{msg_arr[1]}' ").fetchone()

    if res is not None:
        return 'The username is taken.\nTry another one'
    
    username = msg_arr[1]
    from hashlib import pbkdf2_hmac
    from os import urandom

    salt = urandom(16)
    password = msg_arr[2]
    hash = pbkdf2_hmac('sha256', password.encode(), salt, 10_000)
    fullname = msg_arr[3]
    phone = msg_arr[4]
    email = msg_arr[5]
    address = msg_arr[6]
    try:
        query = f'INSERT INTO {table}(Username, Salt, Hash, FullName, Phone, Email, Address) VALUES(?,?,?,?,?,?,?)'
        cur.execute(query, (username, salt, hash, fullname, phone, email, address))
        con.commit()
        con.close()
        return 'Sucess'
    except IntegrityError as error :
        con.close()
        return error

def book(id, msg_arr):
    con = connect("file:Database/database.db?mode=rw", uri=True)
    cur = con.cursor()

    pickup = msg_arr[1]
    dropoff = msg_arr[2]
    date = msg_arr[3]
    time = msg_arr[4]

    query = "INSERT INTO bookings(CustomerID, PickupLocation, DropoffLocation, Date, Time, Status) VALUES(?,?,?,?,?,?)"
    res = cur.execute(f"SELECT BookingID FROM bookings WHERE CustomerID = {id} AND Status NOT IN ('CANCELLED','COMPLETED')").fetchone()
    if res is not None:
        return ['You have already booked a ride', None]
    try:
        cur.execute(query, (id, pickup, dropoff, date, time, 'REQUESTED'))
        con.commit()
        res = cur.execute(f"SELECT BookingID FROM bookings WHERE CustomerID = {id} AND Status = 'REQUESTED'").fetchone()
        con.close
        return ['Sucess', res[0]]
    except:
        con.close()
        return ['Could not book', None]
    
    finally:
        con.close()

def cancel_ride(user, id):
    con = connect("file:Database/database.db?mode=rw", uri=True)
    cur = con.cursor()

    cur.execute(f"UPDATE bookings SET status = 'CANCELLED' WHERE CustomerID = {id} AND Status NOT IN ('CANCELLED','COMPLETED')")
    con.commit()
    return 'CANCELLED'





