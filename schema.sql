-- =============================================================================
-- schema.sql
-- Enterprise E-Commerce Order Management System — Database Schema
-- =============================================================================
-- This file is a reference/setup script for the raw database schema behind
-- the SQLAlchemy models in common/database.py. Even though SQLAlchemy's
-- init_db() can create these tables for you automatically from the Python
-- models, this .sql file is useful for:
--   1. Setting up the database manually in MySQL Workbench / pgAdmin / DBeaver
--   2. Reviewing the full schema and relationships in one place as a team
--   3. Running the sample report queries at the bottom directly for testing
--      Member 6's Reports & Analytics module before the Python code is ready
--
-- Written for MySQL (InnoDB, to support foreign keys). If your team uses
-- PostgreSQL instead, swap AUTO_INCREMENT -> SERIAL/GENERATED ALWAYS AS
-- IDENTITY and remove the ENGINE=InnoDB lines; the rest is standard SQL.
-- =============================================================================

CREATE DATABASE IF NOT EXISTS ecommerce_oms;
USE ecommerce_oms;

-- Safe re-run order: children dropped before parents.
DROP TABLE IF EXISTS shipments;
DROP TABLE IF EXISTS payments;
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS cart_items;
DROP TABLE IF EXISTS carts;
DROP TABLE IF EXISTS stock_transactions;
DROP TABLE IF EXISTS inventory;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS addresses;
DROP TABLE IF EXISTS customers;

