import sqlite3
from os import urandom
from hashlib import pbkdf2_hmac


con = sqlite3.connect("Database/database.db")
cur = con.cursor()

# table schema
query = ['create table customers ('
         ' CustomerID integer primary key autoincrement,' 
         ' Username varchar(255) not null unique,'
         ' Salt varbinary(16) not null,'
         ' Hash varbinary(32) not null,'
         ' FullName varchar(255) not null,'
         ' Phone int not null unique,'
         ' Email varchar(255) not null,'
         ' Address varchar(255) not null'
         ')',

         'create table drivers ('
         ' DriverID integer primary key autoincrement,' 
         ' Username varchar(255) not null unique,'
         ' Salt varbinary(16) not null,'
         ' Hash varbinary(32) not null,'
         ' FullName varchar(255) not null,'
         ' Phone int not null unique,'
         ' Email varchar(255) not null,'
         ' Address varchar(255) not null,'
         ' LicenceNo varchar(255) unique not null,'
         ' VehicleNo varchar(255) unique not null,'
         ' VehicleType varchar(50) not null,'
         ' VehicleDes varchar(255),'
         ' Status varchar(50) not null'
         ')',
         
         'create table admins ('
         ' AdminID integer primary key autoincrement,' 
         ' Username varchar(255) not null unique,'
         ' Salt varbinary(16) not null,'
         ' Hash varbinary(32) not null,'
         ' FullName varchar(255) not null,'
         ' Phone int not null unique,'
         ' Email varchar(255) not null'
         ')',
         
         'create table bookings ('
         ' BookingID integer primary key autoincrement,'
         ' CustomerID int not null,'
         ' DriverID int,'
         ' PickupLocation varchar(255) not null,'
         ' DropoffLocation varchar(255) not null,'
         ' Date date not null,'
         ' Time time(7) not null,'
         ' Status varchar(50) not null,'
         ' foreign key(CustomerID) references customers(CustomerID),'
         ' foreign key(DriverID) references drivers(DriverID)'
         ')',
         
         'create table adminBooking ('
         ' AdminID int not null,'
         ' BookingID int not null,'
         ' AssignedDriverID int not null,'
         ' foreign key(AdminID) references admins(AdminID),'
         ' foreign key(BookingID) references bookings(BookingID),'
         ' foreign key(AssignedDriverID) references drivers(DriverID)'
         ')']

for q in query:
    try:
        res = cur.execute(q)
        tableName = q.split(' ')[2]
        print(f'table {tableName} created succesfully')
    except sqlite3.OperationalError as error:
        print(error)

salt = urandom(16)
password = 'taxi booking' # default
hash = pbkdf2_hmac('sha256', password.encode(), salt, 10_000)
USERNAME = 'Server Admin'
Phone = 9876543210
Email = 'server@admin.com'
Fullname = 'Server D. Admin'

try:
    cur.execute('insert into admins (Username, Salt, Hash, FullName, Phone, Email) values(?, ?, ?, ?, ?, ?,)',
                (USERNAME, salt, hash, Fullname, Phone, Email))
    con.commit()
except:
    print('Server admin already exists')

# p = '1234567890'
# hash1 = pbkdf2_hmac('sha256', p.encode(), salt, 10_000)
# cur.execute('insert into customers (Username, Salt, Hash, FullName, Phone, Email, Address) values(?, ?, ?, ?, ?, ?, ?)',
#             ('milan', salt, hash1, 'Milan Gurung', Phone, 'milan@gmail.com', 'Hattiban'))
# p = '1234567890'
# hash1 = pbkdf2_hmac('sha256', p.encode(), salt, 10_000)
# cur.execute('insert into drivers (Username, Salt, Hash, FullName, Phone, Email, Address, LicenceNo, VehicleNo, VehicleType, VehicleDes, Status) values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
#             ('milan', salt, hash1, 'Milan Gurung', Phone, 'milan@gmail.com', 'Hattiban', '006-0239009', 'BAGMATI A AA0001', 'Bike', 'Red Honda', 'AVAILABLE'))

# cur.execute('UPDATE bookings SET DriverID = 1 WHERE BookingID = 5')

# # cur.execute('drop table customers')
# # cur.execute('drop table drivers')
# # cur.execute('drop table admins')
# # cur.execute('drop table bookings')
# # cur.execute('drop table adminBooking')
# con.commit()

con.close()

