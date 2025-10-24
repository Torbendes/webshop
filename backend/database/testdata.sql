USE webshop;
GO

/* =========================================
   1️⃣ Insert Users
   ========================================= */
INSERT INTO Users (username, email, first_name, last_name, password_hash, street, house_number, postal_code, city, country)
VALUES 
('alice', 'alice@example.com', 'Alice', 'Smith', 'hashedpassword1', 'Maple Street', '12', '1000', 'Brussels', 'Belgium'),
('bob', 'bob@example.com', 'Bob', 'Johnson', 'hashedpassword2', 'Oak Avenue', '34', '2000', 'Antwerp', 'Belgium'),
('carol', 'carol@example.com', 'Carol', 'Williams', 'hashedpassword3', 'Pine Road', '56', '3000', 'Ghent', 'Belgium');
GO

/* =========================================
   2️⃣ Insert Warehouses
   ========================================= */
INSERT INTO Warehouses (name, street, house_number, postal_code, city, country, capacity, boss_employee_id)
VALUES 
('Central Warehouse', 'Warehouse Street', '1', '1000', 'Brussels', 'Belgium', 1000, NULL),
('North Warehouse', 'Northern Road', '5', '2000', 'Antwerp', 'Belgium', 500, NULL);
GO

/* =========================================
   3️⃣ Insert Employees (los van Users)
   ========================================= */
INSERT INTO Employees (first_name, last_name, role, hired_at, warehouse_id, street, house_number, postal_code, city, country)
VALUES
('Alice', 'Smith', 'manager', GETDATE(), 1, 'Maple Street', '12', '1000', 'Brussels', 'Belgium'),
('Bob', 'Johnson', 'warehouse', GETDATE(), 2, 'Oak Avenue', '34', '2000', 'Antwerp', 'Belgium');
GO

/* =========================================
   4️⃣ Insert Items (created_by = username)
   ========================================= */
INSERT INTO Items (name, description, price, created_by, is_available)
VALUES
('Laptop', 'High-end gaming laptop', 1500.00, 'alice', 1),
('Smartphone', 'Latest model smartphone', 800.00, 'bob', 1),
('Headphones', 'Noise-cancelling headphones', 200.00, 'carol', 1);
GO

/* =========================================
   5️⃣ Insert Reviews (reviewer_username / reviewed_username)
   ========================================= */
-- Item reviews
INSERT INTO Reviews (reviewer_username, item_id, review_type, rating, comment)
VALUES
('bob', 1, 'item', 5, 'Great laptop, very fast!'),
('carol', 2, 'item', 4, 'Nice smartphone, battery could be better.');

-- User reviews
INSERT INTO Reviews (reviewer_username, reviewed_username, review_type, rating, comment)
VALUES
('alice', 'carol', 'user', 5, 'Carol is a very reliable seller.'),
('bob', 'alice', 'user', 4, 'Alice responds quickly and is helpful.');
GO
