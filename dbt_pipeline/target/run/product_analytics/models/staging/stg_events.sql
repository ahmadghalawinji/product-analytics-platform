

  create view "dev"."analytics"."stg_events__dbt_tmp" as (
    select
    event_id,
    user_id,
    lower(trim(event_name)) as event_name,
    event_timestamp,
    cast(event_timestamp as date) as event_date,
    session_id,
    lower(trim(device_type)) as device_type,
    upper(trim(country)) as country,
    metadata
from "dev"."raw_data"."events"
where event_id is not null
  ) ;
