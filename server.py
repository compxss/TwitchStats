from http.server import HTTPServer, SimpleHTTPRequestHandler

server = HTTPServer(("localHost", 8000), SimpleHTTPRequestHandler)

print("Сервер запущен")
print("http://localhost:8000")

server.serve_forever()
