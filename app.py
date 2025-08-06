#!/usr/bin/env python

import asyncio
import http
import signal

from websockets.asyncio.server import serve


async def echo(websocket):
    async for message in websocket:
        await websocket.send(message)


async def health_check(path, request_headers):
    if path == "/healthz":
        return http.HTTPStatus.OK, [("Content-Type", "text/plain")], b"OK\n"
    return None


async def main():
    port = 8000
    async with serve(echo, "", port, process_request=health_check) as server:
        stop = asyncio.Event()

        def on_stop():
            stop.set()

        loop = asyncio.get_running_loop()
        if hasattr(signal, "SIGTERM"):
            loop.add_signal_handler(signal.SIGTERM, on_stop)
        loop.add_signal_handler(signal.SIGINT, on_stop)

        await stop.wait()

if __name__ == "__main__":
    asyncio.run(main())
