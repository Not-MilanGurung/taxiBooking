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

def record_entry(table: str, data: list[tuple], con_in: Connection = None):
    
    cur = con.cursor()
    columns = tuple
    values = tuple
    for x in data:
        columns += x[0]
        values += x[1]

    query = f'insert into {table}{columns} values{values}'
    cur.execute(query)
    con.commit()
    cur.close()
    return 'Inserted sucessfully'

def update_record(table: str, data: str, where: str, con_in: Connection = None):

    cur = con.cursor()

    query = f'update {table} set {data} where {where}'
    cur.execute(query)
    con.commit()
    cur.close()
    return 'Updated sucessfully'

def delete_record(table: str, where: str, con_in: Connection = None):

    cur = con.cursor()
    query = f'delete from {table} where {where}'
    cur.execute(query)
    con.commit()
    cur.close()
    return 'Deleted sucessfully'


