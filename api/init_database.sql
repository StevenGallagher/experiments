-- create tables
CREATE TABLE IF NOT EXISTS products (
  [product_id] INTEGER PRIMARY KEY,
  [product_name] TEXT
);

CREATE TABLE IF NOT EXISTS prices (
  [product_id] INTEGER PRIMARY KEY,
  [price] INTEGER
);

-- insert records
INSERT INTO products (product_id, product_name)
VALUES (1, 'Computer'),
       (2, 'Printer'),
       (3, 'Tablet'),
       (4, 'Desk'),
       (5, 'Chair')
;

INSERT INTO prices (product_id, price)
VALUES (1, 800),
       (2, 200),
       (3, 300),
       (4, 450),
       (5, 150)
;