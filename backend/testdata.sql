USE webshop;
-- GO mag hier, maar niet tussen DECLARE en INSERTS met variabelen

/* =========================================
   1️⃣ Declare ID variables
   ========================================= */
DECLARE @AliceId INT, @BobId INT, @CarolId INT;
DECLARE @Warehouse1Id INT, @Warehouse2Id INT;
DECLARE @Item1Id INT, @Item2Id INT, @Item3Id INT;

-- 2️⃣ Insert Users
INSERT INTO Users (username, email, first_name, last_name, password_hash, street, house_number, postal_code, city, country)
VALUES ('alice', 'alice@example.com', 'Alice', 'Smith', 'hashedpassword1', 'Maple Street', '12', '1000', 'Brussels', 'Belgium');
SET @AliceId = SCOPE_IDENTITY();

INSERT INTO Users (username, email, first_name, last_name, password_hash, street, house_number, postal_code, city, country)
VALUES ('bob', 'bob@example.com', 'Bob', 'Johnson', 'hashedpassword2', 'Oak Avenue', '34', '2000', 'Antwerp', 'Belgium');
SET @BobId = SCOPE_IDENTITY();

INSERT INTO Users (username, email, first_name, last_name, password_hash, street, house_number, postal_code, city, country)
VALUES ('carol', 'carol@example.com', 'Carol', 'Williams', 'hashedpassword3', 'Pine Road', '56', '3000', 'Ghent', 'Belgium');
SET @CarolId = SCOPE_IDENTITY();

-- 3️⃣ Insert Warehouses
INSERT INTO Warehouses (name, street, house_number, postal_code, city, country, capacity, boss_employee_id)
VALUES ('Central Warehouse', 'Warehouse Street', '1', '1000', 'Brussels', 'Belgium', 1000, NULL);
SET @Warehouse1Id = SCOPE_IDENTITY();

INSERT INTO Warehouses (name, street, house_number, postal_code, city, country, capacity, boss_employee_id)
VALUES ('North Warehouse', 'Northern Road', '5', '2000', 'Antwerp', 'Belgium', 500, NULL);
SET @Warehouse2Id = SCOPE_IDENTITY();

-- 4️⃣ Insert Employees
INSERT INTO Employees (user_id, role, hired_at, warehouse_id, street, house_number, postal_code, city, country)
VALUES (@AliceId, 'manager', GETDATE(), @Warehouse1Id, 'Maple Street', '12', '1000', 'Brussels', 'Belgium');

INSERT INTO Employees (user_id, role, hired_at, warehouse_id, street, house_number, postal_code, city, country)
VALUES (@BobId, 'warehouse', GETDATE(), @Warehouse2Id, 'Oak Avenue', '34', '2000', 'Antwerp', 'Belgium');

-- 5️⃣ Insert Items
INSERT INTO Items (name, description, price, created_by, is_available)
VALUES ('Laptop', 'High-end gaming laptop', 1500.00, @AliceId, 1);
SET @Item1Id = SCOPE_IDENTITY();

INSERT INTO Items (name, description, price, created_by, is_available)
VALUES ('Smartphone', 'Latest model smartphone', 800.00, @BobId, 1);
SET @Item2Id = SCOPE_IDENTITY();

INSERT INTO Items (name, description, price, created_by, is_available)
VALUES ('Headphones', 'Noise-cancelling headphones', 200.00, @CarolId, 1);
SET @Item3Id = SCOPE_IDENTITY();

-- 6️⃣ Insert Reviews
-- Item reviews
INSERT INTO Reviews (reviewer_id, item_id, review_type, rating, comment)
VALUES (@BobId, @Item1Id, 'item', 5, 'Great laptop, very fast!');

INSERT INTO Reviews (reviewer_id, item_id, review_type, rating, comment)
VALUES (@CarolId, @Item2Id, 'item', 4, 'Nice smartphone, battery could be better.');

-- User reviews
INSERT INTO Reviews (reviewer_id, reviewed_user_id, review_type, rating, comment)
VALUES (@AliceId, @CarolId, 'user', 5, 'Carol is a very reliable seller.');

INSERT INTO Reviews (reviewer_id, reviewed_user_id, review_type, rating, comment)
VALUES (@BobId, @AliceId, 'user', 4, 'Alice responds quickly and is helpful.');
