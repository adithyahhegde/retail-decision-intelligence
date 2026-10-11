SELECT sku, order_date, SUM(units) AS ordered_units
FROM order_lines
WHERE order_date >= ? AND order_date <= ?
GROUP BY sku, order_date
ORDER BY sku, order_date;
