
    
    

select
    event_date as unique_field,
    count(*) as n_records

from "dev"."analytics"."fct_daily_active_users"
where event_date is not null
group by event_date
having count(*) > 1


