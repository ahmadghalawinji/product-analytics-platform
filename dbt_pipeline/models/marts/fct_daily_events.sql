select
    event_date,
    event_name,
    device_type,
    country,
    count(*) as total_events,
    count(distinct user_id) as unique_users,
    count(distinct session_id) as unique_sessions
from {{ ref('stg_events') }}
group by 1, 2, 3, 4
