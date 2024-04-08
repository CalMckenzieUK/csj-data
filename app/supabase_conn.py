import os
import MySQLdb
import pyodbc
from dotenv import load_dotenv
import pandas as pd
import supabase


load_dotenv()


def supabase_query(sql_query):
    try:
        cnxn = pyodbc.connect(
        "DRIVER={PostgreSQL Unicode};"
        "SERVER=" + os.getenv("HOST") + ";"
        "DATABASE=" + os.getenv("DBNAME") + ";"
        "UID=" + os.getenv("USERNAME") + ";"
        "PWD=" + os.getenv("PASSWORD") + ";"
    )
        df = pd.read_sql(sql_query, cnxn)
        return df
    except:

        cnxn = pyodbc.connect(
        "DRIVER={PostgreSQL Unicode};"
        "SERVER=" + os.environ["HOST"] + ";"
        "DATABASE=" + os.environ["DBNAME"] + ";"
        "UID=" + os.environ["USER"] + ";"
        "PWD=" + os.environ["PASSWORD"] + ";"
    )
        df = pd.read_sql(sql_query, cnxn)
        return df



def database_query(sql_query):
    try:
        connection = MySQLdb.connect(
        host=os.getenv("host"),
        user=os.getenv("username"),
        passwd=os.getenv("password"),
        db=os.getenv("dbname"),
        autocommit=True,
        # ssl_mode="VERIFY_iDENTITY",
        ssl={"ca": "/etc/ssl/certs/ca-certificates.crt"})
    except:
        connection = MySQLdb.connect(
        host=os.environ["host"],
        user=os.environ["username"],
        passwd=os.environ["password"],
        db=os.environ["dbname"],
        autocommit=True,
        # ssl_mode="VERIFY_iDENTITY",
        ssl={"ca": "/etc/ssl/certs/ca-certificates.crt"})
    try:
        c = connection.cursor()
        c.execute(sql_query)
        results = c.fetchall()
        return results
    except MySQLdb.Error as e:
        print("MySQL Error:", e)
    finally:
        c.close()
        connection.close()


def supabase_write_rows():
    import os
    from supabase import create_client, Client
    try:
        
        url = os.getenv("URL")
        key = os.getenv("KEY")
        supabase: Client = create_client(url, key)
    except:
        url: str = os.environ.get("URL")
        key = os.environ.get("KEY")
        supabase: Client = create_client(url, key)

    # create a new row in the lol table
    data = [
        {'lol': 'John'},
        {'lol': 'Jane'},
    ]
    table_name = 'lol'
    print(supabase.table(table_name).insert(data).execute())
    
    



    print('completed')
    return


if __name__ == '__main__':
    supabase_write_rows()