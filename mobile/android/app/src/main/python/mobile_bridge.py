"""Android bridge for the existing POLITICS table server.

The mobile shell does not fork game logic. It starts the same stdlib HTTP
table on loopback and lets Android own only lifecycle and store purchase UI.
"""

import threading

import serve

_SERVER = None
_THREAD = None


def start_server(port=5300, seats=3):
    global _SERVER, _THREAD
    if _SERVER is not None:
        return int(port)

    serve.TABLE = serve.Table(seats=int(seats))
    _SERVER = serve.ThreadingHTTPServer(("127.0.0.1", int(port)), serve.H)
    _THREAD = threading.Thread(target=_SERVER.serve_forever, daemon=True)
    _THREAD.start()
    return int(port)


def stop_server():
    global _SERVER, _THREAD
    if _SERVER is not None:
        _SERVER.shutdown()
        _SERVER.server_close()
    _SERVER = None
    _THREAD = None
