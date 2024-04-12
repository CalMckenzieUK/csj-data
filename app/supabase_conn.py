import os
from dotenv import load_dotenv
import pandas as pd
from supabase import create_client, Client
import supabase
load_dotenv()

def supabase_write_rows(df: pd.DataFrame, table_name: str, columns: list=None):

    try:
        url = os.getenv("URL")
        key = os.getenv("KEY")
        supabase: Client = create_client(url, key)
    except:
        url: str = os.environ.get("URL")
        key = os.environ.get("KEY")
        supabase: Client = create_client(url, key)
    
    existing_rows = superbase_read_all_rows(table_name)
    existing_rows = pd.DataFrame(existing_rows)
    if existing_rows.shape[0] == 0:
        print('no existing rows in table: ', table_name)
        df = df.to_dict(orient='records')
        supabase.table(table_name).insert(df).execute()
        print(f'updated table {table_name} with {len(df)} rows')
        return
    existing_rows.columns = columns
    try:
        if set(df.dtypes) != set(existing_rows.dtypes):
            df['uid'] = df['uid'].astype(existing_rows['uid'].dtype)
        existing_uids = existing_rows['uid'].tolist()
        df = df[~df['uid'].isin(existing_uids)]
        if df.shape[0] > 0:
            df = df.to_dict(orient='records')
            supabase.table(table_name).insert(df).execute()
            print(f'updated table {table_name} with {len(df)} rows')
        else: print('no new data to write into table: ', table_name)
    except Exception as e:
        if set(df.dtypes) != set(existing_rows.dtypes):
            df['uid'] = df['uid'].astype(existing_rows['uid'].dtype)
        existing_uids = existing_rows['uid'].tolist()
        df = df[~df['uid'].isin(existing_uids)]
        if df.shape[0] > 0:
            print('writing data,')
            df = df.to_dict(orient='records')
            supabase.table(table_name).insert(df).execute()
            print(f'updated table {table_name} with {len(df)} rows')
        else: print('no new data to write into table: ', table_name)
    return

def superbase_read_all_rows(table_name):
    try:
        url = os.getenv("URL")
        key = os.getenv("KEY")
        supabase: Client = create_client(url, key)
    except:
        url: str = os.environ.get("URL")
        key = os.environ.get("KEY")
        supabase: Client = create_client(url, key)

    response = supabase.table(table_name).select('*').execute()
    return response.data

def supabase_max_date(table_name):
    try:
        url = os.getenv("URL")
        key = os.getenv("KEY")
        supabase: Client = create_client(url, key)
    except:
        url: str = os.environ.get("URL")
        key = os.environ.get("KEY")
        supabase: Client = create_client(url, key)

    response = supabase.table(table_name).select('scraped_date').order('scraped_date', desc='True').limit(1).execute()
    return response

def superbase_delete_all_rows(table, column):
    try:
        url = os.getenv("URL")
        key = os.getenv("KEY")
        supabase: Client = create_client(url, key)

    except:
        url: str = os.environ.get("URL")
        key = os.environ.get("KEY")
        supabase: Client = create_client(url, key)

    response = supabase.table(table).delete().neq(column,'').execute()
    return response
if __name__ == '__main__':
    df = pd.DataFrame({'lol': ['John', 'Jane']})
    # df = df.to_dict(orient='records')
    supabase_write_rows(df, 'lol')  
    response = superbase_read_all_rows('lol')
    # df = pd.DataFrame(superbase_read_all_rows('lol'), columns=['lol'])
    # print(df)
    # supabase_write_rows(df, 'lol')
    # superbase_delete_all_rows('lol', 'lol')