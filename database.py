import sqlite3
from datetime import datetime

def get_connection():
    return sqlite3.connect("streamers.db")

def create_database():

    connection = get_connection()
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

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS viewer_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            streamer_id INTEGER NOT NULL,
            viewers INTEGER NOT NULL,
            recorded_at TEXT NOT NULL,
            FOREIGN KEY (streamer_id)
                REFERENCES streamers(id)
        )
    """)

    connection.commit()
    connection.close()

def add_streamer(name, viewers, followers, average_online, peak, online):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO streamers
        (name, viewers, followers, average_online, peak, online)

        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        name,
        viewers,
        followers,
        average_online,
        peak,
        int(online)
    ))

    connection.commit()
    connection.close()

def add_history(streamer_name, viewers):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id
        FROM streamers
        WHERE name = ?
    """, (streamer_name,))

    row = cursor.fetchone()

    if row is None:

        print(
            "Стример не найден:",
            streamer_name
        )

        connection.close()
        return

    streamer_id = row[0]

    recorded_at = datetime.now().isoformat()

    cursor.execute("""
        INSERT INTO viewer_history
        (streamer_id, viewers, recorded_at)

        VALUES (?, ?, ?)
    """, (
        streamer_id,
        viewers,
        recorded_at
    ))

    connection.commit()
    connection.close()

create_database()

add_streamer(
    "StreamerOne",
    12450,
    245000,
    11900,
    18721,
    True
)

add_streamer(
    "StreamerTwo",
    0,
    18000,
    8200,
    15300,
    False
)

add_streamer(
    "StreamerThree",
    1,
    23,
    1,
    2,
    True
)

add_streamer(
    "StreamerFourth",
    820,
    21000,
    950,
    1320,
    True
)

history = [1, 140, 680, 2300, 9100, 12000, 10500, 12500]

for viewers in history:

    add_history("StreamerOne", viewers)

print("База данных создана!")
