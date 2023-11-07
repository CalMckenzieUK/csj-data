import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

#function that goes to webpage, clicks a button called 'search', and returns the html of the page
def button_click():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get('https://www.civilservicejobs.service.gov.uk/csr/index.cgi')
    driver.find_element(By.NAME, 'search_button').click()
    #sleep(5)
    all_results_pages = []
    page = 1
    html = driver.page_source
    driver.quit()
    return html

def scrape(url):
    soup = BeautifulSoup(url, 'html.parser')
    job_postings = soup.find_all('li', class_='search-results-job-box')
    job_data = []
    for posting in job_postings:
        try: 
            ad = posting.get_text().strip().splitlines()
            ad = list(filter(None, ad))
            print(ad)
            title = ad[0]
            department = ad[1]
            location = ad[2]
            salary = ad[3]
            closing_date = ad[4]
            uid = ad[5]
            job_data.append([title, department, location, salary, closing_date, uid])
        except:
            pass
    
    df = pd.DataFrame(job_data, columns=['Title', 'Department', 'Location', 'Salary', 'Closing Date', 'UID'])
    print(df)
    

scrape(button_click())
# Loop through each job posting and extract details
ads = scrape()
