WITH product_revenue AS (
    SELECT
        p.name,
        p.category,
        SUM(si.quantity * si.unit_price_at_sale) AS total_revenue
    FROM sale_items si
    JOIN products p ON p.product_id = si.product_id
    GROUP BY p.name, p.category
)
SELECT
    name,
    category,
    total_revenue,
    RANK() OVER (PARTITION BY category ORDER BY total_revenue DESC) AS rank_in_category
FROM product_revenue
ORDER BY total_revenue DESC;
 
 