WITH order_details AS (
    SELECT 
        o.id AS order_id,
        o.number AS order_number,
        c.name AS customer_name,
        o.date AS order_date,
        op.id AS order_product_id,
        p.id AS product_id,
        p.name AS product_name,
        op.quantity AS product_quantity,
        op.price AS product_price,
        op.sum AS product_total
    FROM orders o
    JOIN customers c ON o.customer_id = c.id
    JOIN orders_products op ON o.id = op.order_id
    JOIN products p ON op.product_id = p.id
),
material_costs AS (
    SELECT 
        od.order_id,
        od.order_number,
        od.customer_name,
        od.order_date,
        od.order_product_id,
        od.product_id,
        od.product_name,
        od.product_quantity,
        od.product_price,
        od.product_total,
        COALESCE(SUM(sm.quantity * m.price), 0) AS material_cost_per_unit,
        COALESCE(SUM(sm.quantity * m.price * od.product_quantity), 0) AS total_material_cost
    FROM order_details od
    LEFT JOIN specifications s ON od.product_id = s.product_id
    LEFT JOIN specifications_materials sm ON s.id = sm.spec_id
    LEFT JOIN materials m ON sm.material_id = m.id
    GROUP BY od.order_id, od.order_number, od.customer_name, od.order_date, 
             od.order_product_id, od.product_id, od.product_name, 
             od.product_quantity, od.product_price, od.product_total
)
SELECT 
    order_id,
    order_number,
    customer_name,
    order_date,
    product_name,
    product_quantity,
    product_price,
    product_total,
    material_cost_per_unit,
    total_material_cost,
    product_total - total_material_cost AS profit
FROM material_costs;