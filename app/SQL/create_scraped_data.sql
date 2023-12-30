drop table if exists scraped_data; 
create table scraped_data
(
title varchar(255),
department varchar(255),
location text,
salary varchar(255),
closing_date varchar(255),
uid varchar(255) not null primary key,
url text
)