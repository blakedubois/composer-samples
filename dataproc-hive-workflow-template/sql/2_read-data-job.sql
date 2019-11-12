

CREATE EXTERNAL TABLE result_table
(name STRING,
 total_salary INTEGER)
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t'
STORED AS TEXTFILE LOCATION '${hivevar:OUTPUT_PATH}/output/result_table/';


INSERT OVERWRITE TABLE result_table
        SELECT name, sum(salary) FROM logs GROUP BY name;