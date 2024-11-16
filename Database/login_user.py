import sqlite3

con = sqlite3.connect("./Database/user.db")
cur = con.cursor()

# cur.execute("CREATE TABLE login(Id INTEGER PRIMARY KEY AUTOINCREMENT, UserName, Password, Phone, Address, Email, Name)")
# cur.execute("DROP TABLE login")

def login(user_name: str, password: str) -> bool:

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
