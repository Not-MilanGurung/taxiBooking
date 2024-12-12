from sqlite3 import connect, Connection
from hashlib import pbkdf2_hmac
from pathlib import Path

con = connect("Database/database.db")
cur = con.cursor()



def login(user_name: str, password: str):


    res = cur.execute(f"SELECT Salt, Hash  FROM admins WHERE Username = '{user_name}'")
    p = res.fetchone()
    if p is None:
        return 'UserName is not registered'

    hash = pbkdf2_hmac('sha256', password.encode() , p[0], 10_000) 

    # Check if the hash matches
    if p[1] != hash:
        return 'Incorrect password'

    
    # Login if the requirements are met
    return user_name


def current_rides():
    query = "SELECT BookingID, PickupLocation, DropoffLocation, Date, Time, CustomerID, DriverID FROM bookings WHERE Status NOT IN ('CANCELLED', 'COMPLETED') AND DriverID IS NOT NULL"
    res = cur.execute(query)
    return res

def unassigined_rides():
    query = "SELECT BookingID, PickupLocation, DropoffLocation, Date, Time, CustomerID, DriverID FROM bookings WHERE Status NOT IN ('CANCELLED', 'COMPLETED') AND DriverID IS NULL"
    res = cur.execute(query)
    return res

def double_booked_rides():
    query = "SELECT BookingID, PickupLocation, DropoffLocation, Date, Time, CustomerID, DriverID FROM bookings WHERE Status NOT IN ('CANCELLED', 'COMPLETED') GROUP BY DriverID HAVING COUNT(DriverID)>1"
    res = cur.execute(query)
    return res

def profile(username):
    query = f"SELECT Username, FullName, Phone, Email FROM admins WHERE Username = '{username}'"
    res = cur.execute(query).fetchone()
    return res

def driver_list():
    query = "SELECT DriverID, FullName, VehicleType, Status FROM drivers GROUP BY Status"
    res = cur.execute(query).fetchall()
    return res

def personal_detail( name , address: str, phone = 00,  email: str = '') :

    cur = con.cursor()

    query = f"SELECT phone from customer where phone={phone}"
    res = cur.execute(query)
    if res.fetchone() is not(None):
        return 'The phone is already registered. Try logging in or using a different phone'
    
    return (name, address, phone, email)

def assign_driver(bookingID, driverID):
    query = f"UPDATE bookings SET DriverID = {driverID} WHERE BookingID = {bookingID}"
    try:
        cur.execute(query)
        con.commit()
        return 'Assigined'
    except:
        return 'Error occured'


def close_connection():
    con.close()

if __name__ == '__main__':
    print(login('Server Admin', 'taxi booking'))