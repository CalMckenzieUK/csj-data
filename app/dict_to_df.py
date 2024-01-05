import pandas as pd
from datetime import datetime
todays_date = datetime.now().date()
from app.databaseconnection import database_query
from app.nlp_analysis import application_process, apply_at_advertisers_site, civil_service_behaviours

def dict_to_df(input, dict_name):
    uids = []
    data  = []
    
    for i in input:
       uids.append(i[0])
       if type(i[1]) == dict:
           data.append(i[1])
       else:
           temp_dict = {}
           for dicts in i[1]:
               temp_dict.update(dicts)
           data.append(temp_dict)
    df = pd.DataFrame(data, index=uids)
    df.index.name = 'UID'
    #turn index into column
    df.reset_index(level=0, inplace=True)


    database_query(f"DROP TABLE IF EXISTS {dict_name};")
    with open(f'app/SQL/create_{dict_name}.sql', 'r') as file:
        create_table_sql = file.read()
    database_query(create_table_sql)
    table_columns = database_query(f"SHOW COLUMNS FROM {dict_name};")
    table_columns = [i[0] for i in table_columns]
    table_columns = ', '.join(table_columns).strip('[').strip(']')
    rows = [tuple(x) for x in df.to_numpy()]
    for i in rows:
        element = []
        for j in range(len(i)):
            element.append(i[j])
        element = ', '.join(str(e) for e in element).strip('[').strip(']')
        database_query(f"""insert into {dict_name} ({table_columns}) values ({element})""")



def dict_to_df_full_text(input, dict_name):
    uids = []
    data  = []
    temp_dict = {}
    for key, value in input.items():
            uids.append(key)
            temp_dict['Full Text'] = value
    data.append(temp_dict)
    df = pd.DataFrame(data, index=uids)
    df.index.name = 'UID'




def dict_to_def_setup_and_execution():

    # with open(f'data/dicts/application_process_dict.txt', 'r') as f:
    #     application_process_dict = eval(f.read())
    full_text = pd.DataFrame(database_query('select * from full_ad_text limit 100;'), columns=['UID', 'Full Text', 'Scraped Date'])
    application_process_dict = application_process(full_text)
    # with open(f'data/dicts/apply_at_advertisers_site.txt', 'r') as f:
    #     apply_at_advertisers_sites_dict = eval(f.read())
    apply_at_advertisers_sites_dict = apply_at_advertisers_site(full_text)

    # with open(f'data/dicts/csb.txt', 'r') as f:
    #     csb_dict = eval(f.read())
    csb_dict = civil_service_behaviours(full_text)





    dict_to_df(csb_dict, 'cs_behaviours')
    dict_to_df(apply_at_advertisers_sites_dict, 'apply_at_advertisers_site')
    dict_to_df(application_process_dict, 'application_process')


if __name__ == '__main__':
    dict_to_def_setup_and_execution()