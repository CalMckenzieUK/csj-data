import os
import MySQLdb
from dotenv import load_dotenv


load_dotenv()

def database_query(sql_query):
    connection = MySQLdb.connect(
        host=os.getenv("DATABASE_HOST"),
        user=os.getenv("DATABASE_USERNAME"),
        passwd=os.getenv("DATABASE_PASSWORD"),
        db=os.getenv("DATABASE"),
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

if __name__ == '__main__':
    with open('app/SQL/create_ad_qualities.sql', 'r') as sql_file:
        sql_query = sql_file.read()
    print(database_query(sql_query))