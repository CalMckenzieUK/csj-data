insert into application_process (
    UID
    , CV
    , personal_statement
    , references
    , application_form
    , cover_letter
    , presentation
    , interview
    , portfolio
    , test)
select * from application_process
where UID not in (select distinct(UID) from application_process)
