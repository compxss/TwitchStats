import sqlite3
import time
from datetime import datetime

from source import get_streamer_data

def get_connection():
    return sqlite3.connect("streamers.db")

def get_streamers():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, name, viewers
        FROM streamers
        WHERE online = 1
    """)

    streamers = cursor.fetchall()

    connection.close()

    return streamers

def save_viewers(streamer_id, viewers):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO viewer_history
        (streamer_id, viewers, recorded_at)

        VALUES (?, ?, ?)
    """, (
        streamer_id,
        viewers,
        datetime.now().isoformat()
    ))

    cursor.execute("""
        UPDATE streamers
        SET viewers = ?
        WHERE id = ?
    """, (
        viewers,
        streamer_id
    ))

    connection.commit()
    connection.close()

while True:

    streamers = get_streamers()

    print("\ndata collection...")

    for streamer in streamers:

        streamer_id = streamer[0]
        name = streamer[1]
        current_viewers = streamer[2]

        data = get_streamer_data(name, current_viewers)

        new_viewers = data["viewers"]

        save_viewers(streamer_id, new_viewers)

        print(name, "->", new_viewers, "зрителей")

    time.sleep(10)