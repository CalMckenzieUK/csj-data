import os
from dotenv import load_dotenv
import pandas as pd
from supabase import create_client, Client
import supabase
load_dotenv()

def supabase_write_rows(df: pd.DataFrame, table_name: str, columns: list=None, skip=False):
    try:
        url = os.getenv("URL")
        key = os.getenv("KEY")
        supabase: Client = create_client(url, key)
    except:
        url: str = os.environ.get("URL")
        key = os.environ.get("KEY")
        supabase: Client = create_client(url, key)
    
    if skip==True:
        df = df.to_dict(orient='records')
        supabase.table(table_name).insert(df).execute()
        print('table updated with new data: ', table_name)
        return 


    existing_rows = superbase_read_all_rows(table_name)
    existing_rows = pd.DataFrame(existing_rows)
    existing_rows.columns = columns
    if existing_rows.shape[0] == 0:
        print('no existing rows in table: ', table_name)
        df = df.to_dict(orient='records')
        supabase.table(table_name).insert(df).execute()
        print(f'updated table {table_name} with {len(df)} rows')
        return
    
    try:
        if set(df.dtypes) != set(existing_rows.dtypes):
            df['uid'] = df['uid'].astype(existing_rows['uid'].dtype)
        existing_uids_list = existing_rows['uid'].tolist()
        df = df[~df['uid'].isin(existing_uids_list)]
        if df.shape[0] > 0:
            df_dict = df.to_dict(orient='records')
            supabase.table(table_name).insert(df_dict).execute()
            print(f'updated table {table_name} with {len(df_dict)} rows')
        else: print('no new data to write into table: ', table_name)
    except Exception as e:
        if set(df.dtypes) != set(existing_rows.dtypes):
            df['uid'] = df['uid'].astype(existing_rows['uid'].dtype)
        existing_uids = existing_rows['uid'].tolist()
        print(df.shape)
        df['uid'] = df['uid'].astype(str)
        df = df[~df['uid'].isin(existing_uids)]
        print(df.shape)
        if df.shape[0] > 0:
            print('writing data,')
            df = df.to_dict(orient='records')
            print(df)
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