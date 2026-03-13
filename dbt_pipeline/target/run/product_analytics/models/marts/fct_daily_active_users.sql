
  
    

  create  table
    "dev"."analytics"."fct_daily_active_users__dbt_tmp"
    
    
    
  as (
    select
    event_date,
    count(distinct user_id) as daily_active_users
from "dev"."analytics"."stg_events"
group by 1
  );
  