from sqlite3 import Connection

# cur.execute("CREATE TABLE login(Id INTEGER PRIMARY KEY AUTOINCREMENT, UserName, Password, Phone, Address, Email, Name)")
# cur.execute("DROP TABLE login")

def login(con: Connection, user_name: str, password: str) -> bool:

    cur = con.cursor()
    # Checking if the User Name is registered
    res = cur.execute(f"SELECT Password FROM login WHERE UserName = '{user_name}'")
    p = res.fetchone()
    if p is None:
        print('UserName is not registered')
        return False
    
    # Check if the password matches
    if p[0] != password:
        print('Incorrect password')
        return False
    
    # Login if the requirements are met
    print(f'Welcome, {user_name}')
    return True

    
def personal_detail(con: Connection, name , address: str, phone: int, email: str) -> bool:
    cur = con.cursor()
    #Query database if the phone number is already registered
    res = cur.execute(f"SELECT phone from login where phone={phone}")
    if res.fetchone() is not(None):
        print('The phone is already registered. Try logging in or using a different phone')
        return False

    # Looping till a valid username is given
    while True:
        user = input('Create your username: ')

        # Checking if the username is already taken
        res = cur.execute(f"SELECT UserName from login where UserName='{user}'")  
        if res.fetchone() is not(None):
            print('The username is taken, try another one')
            return False
        

        password = input('Enter your password: ')
        # Joining first, middle and last name with space between them into a single string
        fullName = " ".join(name)

        data = (user, password, phone, address, email, fullName)
        cur.execute("INSERT INTO login(UserName, Password, Phone, Address, Email, Name) VALUES(?, ?, ?, ?, ?, ?)", data)

        # Commiting the operations into the database
        con.commit()
        return True