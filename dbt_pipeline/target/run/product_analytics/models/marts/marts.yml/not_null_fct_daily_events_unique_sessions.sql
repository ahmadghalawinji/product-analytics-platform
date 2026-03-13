
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select unique_sessions
from "dev"."analytics"."fct_daily_events"
where unique_sessions is null



  
  
      
    ) dbt_internal_test