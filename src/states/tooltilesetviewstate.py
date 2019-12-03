import pygame
from pygame.locals import *

from src.states import MapState, State
from src.tile import Tile
from src.map import Map
from src.configs import CONFIG

from src.system.resourcemanager import rm

class ToolTilesetViewState(MapState):
    def __init__(self, screen, player):
        MapState.__init__(self, screen, player)
        self.cur_map = self.gen_tileset_map(0)
        self.set_map(self.cur_map)

        self.fixed_camera = True
        self.bg_colour = (255, 255, 255)
        self.show_numbers = True

    def run_mainloop(self):
        pass

    def step(self):
        pass

    def gen_tileset_map(self, tileset_id):
        filename = CONFIG['tile_configs']['tilesets'][tileset_id]['filename']
        rm.load_tileset_by_id(tileset_id)
        testmap = Map()
        testmap.empty_map()
        x = 0
        y = 0
        count = 0
        for tileconfig in rm.tilesets[filename]:
            if y >= CONFIG['tool_tileviewer_max_col_size']:
                x += 1
                y = 0

            tile = Tile(0)
            tile.tileset_id = tileset_id
            tile.tile_id = count

            if x not in testmap.tiles:
                testmap.tiles.append([])
            testmap.tiles[x].append(tile)
            y += 1
            count += 1

        return testmap

    def cycle_through_sets(self):
        # TODO cycle through all available tilesets
        pass

    def _draw_tile(self, tile, x, y):
        self.screen.blit(
                rm.get_tile_by_id(tile.tileset_id, tile.tile_id, CONFIG['zoom_levels'][self.zoom_level]), (
                    x * self.get_zoomed_tile_size(),
                    y * self.get_zoomed_tile_size()))
        if self.show_numbers:
            text = rm.get_bold_font(0).render(str(tile.tile_id), 1, CONFIG['tool_tileviewer_font_colour'])
            self.screen.blit(text, (
                                        x * self.get_zoomed_tile_size(),
                                        y * self.get_zoomed_tile_size(),
                                    )
                            )

    def input(self, im):
        keystate = pygame.key.get_pressed()

        if im.is_key_event(KEYDOWN, K_q):
            self.show_numbers = not self.show_numbers
            self._force_draw()

        MapState.input(self, im)
