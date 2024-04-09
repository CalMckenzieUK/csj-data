import pandas as pd 
from datetime import datetime


todays_date = datetime.now().date() 

def application_process(df):
    df.columns = ['UID', 'Full Text', 'Scraped Date']
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

        if 'cv' in str(texts[i]).lower():
            cv['CV'] = 'True'
        if 'personal statement' in str(texts[i]).lower():
            personal_statement['Personal Statement'] = 'True'
        if 'references' in str(texts[i]).lower():
            references['References'] = 'True'
        if 'application form' in str(texts[i]).lower():
            application_form['Application Form'] = 'True'
        if 'cover letter' in str(texts[i]).lower() or 'covering letter' in str(texts[i]).lower():
            cover_letter['Cover Letter'] = 'True'
        if 'presentation' in str(texts[i]).lower():
            presentation['Presentation'] = 'True'
        if 'interview' in str(texts[i]).lower():
            interview['Interview'] = 'True'
        if 'portfolio' in str(texts[i]).lower():
            portfolio['Portfolio'] = 'True'
        if ' test ' in str(texts[i]).lower():
            test['Test'] = 'True'

        application_process_dict[uids[i]] = [cv, personal_statement, references, application_form, cover_letter, presentation, interview, portfolio, test]
    output_array = []
    for key, values in application_process_dict.items():
        output_array.append([key, values])
    # with open(f'data/dicts/application_process_dict.txt', 'w') as f:
    #     f.write(str(output_array))
    print('finished application_process_dict')
    return output_array

def apply_at_advertisers_site(df):
    uids = df['UID'].str.extract('(\d+)', expand=False).astype(int)
    texts = df['Full Text']
    apply_at_advertisers_sites_dict = {}

    for i in range(len(df['Full Text'])):
        apply_at_advertisers_sites = {"Apply at advertiser's site":False}

        if "apply at advertiser" in str(texts[i]).lower():
            apply_at_advertisers_sites["Apply at advertiser's site"] = True

        apply_at_advertisers_sites_dict[uids[i]] = [apply_at_advertisers_sites]
    output_array = []
    for key, values in apply_at_advertisers_sites_dict.items():
        output_array.append([key, values])
    # with open(f'data/dicts/apply_at_advertisers_site.txt', 'w') as f:
    #     f.write(str(output_array))
    print('finished apply_at_advertisers_sites_dict')

    return output_array

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
    # with open(f'data/dicts/csb.txt', 'w') as f:
    #     f.write(str(output_array))
    print('finished csb_dict')

    return output_array

if __name__ == "__main__":
    from databaseconnection import database_query
    try:
        df = pd.DataFrame(database_query('select * from full_ad_text'), columns=['UID', 'Full Text', 'Scraped Date'])
        application_process(df)
        apply_at_advertisers_site(df)
        civil_service_behaviours(df)
    except Exception as e:
        print('Failed to import from full_ad_text: ', e)
else:
    from app.databaseconnection import database_query