/* =========================================
   DATABASE: webshop
   PLATFORM: Microsoft SQL Server
   PURPOSE: Webshop tables
   ========================================= */

-- 1️⃣ Create database and use it
IF DB_ID('webshop') IS NULL
    CREATE DATABASE webshop;
GO

USE webshop;
GO

/* =========================================
   2️⃣ Users
   ========================================= */
CREATE TABLE Users (
    username NVARCHAR(50) PRIMARY KEY,
    email NVARCHAR(100) UNIQUE NOT NULL,
    first_name NVARCHAR(50) NOT NULL,
    last_name NVARCHAR(50) NOT NULL,
    password_hash NVARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT GETDATE(),

    -- Optional address
    street NVARCHAR(100) NULL,
    house_number NVARCHAR(10) NULL,
    postal_code NVARCHAR(15) NULL,
    city NVARCHAR(50) NULL,
    country NVARCHAR(50) NULL
);
GO

/* =========================================
   3️⃣ Warehouses
   ========================================= */
CREATE TABLE Warehouses (
    warehouse_id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(100) NOT NULL,

    -- Address
    street NVARCHAR(100) NOT NULL,
    house_number NVARCHAR(10) NOT NULL,
    postal_code NVARCHAR(15) NOT NULL,
    city NVARCHAR(50) NOT NULL,
    country NVARCHAR(50) NOT NULL,

    capacity INT CHECK (capacity >= 0),
    boss_employee_id INT NULL
);
GO

/* =========================================
   4️⃣ Employees
   ========================================= */
CREATE TABLE Employees (
    employee_id INT IDENTITY(1,1) PRIMARY KEY,
    first_name NVARCHAR(50) NOT NULL,
    last_name NVARCHAR(50) NOT NULL,
    role NVARCHAR(50) NOT NULL,
    hired_at DATETIME DEFAULT GETDATE(),
    warehouse_id INT NULL,

    -- Optional address
    street NVARCHAR(100) NULL,
    house_number NVARCHAR(10) NULL,
    postal_code NVARCHAR(15) NULL,
    city NVARCHAR(50) NULL,
    country NVARCHAR(50) NULL,

    -- Foreign key naar Warehouses
    CONSTRAINT FK_Employees_Warehouse FOREIGN KEY (warehouse_id)
        REFERENCES Warehouses(warehouse_id) 
        ON DELETE SET NULL
);
GO

/* =========================================
   5️⃣ Items
   ========================================= */
CREATE TABLE Items (
    item_id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(100) NOT NULL,
    description NVARCHAR(MAX),
    price DECIMAL(10,2) CHECK (price >= 0),
    created_by NVARCHAR(50) NULL,
    created_at DATETIME DEFAULT GETDATE(),
    is_available BIT DEFAULT 0,

    CONSTRAINT FK_Items_CreatedBy FOREIGN KEY (created_by)
        REFERENCES Users(username) ON DELETE SET NULL
);
GO

/* =========================================
   6️⃣ Reviews (for items or users)
   ========================================= */
CREATE TABLE Reviews (
    review_id INT IDENTITY(1,1) PRIMARY KEY,
    reviewer_username NVARCHAR(50) NOT NULL,
    reviewed_username NVARCHAR(50) NULL,
    item_id INT NULL,
    review_type NVARCHAR(10) NOT NULL CHECK (review_type IN ('item','user')),
    rating INT CHECK (rating BETWEEN 1 AND 5),
    comment NVARCHAR(MAX),
    created_at DATETIME DEFAULT GETDATE(),

    -- Foreign keys
    CONSTRAINT FK_Reviews_Reviewer FOREIGN KEY (reviewer_username) 
        REFERENCES Users(username) ON DELETE CASCADE,

    CONSTRAINT FK_Reviews_ReviewedUser FOREIGN KEY (reviewed_username) 
        REFERENCES Users(username) ON DELETE NO ACTION,

    CONSTRAINT FK_Reviews_Item FOREIGN KEY (item_id) 
        REFERENCES Items(item_id) ON DELETE CASCADE,

    -- Ensure review is either for an item OR a user, not both
    CONSTRAINT CK_Reviews_Target CHECK (
        (review_type = 'item' AND item_id IS NOT NULL AND reviewed_username IS NULL) OR
        (review_type = 'user' AND reviewed_username IS NOT NULL AND item_id IS NULL)
    )
);
GO

/* =========================================
   7️⃣ ItemPhotos
   ========================================= */
CREATE TABLE ItemPhotos (
    photo_id INT IDENTITY(1,1) PRIMARY KEY,
    item_id INT NOT NULL,
    photo_data VARBINARY(MAX) NOT NULL,
    created_at DATETIME DEFAULT GETDATE(),

    CONSTRAINT FK_ItemPhotos_Item FOREIGN KEY (item_id)
        REFERENCES Items(item_id)
        ON DELETE CASCADE
);
GO
