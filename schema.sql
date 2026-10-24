-- show tables;
-- DROP TABLE IF EXISTS combo, customer, menu_item, dining_table, food_order, order_item;
-- ============================================================
--  1. สร้างตารางพร้อมระบุคอลัมน์และข้อกำหนด (Constraints)
-- ============================================================
ALTER TABLE food_order AUTO_INCREMENT = 1;

CREATE TABLE customer (
    cust_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(15),
    member_tier ENUM('Bronze', 'Silver', 'Gold', 'VIP') DEFAULT 'Bronze'
);

CREATE TABLE menu_item (
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    is_available BOOLEAN DEFAULT TRUE
);

CREATE TABLE dining_table (
    table_id INT AUTO_INCREMENT PRIMARY KEY,
    seats INT NOT NULL,
    zone VARCHAR(50) DEFAULT 'Indoor'
);

CREATE TABLE food_order (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    cust_id INT,
    table_id INT NOT NULL,
    order_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    status ENUM('open', 'paid') DEFAULT 'open',
    FOREIGN KEY (cust_id) REFERENCES customer(cust_id) ON DELETE SET NULL,
    FOREIGN KEY (table_id) REFERENCES dining_table(table_id) ON DELETE CASCADE
);

CREATE TABLE order_item (
    order_id INT NOT NULL,
    item_id INT NOT NULL,
    qty INT NOT NULL DEFAULT 1,
    note VARCHAR(255),
    PRIMARY KEY (order_id, item_id),
    FOREIGN KEY (order_id) REFERENCES food_order(order_id) ON DELETE CASCADE,
    FOREIGN KEY (item_id) REFERENCES menu_item(item_id) ON DELETE CASCADE
);

CREATE TABLE combo (
    combo_id INT AUTO_INCREMENT PRIMARY KEY,
    item_id INT NOT NULL,
    sub_item_id INT NOT NULL,
    amount INT NOT NULL DEFAULT 1,
    FOREIGN KEY (item_id) REFERENCES menu_item(item_id) ON DELETE CASCADE,
    FOREIGN KEY (sub_item_id) REFERENCES menu_item(item_id) ON DELETE CASCADE
);

-- ============================================================
--  2. INSERT ข้อมูลตัวอย่าง (Sample Data)
-- ============================================================

-- 2.1 ข้อมูลลูกค้า (customer)
INSERT INTO customer (name, phone, member_tier) VALUES
('กิตติพงษ์ มั่นคง', '0861112223', 'VIP'),
('สมสี มีใจ', '0877888999', 'VIP'),
('สมชาย ใจดี', '0812345678', 'Gold'),
('กัยตินัน หน่อยชำนาน', '0878855662', 'Gold'),
('วิภาดา รักดี', '0898765432', 'Silver'),
('ภูสิทธิ์ ถินนอก', '0826648753', 'Silver'),
('อาบาตาคำ ไม่ไหวเเล้ว', '0836644125', 'Bronze'),
('อนันต์ มีสุข', '0855556666', 'Bronze');
-- 2.2 ข้อมูลรายการอาหาร/เครื่องดื่ม (menu_item)
INSERT INTO menu_item (name, category, price, is_available) VALUES
('ข้าวมันไก่', 'Main', 60.00, TRUE),           
('ข้าวผัดกุ้ง', 'Main', 80.00, TRUE),           
('ต้มยำกุ้ง', 'Main', 150.00, TRUE),          
('ชาดำเย็น', 'Drink', 30.00, TRUE),            
('น้ำอัดลม', 'Drink', 25.00, TRUE),            
('เซ็ตสุดคุ้ม A', 'Combo', 150.00, TRUE),       
('เซ็ตครอบครัว B', 'Combo', 300.00, TRUE);      

-- 2.3 ข้อมูลโต๊ะอาหาร (dining_table)
INSERT INTO dining_table (seats, zone) VALUES
(2, 'Indoor'),    -- table_id = 1
(4, 'Indoor'),    -- table_id = 2
(4, 'Outdoor'),   -- table_id = 3
(8, 'VIP Room'),  -- table_id = 4
(5, 'Indoor'),    
(6, 'Indoor'),    
(5, 'Outdoor'),   
(10, 'VIP Room');  

-- 2.4 ข้อมูลคำสั่งซื้อ (food_order)
-- *มี status 'open' อยู่ที่ table_id = 2 เพื่อรองรับการทดสอบ "เปิดออเดอร์ซ้ำโต๊ะเดิมไม่ได้"*
INSERT INTO food_order (cust_id, table_id, order_time, status) VALUES
(1, 1, '2026-10-07 12:00:00', 'paid'),   
(2, 2, NOW(), 'open'),                   
(3, 3, NOW(), 'open');                   

-- 2.5 ข้อมูลรายการที่สั่งในออเดอร์ (order_item)
INSERT INTO order_item (order_id, item_id, qty, note) VALUES
-- Order 1
(1, 1, 2, 'ไม่เอาหนัง'),
(1, 4, 2, 'หวานน้อย'),
-- Order 2 (โต๊ะ 2)	
(2, 6, 1, 'เผ็ดปกติ'),
(2, 5, 1, 'ขอแก้วใส่น้ำแข็ง'),
-- Order 3 (โต๊ะ 3)
(3, 3, 1, 'เผ็ดมาก'),
(3, 2, 2, 'ไม่ใส่ผักกาดหอม');

-- 2.6 ข้อมูลชุด Combo (combo)
-- เชื่อมโยงเมนูชุดกับเมนูย่อย
INSERT INTO combo (item_id, sub_item_id, amount) VALUES
-- เซ็ตสุดคุ้ม A (item_id 6) ประกอบด้วย ข้าวมันไก่ (1) + ชาดำเย็น (4)
(6, 1, 1),
(6, 4, 4),
-- เซ็ตครอบครัว B (item_id 7) ประกอบด้วย ข้าวผัดกุ้ง (2) + ต้มยำกุ้ง (3) + น้ำอัดลม (5) 2 ขวด
(7, 2, 2),
(7, 3, 1),
(7, 5, 2);
