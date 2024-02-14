import pandas as pd
from datetime import datetime
from app.databaseconnection import database_query

todays_date = datetime.now().date()

def cleaning():
    try: 
        df  = pd.DataFrame(database_query('select * from scraped_data'))
    except Exception as e:        
        print('Error when trying to query database for scraped_data: ', e)
    try:
        df_full_ad = pd.DataFrame(database_query('select * from full_ad_text'))
        df_full_ad.columns = ['UID', 'Full Ad Text', 'scraped_date']
        df_full_ad['UID'] = df_full_ad['UID'].str.replace('Reference : ', '').astype(str)
    except Exception as e:    
        print('Error when trying to query database for full_ad_text: ', e)
    df.columns = ['Title', 'Department', 'Location', 'Salary', 'Closing Date', 'UID', 'URL']
    df['UID'] = df['UID'].str.replace('Reference : ', '').astype(str)
    df = pd.merge(df, df_full_ad, on='UID', how='left')
    df['Salary'] = df['Salary'].str.extract(r'(\d{2,3},\d{3})')
    #split closing date by spaces and take the last 3 items in the list
    df['Closing Date'] = df['Closing Date'].str.split().str[-3:].str.join(' ').str.replace('th', '').str.replace('rd', '').str.replace('nd', '').str.replace('st', '')

    

    closing_dates = df['Closing Date']
    closing_dates_dates = []
    for date in closing_dates:
        try:
            closing_dates_dates.append(datetime.strptime(str(date), '%d %B %Y'))
        except:
            closing_dates_dates.append(pd.to_datetime(todays_date))

    # df['Closing Date'] = pd.to_datetime(df['Closing Date'], format='%d %B %Y')
    df['Closing Date'] = closing_dates_dates
    df['Closing Date'] = df['Closing Date'].dt.date
    df['Closing Date'] = df['Closing Date'].astype(str)

    with open('app/SQL/create_cleaned_data.sql', 'r') as file:
        create_table_sql = file.read()
    database_query(create_table_sql)
    df.drop('Full Ad Text', axis=1, inplace=True)
    df['scraped_date'] = str(todays_date)
    rows = [tuple(x) for x in df.to_numpy()]

    for i in rows:
        database_query(f"insert into cleaned_data (title, department, location, salary, closing_date, uid, url, scraped_date) values {i}")

    try: csb_df = pd.DataFrame(database_query('select * from cs_behaviours'))
    except Exception as e: print('Error when trying to query database for cs_behaviours: ', e)
    try: apply_at_advertisers_df = pd.DataFrame(database_query('select * from apply_at_advertisers_site'))
    except Exception as e: print('Error when trying to query database for apply_at_advertisers_site: ', e)
    try: application_process_df = pd.DataFrame(database_query('select * from application_process'))
    except Exception as e: print('Error when trying to query database for application_process: ', e)

    #csb_df columns: UID, Seeing the Big Picture, Changing and Improving, Making Effective Decisions, Communicating and Influencing, Leadership, Working Together, Delivering at Pace, Managing a Quality Service, Developing Self and Others
    csb_df.columns = ['UID', 'Making Effective Decisions', 'Changing and Improving', 'Seeing the Big Picture', 'Communicating and Influencing', 'Working Together', 'Managing a Quality Service', 'Leadersip', 'Delivering at Pace', 'Developing Self and Others']
    apply_at_advertisers_df.columns = ['UID', 'Apply at Advertiser\'s Site']
    application_process_df.columns = ['UID', 'CV', 'Personal Statement', 'References', 'Application Form', 'Cover Letter', 'Presentation', 'Interview', 'Portfolio', 'Test']

    ad_qualities_df = pd.merge(csb_df, apply_at_advertisers_df, on='UID', how='left')
    ad_qualities_df = pd.merge(ad_qualities_df, application_process_df, on='UID', how='left')

    # ad_qualities_df.to_csv(f'data/ad_qualities-{todays_date}.csv', index=False)
    database_query("DROP TABLE IF EXISTS ad_qualities;")
    with open('app/SQL/create_ad_qualities.sql', 'r') as file:
        create_ad_qualities_table_sql = file.read()
    database_query(create_ad_qualities_table_sql)
    print('1')
    rows = [tuple(x) for x in ad_qualities_df.to_numpy()]
    for i in rows:
        database_query(f'''insert into ad_qualities (uid, 
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
    
    with open('app/SQL/create_all_time_ad_qualities.sql', 'r') as file:
        create_all_time_ad_qualities_table_sql = file.read()
    database_query(create_all_time_ad_qualities_table_sql)

    with open('app/SQL/insert_new_into_all_time_ad_qualities.sql', 'r') as file:
        insert_all_time_ad_qualities_sql = file.read()
    database_query(insert_all_time_ad_qualities_sql)

    with open('app/SQL/create_scraped_dates.sql', 'r') as file:
        create_scraped_table_sql = file.read()
    database_query(create_scraped_table_sql)
    database_query(f"insert into scraped_dates (scraped_date) values ('{todays_date}')")
    print('2')

    with open('app/SQL/create_all_time_listings.sql', 'r') as file:
            create_all_time_table_sql = file.read()
    database_query(create_all_time_table_sql)
    print('3')
    with open('app/SQL/insert_new_into_all_time.sql', 'r') as file:
            insert_all_time_sql = file.read()
    print('3.5')
    database_query(insert_all_time_sql)
    print('4')

    return
    



if __name__ == '__main__':
    cleaning()
    

        