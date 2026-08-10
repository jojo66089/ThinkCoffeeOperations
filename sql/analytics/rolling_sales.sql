WITH daily_totals AS (
    SELECT
        store_id,
        DATE(sale_timestamp) AS sale_date,
        SUM(net_sales) AS daily_sales
    FROM sales
    GROUP BY store_id, DATE(sale_timestamp)
)
SELECT
    s.name,
    dt.sale_date,
    dt.daily_sales,
    AVG(dt.daily_sales) OVER (
        PARTITION BY dt.store_id
        ORDER BY dt.sale_date
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS rolling_7d_avg
FROM daily_totals dt
JOIN stores s ON s.store_id = dt.store_id
ORDER BY s.name, dt.sale_date;
 