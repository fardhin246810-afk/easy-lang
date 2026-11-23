"""Local HTTP API and static web server for Easy Lang."""
from __future__ import annotations
import json
import os
import socket
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit
from mt_config import BASE_MODEL_DIR, FINETUNED_DIR, ROOT_DIR
from translation_engine import TranslationEngine, model_files_exist
ENGINE = TranslationEngine()
MAX_REQUEST_BYTES = 64 * 1024
STATIC_FILES = {"index.html", "manifest.json", "sw.js"}

def get_local_ip():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.connect(("10.255.255.255", 1))
        return sock.getsockname()[0]
    except OSError:
        return "127.0.0.1"
    finally:
        sock.close()

class EasyLangHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT_DIR), **kwargs)

    def translate_path(self, path):
        relative = unquote(urlsplit(path).path).lstrip("/") or "index.html"
        candidate = (ROOT_DIR / relative).resolve()
        assets_dir = (ROOT_DIR / "assets").resolve()
        allowed = relative in STATIC_FILES or candidate == assets_dir or assets_dir in candidate.parents
        if not allowed or not candidate.is_file():
            return str(ROOT_DIR / "__easy_lang_not_found__")
        return str(candidate)

    def _json(self, status, payload):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = urlsplit(self.path).path
        if path == "/api/health":
            ready = model_files_exist(BASE_MODEL_DIR) or model_files_exist(FINETUNED_DIR)
            self._json(200, {"ok": True, "model_ready": ready, "device": ENGINE.device, "message": "Local model ready" if ready else "Model not installed. Run python download_model.py."})
            return
        if path == "/api/languages":
            try:
                self._json(200, {"languages": ENGINE.languages()})
            except (RuntimeError, OSError, ValueError) as exc:
                self._json(503, {"error": str(exc)})
            return
        super().do_GET()

    def do_POST(self):
        path = urlsplit(self.path).path
        if path not in {"/api/detect", "/api/translate"}:
            self._json(404, {"error": "Endpoint not found."})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0 or length > MAX_REQUEST_BYTES:
                self._json(413, {"error": "Request body is empty or too large."})
                return
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
            if not isinstance(payload, dict):
                raise ValueError("Request body must be a JSON object.")
            if path == "/api/detect":
                self._json(200, {"detected": ENGINE.detect(payload.get("text", ""))})
                return
            result = ENGINE.translate(payload.get("text", ""), payload.get("source_language"), payload.get("target_language"), payload.get("num_beams", 4))
            self._json(200, result)
        except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
            self._json(400, {"error": str(exc)})
        except (RuntimeError, OSError) as exc:
            self._json(503, {"error": str(exc)})

def main():
    port = int(os.getenv("EASYLANG_PORT", "8000"))
    server = ThreadingHTTPServer(("0.0.0.0", port), EasyLangHandler)
    print("=" * 62)
    print("EASY LANG — LOCAL OFFLINE TRANSLATION SERVER")
    print("=" * 62)
    print(f"On this computer: http://localhost:{port}")
    print(f"On a phone on the same Wi-Fi: http://{get_local_ip()}:{port}")
    print("Translation runs on this computer using locally installed NLLB model files.")
    if not (model_files_exist(BASE_MODEL_DIR) or model_files_exist(FINETUNED_DIR)):
        print("Model not installed. Run: python download_model.py")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
    finally:
        server.server_close()

if __name__ == "__main__":
    main()
