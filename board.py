import numpy as np
import requests as rq

URL_BOARD = 'https://www.reddit.com/api/place/board-bitmap'


class Board:
    _colormap = {
        0 : (255, 255, 255),
        1 : (228, 228, 228),
        2 : (136, 136, 136),
        3 : (34, 34, 34),
        4 : (255, 167, 209),
        5 : (229, 0, 0),
        6 : (229, 149, 0),
        7 : (160, 106, 66),
        8 : (229, 217, 0),
        9 : (148, 224, 68),
        10: (2, 190, 1),
        11: (0, 211, 221),
        12: (0, 131, 199),
        13: (0, 0, 234),
        14: (207, 110, 228),
        15: (130, 0, 128)
    }

    def __init__(self, w=1000, h=1000, fetch=True):
        self.w = w
        self.h = h
        self.board = np.zeros((self.w, self.h), dtype=np.uint8)
        if fetch:
            self.refresh()

    def refresh(self):
        board_binary = rq.get(URL_BOARD)
        self.update_board(board_binary.content)

    def update_pixel(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.board[y][x] = color

    def update_board(self, board):
        y = x = 0
        i = 4
        while y < len(self.board):
            self.board[y][x] = board[i] >> 4
            self.board[y][x+1] = board[i] & 0x0f
            i += 1
            x += 2
            if x >= self.w:
                y += 1
                x = 0
    
    def as_rgb(self):
        rgb_board = np.zeros((self.h, self.w, 3), dtype=np.uint8)
        for color_id, color in self._colormap.items():
            rgb_board[self.board==color_id] = color
        return rgb_board
