from board import Board
import argparse
import asyncio
import json
import re
import requests as rq
import sys
import threading
import time
import websockets


URL_PLACE = 'https://www.reddit.com/r/place/'


class PlaceServer:
    def __init__(self):
        pass

    def run(self, args):
        self.board = Board()

        # Thread handling board updates
        self.update_thread = threading.Thread(target=self.manage_board)
        self.update_thread.start()

    def manage_board(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.update_loop())

    async def update_loop(self):
        ws_url = get_place_websocket_url()
        async with websockets.connect(ws_url) as ws:
            while True:
                data = await ws.recv()
                if data:
                    data = json.loads(data)
                    if data['type'] == 'place':
                        self.update_pixel(data['payload'])

    def update_pixel(self, payload):
        x = payload['x']
        y = payload['y']
        color = payload['color']
        self.board.update_pixel(x, y, color)


def get_place_websocket_url():
    while True:
        res = rq.get(URL_PLACE)
        match = re.search(r'place_websocket_url": "([^"]+)', res.text)
        if match:
            return match.group(1)

def main():
    args = parse_args()
    server = PlaceServer()
    server.run(args)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('host',
                        help='Hosts to allow')
    parser.add_argument('port', type=int, default=8080,
                        help='Port to listen to')
    return parser.parse_args()
if __name__ == '__main__':
    main()
