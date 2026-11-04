import os
import sqlite3
from database import get_db_connection
from config import BASE_DIR

def init_database():
    """Đảm bảo CSDL được khởi tạo theo schema chuẩn 3NF refactored."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Kiểm tra xem bảng Booking_Master đã tồn tại chưa
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Booking_Master'")
    if not cursor.fetchone():
        schema_path = os.path.join(BASE_DIR, 'db', 'schema_refactored.sql')
        if os.path.exists(schema_path):
            with open(schema_path, 'r', encoding='utf-8') as f:
                schema_sql = f.read()
            cursor.executescript(schema_sql)
            conn.commit()

    conn.close()
