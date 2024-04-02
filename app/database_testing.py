import os
import MySQLdb
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

def database_query(sql_query):
    try:
        connection = MySQLdb.connect(
        host=os.getenv("DATABASE_HOST"),
        user=os.getenv("DATABASE_USERNAME"),
        passwd=os.getenv("DATABASE_PASSWORD"),
        db=os.getenv("DATABASE"),
        autocommit=True,
        # ssl_mode="VERIFY_iDENTITY",
        ssl={"ca": "/etc/ssl/certs/ca-certificates.crt"})
    except:
        connection = MySQLdb.connect(
        host=os.environ["DATABASE_HOST"],
        user=os.environ["DATABASE_USERNAME"],
        passwd=os.environ["DATABASE_PASSWORD"],
        db=os.environ["DATABASE"],
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
    print(database_query(
        """
        update all_time_ad_qualities
        left join all_time_listings on all_time_ad_qualities.uid = all_time_listings.uid
        set cv = 1 
        where LOWER(full_ad_text) like '%cv%'
        and cv = 0;

        
        """
        # update all_time_ad_qualities
        # set cv = 1
        # where uid in (
        # select all_time_ad_qualities.uid from all_time_ad_qualities
        # left join all_time_listings on all_time_ad_qualities.uid = all_time_listings.uid 
        # where LOWER(full_ad_text) like '%cv%'
        # and cv = 0);
        ))