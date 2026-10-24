# ============================================================
#  db.py — ชั้นติดต่อฐานข้อมูล  ★★★ นิสิตเขียน SQL ในไฟล์นี้ ★★★
#  มองหาคำว่า  # TODO  ทุกฟังก์ชัน — ใช้ %s เป็น placeholder เสมอ (กัน SQL injection)
# ============================================================
import mysql.connector
import config


def get_connection():
    return mysql.connector.connect(
        host=config.DB_HOST, user=config.DB_USER, password=config.DB_PASSWORD,
        database=config.DB_NAME, port=config.DB_PORT)


def run_query(sql, params=None):
    """รัน SELECT คืนผลเป็น list ของ dict"""
    conn = get_connection(); cur = conn.cursor(dictionary=True)
    cur.execute(sql, params or ()); rows = cur.fetchall()
    cur.close(); conn.close(); return rows


def run_command(sql, params=None):
    """รัน INSERT / UPDATE / DELETE แล้ว commit"""
    conn = get_connection(); cur = conn.cursor()
    cur.execute(sql, params or ()); conn.commit()
    out = {"new_id": cur.lastrowid, "affected": cur.rowcount}
    cur.close(); conn.close(); return out


def blank_to_none(value):
    """ช่องที่ไม่ได้กรอกในฟอร์มจะส่งมาเป็น "" — แปลงเป็น None (= NULL ใน SQL)
    ใช้กับคอลัมน์ที่ว่างได้ เช่น return_date, paid_date  เพราะ MySQL ไม่รับ '' เป็น DATE"""
    return None if value in ("", None) else value


def _todo(name):
    raise NotImplementedError(f"TODO: ยังไม่ได้เขียนฟังก์ชัน {name} ใน db.py")


# ---------- ลูกค้า (customer) ----------
def search_customers(filters):
    sql = "SELECT * FROM customer WHERE 1=1"
    params = []
    if "name" in filters and filters["name"]:
        sql += " AND name LIKE %s"
        params.append(f"%{filters['name']}%")
    if "phone" in filters and filters["phone"]:
        sql += " AND phone LIKE %s"
        params.append(f"%{filters['phone']}%")
    if "member_tier" in filters and filters["member_tier"]:
        sql += " AND member_tier = %s"
        params.append(filters["member_tier"])
    return run_query(sql, params)
    """ค้นหา ลูกค้า ตามเงื่อนไข (name, phone, member_tier)
    คำใบ้: เริ่มจาก sql = "SELECT * FROM customer WHERE 1=1"
    แล้วต่อเงื่อนไขเฉพาะ filter ที่มีค่า (ข้อความใช้ LIKE %s, อื่น ๆ ใช้ = %s)"""
    # TODO: เขียน SQL ค้นหาแบบยืดหยุ่นตาม filters (ใช้ %s เสมอ)
    _todo("search_customers")


def get_customer(cust_id):
    rows = run_query("SELECT * FROM customer WHERE cust_id = %s", (cust_id,))
    return rows[0] if rows else None
    """ดึง ลูกค้า 1 รายการตาม cust_id (ใช้ตอนเปิดฟอร์มแก้ไข)"""
    # TODO: SELECT * FROM customer WHERE cust_id = %s แล้วคืนแถวเดียว
    _todo("get_customer")


def create_customer(data):
    sql = "INSERT INTO customer (name, phone, member_tier) VALUES (%s, %s, %s)"
    params = (data["name"], data["phone"], data["member_tier"])
    return run_command(sql, params)
    """เพิ่ม ลูกค้า ใหม่ — data มีคีย์: name, phone, member_tier"""
    # TODO: INSERT INTO customer (...) VALUES (%s, ...)
    _todo("create_customer")


def update_customer(cust_id, data):
    sql = "UPDATE customer SET name=%s, phone=%s, member_tier=%s WHERE cust_id=%s"
    params = (data["name"], data["phone"], data["member_tier"], cust_id)
    return run_command(sql, params)
    """แก้ไข ลูกค้า ตาม cust_id"""
    # TODO: UPDATE customer SET ... WHERE cust_id=%s
    _todo("update_customer")