-- =============================================================================
-- Member 1: Customer Management
-- =============================================================================
CREATE TABLE customers (
    customer_id     INT AUTO_INCREMENT PRIMARY KEY,
    name            VARCHAR(100)  NOT NULL,
    email           VARCHAR(150)  NOT NULL UNIQUE,
    phone           VARCHAR(20),
    is_active       BOOLEAN       NOT NULL DEFAULT TRUE,
    created_at      DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP
                                  ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE addresses (
    address_id      INT AUTO_INCREMENT PRIMARY KEY,
    customer_id     INT           NOT NULL,
    address_line1   VARCHAR(150)  NOT NULL,
    address_line2   VARCHAR(150),
    city            VARCHAR(80)   NOT NULL,
    state           VARCHAR(80)   NOT NULL,
    postal_code     VARCHAR(20)   NOT NULL,
    country         VARCHAR(80)   NOT NULL,
    is_default      BOOLEAN       NOT NULL DEFAULT FALSE,
    CONSTRAINT fk_addresses_customer
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        ON DELETE CASCADE
) ENGINE=InnoDB;

-- =============================================================================
-- Member 2: Product Management
-- =============================================================================
CREATE TABLE categories (
    category_id     INT AUTO_INCREMENT PRIMARY KEY,
    name            VARCHAR(100)  NOT NULL UNIQUE,
    description     VARCHAR(255)
) ENGINE=InnoDB;

CREATE TABLE products (
    product_id      INT AUTO_INCREMENT PRIMARY KEY,
    name            VARCHAR(150)  NOT NULL,
    description     TEXT,
    category_id     INT           NOT NULL,
    price           DECIMAL(10,2) NOT NULL CHECK (price >= 0),
    is_active       BOOLEAN       NOT NULL DEFAULT TRUE,
    created_at      DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP
                                  ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_products_category
        FOREIGN KEY (category_id) REFERENCES categories(category_id)
        ON DELETE RESTRICT
) ENGINE=InnoDB;

-- =============================================================================
-- Member 3: Inventory Management
-- =============================================================================
CREATE TABLE inventory (
    inventory_id        INT AUTO_INCREMENT PRIMARY KEY,
    product_id          INT           NOT NULL UNIQUE,
    quantity            INT           NOT NULL DEFAULT 0 CHECK (quantity >= 0),
    low_stock_threshold INT           NOT NULL DEFAULT 10,
    updated_at          DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP
                                       ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_inventory_product
        FOREIGN KEY (product_id) REFERENCES products(product_id)
        ON DELETE CASCADE
) ENGINE=InnoDB;

-- Full audit trail of every stock change (add stock, reduce on order, etc.)
CREATE TABLE stock_transactions (
    transaction_id  INT AUTO_INCREMENT PRIMARY KEY,
    product_id      INT           NOT NULL,
    change_qty      INT           NOT NULL,          -- positive = stock in, negative = stock out
    transaction_type ENUM('IN', 'OUT', 'ADJUSTMENT') NOT NULL,
    reason          VARCHAR(150),                    -- e.g. 'order #45 confirmed', 'restock', 'return'
    created_at      DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_stock_txn_product
        FOREIGN KEY (product_id) REFERENCES products(product_id)
        ON DELETE CASCADE
) ENGINE=InnoDB;

-- =============================================================================
-- Member 4: Cart and Order Management
-- =============================================================================
CREATE TABLE carts (
    cart_id         INT AUTO_INCREMENT PRIMARY KEY,
    customer_id     INT           NOT NULL,
    created_at      DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_carts_customer
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE cart_items (
    cart_item_id    INT AUTO_INCREMENT PRIMARY KEY,
    cart_id         INT           NOT NULL,
    product_id      INT           NOT NULL,
    quantity        INT           NOT NULL DEFAULT 1 CHECK (quantity > 0),
    CONSTRAINT fk_cart_items_cart
        FOREIGN KEY (cart_id) REFERENCES carts(cart_id)
        ON DELETE CASCADE,
    CONSTRAINT fk_cart_items_product
        FOREIGN KEY (product_id) REFERENCES products(product_id)
        ON DELETE CASCADE,
    CONSTRAINT uq_cart_product UNIQUE (cart_id, product_id)
) ENGINE=InnoDB;

CREATE TABLE orders (
    order_id        INT AUTO_INCREMENT PRIMARY KEY,
    customer_id     INT           NOT NULL,
    order_date      DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status          ENUM('PENDING', 'CONFIRMED', 'SHIPPED', 'DELIVERED', 'CANCELLED')
                                  NOT NULL DEFAULT 'PENDING',
    total_amount    DECIMAL(12,2) NOT NULL DEFAULT 0.00 CHECK (total_amount >= 0),
    CONSTRAINT fk_orders_customer
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        ON DELETE RESTRICT
) ENGINE=InnoDB;

CREATE TABLE order_items (
    order_item_id   INT AUTO_INCREMENT PRIMARY KEY,
    order_id        INT           NOT NULL,
    product_id      INT           NOT NULL,
    quantity        INT           NOT NULL CHECK (quantity > 0),
    unit_price      DECIMAL(10,2) NOT NULL CHECK (unit_price >= 0),  -- price at time of order
    CONSTRAINT fk_order_items_order
        FOREIGN KEY (order_id) REFERENCES orders(order_id)
        ON DELETE CASCADE,
    CONSTRAINT fk_order_items_product
        FOREIGN KEY (product_id) REFERENCES products(product_id)
        ON DELETE RESTRICT
) ENGINE=InnoDB;

-- =============================================================================
-- Member 5: Payment and Delivery
-- =============================================================================
CREATE TABLE payments (
    payment_id      INT AUTO_INCREMENT PRIMARY KEY,
    order_id        INT           NOT NULL UNIQUE,
    amount          DECIMAL(12,2) NOT NULL CHECK (amount >= 0),
    payment_method  ENUM('CARD', 'UPI', 'NET_BANKING', 'COD', 'WALLET') NOT NULL,
    payment_status  ENUM('PENDING', 'SUCCESS', 'FAILED', 'REFUNDED') NOT NULL DEFAULT 'PENDING',
    payment_date    DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_payments_order
        FOREIGN KEY (order_id) REFERENCES orders(order_id)
        ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE shipments (
    shipment_id       INT AUTO_INCREMENT PRIMARY KEY,
    order_id          INT           NOT NULL UNIQUE,
    address_id        INT           NOT NULL,
    shipment_status   ENUM('PROCESSING', 'SHIPPED', 'OUT_FOR_DELIVERY', 'DELIVERED', 'RETURNED')
                                    NOT NULL DEFAULT 'PROCESSING',
    tracking_number   VARCHAR(50),
    shipped_date      DATETIME,
    delivered_date    DATETIME,
    CONSTRAINT fk_shipments_order
        FOREIGN KEY (order_id) REFERENCES orders(order_id)
        ON DELETE CASCADE,
    CONSTRAINT fk_shipments_address
        FOREIGN KEY (address_id) REFERENCES addresses(address_id)
        ON DELETE RESTRICT
) ENGINE=InnoDB;

-- =============================================================================
-- Helpful indexes (beyond the automatic ones on primary/unique/foreign keys)
-- =============================================================================
CREATE INDEX idx_products_category      ON products(category_id);
CREATE INDEX idx_products_active        ON products(is_active);
CREATE INDEX idx_orders_customer        ON orders(customer_id);
CREATE INDEX idx_orders_status          ON orders(status);
CREATE INDEX idx_orders_date            ON orders(order_date);
CREATE INDEX idx_order_items_product    ON order_items(product_id);
CREATE INDEX idx_inventory_quantity     ON inventory(quantity);
CREATE INDEX idx_stock_txn_product      ON stock_transactions(product_id);

-- =============================================================================
-- Sample Reports & Analytics queries (Member 6)
-- These mirror what the reports_analytics module should produce in Python;
-- useful to test/validate logic directly in SQL first.
-- =============================================================================

-- 1. Monthly sales report (total revenue and order count per month)
SELECT
    DATE_FORMAT(order_date, '%Y-%m') AS sales_month,
    COUNT(order_id)                  AS total_orders,
    SUM(total_amount)                AS total_revenue
FROM orders
WHERE status IN ('CONFIRMED', 'SHIPPED', 'DELIVERED')
GROUP BY DATE_FORMAT(order_date, '%Y-%m')
ORDER BY sales_month DESC;

-- 2. Best-selling products (by quantity sold)
SELECT
    p.product_id,
    p.name,
    SUM(oi.quantity)                 AS units_sold,
    SUM(oi.quantity * oi.unit_price) AS revenue_generated
FROM order_items oi
JOIN products p ON p.product_id = oi.product_id
JOIN orders o   ON o.order_id = oi.order_id
WHERE o.status <> 'CANCELLED'
GROUP BY p.product_id, p.name
ORDER BY units_sold DESC
LIMIT 10;

-- 3. Customer purchase history (a single customer's full order list)
SELECT
    o.order_id,
    o.order_date,
    o.status,
    o.total_amount,
    p.payment_status,
    s.shipment_status
FROM orders o
LEFT JOIN payments p  ON p.order_id = o.order_id
LEFT JOIN shipments s ON s.order_id = o.order_id
WHERE o.customer_id = :customer_id   -- replace :customer_id with an actual ID
ORDER BY o.order_date DESC;

-- 4. Pending orders (not yet delivered or cancelled)
SELECT
    o.order_id,
    c.name  AS customer_name,
    o.order_date,
    o.status,
    o.total_amount
FROM orders o
JOIN customers c ON c.customer_id = o.customer_id
WHERE o.status IN ('PENDING', 'CONFIRMED', 'SHIPPED')
ORDER BY o.order_date ASC;

-- 5. Revenue by product category
SELECT
    cat.category_id,
    cat.name                         AS category_name,
    SUM(oi.quantity * oi.unit_price) AS category_revenue
FROM order_items oi
JOIN products p     ON p.product_id = oi.product_id
JOIN categories cat ON cat.category_id = p.category_id
JOIN orders o       ON o.order_id = oi.order_id
WHERE o.status <> 'CANCELLED'
GROUP BY cat.category_id, cat.name
ORDER BY category_revenue DESC;

-- 6. Low-stock products (bonus — useful for Member 3's dashboard too)
SELECT
    p.product_id,
    p.name,
    i.quantity,
    i.low_stock_threshold
FROM inventory i
JOIN products p ON p.product_id = i.product_id
WHERE i.quantity <= i.low_stock_threshold
ORDER BY i.quantity ASC;