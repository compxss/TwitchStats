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
        SELECT name, viewers, followers, average_online, peak, online
        FROM streamers
        WHERE name = ?
    """, (name))

    row = cursor.fetchone()

    connection.close()

    if row is None:
        return None

    return {
        "name": row[0],
        "viewers": row[1],
        "followers": row[2],
        "average_online": row[3],
        "peak": row[4],
        "online": bool(row[5])
        }

class Handler (BaseHTTPRequestHandler):

    def send_json(self, data):
        response = json.dumps(data, ensure_ascii=False)

        self.send_response(200)

        self.send_header("Content-Type", "application/json")
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

            if name in streamers:

                data = {
                    "name": name,
                    **streamers[name]
                }

                self.send_json(data)

            else:
                
                self.send_response(404)

                self.send_header("Access-Control-Allow-Origin", "*")
                
                self.end_headers()

                self.wfile.write(b"Streamer not found")
            
            return

        self.send_response(404)

        self.send_header("Access-Control-Allow-Origin", "*")
        
        self.end_headers()

server = HTTPServer(("localhost", 8000), Handler)

print("API запущен!")
print("http://localhost:8000")

server.serve_forever()
