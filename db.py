import sqlite3
from datetime import date

DB_FILE = "my dataBase.db"

def get_db_connection():
    """Establishes a connection to the local SQLite file."""
    conn = sqlite3.connect(DB_FILE)
    # This row factory makes SQLite return records as dictionaries instead of tuples
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Creates the local database file, defines table schemas, and seeds records."""
    conn = get_db_connection()
    cur = conn.cursor()
    
    # 1. Create Table with 5 distinct data types
    cur.execute("DROP TABLE IF EXISTS inventory;")
    cur.execute("""
        CREATE TABLE inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT, -- 1. Integer
            item_name TEXT NOT NULL,              -- 2. String/Text
            price REAL NOT NULL,                  -- 3. Float/Numeric
            date_received TEXT NOT NULL,          -- 4. Date (Stored as ISO text in SQLite)
            is_fragile INTEGER NOT NULL           -- 5. Boolean (Stored as 0 or 1 in SQLite)
        );
    """)
    
    # 2. Seed Mock Data
    sample_data = [
        ("Dell Laptop", 899.99, "2026-01-15", 0),
        ("Mechanical Keyboard", 45.50, "2026-04-10", 0),
        ("Curved Monitor", 249.99, "2026-03-22", 1),
        ("USB-C Hub", 19.99, "2026-05-01", 0),
        ("Ceramic Coffee Mug", 12.00, "2026-02-28", 1),
        ("Wireless Mouse", 29.99, "2026-05-20", 0)
    ]
    
    cur.executemany("""
        INSERT INTO inventory (item_name, price, date_received, is_fragile)
        VALUES (?, ?, ?, ?);
    """, sample_data)
    
    conn.commit()
    cur.close()
    conn.close()
    print(f"Database file '{DB_FILE}' created and seeded successfully!")

if __name__ == "__main__":
    init_db()






