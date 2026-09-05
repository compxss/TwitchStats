import sqlite3

def create_database():
    connection = sqlite3.connect("streamers.db")

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS streamers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            viewers INTEGER DEFAULT 0,
            followers INTEGER DEFAULT 0,
            average_online INTEGER DEFAULT 0,
            peak INTEGER DEFAULT 0,
            online INTEGER DEFAULT 0
        )
    """)

    connection.commit()
    connection.close()

create_database()

print("База данных создана!")