import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from datetime import datetime, date
todays_date = date.today()

def button_click():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get('https://www.civilservicejobs.service.gov.uk/csr/index.cgi')
    driver.find_element(By.NAME, 'search_button').click()
    #sleep(5)
    all_results_pages = []
    html = driver.page_source
    all_results_pages.append(html)
    print(all_results_pages)
    for i in range(len(all_results_pages)):
        try:
            driver.find_element(By.LINK_TEXT, f'{i}').click()
            all_results_pages.append(driver.page_source)
        except:
            break
    driver.quit()
    print(len(all_results_pages))
    return all_results_pages

def scrape(url):
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
            except:
                pass
        
    
    df = pd.DataFrame(job_data, columns=['Title', 'Department', 'Location', 'Salary', 'Closing Date', 'UID', 'URL'])
    todays_date = date.today()
    df.to_csv(f'/workspaces/flask_app/data/data-{todays_date}.csv', index=False)
    return df
    
def full_ad(df):
    print('starting full_ad function')
    job_uids = df['UID']
    job_urls = df['URL']
    html = []
    for i in job_urls:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)
        driver.get(i)
        driver.page_source
        html.append(driver.page_source)
        driver.quit()
        print('finished scraping job ', i)
    page_texts = []
    counter = 0
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
        counter += 1
        page_texts.append(page_content)
    page_texts_dict = {}
    for i in page_texts:
        print(i[0][0])
        page_texts_dict[i[0][0]] = i[0][1]
        
    page_texts_df = pd.DataFrame(page_texts_dict.items(), columns=["UID", "Full Text"])
    page_texts_df.to_csv(f'/workspaces/flask_app/data/full_ad_text-{todays_date}.csv', index=False)
            
    return page_texts

if __name__ == '__main__':
    full_ad(scrape(button_click()))

