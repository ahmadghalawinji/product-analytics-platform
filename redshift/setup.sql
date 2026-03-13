-- Raw layer (10M events loaded)
DROP TABLE IF EXISTS raw_data.events;
CREATE TABLE raw_data.events (...);  -- Your exact CREATE
COPY raw_data.events FROM 's3://ahmad-ghalawinji...' ...;
