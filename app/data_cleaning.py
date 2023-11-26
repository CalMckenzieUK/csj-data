import pandas as pd
from datetime import datetime
todays_date = datetime.now().date()


try: 
    df  = pd.DataFrame(pd.read_csv(f'data/data{todays_date}.csv'), index=False)
except: 
    df = pd.DataFrame(pd.read_csv(f'data/data-2023-11-25.csv'))

try:
    df_full_ad = pd.DataFrame(pd.read_csv(f'data/full_ad_text-{todays_date}.csv'), index=False)
except:
    df_full_ad = pd.DataFrame(pd.read_csv(f'data/full_ad_text-2023-11-26.csv'))

df = pd.merge(df, df_full_ad, on='UID', how='left')
df['UID'] = df['UID'].str.replace('Reference : ', '').astype(str)
df['Salary'] = df['Salary'].str.extract(r'(\d{2,3},\d{3})')
#set closing date as last 18 chars of closing date
df['Closing Date'] = pd.to_datetime(df['Closing Date'].str[-18:])
df.to_csv(f'data/cleaned_data-{todays_date}.csv', index=False)