def delete_customer(cust_id):
    sql = "DELETE FROM customer WHERE cust_id=%s"
    return run_command(sql, (cust_id,))
    """ลบ ลูกค้า ตาม cust_id"""
    # TODO: DELETE FROM customer WHERE cust_id=%s
    _todo("delete_customer")

# ---------- เมนูอาหาร (menu_item) ----------
def search_items(filters):
    sql = "SELECT * FROM menu_item WHERE 1=1"
    params = []
    if "name" in filters and filters["name"]:
        sql += " AND name LIKE %s"
        params.append(f"%{filters['name']}%")
    if "category" in filters and filters["category"]:
        sql += " AND category = %s"
        params.append(filters["category"])
    return run_query(sql, params)
    """ค้นหา เมนูอาหาร ตามเงื่อนไข (name, category)
    คำใบ้: เริ่มจาก sql = "SELECT * FROM menu_item WHERE 1=1"
    แล้วต่อเงื่อนไขเฉพาะ filter ที่มีค่า (ข้อความใช้ LIKE %s, อื่น ๆ ใช้ = %s)"""
    # TODO: เขียน SQL ค้นหาแบบยืดหยุ่นตาม filters (ใช้ %s เสมอ)
    _todo("search_items")


def get_item(item_id):
    rows = run_query("SELECT * FROM menu_item WHERE item_id = %s", (item_id,))
    return rows[0] if rows else None
    """ดึง เมนูอาหาร 1 รายการตาม item_id (ใช้ตอนเปิดฟอร์มแก้ไข)"""
    # TODO: SELECT * FROM menu_item WHERE item_id = %s แล้วคืนแถวเดียว
    _todo("get_item")


def create_item(data):
    sql = "INSERT INTO menu_item (name, category, price, is_available) VALUES (%s, %s, %s, %s)"
    params = (data["name"], data["category"], data["price"], data["is_available"])
    return run_command(sql, params)
    """เพิ่ม เมนูอาหาร ใหม่ — data มีคีย์: name, category, price, is_available"""
    # TODO: INSERT INTO menu_item (...) VALUES (%s, ...)
    _todo("create_item")


def update_item(item_id, data):
    sql = "UPDATE menu_item SET name=%s, category=%s, price=%s, is_available=%s WHERE item_id=%s"
    params = (data["name"], data["category"], data["price"], data["is_available"], item_id)
    return run_command(sql, params)
    """แก้ไข เมนูอาหาร ตาม item_id"""
    # TODO: UPDATE menu_item SET ... WHERE item_id=%s
    _todo("update_item")


def delete_item(item_id):
    sql = "DELETE FROM menu_item WHERE item_id=%s"
    return run_command(sql, (item_id,))
    """ลบ เมนูอาหาร ตาม item_id"""
    # TODO: DELETE FROM menu_item WHERE item_id=%s
    _todo("delete_item")

