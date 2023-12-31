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


app = Flask(__name__)
todays_date = datetime.now().date() 

def run_etl_pipeline(regardless_of_date=False):
    
    max_date = str(database_query('select max(scraped_date) from scraped_dates')).strip('[(,)]')
    if max_date == str("'"+str(todays_date)+"'") and regardless_of_date == False:
        print('started from database')
        ads = pd.DataFrame(database_query('select * from cleaned_data'))
        ads.columns = ['Job Title', 'Department', 'Location', 'Salary', 'Closing Date', 'UID', 'URL']
        full_text = pd.DataFrame(database_query('select * from full_ad_text'))
        full_text.columns = ['UID', 'Full Text']
        print('starting application_process')
    else:
        ads = scrape(button_click())
        full_text = full_ad(ads)
        application_process(full_text)
        apply_at_advertisers_site(full_text)
        civil_service_behaviours(full_text)
        dict_to_def_setup_and_execution()
        cleaning()
    return f'Refreshed as of {str(todays_date)}'


@app.route('/', methods=['GET', 'POST'])
def main():
    print('main triggered')
    var_test = 'nothing'
    if request.method == 'POST':
        run_etl_pipeline(True) 
    max_date = str(database_query('select max(scraped_date) from scraped_dates')).strip('[(,)]')
    ads = pd.DataFrame(database_query('select * from cleaned_data'))
    ads.columns = ['Job Title', 'Department', 'Location', 'Salary', 'Closing Date', 'UID', 'URL']
    full_text = pd.DataFrame(database_query('select * from full_ad_text'))
    full_text.columns = ['UID', 'Full Text']

    homepage_title = "CS Jobs Helper"
    main_content_title = 'Current vacancies'
    main_content = 'main content'
    footer = 'Not Copyright'
    side_title = 'Options'
    return flask.render_template('index.html', tables=ads.values, titles=ads.columns.values, title=homepage_title, side_title=side_title, main_content_title=main_content_title, main_content=main_content, footer=footer, var_test=var_test, max_date=max_date)

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
