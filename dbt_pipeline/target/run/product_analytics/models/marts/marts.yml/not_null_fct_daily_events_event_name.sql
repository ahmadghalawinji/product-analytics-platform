
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select event_name
from "dev"."analytics"."fct_daily_events"
where event_name is null



  
  
      
    ) dbt_internal_test