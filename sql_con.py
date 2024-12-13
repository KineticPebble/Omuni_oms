'''script containing function for providing sql connection object

1 Function:
    - get_con
'''
import pyodbc
import auth

def get_con(database: str, server:str) -> pyodbc.connect:
    '''Create a database connection with pyodbc

    Parameters:
        database: Name of the database
        server: IP or Hostname of the server
    
    Returns:
        SQL Connection object
    '''
    connect_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};'
    # connect_string = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=10.91.4.192;'
    connect_string += f'DATABASE={database};UID={auth.sql_usr};PWD={auth.sql_ps}'
    connection = pyodbc.connect(connect_string)
    return connection
