from app.csj_scrape import scrape, button_click, full_ad
from app.data_cleaning import cleaning
from app.dict_to_df import dict_to_df, dict_to_def_setup_and_execution
from app.nlp_analysis import application_process, apply_at_advertisers_site, civil_service_behaviours
from app.function_test import function_test
from app.databaseconnection import database_query
from markupsafe import Markup
from flask import request, url_for, Flask
import pandas as pd
import flask
from datetime import datetime, date
import os

todays_date = datetime.now().date() 

def run_etl_pipeline():
        scrape(button_click())
        full_ad(pd.DataFrame(database_query('select * from scraped_data;'), columns=['Title', 'Department', 'Location', 'Salary', 'Closing Date', 'UID', 'URL']))
        full_text = pd.DataFrame(database_query('select * from full_ad_text;'), columns=['UID', 'Full Text', 'Scraped Date'])
        application_process(full_text)
        apply_at_advertisers_site(full_text)
        civil_service_behaviours(full_text)
        dict_to_def_setup_and_execution()
        cleaning()
        return

def main():
    run_etl_pipeline()

if __name__ == '__main__':
    main()
