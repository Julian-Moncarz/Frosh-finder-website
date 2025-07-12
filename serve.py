#!/usr/bin/env python3
"""
Simple HTTP Server for Local Testing
Replicates what GitHub Pages does - serves static files over HTTP
"""

import http.server
import socketserver
import webbrowser
import os
from pathlib import Path

def serve_local():
    """Start a simple HTTP server for local testing"""
    PORT = 8000
    
    # Change to the directory containing the files
    os.chdir(Path(__file__).parent)
    
    # Create server
    Handler = http.server.SimpleHTTPRequestHandler
    
    print("🚀 Starting local server...")
    print("=" * 50)
    print(f"📡 Server running at: http://localhost:{PORT}")
    print(f"📄 Serving files from: {os.getcwd()}")
    print("=" * 50)
    print("✅ Your website will open automatically!")
    print("🔍 Test the search functionality")
    print("⏹️  Press Ctrl+C to stop the server")
    print()
    
    try:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            # Auto-open browser
            webbrowser.open(f'http://localhost:{PORT}')
            
            print(f"📊 Serving {PORT} - ready for testing!")
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n🛑 Server stopped!")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        print("💡 Try a different port if 8000 is busy")

if __name__ == "__main__":
    serve_local() 