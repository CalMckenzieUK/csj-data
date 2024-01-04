
insert into all_time_listings (title, department, location, salary, closing_date, uid, url, full_ad_text, scraped_date)
select title, department, location, salary, closing_date, cleaned_data.uid, url, full_ad_text.full_ad_text, cleaned_data.scraped_date
from cleaned_data 
left join full_ad_text on cleaned_data.uid = full_ad_text.uid
where cleaned_data.uid not in (select distinct(uid) from all_time_listings);
update all_time_listings set full_ad_text = 'No full ad text available' where full_ad_text is null;
