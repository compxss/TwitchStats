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

def get_open_session(streamer_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id
        FROM stream_sessions
        WHERE streamer_id = ?
        AND ended_at IS NULL
        ORDER BY id DESC
        LIMIT 1
    """, (streamer_id,))

    row = cursor.fetchone()

    connection.close()

    if row:
        return row[0]
    
    return None

def start_session(streamer_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO stream_sessions
        (streamer_id, started_at)

        VALUES (?, ?)
    """, (
        streamer_id,
        datetime.now().isoformat()
    ))

    session_id = cursor.lastrowid

    connection.commit()
    connection.close()

    print("New stream session:", session_id)

    return session_id

def end_session(streamer_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE streamer_sessions
        SET ended_at = ?
        WHERE streamer_id = ?
        AND ended_at IS NULL
    """, (
        datetime.now().isoformat(),
        streamer_id
    ))

    connection.commit()
    connection.close()

    print("Stream session ended")

def save_viewers(streamer_id, session_id, viewers):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO viewer_history
        (streamer_id, session_id, viewers, recorded_at)

        VALUES (?, ?, ?, ?)
    """, (
        streamer_id,
        session_id,
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

    print("\nCollecting statistics...")

    for streamer in streamers:

        streamer_id = streamer[0]
        name = streamer[1]
        current_viewers = streamer[2]

        data = get_streamer_data(name, current_viewers)

        online = data["online"]

        session_id = get_open_session(streamer_id)

        if online and session_id is None:
            session_id = start_session(streamer_id)

        elif not online and session_id is not None:
            end_session(streamer_id)

            session_id = None

        if online and session_id is not None:

            save_viewers(streamer_id, session_id, data["viewers"])
            print(name, "->", data["viewers"], "зрителей")

    time.sleep(10)
