import pandas as pd
from datetime import datetime
todays_date = datetime.now().date()
from app.databaseconnection import database_query
from app.nlp_analysis import application_process, apply_at_advertisers_site, civil_service_behaviours
from app.clear_staging_tables import clear_staging_tables
from app.supabase_conn import superbase_read_all_rows, supabase_write_rows


def dict_to_df(input, dict_name, columns: list):
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
    df.index.name = 'uid'
    #turn index into column
    df.reset_index(level=0, inplace=True)


    #added below to replace three SQL scripts for csb_dict, apply_at_advertisers_sites_dict, application_process_dict
    clear_staging_tables({dict_name: 'uid'})
    df.columns = columns
    supabase_write_rows(df, dict_name)

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

    full_text = superbase_read_all_rows('full_ad_text')
    full_text = pd.DataFrame(full_text, columns=['uid', 'full_ad_text', 'scraped_date'])
    application_process_dict = application_process(full_text)
    apply_at_advertisers_sites_dict = apply_at_advertisers_site(full_text)
    csb_dict = civil_service_behaviours(full_text)
    dict_to_df(csb_dict, 'cs_behaviours', [
        'uid'
        ,'making_effective_decisions'
        ,'changing_and_improving'
        ,'seeing_the_big_picture'
        ,'communicating_and_influencing'
        ,'working_together'
        ,'managing_a_quality_service'
        ,'leadership'
        ,'delivering_at_pace'
        ,'developing_self_and_others'])
    dict_to_df(apply_at_advertisers_sites_dict, 'apply_at_advertisers_site', ['uid', 'apply_at_advertisers_site'])
    dict_to_df(application_process_dict, 'application_process', [
                                                                 'uid'
                                                                ,'cv'
                                                                ,'personal_statement'
                                                                ,'reference'
                                                                ,'application_form'
                                                                ,'cover_letter'
                                                                ,'presentation'
                                                                ,'interview'
                                                                ,'portfolio'
                                                                ,'test'])


if __name__ == '__main__':
    dict_to_def_setup_and_execution()