import sqlite3
from register_user import personal_detail
con = sqlite3.connect("./Database/user.db")
cur = con.cursor()

# cur.execute("CREATE TABLE login(Id INTEGER PRIMARY KEY AUTOINCREMENT, UserName, Password, Phone, Address, Email, Name)")
# cur.execute("DROP TABLE login")
personal_detail(["Milan","Gurung"], "Lalitpur", 123, "hack@gmail")
res = cur.execute("SELECT * FROM login")
a = res.fetchall()
for x in a:
    print(x)
con.close()