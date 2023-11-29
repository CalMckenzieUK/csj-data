from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Load environment variables from the .env file
load_dotenv()
import os
import MySQLdb


# def sql_alchemy_database_connection():

#     # Create a connection to the database
#     engine = create_engine(
#         f"mysqldb+mysqlconnector://{os.getenv('DATABASE_USERNAME')}:{os.getenv('DATABASE_PASSWORD')}@{os.getenv('DATABASE_HOST')}:{os.getenv('PORT', default=5000)}/csj-helper",
#         echo=True,
#     )

#     # Create a session
#     with engine.connect() as connection:
#         connection.execute("DROP TABLE IF EXISTS test;")
#         connection.execute("CREATE TABLE test (id serial PRIMARY KEY, name VARCHAR(255));")
#         connection.execute("INSERT INTO test (name) VALUES ('Hello1, world');")
#         connection.execute("INSERT INTO test (name) VALUES ('Hello2, world');")
#         connection.execute("INSERT INTO test (name) VALUES ('Hello3, world');")

#     result = connection.execute("SELECT * FROM test;")
#     print("Result:", result)
connection = MySQLdb.connect(
    host=os.getenv("DATABASE_HOST"),
    user=os.getenv("DATABASE_USERNAME"),
    passwd=os.getenv("DATABASE_PASSWORD"),
    db=os.getenv("DATABASE"),
    autocommit=True,
    ssl_mode="VERIFY_CA",
    # See https://planetscale.com/docs/concepts/secure-connections#ca-root-configuration
    # to determine the path to your operating systems certificate file.
    ssl      = {
    "ca": "/etc/ssl/certs/ca-certificates.crt"
  })

def database_query(sql_query):

# Connect to the database
    connection = MySQLdb.connect(
    host=os.getenv("DATABASE_HOST"),
    user=os.getenv("DATABASE_USERNAME"),
    passwd=os.getenv("DATABASE_PASSWORD"),
    db=os.getenv("DATABASE"),
    autocommit=True,
    ssl_mode="VERIFY_CA",
    # See https://planetscale.com/docs/concepts/secure-connections#ca-root-configuration
    # to determine the path to your operating systems certificate file.
    ssl      = {
    "ca": "/etc/ssl/certs/ca-certificates.crt"
  })

    try:
        # Create a cursor to interact with the database
        cursor = connection.cursor()

        # Execute "SHOW TABLES" query
        cursor.execute(sql_query)

        # Fetch the query results
        results = cursor.fetchall()
        return results

    except MySQLdb.Error as e:
        print("MySQL Error:", e)

    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()

if __name__ == "__main__":
    database_query('drop table if exists test; create table test (id varchar(20) primary key, name varchar(20)); insert into test values (1, 2), (3, 4), (5, 6)')
    print(database_query('select * from test;'))
