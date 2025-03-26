from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
from datetime import datetime
import socket
import os

PORT = 5666
LOG_FILE = 'log.txt'
FAVICON_PATH = os.path.join(os.path.dirname(__file__), 'favicon.ico')

class MyHandler(BaseHTTPRequestHandler):
    def log_request_info(self):
        client_ip = self.client_address[0]
        user_agent = self.headers.get('User-Agent', 'Unknown')
        timestamp = datetime.utcnow().isoformat()
        log_entry = f"Time: {timestamp}, IP: {client_ip}, User-Agent: {user_agent}\n"
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(log_entry)

    def do_GET(self):
        parsed_path = urlparse(self.path)
        self.log_request_info()

        if parsed_path.path == '/':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(b'<h1 style="font-size: 24px; font-weight: bold;">Kolobok suspendit</h1>')

        elif parsed_path.path == '/user':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(b'<h1 style="font-size: 24px; font-weight: bold;">Pinocchius masturbavit et ardens est.</h1>')

        elif parsed_path.path == '/favicon.ico':
            print(f"Looking for favicon at: {FAVICON_PATH}")  
            if os.path.exists(FAVICON_PATH):
                self.send_response(200)
                self.send_header('Content-Type', 'image/x-icon')
                self.end_headers()
                with open(FAVICON_PATH, 'rb') as f:
                    self.wfile.write(f.read())
            else:
                self.send_response(500)
                self.send_header('Content-Type', 'text/plain')
                self.end_headers()
                self.wfile.write(b'Error loading favicon.ico\n')

        else:
            self.send_response(404)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(b'<h1 style="font-size: 24px; font-weight: bold;">404 not found</h1>')

def run(server_class=HTTPServer, handler_class=MyHandler):
    server_address = ('127.0.0.1', PORT)
    httpd = server_class(server_address, handler_class)
    print(f"Listening on 127.0.0.1:{PORT}")
    httpd.serve_forever()

if __name__ == '__main__':
    run()
