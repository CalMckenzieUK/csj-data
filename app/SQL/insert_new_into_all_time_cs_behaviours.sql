insert into all_time_cs_behaviours (
    UID
    , making_effective_decisions
    , changing_and_improving
    , seeing_the_big_picture
    , communicating_and_influencing
    , working_together
    , managing_a_quality_service
    , leadership
    , delivering_at_pace
    , developing_self_and_others)
select * from cs_behaviours
where UID not in (select distinct(UID) from all_time_cs_behaviours)