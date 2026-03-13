
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select session_end_at
from "dev"."analytics"."int_sessions"
where session_end_at is null



  
  
      
    ) dbt_internal_test