import sqlite3


con = sqlite3.connect("./Database/user.db")
cur = con.cursor()
    
def personal_detail(name, address: str, phone: int, email: str) -> bool:

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
        con.close()
        return True

# print(personal_detail(["Ram","Bahadur","Gurung"],"KTM",978,"ton@gmail.com"))