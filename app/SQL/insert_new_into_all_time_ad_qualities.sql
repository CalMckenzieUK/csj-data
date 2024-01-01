insert into all_time_ad_qualities (
    UID
    , developing_self_and_others
    , leadership
    , making_effective_decisions
    , seeing_the_big_picture
    , managing_a_quality_service
    , working_together
    , communicating_and_influencing
    , changing_and_improving
    , delivering_at_pace
    , apply_at_advertisers_site
    , cv
    , personal_statement
    , reference_request
    , application_form
    , cover_letter
    , presentation
    , interview
    , portfolio
    , test)
select * from ad_qualities
where UID not in (select distinct(UID) from all_time_ad_qualities)