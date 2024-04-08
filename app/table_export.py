from databaseconnection import database_query
import pandas as pd

def export_table_to_csv(table_name):
    query = f"SELECT * FROM {table_name}"
    results = pd.DataFrame(database_query(query))
    results.to_csv(f"{table_name}.csv", index=False)
    print(f"Exported {table_name} to {table_name}.csv")


tables = database_query("SHOW TABLES")

for table in tables:
    export_table_to_csv(str(table).strip("()',"))
