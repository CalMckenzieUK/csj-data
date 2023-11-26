import pandas as pd
from datetime import datetime
todays_date = datetime.now().date()

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
    df.to_csv(f'/workspaces/flask_app/data/{dict_name}-{todays_date}.csv')

with open(f'/workspaces/flask_app/data/dicts/application_process_dict-{todays_date}.txt', 'r') as f:
    application_process_dict = eval(f.read())

with open(f'/workspaces/flask_app/data/dicts/apply_at_advertisers_site-{todays_date}.txt', 'r') as f:
    apply_at_advertisers_sites_dict = eval(f.read())

with open(f'/workspaces/flask_app/data/dicts/csb-{todays_date}.txt', 'r') as f:
    csb_dict = eval(f.read())

with open(f'/workspaces/flask_app/data/dicts/full_ad_text-{todays_date}.txt', 'r') as f:
    full_ad_text = eval(f.read())
    
# dict_to_df(csb_dict, 'cs_behaviours')
# dict_to_df(apply_at_advertisers_sites_dict, 'apply_at_advertisers_site')
# dict_to_df(application_process_dict, 'application_process')
dict_to_df(full_ad_text, 'full_ad_text')