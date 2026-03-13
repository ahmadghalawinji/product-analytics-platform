SELECT COUNT(*) FROM raw_data.events;  -- 10,000,000
SELECT COUNT(DISTINCT event_id) FROM raw_data.events;  -- 9,999,999
SELECT event_name, COUNT(*) FROM raw_data.events GROUP BY 1 ORDER BY 2 DESC;
