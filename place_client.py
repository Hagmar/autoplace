#!/usr/bin/env python3

from PIL import Image
import requests as rq

URL_BOARD = 'https://www.reddit.com/api/place/board-bitmap'

def main():
    board = rq.get(URL_BOARD)
    image = Image.new('RGB', (1000,1000))

    image.save('testlol.png', 'PNG')    

if __name__ == '__main__':
    main()
