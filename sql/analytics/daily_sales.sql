SELECT
    s.name AS store_name,
    DATE(sl.sale_timestamp) AS sale_date,
    COUNT(*) AS transaction_count,
    SUM(sl.subtotal) AS gross_sales,
    SUM(sl.net_sales) AS net_sales
FROM sales sl
JOIN stores s ON s.store_id = sl.store_id
GROUP BY s.name, DATE(sl.sale_timestamp)
ORDER BY sale_date DESC, gross_sales DESC;