# ---------- ออเดอร์ (food_order) ----------
def search_orders(filters):
    sql = """SELECT o.order_id, o.cust_id, c.name AS 'ชื่อลูกค้า', o.table_id,
                    o.order_time, o.status, IFNULL(t.total, 0) AS 'total'
             FROM food_order o
             LEFT JOIN customer c ON o.cust_id = c.cust_id
             LEFT JOIN (SELECT oi.order_id, SUM(oi.qty * mi.price) AS total
                        FROM order_item oi
                        INNER JOIN menu_item mi ON oi.item_id = mi.item_id
                        GROUP BY oi.order_id) t ON o.order_id = t.order_id
             WHERE 1=1"""
    params = []
    if filters.get("cust_id"):
        sql += " AND o.cust_id = %s"; params.append(filters["cust_id"])
    if filters.get("table_id"):
        sql += " AND o.table_id = %s"; params.append(filters["table_id"])
    if filters.get("status"):
        sql += " AND o.status = %s"; params.append(filters["status"])
    return run_query(sql, params)

    """ค้นหา ออเดอร์ ตามเงื่อนไข (cust_id, table_id, status)
    ต้องแสดงคอลัมน์: order_id, cust_id, ชื่อลูกค้า, table_id, order_time, status, total (ยอดรวม)
    คำใบ้:
      - JOIN customer เพื่อแสดงชื่อลูกค้า
      - total (ยอดรวมของออเดอร์) ไม่ได้เก็บเป็นคอลัมน์ → ต้องคำนวณ = SUM(qty × price)
        LEFT JOIN กับ subquery ที่รวมยอดของแต่ละ order_id (order_item JOIN menu_item ... GROUP BY order_id)
        แล้วใช้ IFNULL(..., 0) เพราะออเดอร์ที่ยังไม่มีรายการอาหารจะได้ NULL
      - เงื่อนไขทุกตัวใช้ = %s"""
    # TODO: เขียน SQL ค้นหาแบบยืดหยุ่นตาม filters (ใช้ %s เสมอ)
    _todo("search_orders")


def get_order(order_id):
    rows = run_query("SELECT * FROM food_order WHERE order_id = %s", (order_id,))
    if not rows:
        return None
    order = rows[0]
    order["items"] = run_query(
    "SELECT item_id, qty, note FROM order_item WHERE order_id = %s", (order_id,))
    return order



def get_order_items(order_id):
    sql = """SELECT oi.order_id, oi.item_id, mi.name AS 'ชื่อเมนู',
                    oi.qty, oi.note, mi.price, (oi.qty * mi.price) AS 'total'
             FROM order_item oi
             INNER JOIN menu_item mi ON oi.item_id = mi.item_id
             WHERE oi.order_id = %s"""
    return run_query(sql, (order_id,))

def check_table_free(table_id, order_id=None):
    sql_table = "SELECT COUNT(*) AS n FROM dining_table WHERE table_id = %s"
    rows_table = run_query(sql_table, (table_id,))
    if rows_table[0]["n"] == 0:
        raise ValueError(f"ไม่พบโต๊ะหมายเลข {table_id} ในระบบ")

    sql = "SELECT COUNT(*) AS n FROM food_order WHERE table_id = %s AND status = 'open' AND order_id <> %s"
    params = (table_id, order_id or 0)
    rows = run_query(sql, params)
    
    if rows[0]["n"] > 0:
        raise ValueError(f"โต๊ะ {table_id} ยังมีออเดอร์ที่ไม่ชำระเงิน")

def create_order(data):
    status = data.get("status") or "open"
    items = _merge_items(data.get("items"))        # ตรวจก่อน INSERT
    if status == "open":
        check_table_free(data["table_id"])
    order_time = blank_to_none(data.get("order_time")) or datetime.now()

    conn = get_connection(); cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO food_order (cust_id, table_id, order_time, status) VALUES (%s, %s, %s, %s)",
            (data["cust_id"], data["table_id"], order_time, status))
        order_id = cur.lastrowid
        cur.executemany(
        "INSERT INTO order_item (order_id, item_id, qty, note) VALUES (%s, %s, %s, %s)",
        [(order_id, i, q, n) for i, q, n in items])
        conn.commit()                               # สำเร็จทั้งหัวและรายการ หรือไม่ก็ไม่บันทึกเลย
        return {"new_id": order_id, "affected": 1}
    except Exception:
        conn.rollback(); raise
    finally:
        cur.close(); conn.close()


