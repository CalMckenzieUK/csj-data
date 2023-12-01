import streamlit as st 
import pandas as pd
from datetime import datetime
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode
from app.databaseconnection import database_query
todays_date = datetime.now().date()

try: df = new_df = pd.DataFrame(database_query('select * from ad_qualities limit 6;'), columns=['job_uid', 
        'developing_self_and_others', 
        'leadership',
        'making_effective_decisions',
        'seeing_the_big_picture',
        'managing_a_quality_service',
        'working_together',
        'communicating_and_influencing',
        'changing_and_improving',
        'delivering_at_pace',
        'apply_at_advertisers_site',
        'cv',
        'personal_statement',
        'reference_request',
        'application_form',
        'cover_letter',
        'presentation',
        'interview',
        'portfolio',
        'test'] )
except: df = pd.read_csv(f'data/cleaned_data-2023-11-29.csv')
df['Salary'] = df['Salary'].fillna('0')
df['Salary_int'] = df['Salary'].str.replace(',', '').astype(int)
#basic metrics from dataframe
st.set_page_config(layout="wide")
max_sal = df['Salary_int'].max()

df['Full Text'] = df['Full Text'].astype(str)
# job_title_input = st.text_input('Search for a job title').lower()
st.sidebar.title('Filters')
st.sidebar.subheader('Job Title')
job_title_input = st.sidebar.text_input('Search for a job title').lower()
st.sidebar.subheader('Department')
department_input = st.sidebar.text_input('Search for a department').lower()
# st.sidebar.subheader('All text in ad')
# all_text_input = st.sidebar.text_input('Search all text in ad for a keyword').lower()
st.sidebar.subheader('Location')
location_input = st.sidebar.text_input('Search for a location').lower()
st.sidebar.subheader('Salary range slider')
salary_range = st.sidebar.slider('Salary range', 0, max_sal, (0, max_sal))





if st.sidebar.button('Clear Filters'):
    job_title_input = ''
    department_input = ''

#filter dataframe by job title
df = df[df['Title'].str.lower().str.contains(job_title_input) & df['Department'].str.lower().str.contains(department_input) & 
        # df['Full Text'].str.lower().str.contains(str(all_text_input)) & 
        df['Location'].str.lower().str.contains(location_input) & df['Salary_int'].between(salary_range[0], salary_range[1])]
job_texts_containing_data = df.shape[0]
phrase_line = ''
# if len(all_text_input)> 0:
#         phrase_line = f'''Showing ads which contain the word "{all_text_input}"'''
# else:
#      phrase_line = ''

df = df.drop('Full Text', axis=1)
df = df.drop('UID', axis=1)
df = df.drop('Salary_int', axis=1)
number_of_vacancies = df.shape[0]
different_departments = df['Department'].nunique()
job_titles = df['Title'].nunique()
job_titles_containing_data = df['Title'].str.contains(job_title_input).sum()




gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_column("URL",
                    headerName="URL",
                    cellRenderer=JsCode(
                        """
                        class UrlCellRenderer {
                                init(params) {
                                this.eGui = document.createElement('a');
                                this.eGui.innerText = 'Link';
                                this.eGui.setAttribute('href', params.value);
                                this.eGui.setAttribute('style', "text-decoration:none");
                                this.eGui.setAttribute('target', "_blank");
                                        }
                                getGui() {
                                return this.eGui;
                                        }
                                }       
                        """))
gb.configure_default_column(min_column_width=235)
gridOptions = gb.build()


st.write(f''' \n Some headline stats from the data: 
        
        Number of vacancies: {number_of_vacancies} 
        Across {different_departments} departments
        A range of {job_titles} job titles
        {phrase_line}  
         ''')
output_df = df[['Title', 'Department','Location', 'Salary', 'Closing Date', 'URL']]
AgGrid(output_df, gridOptions=gridOptions, height=500, allow_unsafe_jscode=True, allow_unsafe_html=True, width='100%')