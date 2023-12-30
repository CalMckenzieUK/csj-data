drop table if exists application_process; 
create table application_process
(
UID varchar(255) not null primary key
,CV boolean
,personal_statement boolean
,references boolean
,application_form boolean
,cover_letter boolean
,presentation boolean
,interview boolean
,portfolio boolean
,test boolean
)