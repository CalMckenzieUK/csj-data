import streamlit as st 
import pandas as pd
from datetime import datetime
todays_date = datetime.now().date()

try: df = pd.read_csv(f'data/cleaned_data-{todays_date}.csv')
except: df = pd.read_csv(f'data/cleaned_data-2023-11-26.csv')
#basic metrics from dataframe
st.set_page_config(layout="wide")



# job_title_input = st.text_input('Search for a job title').lower()
st.sidebar.title('Filters')
st.sidebar.subheader('Job Title')
job_title_input = st.sidebar.text_input('Search for a job title').lower()
st.sidebar.subheader('Department')
department_input = st.sidebar.text_input('Search for a department').lower()
st.sidebar.subheader('All text in ad')
all_text_input = st.sidebar.text_input('Search all text in ad for a keyword').lower()
st.sidebar.subheader('Location')
location_input = st.sidebar.text_input('Search for a location').lower()

if st.sidebar.button('Clear Filters'):
    job_title_input = ''
    department_input = ''

#filter dataframe by job title
df = df[df['Title'].str.lower().str.contains(job_title_input) & df['Department'].str.lower().str.contains(department_input) & df['Full Text'].str.lower().str.contains(all_text_input) & df['Location'].str.lower().str.contains(location_input)]
df = df.drop('Full Text', axis=1)
df = df.drop('UID', axis=1)
number_of_vacancies = df.shape[0]
different_departments = df['Department'].nunique()
job_titles = df['Title'].nunique()
job_titles_containing_data = df['Title'].str.contains('Data').sum()
phrase_line = ''
if len(all_text_input)> 0:
        phrase_line = f'''There are {job_titles_containing_data} which contain the word "{all_text_input}"'''
else:
     phrase_line = ''
st.write(f''' \n Some headline stats from the data: 
        
        Number of vacancies: {number_of_vacancies} 
        Across {different_departments} departments
        A range of {job_titles} job titles
        {phrase_line}         
         ''')


st.dataframe(df, use_container_width=True)

