import streamlit as st 
import pandas as pd
from datetime import datetime
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode
todays_date = datetime.now().date()

try: df = pd.read_csv(f'data/cleaned_data-{todays_date}.csv')
except: df = pd.read_csv(f'data/cleaned_data-2023-11-26.csv')
try: ad_qualities_df = pd.read_csv(f'data/ad_qualities-{todays_date}.csv')
except: ad_qualities_df = pd.read_csv(f'data/ad_qualities-2023-11-26.csv')

df = pd.merge(df, ad_qualities_df, on='UID', how='left')




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

# change datatype of columns title, department, location and full text to string
df['Title'] = df['Title'].astype(str)
df['Department'] = df['Department'].astype(str)
df['Location'] = df['Location'].astype(str)
df['Full Text'] = df['Full Text'].astype(str)

df = df[df['Title'].str.lower().str.contains(job_title_input) & df['Department'].str.lower().str.contains(department_input) & df['Full Text'].str.lower().str.contains(all_text_input) & df['Location'].str.lower().str.contains(location_input)]
df = df.drop('Full Text', axis=1)
df = df.drop('UID', axis=1)
number_of_vacancies = df.shape[0]
different_departments = df['Department'].nunique()
job_titles = df['Title'].nunique()
job_titles_containing_data = df['Title'].str.contains('Data').sum()
phrase_line = ''
if len(all_text_input)> 0:
        phrase_line = f'''There are {job_titles_containing_data} which contain the phrase: "{all_text_input}"'''
else:
     phrase_line = ''
# remaining_days = pd.to_datetime(df['Closing Date'].value_counts().index[0] - pd.to_datetime(todays_date)).days

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

with st.container():
        st.header(f''' Some headline points from the data:''')
        st.markdown(f''' 
        \n - **{number_of_vacancies} vacancies.** 
        \n - **Across {different_departments} departments.**
        \n - **A range of {job_titles} different job titles.** 
        \n - **{df['Location'].value_counts().index[0]} is/are the most commonly occurring location(s).**
        \n - **{df['Salary'].value_counts().index[0]} is the most commonly occurring salary.**
        \n - **The most common closing date for these positions is: {df['Closing Date'].value_counts().index[0]}.**
        \n **{phrase_line}**        
         ''')

AgGrid(df, gridOptions=gridOptions, height=500, allow_unsafe_jscode=True, allow_unsafe_html=True, width='100%')

# st.dataframe(df, width=10000, height=600, hide_index=True ) 

