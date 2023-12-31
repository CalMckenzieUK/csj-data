create table if not exists all_time_listings
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

