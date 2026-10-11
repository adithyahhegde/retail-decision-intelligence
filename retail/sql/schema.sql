CREATE TABLE products (
    sku TEXT PRIMARY KEY,
    category TEXT NOT NULL CHECK(length(trim(category)) > 0)
) STRICT;
CREATE TABLE order_lines (
    line_id TEXT PRIMARY KEY,
    order_date TEXT NOT NULL,
    sku TEXT NOT NULL REFERENCES products(sku),
    units INTEGER NOT NULL CHECK(units > 0),
    returned_units INTEGER NOT NULL CHECK(returned_units BETWEEN 0 AND units),
    unit_price_paise INTEGER NOT NULL CHECK(unit_price_paise >= 0),
    discount_paise INTEGER NOT NULL CHECK(discount_paise >= 0 AND discount_paise <= units * unit_price_paise),
    unit_cost_paise INTEGER NOT NULL CHECK(unit_cost_paise >= 0),
    fulfillment_paise INTEGER NOT NULL CHECK(fulfillment_paise >= 0)
) STRICT;
