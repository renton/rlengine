from src.tile import Tile
from random import choice, randint
from config import CONFIG

class Map():

    def __init__(self, gen_sample=False):
        self.tiles = []
        self.size_x,self.size_y = 0,0

        if gen_sample:
            self._gen_sample()

    def _gen_sample(self):
        for i in range(CONFIG['sample_map_x_size']):
            self.tiles.append([])
            for j in range(CONFIG['sample_map_y_size']):
                if (j == (CONFIG['sample_map_y_size'] - 1)) or (j == 0) or (i == (CONFIG['sample_map_x_size'] - 1)) or (i == 0):
                    self.tiles[i].append(Tile(1))
                else:
                    if randint(0, 9) == 1:
                        self.tiles[i].append(Tile(3))
                    else:
                        self.tiles[i].append(Tile(2))

        self.size_x = len(self.tiles)
        self.size_y = len(self.tiles[0])


    def is_walkable(self, x, y):
        return self.tiles[x][y].can_move()

    def empty_map(self):
        self.tiles[:] = []
