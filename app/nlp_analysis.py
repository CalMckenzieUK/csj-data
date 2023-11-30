import pandas as pd 
from datetime import datetime

todays_date = datetime.now().date() 

def application_process(df):
    uids = df['UID'].str.extract('(\d+)', expand=False).astype(int)
    texts = df['Full Text']
    
    application_process_dict = {}

    for i in range(len(df['Full Text'])):
        cv = {'CV':'False'}
        personal_statement = {'Personal Statement':'False'}
        references = {'References':'False'}
        application_form = {'Application Form':'False'}
        cover_letter = {'Cover Letter':'False'}
        presentation = {'Presentation':'False'}
        interview = {'Interview':'False'}
        portfolio = {'Portfolio':'False'}
        test = {'Test':'False'}

        if 'CV' in texts[i]:
            cv['CV'] = 'True'
        if 'Personal Statement' in texts[i]:
            personal_statement['Personal Statement'] = 'True'
        if 'References' in texts[i]:
            references['References'] = 'True'
        if 'Application Form' in texts[i]:
            application_form['Application Form'] = 'True'
        if 'Cover Letter' in texts[i]:
            cover_letter['Cover Letter'] = 'True'
        if 'Presentation' in texts[i]:
            presentation['Presentation'] = 'True'
        if 'Interview' in texts[i]:
            interview['Interview'] = 'True'
        if 'Portfolio' in texts[i]:
            portfolio['Portfolio'] = 'True'
        if 'Test' in texts[i]:
            test['Test'] = 'True'

        application_process_dict[uids[i]] = [cv, personal_statement, references, application_form, cover_letter, presentation, interview, portfolio, test]
    output_array = []
    for key, values in application_process_dict.items():
        output_array.append([key, values])
    with open(f'data/dicts/application_process_dict-{todays_date}.txt', 'w') as f:
        f.write(str(output_array))
    return application_process_dict

def apply_at_advertisers_site(df):
    uids = df['UID'].str.extract('(\d+)', expand=False).astype(int)
    texts = df['Full Text']
    apply_at_advertisers_sites_dict = {}

    for i in range(len(df['Full Text'])):
        apply_at_advertisers_sites = {"Apply at advertiser's site":False}

        if "Apply at advertiser's site" in texts[i]:
            apply_at_advertisers_sites["Apply at advertiser's site"] = True

        apply_at_advertisers_sites_dict[uids[i]] = [apply_at_advertisers_sites]
    output_array = []
    for key, values in apply_at_advertisers_sites_dict.items():
        output_array.append([key, values])
    with open(f'data/dicts/apply_at_advertisers_site-{todays_date}.txt', 'w') as f:
        f.write(str(output_array))

    return apply_at_advertisers_sites_dict

def civil_service_behaviours(df):
    uids = df['UID'].str.extract('(\d+)', expand=False).astype(int)
    texts = df['Full Text']
    civil_service_behaviours_dict = {'Seeing the Big Picture', 'Changing and Improving', 'Making Effective Decisions', 'Communicating and Influencing', 'Leadership', 'Working Together', 'Delivering at Pace', 'Managing a Quality Service', 'Developing Self and Others'}
    csb_dict = {}
    for i in range(len(df['Full Text'])):
        temp_dict = {}
        for behaviour in civil_service_behaviours_dict:
            if behaviour in texts[i]:
                temp_dict[behaviour] = 'True'
            else:
                temp_dict[behaviour] = 'False'
        csb_dict[uids[i]] = temp_dict
    output_array = []
    for key, values in csb_dict.items():
        output_array.append([key, values])
    with open(f'data/dicts/csb-{todays_date}.txt', 'w') as f:
        f.write(str(output_array))
    return csb_dict

if __name__ == "__main__":
    try:
        df = pd.read_csv(f'data/full_ad_text-{todays_date}.csv')
        application_process(df)
        apply_at_advertisers_site(df)
        civil_service_behaviours(df)
    except:
        df = pd.read_csv(f'data/full_ad_text-2023-11-29.csv')
        application_process(df)
        apply_at_advertisers_site(df)
        civil_service_behaviours(df)