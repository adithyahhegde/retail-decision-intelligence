WITH line_economics AS (
    SELECT p.category, l.units, l.returned_units,
        (l.units * l.unit_price_paise - l.discount_paise) AS booked_paise,
        (l.units * l.unit_price_paise - l.discount_paise)
            * (l.units - l.returned_units) * 1.0 / l.units AS net_revenue_paise,
        (l.units - l.returned_units) * l.unit_cost_paise AS retained_cogs_paise,
        l.fulfillment_paise
    FROM order_lines l JOIN products p ON l.sku = p.sku
    WHERE l.order_date >= ? AND l.order_date <= ?
)
SELECT category, SUM(units) AS ordered_units,
    SUM(returned_units) AS returned_units,
    SUM(booked_paise) AS booked_paise,
    SUM(net_revenue_paise) AS net_revenue_paise,
    SUM(net_revenue_paise - retained_cogs_paise - fulfillment_paise) AS contribution_paise
FROM line_economics GROUP BY category ORDER BY category;
