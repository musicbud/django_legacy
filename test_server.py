#!/usr/bin/env python3

import json
import socket
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

class RequestLogger(BaseHTTPRequestHandler):
    def log_request_details(self):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"\n{'='*60}")
        print(f"[{timestamp}] {self.command} {self.path}")
        print(f"Client: {self.client_address[0]}:{self.client_address[1]}")
        print(f"Headers:")
        for header, value in self.headers.items():
            print(f"  {header}: {value}")
        
        # Parse query string if present
        parsed_url = urlparse(self.path)
        if parsed_url.query:
            print(f"Query params:")
            query_params = parse_qs(parsed_url.query)
            for key, values in query_params.items():
                print(f"  {key}: {values}")
    
    def do_GET(self):
        self.log_request_details()
        
        # CORS headers
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        
        # Simple response based on endpoint
        if '/me/profile' in self.path:
            response = {"message": "Profile endpoint called", "method": "GET"}
        elif '/bud/profile' in self.path:
            response = {"message": "Bud profile endpoint called", "method": "GET"}
        elif '/login' in self.path:
            response = {"message": "Login endpoint called", "method": "GET"}
        else:
            response = {"message": f"Endpoint {self.path} called", "method": "GET"}
        
        self.wfile.write(json.dumps(response).encode())
    
    def do_POST(self):
        self.log_request_details()
        
        # Read request body
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length > 0:
            body = self.rfile.read(content_length).decode()
            print(f"Request body:")
            try:
                if body:
                    if self.headers.get('Content-Type') == 'application/json':
                        parsed_body = json.loads(body)
                        print(json.dumps(parsed_body, indent=2))
                    else:
                        print(body)
            except json.JSONDecodeError:
                print(body)
        
        # CORS headers
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        
        # Simple response
        if '/login' in self.path:
            response = {
                "access": "fake-access-token",
                "refresh": "fake-refresh-token",
                "user": {"id": 1, "username": "testuser"}
            }
        else:
            response = {"message": f"POST to {self.path} successful", "status": "ok"}
        
        self.wfile.write(json.dumps(response).encode())
    
    def do_PUT(self):
        self.do_POST()  # Same logic as POST
    
    def do_DELETE(self):
        self.log_request_details()
        
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        
        response = {"message": f"DELETE {self.path} successful", "status": "ok"}
        self.wfile.write(json.dumps(response).encode())
    
    def do_OPTIONS(self):
        self.log_request_details()
        
        # CORS preflight response
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-Requested-With')
        self.send_header('Access-Control-Max-Age', '3600')
        self.end_headers()
    
    def log_message(self, format, *args):
        # Suppress default request logging to keep output clean
        pass

def run_server(port=8000):
    # Check if port is available
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex(('localhost', port))
    sock.close()
    
    if result == 0:
        print(f"Port {port} is already in use. Please stop the existing service.")
        return
    
    server_address = ('', port)
    httpd = HTTPServer(server_address, RequestLogger)
    
    print(f"🚀 Test API Server started on http://localhost:{port}")
    print("📡 Logging all HTTP requests from Flutter app...")
    print("Press Ctrl+C to stop the server")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print(f"\n🛑 Server stopped")

if __name__ == '__main__':
    run_server()