def update_order(order_id, data):
    status = data.get("status") or "open"
    items = _merge_items(data.get("items"))
    if status == "open":
        check_table_free(data["table_id"], order_id)
    order_time = blank_to_none(data.get("order_time")) or datetime.now()

    conn = get_connection(); cur = conn.cursor()
    try:
        cur.execute(
            "UPDATE food_order SET cust_id=%s, table_id=%s, order_time=%s, status=%s WHERE order_id=%s",
            (data["cust_id"], data["table_id"], order_time, status, order_id))
        # เก็บ note เดิมไว้ก่อนลบ แล้วใส่กลับให้เมนูที่ยังอยู่
        cur.execute("DELETE FROM order_item WHERE order_id=%s", (order_id,))
        notes = {r[0]: r[1] for r in cur.fetchall()}
        cur.execute("DELETE FROM order_item WHERE order_id=%s", (order_id,))
        cur.executemany(
    "INSERT INTO order_item (order_id, item_id, qty, note) VALUES (%s, %s, %s, %s)",
    [(order_id, i, q, n) for i, q, n in items])
        conn.commit()
        return {"new_id": None, "affected": 1}
    except Exception:
        conn.rollback(); raise
    finally:
        cur.close(); conn.close()


def delete_order(order_id):
    # order_item มี ON DELETE CASCADE ลบหัวออเดอร์ทีเดียวพอ
    return run_command("DELETE FROM food_order WHERE order_id=%s", (order_id,))


def update_order_item(order_id, item_id, data):
    return run_command("UPDATE order_item SET qty=%s, note=%s WHERE order_id=%s AND item_id=%s",
                       (data["qty"], blank_to_none(data.get("note")), order_id, item_id))


def delete_order_item(order_id, item_id):
    return run_command("DELETE FROM order_item WHERE order_id=%s AND item_id=%s",
                       (order_id, item_id))
    
def _merge_items(items):

    merged = {}
    for it in items or []:
        item_id, qty = int(it["item_id"]), int(it.get("qty") or 1)
        if qty < 1:
            raise ValueError("จำนวนต้องมากกว่า 0")
        note = (it.get("note") or "").strip()
        m = merged.setdefault(item_id, {"qty": 0, "notes": []})
        m["qty"] += qty
        if note and note not in m["notes"]:
            m["notes"].append(note)
    if not merged:
        raise ValueError("กรุณาเลือกรายการอาหารอย่างน้อย 1 รายการ")
    # คืนเป็นรายการ (item_id, qty, note) พร้อมใช้กับ executemany
    return [(i, m["qty"], blank_to_none(", ".join(m["notes"]))) for i, m in merged.items()]
# ============================================================
#  REPORT (รายงาน — ใช้ JOIN + GROUP BY + subquery)
#  ★ ชื่อคอลัมน์ใน SELECT จะกลายเป็นหัวตารางบนเว็บ — ใช้ AS 'ชื่อภาษาไทย' ได้
# ============================================================
def report_summary():
    sql = """SELECT
               (SELECT COUNT(*) FROM customer)    AS 'ลูกค้า',
               (SELECT COUNT(*) FROM menu_item)   AS 'เมนู',
               (SELECT COUNT(*) FROM food_order)  AS 'ออเดอร์',
               (SELECT IFNULL(SUM(oi.qty * mi.price), 0)
                  FROM order_item oi
                  INNER JOIN menu_item mi ON oi.item_id = mi.item_id) AS 'ยอดขายรวม',
               (SELECT COUNT(*) FROM food_order WHERE status = 'open') AS 'ออเดอร์ที่ยังไม่ชำระ',
               (SELECT IFNULL(SUM(oi.qty * mi.price), 0)
                  FROM food_order o
                  INNER JOIN order_item oi ON o.order_id = oi.order_id
                  INNER JOIN menu_item mi ON oi.item_id = mi.item_id
                  WHERE o.status = 'paid') AS 'ยอดที่ชำระแล้ว'"""
    return run_query(sql)[0]

def report_popular_items():
    sql = """SELECT mi.name AS 'เมนู', mi.category AS 'หมวดหมู่',
                    SUM(oi.qty) AS 'จำนวนที่ขายได้',
                    SUM(oi.qty * mi.price) AS 'รายได้'
             FROM order_item oi
             INNER JOIN menu_item mi ON oi.item_id = mi.item_id
             GROUP BY mi.item_id, mi.name, mi.category
             ORDER BY SUM(oi.qty) DESC
             LIMIT 5"""
    return run_query(sql)

