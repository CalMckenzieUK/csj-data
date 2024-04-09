from app.csj_scrape import scrape, button_click, full_ad
from app.data_cleaning import cleaning
from app.dict_to_df import dict_to_def_setup_and_execution
from app.databaseconnection import database_query
import pandas as pd
from datetime import datetime
import os
from app.clear_staging_tables import clear_staging_tables
from supabase import create_client, Client
from app.supabase_conn import superbase_read_all_rows

try:
    url: str = os.environ.get("URL")
    key: str = os.environ.get("KEY")
    supabase: Client = create_client(url, key)
except:
    url: str = os.getenv("URL")
    key: str = os.getenv("KEY")
    supabase: Client = create_client(url, key)

todays_date = datetime.now().date() 

def run_etl_pipeline():
        scrape(button_click())
        print('completed scraping')
        scraped_df = pd.DataFrame(superbase_read_all_rows('scraped_data'))
        scraped_df.columns = ['Title', 'Department', 'Location', 'Salary', 'Closing Date', 'UID', 'URL']
        full_ad(scraped_df)
        print('completed full ad')
        # full_text = pd.DataFrame(database_query('select * from full_ad_text'), columns=['UID', 'Full Text', 'Scraped Date'])
        # application_process(full_text)
        # apply_at_advertisers_site(full_text)
        # civil_service_behaviours(full_text)
        dict_to_def_setup_and_execution()
        print('commpleted dict to df')
        cleaning()
        return

def main():
    try:
        clear_staging_tables({'scraped_data':'uid'
                              ,'full_ad_text':'uid'
                              , 'cleaned_data': 'uid'
                              , 'ad_qualities': 'uid'
                              , 'application_process': 'uid'
                              , 'apply_at_advertisers_site': 'uid'
                              , 'cs_behaviours': 'uid'})
        run_etl_pipeline()
        print('cleaning done')
        clear_staging_tables({'scraped_data':'uid'
                              ,'full_ad_text':'uid'
                              , 'cleaned_data': 'uid'
                              , 'ad_qualities': 'uid'
                              , 'application_process': 'uid'
                              , 'apply_at_advertisers_site': 'uid'
                              , 'cs_behaviours': 'uid'})
    except Exception as e:
        print('Error when trying to run ETL pipeline: ', e)
if __name__ == '__main__':
    main()
