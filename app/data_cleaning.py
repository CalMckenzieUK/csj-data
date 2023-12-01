import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()
import os
import MySQLdb
from app.databaseconnection import database_query

todays_date = datetime.now().date()


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



def cleaning():
    try: 
        df  = pd.DataFrame(pd.read_csv(f'data/data-{todays_date}.csv'))
    except: 
        
        
        print('used old file in cleaning 1')
        df = pd.DataFrame(pd.read_csv(f'data/data-2023-11-29.csv'))

    try:
        df_full_ad = pd.DataFrame(pd.read_csv(f'data/full_ad_text-{todays_date}.csv'))
    except:
            
        print('used old file in cleaning 2')
        df_full_ad = pd.DataFrame(pd.read_csv(f'data/full_ad_text-2023-11-29.csv'))
    print(df['Closing Date'])

    df = pd.merge(df, df_full_ad, on='UID', how='left')
    df['UID'] = df['UID'].str.replace('Reference : ', '').astype(str)
    df['Salary'] = df['Salary'].str.extract(r'(\d{2,3},\d{3})')
    #split closing date by spaces and take the last 3 items in the list
    df['Closing Date'] = df['Closing Date'].str.split().str[-3:].str.join(' ').str.replace('th', '').str.replace('rd', '').str.replace('nd', '').str.replace('st', '')

    
    df['Closing Date'] = pd.to_datetime(df['Closing Date'], format='%d %B %Y')
    df.to_csv(f'data/cleaned_data-{todays_date}.csv', index=False)


    try: csb_df = pd.read_csv(f'data/cs_behaviours-{todays_date}.csv')
    except: csb_df = pd.read_csv(f'data/cs_behaviours-2023-11-29.csv')
    try: apply_at_advertisers_df = pd.read_csv(f'data/apply_at_advertisers_site-{todays_date}.csv')
    except: apply_at_advertisers_df = pd.read_csv(f'data/apply_at_advertisers_site-2023-11-29.csv') 
    try: application_process_df = pd.read_csv(f'data/application_process-{todays_date}.csv')
    except: application_process_df = pd.read_csv(f'data/application_process-2023-11-29.csv')

    ad_qualities_df = pd.merge(csb_df, apply_at_advertisers_df, on='UID', how='left')
    ad_qualities_df = pd.merge(ad_qualities_df, application_process_df, on='UID', how='left')

    # ad_qualities_df.to_csv(f'data/ad_qualities-{todays_date}.csv', index=False)
    database_query("DROP TABLE IF EXISTS ad_qualties;")
    database_query("DROP TABLE IF EXISTS ad_qualities;")
    with open('app/SQL/create_ad_qualities.sql', 'r') as file:
        create_table_sql = file.read()
    database_query(create_table_sql)
    
    rows = [tuple(x) for x in ad_qualities_df.to_numpy()]
    for i in rows:
        database_query(f'''insert into ad_qualities (job_uid, 
        developing_self_and_others, 
        leadership,
        making_effective_decisions,
        seeing_the_big_picture,
        managing_a_quality_service,
        working_together,
        communicating_and_influencing,
        changing_and_improving,
        delivering_at_pace,
        apply_at_advertisers_site,
        cv,
        personal_statement,
        reference_request,
        application_form,
        cover_letter,
        presentation,
        interview,
        portfolio,
        test)
        values {i}''')

    



if __name__ == '__main__':
    cleaning()
    new_df = pd.DataFrame(database_query('select * from ad_qualities limit 6;'), columns=['job_uid', 
        'developing_self_and_others', 
        'leadership',
        'making_effective_decisions',
        'seeing_the_big_picture',
        'managing_a_quality_service',
        'working_together',
        'communicating_and_influencing',
        'changing_and_improving',
        'delivering_at_pace',
        'apply_at_advertisers_site',
        'cv',
        'personal_statement',
        'reference_request',
        'application_form',
        'cover_letter',
        'presentation',
        'interview',
        'portfolio',
        'test'] )

        