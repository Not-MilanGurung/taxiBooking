user_detail_db = [['Milan','1234',['Milan','','Gurung'],'Hattiban, Lalitpur',9742821010,'notmilan@hotmail.com'],]
def dailogue(s: str):
    print(s)
def store(db, username, password, name, address, phone, email):
    db += [[username, password, name, address, phone, email]]

def home(user: str):
    print(f'Welcome, {user}')

def search(username, db):
    for user in user_detail_db:
        if user[0] == username:
            return user[1]
    else:
        return None

def query(username, password):
    temp = search(username, user_detail_db)
    if password == temp:
        return 1
    else:
        return 0
    
def login(username: str, password: str):

    if not(query(username, password)):
        dailogue('Wrong Credentials. Try again.')
        return 0
    home(username)

def register(name, address, phone, email):
    if phone not in [user[4] for user in user_detail_db]:
        username = input('Create a username: ')
        while username in [user[0] for user in user_detail_db]:
            dailogue('User name take. Try different one')
            username = input('Create a username: ')
        else:
            password = input('Enter a password: ')
            store(user_detail_db,username, password, name, address, phone, email)
            print(user_detail_db)
    else:
        dailogue('The phone number is already registerd. Try login or another number')
        main()
            

def main():
    y = 'n'
    new = input('Are you a new user?(y/n) : ')
    print(new)
    if new == 'y':
        dailogue('Register')
        fname = input('Enter first name: ')
        mname = input('Enter middle name(optional): ')
        lname = input('Enter lastname name: ')
        name = [fname, mname, lname]
        address = input('Enter your address: ')
        phone = int(input('Enter your phone number: '))
        email = input('Enter your emial: ')
        register(name, address, phone, email)
    dailogue('Login')
    while y != 'y':
        user = input('Enter the username: ')
        password = input('Enter the password: ')
        login(user, password)
        y = input('Exit?(y/n): ')

def __init__():
    main()