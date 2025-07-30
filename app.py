#!/usr/bin/env python3
import asyncio
import json
import threading
import time
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler
import websockets   # pip install websockets

GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbwyVhzqCKILnTyw24ZwwMV0LXG7cVdCL2fxGe0aUTIVdJTDRl-557Miow2ReaKNlORD/exec"

# ---------- WebSocket ----------
WS_CLIENTS = set()

async def ws_register(ws):
    WS_CLIENTS.add(ws)
    try:
        data = requests.get(GOOGLE_SCRIPT_URL, timeout=10).json()
    except Exception as e:
        data = {"error": str(e)}
    await ws_broadcast(data)
    print("[WS] client connected")

async def ws_unregister(ws):
    WS_CLIENTS.discard(ws)
    print("[WS] client disconnected")

async def ws_broadcast(data):
    if WS_CLIENTS:
        payload = json.dumps(data, ensure_ascii=False)
        await asyncio.gather(*(c.send(payload) for c in WS_CLIENTS), return_exceptions=True)

async def ws_handler(ws):
    try:
        await ws_register(ws)
        await ws.send(json.dumps({"status": "connected"}))
        async for message in ws:
            print(f"[WS] received: {message}")
    except websockets.exceptions.ConnectionClosedError as e:
        print(f"[WS] closed with error: {e}")
    except Exception as e:
        print(f"[WS] unexpected error: {e}")
    finally:
        await ws_unregister(ws)

# ---------- HTTP ----------
class WebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/webhook":
            try:
                data = requests.get(GOOGLE_SCRIPT_URL, timeout=10).json()
            except Exception as e:
                data = {"error": str(e)}
            asyncio.run(ws_broadcast(data))
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")
        else:
            self.send_error(404)

def http_thread():
    port = 8181  # 避开 8080 冲突
    try:
        httpd = HTTPServer(("0.0.0.0", port), WebhookHandler)
        print(f"[HTTP] /webhook listening on 0.0.0.0:{port}")
        httpd.serve_forever()
    except OSError as e:
        print(f"[HTTP] Failed to bind port {port}: {e}")

# ---------- 启动 ----------
def main():
    async def ws_main():
        async with websockets.serve(ws_handler, "0.0.0.0", 8765):  # No `path` param
            print("[WS] listening on ws://0.0.0.0:8765")
            await asyncio.Future()

    threading.Thread(target=http_thread, daemon=True).start()
    asyncio.run(ws_main())

if __name__ == "__main__":
    main()
