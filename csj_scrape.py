
import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape():
# Send GET request to website URL
    url = 'https://www.civilservicejobs.service.gov.uk/csr/index.cgi?SID=cGFnZWNsYXNzPVNlYXJjaCZwYWdlYWN0aW9uPXNlYXJjaGNvbnRleHQmb3duZXI9NTA3MDAwMCZvd25lcnR5cGU9ZmFpciZjb250ZXh0aWQ9NTY1MDIwNzEmcmVxc2lnPTE2OTkwMjA0MjEtODA5ZWEzOTAzZGYyY2RmZWZlMDA4NDQyNjg5MzYyOWZiYmRkNWJjYQ=='
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
    return df
        



    
# Loop through each job posting and extract details
ads = scrape()
