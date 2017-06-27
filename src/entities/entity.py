from config import CONFIG
from src.system.logger import log
from random import randint
import uuid

class Entity():
    def __init__(self, e_id):
        self.e_id = e_id
        self.u_id = uuid.uuid4().hex
        self.ai = True

        self.cur_map = None
        self.x = None
        self.y = None

        self.hp             = 1
        self.max_hp         = 1
        self.move_speed     = 10
        self.tile_id        = 3024
        self.tileset_id     = 0
        self.name           = ''
        self.description    = ''

        self.active         = True
        self.delay          = 10
        self.indestructable = False
        self.attackable     = False
        self.passable       = False

        self.stats = {}
        self.inventory = {}
        
        # TODO overrides - this should be passed as an optional param instead of config
        self._load_data({})

    def _decorator_is_active(func):
        def func_wrapper(*args):
            if args[0].active:
                return func(*args)
            else:
                return False
        return func_wrapper

    def get_tiles_to_draw(self):
        return [self._generate_base_tile()]

    def _generate_base_tile(self):
        return (self.tileset_id, self.tile_id)

    def _load_data(self, dataset):
        for k,v in dataset.items():
            if hasattr(v, '__call__'):
                setattr(self, k, v())
            else:
                setattr(self, k, v)

    def _modify_data(self, daataset):
        for k,v in dataset.items():
            if hasattr(self, k):
                if hasattr(v, '__call__'):
                    setattr(self, k, getattr(self, k) + v())
                else:
                    setattr(self, k, getattr(self, k) + v)

    # deprecated
    def getd(self, stat_key):
        # don't throw so we see key erros
        if hasattr(self, stat_key):
            return getattr(self, stat_key)
        return None

    def set_ai(self, flag):
        self.ai = flag

    @_decorator_is_active
    def step(self, map):
        pass

    @_decorator_is_active
    def walk(self, map, x, y):
        if map.is_walkable(self.x + x, self.y + y):
            if (x == 0 and y == 0):
                # wait
                return True
            else:
                self.move(map, self.x + x, self.y + y)
                self.adjust_delay(self.move_speed)
                return True
        else:
            return False

    @_decorator_is_active
    def move(self, map, x, y):
        if map.tiles[x][y].can_move():
            map.tiles[self.x][self.y].unset_entity(self)
            self.x = x
            self.y = y
            map.tiles[self.x][self.y].set_entity(self)
            return True
        else:
            return False

    def print_stats(self):
        for attr in dir(self):
            value = getattr(self, attr)
            if not hasattr(value, '__call__'):
                print attr + ' : ' + str(getattr(self, attr))

    @_decorator_is_active
    def attack(self, target):
        pass

    def add_to_map(self, x, y, map):
        self.x = x
        self.y = y
        self.cur_map = map

    def remove_from_map(self):
        if self.cur_map:
            self.cur_map.tiles[self.x][self.y].unset_entity(self)
        self.y = None
        self.x = None
        self.cur_map  = None

    @_decorator_is_active
    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp < 0:
            self.hp = 0

    def adjust_delay(self, adj):
        self.delay += int(adj)
