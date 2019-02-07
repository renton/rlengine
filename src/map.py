from src.tile import Tile
from random import choice, randint
from config import CONFIG

#TODO relative path loading
#TODO does each tile need an instantiated instance? lots of overhead
#TODO support more than just square maps
#TODO swap x + y

class Map():

    def __init__(self, bg_file=None):
        self.tiles = []
        self.size_x,self.size_y = 0,0
        self.bg_file = bg_file

        if not bg_file:
            self._gen_sample()
        else:
            self._load_map()

    def _load_map(self):
        x, y = 0, 0
        with open(self.bg_file, 'r') as f:
            for line in f:
                self.tiles.append([])
                for cell in line.split(' '):
                    self.tiles[y].append(Tile(int(cell)))
                y += 1
        print len(self.tiles)

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
