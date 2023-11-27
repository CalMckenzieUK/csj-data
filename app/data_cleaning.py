import pandas as pd
from datetime import datetime
todays_date = datetime.now().date()

def cleaning():
    try: 
        df  = pd.DataFrame(pd.read_csv(f'data/data{todays_date}.csv'), index=False)
    except: 
        df = pd.DataFrame(pd.read_csv(f'data/data-2023-11-25.csv'))

    try:
        df_full_ad = pd.DataFrame(pd.read_csv(f'data/full_ad_text-{todays_date}.csv'))
    except:
        df_full_ad = pd.DataFrame(pd.read_csv(f'data/full_ad_text-2023-11-26.csv'))
    df = pd.merge(df, df_full_ad, on='UID', how='left')
    df['UID'] = df['UID'].str.replace('Reference : ', '').astype(str)
    df['Salary'] = df['Salary'].str.extract(r'(\d{2,3},\d{3})')
    #set closing date as last 18 chars of closing date
    df['Closing Date'] = pd.to_datetime(df['Closing Date'].str[-18:])
    df.to_csv(f'data/cleaned_data-{todays_date}.csv', index=False)


    try: csb_df = pd.read_csv(f'data/cs_behaviours-{todays_date}.csv')
    except: csb_df = pd.read_csv(f'/data/cs_behaviours-2023-11-26.csv')
    try: apply_at_advertisers_df = pd.read_csv(f'data/apply_at_advertisers_site-{todays_date}.csv')
    except: apply_at_advertisers_df = pd.read_csv(f'data/apply_at_advertisers_site-2023-11-26.csv') 
    try: application_process_df = pd.read_csv(f'data/application_process-{todays_date}.csv')
    except: application_process_df = pd.read_csv(f'data/application_process-2023-11-26.csv')

    ad_qualities_df = pd.merge(csb_df, apply_at_advertisers_df, on='UID', how='left')
    ad_qualities_df = pd.merge(ad_qualities_df, application_process_df, on='UID', how='left')

    ad_qualities_df.to_csv(f'data/ad_qualities-{todays_date}.csv', index=False)
if __name__ == '__main__':
    cleaning()