#!/usr/bin/env python3

import json
import socket
import time
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

class APIDebugHandler(BaseHTTPRequestHandler):
    def log_request_details(self):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"\n{'='*80}")
        print(f"🔍 [{timestamp}] {self.command} {self.path}")
        print(f"📍 Client: {self.client_address[0]}:{self.client_address[1]}")
        print(f"📋 Headers:")
        for header, value in self.headers.items():
            # Mask sensitive headers
            if header.lower() in ['authorization', 'cookie']:
                value = f"{'*' * min(len(value), 20)}..."
            print(f"    {header}: {value}")
        
        # Parse query string
        parsed_url = urlparse(self.path)
        if parsed_url.query:
            print(f"🔗 Query Parameters:")
            query_params = parse_qs(parsed_url.query)
            for key, values in query_params.items():
                print(f"    {key}: {values}")
    
    def log_response(self, status_code, response_data):
        print(f"📤 Response: {status_code}")
        if response_data:
            try:
                if isinstance(response_data, str):
                    data = json.loads(response_data)
                else:
                    data = response_data
                print(f"📦 Response Body:")
                print(json.dumps(data, indent=2)[:500] + ("..." if len(json.dumps(data, indent=2)) > 500 else ""))
            except:
                print(f"📦 Response Body: {str(response_data)[:200]}...")
    
    def get_realistic_response(self, endpoint, method):
        """Return realistic API responses for different endpoints"""
        
        # Authentication endpoints
        if '/login' in endpoint and method == 'POST':
            return {
                "access": "fake-jwt-access-token-12345",
                "refresh": "fake-jwt-refresh-token-67890",
                "user": {
                    "id": 1,
                    "username": "testuser",
                    "email": "test@example.com",
                    "profile": {
                        "display_name": "Test User",
                        "bio": "Music lover and Flutter developer"
                    }
                }
            }
        
        # User profile endpoints
        if '/me/profile' in endpoint:
            return {
                "id": 1,
                "username": "testuser",
                "email": "test@example.com",
                "display_name": "Test User",
                "bio": "Music lover and Flutter developer",
                "avatar_url": "https://example.com/avatar.jpg",
                "created_at": "2024-01-01T00:00:00Z",
                "spotify_connected": True,
                "lastfm_connected": False,
                "ytmusic_connected": True
            }
        
        # Bud profile endpoint
        if '/bud/profile' in endpoint:
            return {
                "bud": {
                    "id": 2,
                    "username": "musicbud",
                    "display_name": "Music Bud",
                    "bio": "Your music companion",
                    "avatar_url": "https://example.com/bud-avatar.jpg"
                },
                "compatibility_score": 85,
                "common_artists": 12,
                "common_tracks": 8,
                "match_reasons": ["Similar taste in Rock", "Both love Jazz"]
            }
        
        # Top items endpoints
        if '/me/top/artists' in endpoint:
            return {
                "items": [
                    {
                        "id": "artist1",
                        "name": "The Beatles",
                        "image_url": "https://example.com/beatles.jpg",
                        "play_count": 156,
                        "genres": ["Rock", "Pop"]
                    },
                    {
                        "id": "artist2", 
                        "name": "Radiohead",
                        "image_url": "https://example.com/radiohead.jpg",
                        "play_count": 89,
                        "genres": ["Alternative Rock", "Electronic"]
                    }
                ],
                "total": 2,
                "page": 1,
                "has_more": False
            }
        
        if '/me/top/tracks' in endpoint:
            return {
                "items": [
                    {
                        "id": "track1",
                        "name": "Hey Jude",
                        "artist": "The Beatles",
                        "album": "Hey Jude",
                        "image_url": "https://example.com/hey-jude.jpg",
                        "play_count": 45,
                        "duration_ms": 431000
                    },
                    {
                        "id": "track2",
                        "name": "Creep", 
                        "artist": "Radiohead",
                        "album": "Pablo Honey",
                        "image_url": "https://example.com/creep.jpg",
                        "play_count": 38,
                        "duration_ms": 238000
                    }
                ],
                "total": 2,
                "page": 1,
                "has_more": False
            }
        
        # Liked items endpoints
        if '/me/liked/artists' in endpoint:
            return {
                "items": [
                    {
                        "id": "liked_artist1",
                        "name": "Pink Floyd",
                        "image_url": "https://example.com/pink-floyd.jpg",
                        "liked_at": "2024-09-15T10:30:00Z"
                    }
                ],
                "total": 1
            }
        
        # Discover endpoints  
        if '/discover' in endpoint:
            return {
                "featured_artists": [
                    {
                        "id": "featured1",
                        "name": "New Artist",
                        "image_url": "https://example.com/new-artist.jpg",
                        "reason": "Based on your listening history"
                    }
                ],
                "trending_tracks": [
                    {
                        "id": "trending1",
                        "name": "Hot New Track",
                        "artist": "Trending Artist",
                        "play_count": 1000000
                    }
                ]
            }
        
        # Chat/Channel endpoints
        if '/channels' in endpoint:
            return {
                "channels": [
                    {
                        "id": "channel1",
                        "name": "Rock Lovers",
                        "description": "For rock music enthusiasts",
                        "member_count": 156,
                        "created_at": "2024-08-01T00:00:00Z"
                    },
                    {
                        "id": "channel2",
                        "name": "Jazz Corner", 
                        "description": "Smooth jazz discussions",
                        "member_count": 89,
                        "created_at": "2024-07-15T00:00:00Z"
                    }
                ],
                "total": 2
            }
        
        # Default response
        return {
            "message": f"Mock response for {endpoint}",
            "method": method,
            "timestamp": datetime.now().isoformat(),
            "status": "ok"
        }
    
    def send_json_response(self, status_code, data):
        response_json = json.dumps(data)
        
        self.send_response(status_code)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-Requested-With')
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(response_json)))
        self.end_headers()
        
        self.wfile.write(response_json.encode())
        self.log_response(status_code, data)
    
    def read_request_body(self):
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length > 0:
            body = self.rfile.read(content_length).decode()
            print(f"📨 Request Body:")
            try:
                if body and self.headers.get('Content-Type', '').startswith('application/json'):
                    parsed_body = json.loads(body)
                    print(json.dumps(parsed_body, indent=2))
                    return parsed_body
                else:
                    print(body)
                    return body
            except json.JSONDecodeError as e:
                print(f"Invalid JSON: {e}")
                print(body)
                return body
        return None
    
    def do_GET(self):
        self.log_request_details()
        response_data = self.get_realistic_response(self.path, 'GET')
        self.send_json_response(200, response_data)
    
    def do_POST(self):
        self.log_request_details()
        request_body = self.read_request_body()
        response_data = self.get_realistic_response(self.path, 'POST')
        
        # Handle login specifically
        if '/login' in self.path and request_body:
            if isinstance(request_body, dict):
                username = request_body.get('username', 'unknown')
                response_data['user']['username'] = username
        
        self.send_json_response(200, response_data)
    
    def do_PUT(self):
        self.log_request_details()
        request_body = self.read_request_body()
        response_data = self.get_realistic_response(self.path, 'PUT')
        self.send_json_response(200, response_data)
    
    def do_DELETE(self):
        self.log_request_details()
        response_data = {"message": f"DELETE {self.path} successful", "status": "deleted"}
        self.send_json_response(200, response_data)
    
    def do_OPTIONS(self):
        self.log_request_details()
        print(f"🔄 CORS Preflight Request")
        
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-Requested-With')
        self.send_header('Access-Control-Max-Age', '3600')
        self.end_headers()
        
        print(f"✅ CORS Headers Sent")
    
    def log_message(self, format, *args):
        # Suppress default request logging
        pass

def run_debug_server(port=8000):
    # Check if port is available
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex(('localhost', port))
    sock.close()
    
    if result == 0:
        print(f"❌ Port {port} is already in use. Please stop the existing service.")
        return
    
    server_address = ('', port)
    httpd = HTTPServer(server_address, APIDebugHandler)
    
    print(f"🚀 API Debug Server started on http://localhost:{port}")
    print(f"📊 Providing realistic mock responses for Flutter app testing")
    print(f"🔍 Detailed request/response logging enabled")
    print(f"⚡ Ready to capture Flutter API calls...")
    print("Press Ctrl+C to stop the server\n")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print(f"\n🛑 Debug server stopped")

if __name__ == '__main__':
    run_debug_server()