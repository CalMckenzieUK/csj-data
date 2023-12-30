drop table if exists cs_behaviours; 
create table cs_behaviours
(
UID varchar(255) not null primary key
,making_effective_decisions boolean
,changing_and_improving boolean
,seeing_the_big_picture boolean
,communicating_and_influencing boolean
,working_together boolean
,managing_a_quality_service boolean
,leadership boolean
,delivering_at_pace boolean
,developing_self_and_others boolean
)