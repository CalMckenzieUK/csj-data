import os
from supabase import create_client, Client


def clear_staging_tables(tables: dict):
    
    try:
        url = os.getenv("URL")
        key = os.getenv("KEY")
        supabase: Client = create_client(url, key)
    except:
        url: str = os.environ.get("URL")
        key = os.environ.get("KEY")
        supabase: Client = create_client(url, key)
    
    for table, column in tables.items():
        supabase.table(table).delete().neq(column, '').execute()
        print(f'cleared table {table}')
    return
