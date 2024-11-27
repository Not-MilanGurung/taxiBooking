from sqlite3 import connect, Connection

con = connect("Database/user.db")

# cur.execute("CREATE TABLE login(Id INTEGER PRIMARY KEY AUTOINCREMENT, UserName, Password, Phone, Address, Email, Name)")
# cur.execute("DROP TABLE login")


def login(user_name: str, password: str):

    cur = con.cursor()

    res = cur.execute(f"SELECT Password FROM login WHERE UserName = '{user_name}'")
    p = res.fetchone()
    if p is None:
        return 'UserName is not registered'

    
    # Check if the password matches
    if p[0] != password:
        return 'Incorrect password'

    
    # Login if the requirements are met
    return True


    
def personal_detail( name , address: str, phone = 00,  email: str = '', con_in: Connection | None = None) :

    cur = con.cursor()

    query = f"SELECT phone from login where phone={phone}"
    res = cur.execute(query)
    if res.fetchone() is not(None):
        return 'The phone is already registered. Try logging in or using a different phone'
    
    return (name, address, phone, email)

def account( username, password, personal: tuple , con_in: Connection | None = None ):  

    cur = con.cursor()
    (name, address, phone, email) = personal

    res = cur.execute(f"SELECT UserName from login where UserName='{username}'")  
    if res.fetchone() is not(None):
        return 'The username is taken, try another one'
    

    data = (username, password, phone, address, email, name)
    cur.execute("INSERT INTO login(UserName, Password, Phone, Address, Email, Name) VALUES(?, ?, ?, ?, ?, ?)", data)

    # Commiting the operations into the database
    con.commit()
    return 'The account has been created. Go to the login page.'

def close_connection():
    con.close()