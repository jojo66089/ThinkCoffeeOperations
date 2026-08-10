SELECT
    p.name AS product,
    s.name AS store,
    COUNT(*) AS waste_incidents,
    SUM(w.quantity_wasted) AS total_wasted,
    CASE WHEN COUNT(*) > 10 THEN 'REVIEW' ELSE 'OK' END AS flag
FROM waste_events w
JOIN products p ON p.product_id = w.product_id
JOIN stores s ON s.store_id = w.store_id
WHERE w.event_timestamp >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY p.name, s.name
HAVING COUNT(*) > 5
ORDER BY waste_incidents DESC;