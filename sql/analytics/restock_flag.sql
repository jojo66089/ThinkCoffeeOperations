SELECT
    s.name AS store,
    p.name AS product,
    i.quantity_on_hand,
    i.reorder_threshold,
    i.last_restocked_at,
    CURRENT_DATE - i.last_restocked_at::date AS days_since_restock
FROM inventory i
JOIN stores s ON s.store_id = i.store_id
JOIN products p ON p.product_id = i.product_id
WHERE i.quantity_on_hand < i.reorder_threshold
ORDER BY (i.quantity_on_hand / i.reorder_threshold) ASC;