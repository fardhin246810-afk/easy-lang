import http.server
import socket
import socketserver
import os
import sys

PORT = 8000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        # Enable CORS and PWA caching headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-cache')
        super().end_headers()

if __name__ == '__main__':
    local_ip = get_local_ip()
    print("=" * 62)
    print("   EASY LANG - SECURE MOBILE & PC OFFLINE APPLICATION SERVER")
    print("=" * 62)
    print(f"\n   [PC Desktop App]:")
    print(f"   • Double click: EasyLang.exe")
    print(f"   • Or open in browser: http://localhost:{PORT}")
    print(f"\n   [Mobile App (Android / iPhone)]:")
    print(f"   • Connect your phone to the same Wi-Fi / Hotspot.")
    print(f"   • Open this URL in your phone's browser:")
    print(f"     👉 http://{local_ip}:{PORT}")
    print(f"\n   [How to Install as App on Phone]:")
    print(f"   • Android: Tap 'Install App' or browser menu (⋮) -> 'Add to Home Screen'")
    print(f"   • iPhone: Tap Share button -> 'Add to Home Screen'")
    print(f"   • Zero security warnings, no APK risk, 100% safe & offline!")
    print("=" * 62)
    print("Press Ctrl+C to stop server.\n")

    with socketserver.TCPServer(("0.0.0.0", PORT), CustomHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")
            sys.exit(0)
