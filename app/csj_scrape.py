import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from datetime import datetime, date
from app.databaseconnection import database_query
import os
from dotenv import load_dotenv
load_dotenv()
todays_date = date.today()

def button_click():
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
    while more_pages:
        try:
            #find next button called 'Go to next results page' and click on it
            driver.find_element(By.PARTIAL_LINK_TEXT, 'next').click()
            all_results_pages.append(driver.page_source)
            print('clicked next page')
        except:
            print('no more pages')
            more_pages = False
    driver.quit()
    print('finished button_click')
    return all_results_pages

def scrape(url):
    print('starting scrape')
    job_data = []
    for i in url[0:1]:
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
            except:
                pass
        
    
    df = pd.DataFrame(job_data, columns=['Title', 'Department', 'Location', 'Salary', 'Closing Date', 'UID', 'URL'])
    todays_date = date.today()
    # df.to_csv(f'data/data-{todays_date}.csv', index=False)

    with open('app/SQL/create_scraped_data.sql', 'r') as file:
        create_table_sql = file.read()
    database_query(create_table_sql)
    
    rows = [tuple(x) for x in df.to_numpy()]
    for i in rows:
        database_query(f'''
            insert into scraped_data 
                (title
                , department
                , location
                , salary
                , closing_date
                , uid
                , url)
            values {i}''')



    print('finished scrape')
    return df
    
def full_ad(df):
    print('starting full_ad')
    job_uids = df['UID']
    job_urls = df['URL']
    html = []
    page_texts = []
    counter = 0
    for i in job_urls:
        print('now scraping: ', i)
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
            counter += 1
            print('now parsing page :',counter)
        html = []
    page_texts_dict = {}
    for i in page_texts:
        page_texts_dict[i[0][0]] = i[0][1]
    page_texts_df = pd.DataFrame(page_texts_dict.items(), columns=["UID", "Full Text"])
    with open('app/SQL/create_full_ad_text.sql', 'r') as file:
        create_table_sql = file.read()
    database_query(create_table_sql)
    
    rows = [tuple(x) for x in page_texts_df.to_numpy()]
    for i in rows:
        element = [i[0],str(i[1]).replace('[','').replace(']','')]
        database_query(f'''
            insert into full_ad_text (uid, full_ad_text) values {element[0], element[1]}''') 
    return page_texts_df

if __name__ == "__main__":
    full_ad(scrape(button_click()))


