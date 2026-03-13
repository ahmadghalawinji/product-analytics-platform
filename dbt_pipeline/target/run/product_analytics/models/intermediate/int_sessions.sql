

  create view "dev"."analytics"."int_sessions__dbt_tmp" as (
    select
    session_id,
    min(user_id) as user_id,
    min(event_timestamp) as session_start_at,
    max(event_timestamp) as session_end_at,
    datediff(second, min(event_timestamp), max(event_timestamp)) as session_duration_seconds,
    count(*) as event_count,
    count(distinct event_name) as distinct_event_types
from "dev"."analytics"."stg_events"
where session_id is not null
group by session_id
  ) ;
