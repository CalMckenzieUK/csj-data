
insert into all_time_listings 
select * from cleaned_data left join full_ad_text on cleaned_data.uid = full_ad_text.uid
where cleaned_date.uid not in (select distintct(uid) from all_time_listings)
(
title varchar(255),
department varchar(255),
location text,
salary varchar(255),
closing_date varchar(255),
uid varchar(255) not null primary key,
url text,
full_ad_text text
)
