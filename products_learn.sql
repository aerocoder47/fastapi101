-- SELECT * FROM products;
-- INSERT INTO products (name, price, inventory, is_sale)
-- VALUES 
-- ('soda', 2, 10, true),
-- ('pizza', 13, 22, true),
-- ('toothbrush', 2, 8, true),
-- ('toilet paper', 4, 100, false),
-- ('xbox', 380, 45, true);

-- SELECT * FROM products;


-- SELECT * FROM products WHERE inventory > 0 AND price >= 20;


-- SELECT * FROM products WHERE id = 1 OR id = 2 OR id = 3;
-- SELECT * FROM products WHERE id IN (1,2,3);

-- SELECT * FROM products;

-- UPDATE products SET name = 'TV YELLOW' WHERE id = 15;

-- name starts with TV
-- SELECT * FROM products WHERE name LIKE 'TV%';

-- SELECT * FROM products ORDER BY inventory DESC, price;

-- SELECT * FROM products ORDER BY id LIMIT 5 OFFSET 2;

-- INSERT INTO products (name, price, inventory) 
-- VALUES 
-- ('Laptop', 50, 25),
-- ('Monitor', 60, 4)
-- returning *;

-- SELECT * FROM products;

DELETE FROM products WHERE id = 11 returning *;
DELETE FROM products WHERE inventory = 0 returning *;

UPDATE products SET name = 'Soda' WHERE id = 10 returning *;
UPDATE products SET name = 'Flour Tortilla', price = 40 WHERE id = 18 returning *;

SELECT * FROM products;





