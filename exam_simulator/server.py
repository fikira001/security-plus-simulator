import http.server
import socketserver
import webbrowser
import os
import sys

PORT = 8000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        # Enable CORS and caching headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        super().end_headers()

def run_server():
    global PORT
    for attempt in range(5):
        try:
            with socketserver.TCPServer(("", PORT), Handler) as httpd:
                url = f"http://localhost:{PORT}"
                print("=" * 65)
                print(f"🚀 CompTIA Security+ (SY0-701) Exam Simulator Running!")
                print(f"📍 URL: {url}")
                print(f"📁 Serving Directory: {DIRECTORY}")
                print("=" * 65)
                print("Press Ctrl+C to stop the server at any time.\n")
                
                # Open browser automatically
                webbrowser.open(url)
                
                httpd.serve_forever()
                break
        except OSError as e:
            print(f"Port {PORT} in use, trying port {PORT + 1}...")
            PORT += 1

if __name__ == '__main__':
    run_server()
