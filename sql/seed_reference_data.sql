BEGIN;

INSERT store (store_id, store_name) VALUES
(1, 'Nomad'),
(2, 'Hudson Yards'),
(3, 'Greenwich Village')

INSERT INTO products (name, category, size, temperature, retail_price, cogs) VALUES
    -- Coffee and lattes
    ('Coffee', 'Coffee', '12oz', 'Hot', 6.50, 0.85),
    ('Coffee', 'Coffee', '16oz', 'Iced', 7.00, 1.05),
     ('Latte', 'Latte', '12oz', 'Hot', 6.50, 1.35),
     ('Latte', 'Latte', '16oz', 'Iced', 7.00, 1.65),
 
    -- Teas (single serving size, brewed from 1 lb bags)
    ('Black Tea', 'Tea', NULL, 5.00, 0.55),
    ('Green Tea', 'Tea', NULL, 5.00, 0.55),
    ('Earl Grey Tea', 'Tea', NULL, 5.00, 0.60),
    ('Ginger Tea', 'Tea', NULL, 5.00, 0.60),
    ('Orange Tea', 'Tea', NULL, 5.00, 0.55),
    ('Peppermint Tea', 'Tea', NULL, 5.00, 0.55),
 
    -- Bottled beverages (sold individually from 12 packs)
    ('Loop Juice', 'Bottled Beverage', NULL, 4.50, 1.80),
    ('Saratoga Water', 'Bottled Beverage', NULL, 3.50, 1.20),
    ('Orange Juice', 'Bottled Beverage', NULL, 4.75, 1.90),
 
    -- Pastries
    ('Plain Croissant', 'Pastry', NULL, 3.75, 1.00),
    ('Almond Croissant', 'Pastry', NULL, 4.75, 1.55),
    ('Ham and Swiss Croissant', 'Pastry', NULL, 5.50, 1.90),
    ('Chocolate Chip Cookie', 'Pastry', NULL, 3.25, 0.78),
    ('Blueberry Muffin', 'Pastry', NULL, 3.95, 0.78),
    ('Banana Chocolate Chip Muffin', 'Pastry', NULL, 3.95, 0.78);

    INSERT INTO employees (full_name, role, hourly_rate, hire_date, home_store_id) VALUES
    -- Nomad (store_id 1)
    ('Maria Delgado', 'Shift Lead', 17.50, '2019-07-01', 1),
    ('Jason Ford', 'Cook', 18.50, '2019-08-12', 1),
    ('Aisha Bello', 'Barista', 16.00, '2020-01-20', 1),
    ('Tyler Osei', 'Barista', 16.00, '2020-05-14', 1),
    ('Lena Marchetti', 'Barista', 16.00, '2021-03-02', 1),
 
    -- Hudson Yards (store_id 2)
    ('Priya Nair', 'Shift Lead', 17.50, '2021-03-01', 2),
    ('Marcus Webb', 'Cook', 18.50, '2021-03-10', 2),
    ('Sofia Reyes', 'Barista', 16.00, '2021-04-22', 2),
    ('Devon Choi', 'Barista', 16.00, '2021-07-19', 2),
    ('Hannah Brooks', 'Barista', 16.00, '2022-02-08', 2),
 
    -- Mercer (store_id 3)
    ('Camille Dubois', 'Shift Lead', 17.50, '2022-09-20', 3),
    ('Elijah Park', 'Cook', 18.50, '2022-10-01', 3),
    ('Grace Whitfield', 'Barista', 16.00, '2022-11-15', 3),
    ('Noah Feldman', 'Barista', 16.00, '2023-01-09', 3),
    ('Isabel Ortiz', 'Barista', 16.00, '2023-03-27', 3);

    COMMIT;