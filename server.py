import json
import base64
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

class ExfiltrationServer(BaseHTTPRequestHandler):
    """Mock server to simulate data exfiltration"""
    
    def do_POST(self):
        """Handle POST requests for data exfiltration"""
        if self.path == '/receive':
            try:
                # Get content length
                content_length = int(self.headers['Content-Length'])
                
                # Read the POST data
                post_data = self.rfile.read(content_length)
                
                # Parse JSON data
                data = json.loads(post_data.decode('utf-8'))
                
                # Log received data
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log_entry = {
                    'timestamp': timestamp,
                    'source_ip': self.client_address[0],
                    'data_size': len(post_data),
                    'encrypted_data': data.get('encrypted_logs', ''),
                    'metadata': data.get('metadata', {})
                }
                
                # Save to server logs
                with open('server_received_logs.json', 'a') as f:
                    f.write(json.dumps(log_entry) + '\n')
                
                print(f"[{timestamp}] Received {len(post_data)} bytes from {self.client_address[0]}")
                
                # Send success response
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                
                response = {'status': 'success', 'message': 'Data received'}
                self.wfile.write(json.dumps(response).encode())
                
            except Exception as e:
                print(f"Error processing request: {e}")
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                
                response = {'status': 'error', 'message': str(e)}
                self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/status':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            response = {
                'status': 'online',
                'server': 'Mock Exfiltration Server',
                'timestamp': datetime.now().isoformat()
            }
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        """Override to customize logging"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {format % args}")

def start_server(port=8080):
    """Start the mock exfiltration server"""
    server_address = ('localhost', port)
    httpd = HTTPServer(server_address, ExfiltrationServer)
    
    print(f"🚀 Mock Exfiltration Server starting on http://localhost:{port}")
    print("📡 Endpoints:")
    print(f"   POST /receive - Receive encrypted data")
    print(f"   GET  /status  - Server status")
    print("⚠️  This is a MOCK server for educational purposes only!")
    print("Press Ctrl+C to stop the server\n")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
        httpd.server_close()

if __name__ == '__main__':
    start_server()
