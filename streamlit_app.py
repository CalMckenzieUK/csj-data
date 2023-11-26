import streamlit as st 
import pandas as pd
from datetime import datetime
todays_date = datetime.now().date()


try: 
    df  = pd.DataFrame(pd.read_csv(f'data/data{todays_date}.csv'), index=False)
except: 
    df = pd.DataFrame(pd.read_csv(f'data/data-2023-11-25.csv'))

try:
    df_full_ad = pd.DataFrame(pd.read_csv(f'data/full_ad{todays_date}.csv'), index=False)
except:
    df_full_ad = pd.DataFrame(pd.read_csv(f'data/full_ad_text-2023-11-24.csv'))

merged_df = pd.merge(df, df_full_ad, on='UID', how='left')

#basic metrics from dataframe
number_of_vacancies = df.shape[0]
different_departments = df['Department'].nunique()
job_titles = df['Title'].nunique()
job_titles_containing_data = df['Title'].str.contains('Data').sum()
st.set_page_config(layout="wide")


st.write(f''' \n Some headline stats from the data: 
        
         Number of vacancies: {number_of_vacancies} 
         Across {different_departments} departments
         A range of {job_titles} job titles
         {job_titles_containing_data} of which contain the word "data"''')

# job_title_input = st.text_input('Search for a job title').lower()
st.sidebar.title('Filters')
st.sidebar.subheader('Job Title')
job_title_input = st.sidebar.text_input('Search for a job title').lower()
st.sidebar.subheader('Department')
department_input = st.sidebar.text_input('Search for a department').lower()

if st.sidebar.button('Clear Filters'):
    job_title_input = ''
    department_input = ''



#filter dataframe by job title
df = df[df['Title'].str.lower().str.contains(job_title_input) & df['Department'].str.lower().str.contains(department_input)]



st.dataframe(df, use_container_width=True)

