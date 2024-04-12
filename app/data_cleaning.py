import pandas as pd
from datetime import datetime
from app.databaseconnection import database_query
from app.supabase_conn import supabase_write_rows, superbase_read_all_rows, superbase_delete_all_rows

todays_date = datetime.now().date()

csv_import = False

def cleaning():
    global csv_import
    # if csv_import == False:
    #     superbase_delete_all_rows('cleaned_data', 'uid') 
    #     superbase_delete_all_rows('ad_qualities', 'uid')   
    try: 
        
        if csv_import == False:
            df = pd.DataFrame(superbase_read_all_rows('scraped_data'))
        else:
            df = pd.DataFrame(pd.read_csv('./scraped_data.csv'))
        df.columns = ['Title', 'Department', 'Location', 'Salary', 'Closing Date', 'uid', 'URL']
    except Exception as e:        
        print('Error when trying to query database for scraped_data: ', e)
    try:
        if csv_import == False:
            df_full_ad = pd.DataFrame(superbase_read_all_rows('full_ad_text'))
        else:
            df_full_ad = pd.DataFrame(pd.read_csv('./full_ad_text.csv'))
        df_full_ad.columns = ['uid', 'Full Ad Text', 'scraped_date']
        df_full_ad['uid'] = df_full_ad['uid'].astype(str).str.replace('Reference : ', '').astype(str)
    except Exception as e:    
        print('Error when trying to query database for full_ad_text: ', e)
    df.columns = ['Title', 'Department', 'Location', 'Salary', 'Closing Date', 'uid', 'URL']

    df['uid'] = df['uid'].astype(str).str.replace('Reference : ', '').astype(str)
    df = pd.merge(df, df_full_ad, on='uid', how='left')
    df['Salary'] = df['Salary'].str.extract(r'(\d{2,3},\d{3})')
    
    if csv_import == True:
        df['Salary'] = 10
    
    #split closing date by spaces and take the last 3 items in the list
    df['Closing Date'] = df['Closing Date'].str.split().str[-3:].str.join(' ').str.replace('th', '').str.replace('rd', '').str.replace('nd', '').str.replace('st', '')

    

    closing_dates = df['Closing Date']
    closing_dates_dates = []
    for date in closing_dates:
        try:
            closing_dates_dates.append(datetime.strptime(str(date), '%d %B %Y'))
        except:
            closing_dates_dates.append(pd.to_datetime(todays_date))

    # df['Closing Date'] = pd.to_datetime(df['Closing Date'], format='%d %B %Y')
    df['Closing Date'] = closing_dates_dates
    df['Closing Date'] = df['Closing Date'].dt.date
    df['Closing Date'] = df['Closing Date'].astype(str)

    df.drop('Full Ad Text', axis=1, inplace=True)
    df['scraped_date'] = str(todays_date)
    df.columns = ['title', 'department', 'location', 'salary', 'closing_date', 'uid', 'url', 'scraped_date']
    
    print('pre')
    if df.shape[0] == 0:
        print('no new data')
    else:
        supabase_write_rows(df, 'cleaned_data')
    print('post')
    try:    
        if csv_import == False:
            csb_df = pd.DataFrame(superbase_read_all_rows('cs_behaviours'))
        else: 
            csb_df = pd.DataFrame(pd.read_csv('./cs_behaviours.csv'))
        csb_df.columns = ['uid'
                                                                                    , 'making_effective_decisions'
                                                                                    , 'changing_and_improving'
                                                                                    , 'seeing_the_big_picture'
                                                                                    , 'communicating_and_influencing'
                                                                                    , 'working_together'
                                                                                    , 'managing_a_quality_service'
                                                                                    , 'leadership'
                                                                                    , 'delivering_at_pace'
                                                                                    , 'developing_self_and_others']
    except Exception as e: print('Error when trying to query database for cs_behaviours: ', e)
    try: 
        if csv_import == False:
            apply_at_advertisers_df = pd.DataFrame(superbase_read_all_rows('apply_at_advertisers_site'))
        else:
            apply_at_advertisers_df = pd.DataFrame(pd.read_csv('./apply_at_advertisers_site.csv'))
        apply_at_advertisers_df.columns = ['uid', 'apply_at_advertisers_site']
    except Exception as e: print('Error when trying to query database for apply_at_advertisers_site: ', e)
    try: 
        if csv_import == False:
            application_process_df = pd.DataFrame(superbase_read_all_rows('application_process'))
        else: 
            application_process_df = pd.DataFrame(pd.read_csv('./application_process.csv'))
        application_process_df.columns=['uid'
                                                                                            , 'CV'
                                                                                            , 'personal_statement'
                                                                                            , 'reference'
                                                                                            , 'application_form'
                                                                                            , 'cover_letter'
                                                                                            , 'presentation'
                                                                                            , 'interview'
                                                                                            , 'portfolio'
                                                                                            , 'test']
    except Exception as e: print('Error when trying to query database for application_process: ', e)

    #csb_df columns: uid, Seeing the Big Picture, Changing and Improving, Making Effective Decisions, Communicating and Influencing, Leadership, Working Together, Delivering at Pace, Managing a Quality Service, Developing Self and Others
    #csb_df.columns = ['uid', 'Making Effective Decisions', 'Changing and Improving', 'Seeing the Big Picture', 'Communicating and Influencing', 'Working Together', 'Managing a Quality Service', 'Leadersip', 'Delivering at Pace', 'Developing Self and Others']
    #apply_at_advertisers_df.columns = ['uid', 'Apply at Advertiser\'s Site']
    #application_process_df.columns = ['uid', 'CV', 'Personal Statement', 'References', 'Application Form', 'Cover Letter', 'Presentation', 'Interview', 'Portfolio', 'Test']

    ad_qualities_df = pd.merge(csb_df, apply_at_advertisers_df, on='uid', how='left')
    ad_qualities_df = pd.merge(ad_qualities_df, application_process_df, on='uid', how='left')

    # ad_qualities_df.to_csv(f'data/ad_qualities-{todays_date}.csv', index=False)
    
    print('1')
    ad_qualities_df.columns = ['uid', 'developing_self_and_others', 'leadership', 'making_effective_decisions', 'seeing_the_big_picture', 'managing_a_quality_service', 'working_together', 'communicating_and_influencing', 'changing_and_improving', 'delivering_at_pace', 'apply_at_advertisers_site', 'cv', 'personal_statement', 'reference_request', 'application_form', 'cover_letter', 'presentation', 'interview', 'portfolio', 'test']
    supabase_write_rows(ad_qualities_df, 'ad_qualities')
    latest_ad_qualities_uids = ad_qualities_df['uid'].unique()
    all_time_ad_qualities_df = pd.DataFrame(superbase_read_all_rows('all_time_ad_qualities'))
    all_time_ad_qualities_df.columns=[
                                                                                            'uid'
    , 'developing_self_and_others'
    , 'leadership'
    , 'making_effective_decisions'
    , 'seeing_the_big_picture'
    , 'managing_a_quality_service'
    , 'working_together'
    , 'communicating_and_influencing'
    , 'changing_and_improving'
    , 'delivering_at_pace'
    , 'apply_at_advertisers_site'
    , 'cv'
    , 'personal_statement'
    , 'reference_request'
    , 'application_form'
    , 'cover_letter'
    , 'presentation'
    , 'interview'
    , 'portfolio'
    , 'test']
    # all_time_ad_qualities_uids = all_time_ad_qualities_df['uid'].unique()
    print(ad_qualities_df['uid'])
    #filter ad_qualities_df to show only uids not in all_time_ad_qualities_df
    all_time_ad_qualities_df['uid'] = all_time_ad_qualities_df['uid'].astype(int)
    ad_qualities_df['uid'] = ad_qualities_df['uid'].astype(int)
    if len(all_time_ad_qualities_df) > 0:
        ad_qualities_df = ad_qualities_df[~ad_qualities_df['uid'].isin(all_time_ad_qualities_df['uid'])]

    print('152')
    supabase_write_rows(ad_qualities_df, 'all_time_ad_qualities', ad_qualities_df.columns)
    print('1.5')
    todays_date_df = pd.DataFrame({'scraped_date': str(todays_date)}, index=[0])
    
    print('1.6')
    # supabase_write_rows(todays_date_df, 'scraped_dates')
    print('2')

    print('3')
    
    cleaned_df = pd.DataFrame(superbase_read_all_rows('cleaned_data'))
    cleaned_df.columns=[
        'title',
        'department',
        'location',
        'salary',
        'closing_date',
        'uid',
        'url',
        'scraped_date']
    if csv_import == False:
        full_ad_df = pd.DataFrame(superbase_read_all_rows('full_ad_text'))
    else:
        full_ad_df = pd.DataFrame(pd.read_csv('./full_ad_text.csv'))
    full_ad_df.columns=['uid', 'full_ad_text', 'scraped_date']
    # cleaned_df['uid'] = cleaned_df['uid'].astype(int)
    cleaned_df = pd.merge(cleaned_df, full_ad_df, on='uid', how='left')
    cleaned_df = cleaned_df[['title', 'department', 'location', 'salary', 'closing_date', 'uid', 'url', 'full_ad_text', 'scraped_date_y']]
    cleaned_df.columns = ['title', 'department', 'location', 'salary', 'closing_date', 'uid', 'url', 'full_ad_text', 'scraped_date']
    latest_cleaned_uids = cleaned_df['uid'].unique()
    if csv_import == False:
        try:
            all_time_listings_df = pd.DataFrame(superbase_read_all_rows('all_time_listings'))
        except:
            all_time_listings_df = pd.DataFrame({'title':[], 'department':[], 'location':[], 'salary':[], 'closing_date':[], 'uid':[], 'url':[], 'full_ad_text':[], 'scraped_date':[]})
    else:
        try:
            all_time_listings_df = pd.DataFrame(pd.read_csv('./all_time_listings.csv'))
        except:
            all_time_listings_df = pd.DataFrame({'title':[], 'department':[], 'location':[], 'salary':[], 'closing_date':[], 'uid':[], 'url':[], 'full_ad_text':[], 'scraped_date':[]})
    all_time_listings_df.columns=['title', 'department', 'location', 'salary', 'closing_date', 'uid', 'url', 'full_ad_text', 'scraped_date']
    all_time_listings_uids = all_time_listings_df['uid'].unique()
    
    if len(all_time_listings_uids) > 0:
        cleaned_df = cleaned_df[~cleaned_df['uid'].isin(all_time_listings_uids)]
    print(cleaned_df.head())
    supabase_write_rows(cleaned_df, 'all_time_listings', cleaned_df.columns)
    print('4')

    return
    



if __name__ == '__main__':
    cleaning()
    

        