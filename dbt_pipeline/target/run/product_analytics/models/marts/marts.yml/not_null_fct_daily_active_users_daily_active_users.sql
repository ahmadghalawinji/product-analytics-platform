
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select daily_active_users
from "dev"."analytics"."fct_daily_active_users"
where daily_active_users is null



  
  
      
    ) dbt_internal_test