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
            authenticated = True

    def run(self, host, port, project):
        pass


def main():
    args = parse_args()
    client = PlaceClient()
    client.login(args.user, args.passwd)
    client.run(args.host, args.port, args.project)

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
    parser.add_argument('--proj', metavar='project',
                        help='ID of the project you want to join')
    return parser.parse_args()

if __name__ == '__main__':
    main()
