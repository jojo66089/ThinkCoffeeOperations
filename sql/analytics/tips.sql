WITH weekly_hours AS (
    SELECT
        DATE_TRUNC('week', shift_date) AS week_start,
        employee_id,
        SUM(EXTRACT(EPOCH FROM (end_time - start_time)) / 3600) AS hours_worked
    FROM shifts
    GROUP BY DATE_TRUNC('week', shift_date), employee_id
),
weekly_tips AS (
    SELECT
        DATE_TRUNC('week', sale_timestamp) AS week_start,
        SUM(tip_amount) AS tip_pool
    FROM sales
    GROUP BY DATE_TRUNC('week', sale_timestamp)
)
SELECT
    wh.week_start,
    e.full_name,
    wh.hours_worked,
    wt.tip_pool,
    ROUND(
        wh.hours_worked / SUM(wh.hours_worked) OVER (PARTITION BY wh.week_start) * wt.tip_pool,
        2
    ) AS tip_share
FROM weekly_hours wh
JOIN weekly_tips wt ON wt.week_start = wh.week_start
JOIN employees e ON e.employee_id = wh.employee_id
ORDER BY wh.week_start DESC, tip_share DESC;