import pypyodbc
import pyodbc


# Creates The DB, or if already created then connects
def CreateorConnectDB(dbname, query):
    connection = pypyodbc.connect(dbname)
    cursor = connection.cursor()
    SQLquery = query
    cursor.execute(SQLquery)
    connection.commit()

# Sends the given query to the DB given
def QueryToDB(dbname, query):
    connection = pyodbc.connect(dbname)
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    cursor.close()
    connection.close()

# Returns a list of the results in columnName
def AssignDBContenttoList(dbname, tableName, columnName):
    connection = pypyodbc.connect(dbname)
    cursor = connection.cursor()
    LinksinDB_list = []
    query = 'SELECT {}'.format(columnName) + ' from {}'.format(tableName)
    for row in  cursor.execute(query):
        LinksinDB_list.append(row[0])
    return LinksinDB_list

# Sends the given query and returns a list of the result
def AssignDBContenttoListWithQuery(dbname, query):
    connection = pypyodbc.connect(dbname)
    cursor = connection.cursor()
    LinksinDB_list = []
    for row in cursor.execute(query):
        LinksinDB_list.append(row[0])
    return LinksinDB_list

def QueryToDBMany(dbname, query, values=None):
    connection = pypyodbc.connect(dbname)
    cursor = connection.cursor()

    try:
        if values:
            cursor.executemany(query, values)
        else:
            cursor.execute(query)

        connection.commit()
    except Exception as e:
        connection.rollback()
        raise e
    finally:
        cursor.close()
        connection.close()

def Connectdb_N_Return_cursorNconn(db_connection_string):
    conn = pyodbc.connect(db_connection_string)
    cursor = conn.cursor()
    return cursor, conn

