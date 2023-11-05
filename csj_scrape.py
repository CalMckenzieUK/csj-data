import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape():
# Send GET request to website URL
    
    csj_url = 'https://www.civilservicejobs.service.gov.uk/csr/index.cgi'
    csj_response = requests.get(csj_url)
    csj_soup = BeautifulSoup(csj_response.content, 'html.parser')
    csj_job_postings = csj_soup.find_all('form')
    narrowed = csj_job_postings[1]
    sid = narrowed.find('input', {'name': 'return_sid'}).get('value')
    url = 'https://www.civilservicejobs.service.gov.uk/csr/index.cgi?SID=cGFnZWNsYXNzPVNlYXJjaCZvd25lcj01MDcwMDAwJm93bmVydHlwZT1mYWlyJmNvbnRleHRpZD01NjY3NjAzMCZwYWdlYWN0aW9uPXNlYXJjaGNvbnRleHQmcmVxc2lnPTE2OTkyMTI1NTctNjUzMDUzNDE2NzcyMzA1YWIzYjZhMzEzMmY4YzNhMjFmMzQxYTk3ZA=='
#    url = f'https://www.civilservicejobs.service.gov.uk/csr/index.cgi?SID={str(sid)}'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    job_postings = soup.find_all('li', class_='search-results-job-box')
    job_data = []
    for posting in job_postings:
        ad = posting.get_text().strip().splitlines()
        title = ad[0]
        department = ad[1]
        location = ad[2]
        salary = ad[4]
        closing_date = ad[6]
        uid = ad[7]
        job_data.append([title, department, location, salary, closing_date, uid])
    
    df = pd.DataFrame(job_data, columns=['Title', 'Department', 'Location', 'Salary', 'Closing Date', 'UID'])
    print(soup.prettify()) 
    return df
    
scrape()


    
# Loop through each job posting and extract details
ads = scrape()
