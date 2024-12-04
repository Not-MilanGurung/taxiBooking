from sqlite3 import connect, Connection
from hashlib import pbkdf2_hmac
from pathlib import Path

con = connect("Database/database.db")



def login(user_name: str, password: str):

    cur = con.cursor()

    res = cur.execute(f"SELECT Salt, Hash  FROM admins WHERE Username = '{user_name}'")
    p = res.fetchone()
    if p is None:
        return 'UserName is not registered'

    hash = pbkdf2_hmac('sha256', password.encode() , p[0], 600_000) 

    # Check if the hash matches
    if p[1] != hash:
        return 'Incorrect password'

    
    # Login if the requirements are met
    return user_name


    
def personal_detail( name , address: str, phone = 00,  email: str = '') :

    cur = con.cursor()

    query = f"SELECT phone from customer where phone={phone}"
    res = cur.execute(query)
    if res.fetchone() is not(None):
        return 'The phone is already registered. Try logging in or using a different phone'
    
    return (name, address, phone, email)

def account( username, password, personal: tuple , con_in: Connection | None = None ):  

    cur = con.cursor()
    (name, address, phone, email) = personal

    res = cur.execute(f"SELECT UserName from customer where UserName='{username}'")  
    if res.fetchone() is not(None):
        return 'The username is taken, try another one'
    

    data = (username, password, phone, address, email, name)
    cur.execute("INSERT INTO customer(UserName, Password, Phone, Address, Email, Name) VALUES(?, ?, ?, ?, ?, ?)", data)

    # Commiting the operations into the database
    con.commit()
    return 'The account has been created. Go to the login page.'

def close_connection():
    con.close()

if __name__ == '__main__':
    print(login('Server Admin', 'taxi booking'))