def report_daily_sales():
    sql = """SELECT DATE(o.order_time) AS 'วันที่',
                    COUNT(DISTINCT o.order_id) AS 'จำนวนออเดอร์',
                    SUM(oi.qty * mi.price) AS 'ยอดขายรวม'
             FROM food_order o
             INNER JOIN order_item oi ON o.order_id = oi.order_id
             INNER JOIN menu_item mi ON oi.item_id = mi.item_id
             GROUP BY DATE(o.order_time)
             ORDER BY DATE(o.order_time)"""
    return run_query(sql)

def report_big_orders():
    sql = """SELECT o.order_id AS 'ออเดอร์', c.name AS 'ชื่อลูกค้า',
                    o.table_id AS 'โต๊ะ', o.status AS 'สถานะ',
                    SUM(oi.qty * mi.price) AS 'ยอดรวม'
             FROM food_order o
             INNER JOIN customer c ON o.cust_id = c.cust_id
             INNER JOIN order_item oi ON o.order_id = oi.order_id
             INNER JOIN menu_item mi ON oi.item_id = mi.item_id
             GROUP BY o.order_id, c.name, o.table_id, o.status
             HAVING SUM(oi.qty * mi.price) > 500
             ORDER BY SUM(oi.qty * mi.price) DESC"""
    return run_query(sql)


def report_top_customers():
    sql = """SELECT c.name AS 'ลูกค้า', c.member_tier AS 'ระดับ',
                    COUNT(DISTINCT o.order_id) AS 'จำนวนออเดอร์',
                    SUM(oi.qty * mi.price) AS 'ยอดซื้อรวม'
             FROM customer c
             INNER JOIN food_order o ON c.cust_id = o.cust_id
             INNER JOIN order_item oi ON o.order_id = oi.order_id
             INNER JOIN menu_item mi ON oi.item_id = mi.item_id
             GROUP BY c.cust_id, c.name, c.member_tier
             ORDER BY SUM(oi.qty * mi.price) DESC"""
    return run_query(sql)

def report_free_tables():
    sql = """SELECT t.table_id AS 'โต๊ะ', t.seats AS 'ที่นั่ง', t.zone AS 'โซน'
             FROM dining_table t
             WHERE t.table_id NOT IN (SELECT table_id FROM food_order WHERE status = 'open')
             ORDER BY t.table_id"""
    return run_query(sql)
# ============================================================
#  รายการรายงานที่แสดงบนหน้า /report  (เรียงตามลำดับที่แสดง)
#  ★ วิธีเพิ่มรายงานใหม่ (ไม่ต้องแก้ไฟล์อื่น):
#    1) เขียนฟังก์ชัน report_xxx() ด้านบน ให้ return run_query(sql)
#    2) เพิ่ม 1 บรรทัดในรายการนี้:  ("ชื่อใน-url", "หัวข้อที่แสดง", ชื่อฟังก์ชัน)
#  ★ รายการนี้ต้องอยู่ท้ายไฟล์ (หลังฟังก์ชันทั้งหมด) ไม่งั้น Python หาชื่อฟังก์ชันไม่เจอ
#  ★ ห้ามตั้งชื่อ url ว่า "summary" (ใช้แล้วสำหรับการ์ดสรุป)
# ============================================================
REPORTS = [
    ("popular-items", "📈 เมนูขายดี (Best Sellers)",        report_popular_items),
    ("daily-sales",   "💰 ยอดขายรวมต่อวัน (Daily Sales)",   report_daily_sales),
    ("big-orders",    "🧾 ออเดอร์ยอดเกิน 500 บาท (HAVING)", report_big_orders),
    ("top-customers", "👑 ลูกค้ายอดซื้อสูงสุด",              report_top_customers),
    ("free-tables",   "🪑 โต๊ะที่ว่างตอนนี้ (Subquery)",     report_free_tables),
]
