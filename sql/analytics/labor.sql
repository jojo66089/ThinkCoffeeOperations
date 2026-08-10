WITH shift_costs AS (
    SELECT
        sh.store_id,
        sh.shift_date,
        SUM(EXTRACT(EPOCH FROM (sh.end_time - sh.start_time)) / 3600 * e.hourly_rate) AS labor_cost
    FROM shifts sh
    JOIN employees e ON e.employee_id = sh.employee_id
    GROUP BY sh.store_id, sh.shift_date
),
daily_revenue AS (
    SELECT
        store_id,
        DATE(sale_timestamp) AS sale_date,
        SUM(net_sales) AS revenue
    FROM sales
    GROUP BY store_id, DATE(sale_timestamp)
)
SELECT
    s.name,
    dr.sale_date,
    dr.revenue,
    sc.labor_cost,
    ROUND(sc.labor_cost / NULLIF(dr.revenue, 0) * 100, 2) AS labor_pct,
    CASE
        WHEN sc.labor_cost / NULLIF(dr.revenue, 0) > 0.35 THEN 'HIGH'
        WHEN sc.labor_cost / NULLIF(dr.revenue, 0) > 0.25 THEN 'MODERATE'
        ELSE 'HEALTHY'
    END AS labor_tier
FROM daily_revenue dr
JOIN shift_costs sc ON sc.store_id = dr.store_id AND sc.shift_date = dr.sale_date
JOIN stores s ON s.store_id = dr.store_id
ORDER BY dr.sale_date DESC, labor_pct DESC;