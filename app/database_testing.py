import os
import MySQLdb
from dotenv import load_dotenv
import pandas as pd


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
    # with open('app/SQL/create_ad_qualities.sql', 'r') as sql_file:
    #     sql_query = sql_file.read()

    sql_query = 'select max(scraped_dates) from scraped_dates;'
    # print(str(database_query('select * from all_time_listings')).strip('[(,)]'))
    # with open('app/SQL/create_all_time_listings.sql', 'r') as file:
    #         create_all_time_table_sql = file.read()
    # database_query(create_all_time_table_sql)
    
#     print(database_query('''

# select count(distinct(uid)) from all_time_listings;
# '''

#     ))
    df = pd.DataFrame(database_query('''                  
                    
    select count(*) from all_time_listings where full_ad_text is not null;
                                     
                                    '''))
    print(df)

