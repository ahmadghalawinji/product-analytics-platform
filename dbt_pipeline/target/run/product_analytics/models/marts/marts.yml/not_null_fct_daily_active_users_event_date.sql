
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select event_date
from "dev"."analytics"."fct_daily_active_users"
where event_date is null



  
  
      
    ) dbt_internal_test