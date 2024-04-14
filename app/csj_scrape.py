from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime, date
import os
from dotenv import load_dotenv
from supabase import create_client, Client
from app.databaseconnection import database_query
from app.supabase_conn import supabase_write_rows, superbase_read_all_rows, superbase_delete_all_rows

try: 
    url: str = os.environ.get("URL")
    key = os.environ.get("KEY")
    supabase: Client = create_client(url, key)
except:
    url = os.getenv("URL")
    key = os.getenv("KEY")
    supabase: Client = create_client(url, key)

MAX_PAGES = 1000
load_dotenv()
todays_date = date.today()

def button_click():
    global MAX_PAGES
    print('starting button_click')
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get('https://www.civilservicejobs.service.gov.uk/csr/index.cgi')
    driver.find_element(By.NAME, 'search_button').click()
    #sleep(5)
    all_results_pages = []
    html = driver.page_source
    all_results_pages.append(html)
    #all_results_pages is the first page of results
    #the below loop should click the next button until it can't find it anymore
    more_pages = True
    pages = 0
    while more_pages:
        try:
            
                #find next button called 'Go to next results page' and click on it
                driver.find_element(By.PARTIAL_LINK_TEXT, 'next').click()
                all_results_pages.append(driver.page_source)
                print(f'clicked next page - added {len(all_results_pages)} pages so far')
                pages += 1
                if pages >= MAX_PAGES:
                    more_pages = False
        except Exception as e:
            print('no more pages, exited with error: ', e)
            more_pages = False
    driver.quit()
    print('finished button_click')
    return all_results_pages

def scrape(url):
    print('starting scrape')
    print(len(url))
    job_data = []
    for i in url:
        soup = BeautifulSoup(i, 'html.parser')
        job_postings = soup.find_all('li', class_='search-results-job-box')
        for posting in job_postings:
            try: 
                ad = posting.get_text().strip().splitlines()
                url = posting.find('a')['href']
                ad = list(filter(None, ad))
                title = ad[0]
                department = ad[1]
                location = ad[2]
                salary = ad[3]
                closing_date = ad[4]
                uid = ad[5]
                job_url = str(url)
                job_data.append([title, department, location, salary, closing_date, uid, job_url])
                print('added to job_data')
            except Exception as e:
                print('error when trying to add to job_data: ', e)
                continue
        
    df = pd.DataFrame(job_data, columns=['Title', 'Department', 'Location', 'Salary', 'Closing Date', 'uid', 'URL'])

    done_df = superbase_read_all_rows('all_time_listings')
    done_df = pd.DataFrame(done_df)
    done_df.columns = ['title', 'department', 'location', 'salary', 'closing_date', 'uid', 'url', 'full_ad_text', 'scraped_date']
    uid_array = done_df['uid'].to_list()
    df['uid']=df['uid'].str.replace('Reference : ', '').astype(str)
    df_uid_array = df['uid'].to_list()
    df = df[~df['uid'].isin(uid_array)]
    df = df[~df['uid'].isin(df_uid_array)]

    if df.shape[0] == 0:
        print('no new data')
        return 0
    else:
        #removed table create_scraped_data SQL (create table & import), added table to clean_staging_tables
        renamed_df = df
        renamed_df.columns = ['title', 'department', 'location', 'salary', 'closing_date', 'uid', 'url']
        print('issue here?')
        supabase_write_rows(renamed_df, 'scraped_data', renamed_df.columns)
        print('finished scrape')
        return 1
    
def full_ad(df: pd.DataFrame):
    table_name = 'scraped_data'
    df.columns=['Title', 'Department', 'Location', 'Salary', 'Closing Date', 'uid', 'URL']
    existing_rows = superbase_read_all_rows('all_time_listings')
    existing_rows = pd.DataFrame(existing_rows)
    df_uids = df['uid']
    existing_uids = existing_rows['uid']
    try:
        if set(df.dtypes) != set(existing_uids.dtypes):
            df['uid'] = df['uid'].astype(existing_rows['uid'].dtype)
        existing_uids = existing_rows['uid'].tolist()
        old_shape = df.shape
        df = df[~df['uid'].isin(existing_uids)]
        print(f'found some uids that have already been processed - now filtered from reprocessing. Old shape: {old_shape}, New shape: {df.shape}')

    except:
        pass
    if df.shape[0] == 0:
        print('no new data')
        return df
    print('starting full_ad')
    job_uids = df['uid']
    job_urls = df['URL']
    html = []
    page_texts = []
    counter = 0

    try:
        for i in job_urls:
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            driver = webdriver.Chrome(options=options)
            driver.get(i)
            driver.page_source
            html.append(driver.page_source)
            driver.quit()

            for page_html in html:

                soup = BeautifulSoup(page_html, 'html.parser')    
                relevant_divs = soup.find('div', class_='vac_display_panel_main')
                page_content = []  
                for page_div in relevant_divs:    
                    try: 
                        full_text = page_div.get_text().strip().splitlines()
                        page_content.append((job_uids[counter], full_text))
                    except Exception as e:
                        pass     
                page_texts.append(page_content)
                print(f'added {len(page_texts)} pages so far')
                counter += 1
                print('now parsing page :',counter)
            html = []
    except Exception as e:
        print('job_url loop failed because:', e)
    try: 
        print('starting page_texts_dict', len(page_texts))
        page_texts_dict = {}
        for i in page_texts:
            try:
                page_texts_dict[i[0][0]] = i[0][1]
                print('added to page_texts_dict')
            except Exception as e:
                print(i)
                print('error when trying to add to page_texts_dict: ', e)
                continue
        page_texts_df = pd.DataFrame(page_texts_dict.items(), columns=["uid", "Full Text"])
        page_texts_df['uid'] = page_texts_df['uid'].str.replace('Reference : ', '').astype(str)
        #removed create)full_ad_text SQL (create table & import), added table to clean_staging_tables
        page_texts_df['scraped_date'] = str(todays_date)
        page_texts_df.columns = ['uid', 'full_ad_text', 'scraped_date']
        supabase_write_rows(page_texts_df, 'full_ad_text')
        return page_texts_df
    except Exception as e:
        print(e)
if __name__ == "__main__":
    superbase_delete_all_rows('scraped_data', 'uid')
    new_values = scrape(button_click())
    if new_values == 0:
        print('no new values, ending script')
    scraped_df = superbase_read_all_rows('scraped_data')
    full_ad(pd.DataFrame(scraped_df))
