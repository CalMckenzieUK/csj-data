import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from datetime import datetime, date

#function that goes to webpage, clicks a button called 'search', and returns the html of the page
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
    for i in range(2,3):
        try:
            print(f'scraping page {i}')
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
        html = []
        for i in df['URL']:
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            driver = webdriver.Chrome(options=options)
            driver.get(i)
            html = driver.page_source
            driver.quit()
            
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        html = driver.page_source
        driver.quit()
        return html

if __name__ == '__main__':
    print(scrape(button_click()).head())

