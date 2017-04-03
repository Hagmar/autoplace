from PIL import Image
import numpy as np
import sys
import logging


class Project:
    _colormap = {
        (255, 255, 255): 0,
        (228, 228, 228): 1,
        (136, 136, 136): 2,
        (34, 34, 34)   : 3,
        (255, 167, 209): 4,
        (229, 0, 0)    : 5,
        (229, 149, 0)  : 6,
        (160, 106, 66) : 7,
        (229, 217, 0)  : 8,
        (148, 224, 68) : 9,
        (2, 190, 1)    : 10,
        (0, 211, 221)  : 11,
        (0, 131, 199)  : 12,
        (0, 0, 234)    : 13,
        (207, 110, 228): 14,
        (130, 0, 128)  : 15
    }
    def __init__(self, image, x, y, pid):
        assert 0 <= x <= 999 and 0 <= y <= 999
        self.x = x
        self.y = y
        self.parse_image(image)
        self.h, self.w = self.target.shape
        self.pid = pid
        self.i = 0
        self.draw_cycle = 10

    def parse_image(self, image):
        data = self.read_image(image)
        self.target = self.map_colors(data)

    def read_image(self, image):
        try:
            img = Image.open(image)
        except OSError:
            logging.error("Could not open image file")
            raise
        assert 0 <= self.x + img.width <= 1000 and 0 <= self.y + img.height <= 1000
        return np.asarray(img)

    def map_colors(self, data):
        mapped_colors = np.zeros((data.shape[:-1]))
        for y, row in enumerate(data):
            for x, pixel in enumerate(row):
                mapped_colors[y][x] = self._colormap.get(tuple(pixel), -1)
        return mapped_colors

    def get_pixel_to_change(self, board):
        board_colors = board.board[self.y:self.y+self.h,
                                   self.x:self.x+self.w]
        diff = board_colors != self.target
        diff[self.target == -1] = False
        pixels = np.argwhere(diff)
        if not pixels.size:
            return None
        index = pixels[self.i%len(pixels)]
        self.i = (self.i + 1) % self.draw_cycle
        board_y = self.y + index[0]
        board_x = self.x + index[1]
        return (board_x, board_y, self.target[index[0]][index[1]])
