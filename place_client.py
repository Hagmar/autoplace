from getpass import getpass
from time import sleep
import argparse
import asyncio
import json
import requests as rq
import sys
import websockets


URL_LOGIN = 'https://www.reddit.com/api/login/{}'
URL_DRAW = 'https://www.reddit.com/api/place/draw.json'


class PlaceClient:
    def __init__(self):
        self.ses = rq.Session()
        self.ses.headers.update({
            'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/56.0.2924.87 Safari/537.36'})

    def login(self, user=None, passwd=None):
        authenticated = False
        while not authenticated:
            while not user:
                user = input('Username: ')
            while not passwd:
                passwd = getpass()

            payload = {
                    'op': 'login-main',
                    'api_type': 'json',
                    'user': user,
                    'passwd': passwd
            }
            res = self.ses.post(URL_LOGIN.format(user), data=payload)
            try:
                response = json.loads(res.text)
            except json.decoder.JSONDecodeError:
                print('Error: Could not decode login response', file=sys.stderr)
                user = passwd = None
                continue
            if response['json']['errors']:
                print('Error: {}'.format(response['json']['errors'][0][1]),
                      file=sys.stderr)
                user = passwd = None
                continue
            modhash = response['json']['data']['modhash']
            self.ses.headers.update({'x-modhash':modhash})
            authenticated = True

    def run(self, host, port, project):
        project = self.get_project_id(project)
        asyncio.get_event_loop().run_until_complete(self.join_project(
            host, port, project))

    def get_project_id(self, project=None):
        while not project:
            project = input('Project ID: ')
        return project

    async def join_project(self, host, port, project):
        ws_uri = 'ws://{}:{}'.format(host, port)
        while True:
            async with websockets.connect(ws_uri) as ws:
                data = {'project' : project}
                await ws.send(json.dumps(data))
                response = await ws.recv()
                print('Received response from server: {}'.format(response))
                json_response = json.loads(response)
                error = json_response['error']
                if error:
                    print('Error: {}'.format(json_response['message']),
                          file=sys.stderr)
                    project = self.get_project_id()
                    continue
                wait = self.draw_pixel(json_response['x'],
                                       json_response['y'],
                                       json_response['color'])
                if not wait:
                    break
                self.wait(wait)

    def draw_pixel(self, x, y, color):
        payload = {
                'x':x,
                'y':y,
                'color':color
        }
        res = self.ses.post(URL_DRAW, data=payload)
        try:
            status = json.loads(res.text)
        except json.decoder.JSONDecodeError:
            print('Error: Drawing failed', file=sys.stderr)
            return False
        print(status)
        if 'wait_seconds' in status:
            print('Drew pixel ({}, {}) successfully!'.format(
                x, y), file=sys.stderr)
            return status['wait_seconds']
        print('Error: Drawing failed', file=sys.stderr)
        print(status)
        return False

    def wait(self, wait):
        print('Sleeping for {} seconds'.format(wait))
        sleep(wait)


def main():
    args = parse_args()
    client = PlaceClient()
    client.login(args.user, args.passwd)
    client.run(args.server_host, args.server_port, args.project)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('server_host', metavar='host',
                        help='Server hosting the projects you want to join')
    parser.add_argument('server_port', metavar='port', type=int,
                        default=8080, nargs='?',
                        help='The port which the server is listening on')
    parser.add_argument('--user',
                        help='Your Reddit username')
    parser.add_argument('--pass', dest='passwd',
                        help='Your Reddit password')
    parser.add_argument('--proj', metavar='project', dest='project',
                        help='ID of the project you want to join')
    return parser.parse_args()

if __name__ == '__main__':
    main()
