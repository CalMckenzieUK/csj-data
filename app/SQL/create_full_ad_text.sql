drop table if exists full_ad_text; 
create table full_ad_text
(
uid varchar(255) not null primary key,
full_ad_text text,
scraped_date varchar(255)
)