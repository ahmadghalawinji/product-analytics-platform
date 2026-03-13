
  
    

  create  table
    "dev"."analytics"."dim_users__dbt_tmp"
    
    
    
  as (
    select
    user_id,
    min(event_timestamp) as first_seen_at,
    max(event_timestamp) as last_seen_at,
    count(*) as lifetime_event_count,
    count(distinct session_id) as lifetime_session_count
from "dev"."analytics"."stg_events"
group by 1
  );
  