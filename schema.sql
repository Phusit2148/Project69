-- ============================================================
--  schema.sql — ระบบร้านอาหาร (นิสิตออกแบบและเขียนเอง)
--  กติกา: 1 ออเดอร์มีหลายเมนู (M:N: order × menu_item ผ่าน order_item),
--         เมนูชุด combo = M:N (menu_item × menu_item)
--  ต้องมี: PK ทุกตาราง, FK ครบ, ชื่อตรงกับ db.py, sample data
-- ============================================================
CREATE TABLE customer (
    cust_id INT AUTO_INCREMENT PRIMARY KEY
    -- TODO: name, phone, member_tier
);
CREATE TABLE menu_item (
    item_id INT AUTO_INCREMENT PRIMARY KEY
    -- TODO: name, category, price, is_available
);
CREATE TABLE dining_table (
    table_id INT AUTO_INCREMENT PRIMARY KEY
    -- TODO: seats, zone
);
CREATE TABLE food_order (
    order_id INT AUTO_INCREMENT PRIMARY KEY
    -- TODO: cust_id (FK), table_id (FK), order_time (DATETIME), status ENUM('open','paid')
    -- ★ ไม่ต้องมีคอลัมน์ยอดรวม — คำนวณจาก order_item × menu_item (ดู search_orders ใน db.py)
);
CREATE TABLE order_item (         -- M:N: food_order × menu_item
    -- TODO: order_id (FK), item_id (FK), qty, note ; PRIMARY KEY (order_id, item_id)
    order_id INT, item_id INT
);
CREATE TABLE combo (              -- M:N: menu_item × menu_item
    combo_id INT AUTO_INCREMENT PRIMARY KEY
    -- TODO: item_id (FK -> menu_item), sub_item_id (FK -> menu_item), amount
);
-- TODO: INSERT ข้อมูลตัวอย่างทุกตาราง
--  ★ ควรมีออเดอร์ status 'open' อย่างน้อย 1 โต๊ะ ไว้ทดสอบ "เปิดออเดอร์ซ้ำโต๊ะเดิมไม่ได้"

--*************************************************************

-- show tables;
-- DROP TABLE IF EXISTS combo, customer, menu_item, dining_table, food_order, order_item;
-- ============================================================
--  1. สร้างตาราง :D
-- ============================================================

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
    -- ถ้าลบลูกค้าออก ประวัติออเดอร์ยังต้องอยู่ทำบัญชี จึงเปลี่ยน cust_id เป็น NULL
    FOREIGN KEY (cust_id) REFERENCES customer(cust_id) ON DELETE SET NULL,
    -- ลบเเล้วหายหมด
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
--  2. INSERT ข้อมูลตัวอย่าง :D
-- ============================================================

INSERT INTO customer (name, phone, member_tier) VALUES
('สมชาย ใจดี', '0812345678', 'Gold'),
('วิภาดา รักดี', '0898765432', 'Silver'),
('กิตติพงษ์ มั่นคง', '0861112223', 'VIP'),
('สมสี มีใจ', '0877888999', 'VIP'),
('ภูสิทธิ์ ถินนอก', '0826648753', 'Silver'),
('กัยตินัน หน่อยชำนาน', '0878855662', 'Gold'),
('อาบาตาคำ ไม่ไหวเเล้ว', '0836644125', 'Bronze'),
('อนันต์ มีสุข', '0855556666', 'Bronze');

INSERT INTO menu_item (name, category, price, is_available) VALUES
('ข้าวมันไก่', 'Main', 60.00, TRUE),           
('ข้าวผัดกุ้ง', 'Main', 80.00, TRUE),           
('ต้มยำกุ้ง', 'Main', 150.00, TRUE),         
('ชาดำเย็น', 'Drink', 30.00, TRUE),            
('น้ำอัดลม', 'Drink', 25.00, TRUE),           
('เซ็ตสุดคุ้ม A', 'Combo', 150.00, TRUE),       
('เซ็ตครอบครัว B', 'Combo', 300.00, TRUE);     

INSERT INTO dining_table (seats, zone) VALUES
(2, 'Indoor'),    
(4, 'Indoor'),    
(4, 'Outdoor'),   
(8, 'VIP Room');  

INSERT INTO food_order (cust_id, table_id, order_time, status) VALUES
(1, 1, '2026-10-07 12:00:00', 'paid'),   
(2, 2, NOW(), 'open'),                   
(3, 3, NOW(), 'open');                   

INSERT INTO order_item (order_id, item_id, qty, note) VALUES
(1, 1, 2, 'ไม่เอาหนัง'),
(1, 4, 2, 'หวานน้อย'),
(2, 6, 1, 'เผ็ดปกติ'),
(2, 5, 1, 'ขอแก้วใส่น้ำแข็ง'),
(3, 3, 1, 'เผ็ดมาก'),
(3, 2, 2, 'ไม่ใส่ผักกาดหอม');

INSERT INTO combo (item_id, sub_item_id, amount) VALUES
(6, 1, 1),
(6, 4, 1),
(7, 2, 1),
(7, 3, 1),
(7, 5, 2);
