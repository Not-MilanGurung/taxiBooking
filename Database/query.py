from sqlite3 import connect, Connection

con = connect("Database/user.db")
# cur = con.cursor()
# res = cur.execute('select * from login')
# print(res.fetchall())
def select_from(table: str, column_query: str, parameter: str, column_get = '*', con_in: Connection = None):

    cur = con.cursor()
    query = f'select {column_get} from {table} where {column_query} = {parameter}'
    res = cur.execute(query)
    data = res.fetchall()
    cur.close()
    return data
