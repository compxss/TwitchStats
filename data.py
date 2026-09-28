from http.server import BaseHTTPRequestHandler, HTTPServer
import sqlite3
import json
from urllib.parse import urlparse, parse_qs

def get_connection():
    return sqlite3.connect("streamers.db")

def get_all_streamers():
    
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT name, viewers, followers, average_online, peak, online
        FROM streamers
    """)

    rows = cursor.fetchall()

    connection.close()

    streamers = {}

    for row in rows:
        name, viewers, followers, average_online, peak, online = row

        streamers[name] = {
            "viewers": viewers,
            "followers": followers,
            "average_online": average_online,
            "peak": peak,
            "online": bool(online)
        }

    return streamers

def get_streamer(name):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, name, viewers, followers, average_online, peak, online
        FROM streamers
        WHERE name = ?
    """, (name,))

    row = cursor.fetchone()

    if row is None:
        connection.close()
        return None

    streamer_id = row[0]

    cursor.execute("""
        SELECT viewers, recorded_at
        FROM viewer_history
        WHERE streamer_id = ?
        ORDER BY recorded_at ASC
    """, (streamer_id,))

    history_rows = cursor.fetchall()

    connection.close()

    history = []

    for history_row in history_rows:

        history.append({
            "viewers": history_row[0],
            "time": history_row[1]
        })

    return {
        "name": row[1],
        "viewers": row[2],
        "followers": row[3],
        "average_online": row[4],
        "peak": row[5],
        "online": bool(row[6]),
        "history": history
        }

class Handler (BaseHTTPRequestHandler):

    def send_json(self, data, status=200):
        response = json.dumps(data, ensure_ascii=False)

        self.send_response(status)

        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        
        self.end_headers()

        self.wfile.write(response.encode("utf-8"))

    def do_GET(self):

        url = urlparse(self.path)

        if url.path == "/api/streamers":

            streamers = get_all_streamers()

            self.send_json(streamers)

            return
        
        if url.path == "/api/streamer":

            params = parse_qs(url.query)

            name = params.get("name", [None])[0]

            if name is None:

                self.send_json(
                    {
                        "error":
                        "Streamer's name not specified"
                    },
                    400
                )

                return

            streamer = get_streamer(name)

            if streamer is None:

                self.send_json(
                    {
                        "error":
                        "Streamer is not found"
                    },
                    404
                )

                return

            self.send_json(streamer)

            return

        self.send_json(
            {
                "error":
                "Page is not found"
            },
            404
        )

server = HTTPServer(("localhost", 8000), Handler)

print("API запущен!")
print("http://localhost:8000")

server.serve_forever()
