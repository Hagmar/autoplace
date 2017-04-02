from board import Board
from project import Project
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
    _invalid_request_response = {
        'error': True,
        'message': 'Invalid request'
    }

    def __init__(self):
        self.projects = {}

    def run(self, args):
        self.board = Board()

        # TODO: Allow several projects
        new_project = Project(args.project_picture, args.x,
                              args.y, args.project_name)
        self.projects[args.project_name] = new_project

        # Thread handling board updates
        self.update_thread = threading.Thread(target=self.manage_board)
        self.update_thread.start()

        start_server = websockets.serve(self.client_loop, args.host, args.port)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()

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

    async def client_loop(self, ws, path):
        request = await ws.recv()
        print('Received: {} from {}'.format(request, ws.remote_address))
        try:
            data = json.loads(request)
        except:
            await ws.send('{"error":true,"message":"Invalid JSON request (invalid JSON)"}')
            return
        if 'project' not in data:
            await ws.send('{"error":true,"message":"Missing project argument"}')
            return
        try:
            project = self.projects[data['project']]
        except KeyError:
            await ws.send('{"error":true,"message":"Project does not exist"}')
            return
        action = project.get_pixel_to_change(self.board)
        if not action:
            await ws.send('{"error":true,"message":"The project is finished!"}')
            return
        (x, y, color) = action
        await ws.send(json.dumps({"error":False,
                                  "x":int(x), "y":int(y),
                                  "color":int(color)}))


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

# TODO: Temporarily requires initial project
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('project_name',
                        help='Name of running project')
    parser.add_argument('project_picture',
                        help='Image to be drawn')
    parser.add_argument('x', type=int,
                        help='X-coordinate to draw image at')
    parser.add_argument('y', type=int,
                        help='Y-coordinate to draw image at')
    parser.add_argument('host', default='0.0.0.0', nargs='?',
                        help='Hosts to allow')
    parser.add_argument('port', type=int, default=8080, nargs='?',
                        help='Port to listen to')
    return parser.parse_args()
if __name__ == '__main__':
    main()
