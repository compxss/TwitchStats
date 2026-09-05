from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse, parse_qs

streamers = {
    "StreamerOne": {
        "viewers": 12450,
        "followers": 245000,
        "average_online": 11900,
        "peak": 18721,
        "online": True,
        "history": [1, 140, 680, 2300, 9100, 12000, 10500, 12500]
    },
    
    "StreamerTwo": {
        "viewers": 0,
        "followers": 18000,
        "average_online": 8200,
        "peak": 15300,
        "online": False,
        "history": [5200, 6100, 7300, 6800, 9100, 12000, 10500, 14000, 12500, 15000]
    },
    
    "StreamerThree": {
        "viewers": 1,
        "followers": 23,
        "average_online": 1,
        "peak": 2,
        "online": True,
        "history": [1, 0, 1, 1, 2, 1, 1, 1, 0, 2]
    },
    
    "StreamerFourth": {
        "viewers": 820,
        "followers": 21000,
        "average_online": 950,
        "peak": 1320,
        "online": True,
        "history": [30, 120, 360, 910, 640, 870, 1200, 950, 590, 680]
    }
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
