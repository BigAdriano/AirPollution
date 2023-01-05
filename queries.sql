
/* query to get the largest percentage increase of co in one hour intervals
SELECT  city,
        co,
        datetime_UTC,
        lead(co) OVER (PARTITION BY city ORDER BY dt DESC)
        AS co_one_before,
        lead(datetime_UTC) OVER (PARTITION BY city ORDER BY dt DESC)
        AS datetime_UTC_before,
        ROUND((((co - lead(co) OVER (PARTITION BY city ORDER BY dt DESC)) / co) * 100), 2)
        AS co_change_in_percent
FROM aogloza_parquet_test
ORDER BY 6 DESC LIMIT 10;

/* query to find the worst hour when it comes to air pollution
SELECT AVG(co + nh3 + no + no2 + o3 + pm10 + pm2_5 + so2) as sum_average, SPLIT(datetime_UTC, ' ')[2] AS hour
FROM aogloza_parquet_test
GROUP BY SPLIT(datetime_UTC, ' ')[2]
ORDER by sum_average DESC LIMIT 10

/* to find the worst city - air pollution on sum_average
SELECT AVG(co + nh3 + no + no2 + o3 + pm10 + pm2_5 + so2) as sum_average, city
FROM aogloza_parquet_test
GROUP BY city
ORDER by sum_average DESC

/* how many times daily norms of pm2.5 has been exceeded
SELECT city, COUNT(*) AS how_many FROM (SELECT city, SPLIT(datetime_UTC, ' ')[1] AS date
FROM aogloza_parquet_test
GROUP BY SPLIT(datetime_UTC, ' ')[1], city
HAVING AVG(pm2_5) > 15)
GROUP BY city
ORDER BY how_many DESC

/* how many times daily norms of pm10 has been exceeded
SELECT city, COUNT(*) AS how_many FROM (SELECT city, SPLIT(datetime_UTC, ' ')[1] AS date
FROM aogloza_parquet_test
GROUP BY SPLIT(datetime_UTC, ' ')[1], city
HAVING AVG(pm10) > 45)
GROUP BY city
ORDER BY how_many DESC

/* check how many times daily norms have been exceeded for specific pollutions
SELECT city, SUM(pm10_a) AS pm10, SUM(pm2_5_a) AS pm2_5, SUM(no2_a) AS no2, SUM(so2_a) AS so2 , SUM(co_a) AS co FROM(
SELECT city,
IF(AVG(pm10)>45,1,0) AS pm10_a,
IF(AVG(pm2_5)>15,1,0) AS pm2_5_a,
IF(AVG(no2)>25,1,0) AS no2_a,
IF(AVG(so2)>40,1,0) AS so2_a,
IF(AVG(co)>4,1,0) AS co_a
FROM aogloza_parquet_test
GROUP BY SPLIT(datetime_UTC, ' ')[1], city)
GROUP BY city