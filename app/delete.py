from datetime import datetime
import pandas as pd
todays_date = datetime.now().date()

todays_date_df = pd.DataFrame({'scraped_date': todays_date}, index=[0])

print(todays_date_df)