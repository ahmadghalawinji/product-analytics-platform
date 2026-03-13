
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select lifetime_session_count
from "dev"."analytics"."dim_users"
where lifetime_session_count is null



  
  
      
    ) dbt_internal_test