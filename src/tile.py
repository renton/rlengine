from random import choice,randint
from src.configs import CONFIG
from src.custom.data.tile_data import *

# note: only 1 destructable entity can ever be on a tile
class Tile():
    def __init__(self, game_tile_id):
        self.projectile_block_chance = 0
        self.game_tile_id = game_tile_id
        self.entities = {}

        self._load_tile_attributes()

    def _load_tile_attributes(self):
        tile_data =  get_tile_data(self.game_tile_id)

        # keep these in memory in case they change, the rest we can grab from static declaration in SETTINGS (name, description)
        self.walkable = tile_data['walkable']
        self.los_over = tile_data['los_over']
        self.tileset_id = tile_data['tileset_id']
        self.tile_id = tile_data['tile_id']

    def set_entity(self, e):
        self.entities[e.u_id] = e

    def unset_entity(self, e):
        if e.u_id in self.entities:
            del self.entities[e.u_id]

    def can_move(self):
        for k,v in self.entities.items():
            if not v.passable:
                return False
        return self.walkable

    def get_entities(self):
        return self.entities

    def get_attackable_target(self):
        for k,v in self.entities.items():
            if v.attackable:
                return v
        return None
