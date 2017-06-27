import pygame
import sys
from pygame.locals import *

from random import randrange, choice, randint

#from ..entities import *
from src.states import State
#from inventorystate import InventoryState
from src.map import Map
from src.player import Player

from src.system.resourcemanager import rm
from src.system.logger import log
from config import CONFIG

#TODO heavy refactoring. this should never be instanced. entity drawing should have it's own renderer. the instanced subclass can define that

class MapState(State):
    def __init__(self, screen, player, defaultmap):
        State.__init__(self, screen, player)

        self._set_camera(0, 0)
        self.zoom_level = 1
        self.fixed_camera = True
        self.camera_target = None
        self.display_health_indicators = True
        self.display_delay_indicators = True
        self.set_map(defaultmap)

        #self.i_state = InventoryState(self.screen, self.p1, self)

        self.entities = []

    def set_map(self, newmap):
        self.cur_map = newmap

    def step(self):
        #if self.p1.e is None or self.p1.get_delay() != 0:
        if self.p1.e is None or self.p1.get_delay() != 0 or self.p1.had_input:
            self._step_entities()
            State.step(self)
            self._force_draw()
            self.p1.wait_for_input()

    # map state only draws implicitly
    def run_mainloop(self):
        self._step()

    def _step_entities(self):
        for entity in self.entities:
            entity.step(self.cur_map)

    def draw(self):
        State.draw(self)
        self._draw_map()

    def _draw_map(self):
        # draw map
        # TODO only need to draw what's in viewport (not the whole map_window)
        if not self.fixed_camera:
            self.set_camera_to_entity(self.camera_target)

        #TODO entity renderers should be classes that can be swapped in and out and decoupled with the mapstate
        for x in range((CONFIG['map_window_size_x'] / CONFIG['zoom_levels'][self.zoom_level])):
            for y in range((CONFIG['map_window_size_y'] / CONFIG['zoom_levels'][self.zoom_level])):
                if ((self.camera_tile_x + x) >= 0) and ((self.camera_tile_y + y) >= 0):
                    if (((self.camera_tile_x + x) < len(self.cur_map.tiles)) and ((self.camera_tile_y + y) < len(self.cur_map.tiles[self.camera_tile_x + x]))):
                        tile = self.cur_map.tiles[self.camera_tile_x + x][self.camera_tile_y + y]
                        self._draw_tile(tile, x, y)
                        for e_uid,e in tile.get_entities().items():
                            if e.cur_map:
                                tiles_to_draw = e.get_tiles_to_draw()
                                for sprite in tiles_to_draw:
                                    self.screen.blit(
                                            rm.get_tile_by_id(sprite[0], sprite[1], CONFIG['zoom_levels'][self.zoom_level]), (
                                                (e.x - self.camera_tile_x) * self.get_zoomed_tile_size(),
                                                (e.y - self.camera_tile_y) * self.get_zoomed_tile_size()))

                                # draw delay
                                if self.display_delay_indicators and self.p1.e != e and self.camera_target and e.attackable:
                                    # TODO better algorithm for outlining
                                    text = rm.get_bold_font(1).render(str(e.delay), 1, (0,0,0))
                                    self.screen.blit(text, (
                                                                (e.x - self.camera_tile_x) * self.get_zoomed_tile_size() - 1,
                                                                ((e.y - self.camera_tile_y) * self.get_zoomed_tile_size()) + self.get_zoomed_tile_size() - rm.fonts[0]['size'] - 2 - 1,
                                                            )
                                                    )

                                    text = rm.get_bold_font(1).render(str(e.delay), 1, CONFIG['delay_indicator_colour'])
                                    self.screen.blit(text, (
                                                                (e.x - self.camera_tile_x) * self.get_zoomed_tile_size(),
                                                                ((e.y - self.camera_tile_y) * self.get_zoomed_tile_size()) + self.get_zoomed_tile_size() - rm.fonts[0]['size'] - 2,
                                                            )
                                                    )
                                #draw lifebars
                                if self.display_health_indicators and e.attackable:
                                    pygame.draw.rect(self.screen, CONFIG['lifebar_bg_colour'], (
                                        ((e.x - self.camera_tile_x) * self.get_zoomed_tile_size()),
                                        ((e.y - self.camera_tile_y) * self.get_zoomed_tile_size()),
                                        self.get_zoomed_tile_size(),
                                        CONFIG['lifebar_height']),
                                        0)

                                    if e.hp > (e.max_hp / 2):
                                        colour = CONFIG['lifebar_fg_colour']
                                    else:
                                        if e.hp > (e.max_hp / 4):
                                            colour = CONFIG['lifebar_fg_warning_colour']
                                        else:
                                            colour = CONFIG['lifebar_fg_danger_colour']

                                    pygame.draw.rect(self.screen, colour, (
                                        ((e.x - self.camera_tile_x) * self.get_zoomed_tile_size()),
                                        ((e.y - self.camera_tile_y) * self.get_zoomed_tile_size()),
                                        ((float)(e.hp / 100.0) * (float)(self.get_zoomed_tile_size())),
                                        CONFIG['lifebar_height']),
                                        0)


    def _draw_tile(self, tile, x, y):
        self.screen.blit(
                rm.get_tile_by_id(tile.tileset_id, tile.tile_id, CONFIG['zoom_levels'][self.zoom_level]), (
                    x * self.get_zoomed_tile_size(),
                    y * self.get_zoomed_tile_size()))

    def get_zoomed_tile_size(self):
        return (CONFIG['tile_size'] * CONFIG['zoom_levels'][self.zoom_level])

    def set_follow_camera(self, e):
        self.fixed_camera = False
        self.camera_target = e

    def _set_camera(self, x, y):
        self.camera_tile_x, self.camera_tile_y = (x, y)

    def input(self, im):
        keystate = pygame.key.get_pressed()

        # TODO camera should be able to pan to blackness at any zoom level
        if im.is_key_event(KEYDOWN, K_w) or keystate[K_w]:
            self._set_camera(self.camera_tile_x,self.camera_tile_y - 1)
            self._force_draw()
        if im.is_key_event(KEYDOWN, K_d) or keystate[K_d]:
            self._set_camera(self.camera_tile_x + 1,self.camera_tile_y)
            self._force_draw()
        if im.is_key_event(KEYDOWN, K_s) or keystate[K_s]:
            self._set_camera(self.camera_tile_x,self.camera_tile_y + 1)
            self._force_draw()
        if im.is_key_event(KEYDOWN, K_a) or keystate[K_a]:
            self._set_camera(self.camera_tile_x - 1,self.camera_tile_y)
            self._force_draw()

        if im.is_key_event(KEYDOWN, K_q):
            self.fixed_camera = not self.fixed_camera
            log.add_log("camera: " + ("fixed" if self.fixed_camera else "follow")) 
            self._force_draw()

        if im.is_key_event(KEYDOWN, K_z):
            if self.zoom_level > CONFIG['min_zoom']:
                self.zoom_level -= 1
                self._force_draw()
        if im.is_key_event(KEYDOWN, K_x):
            if self.zoom_level < CONFIG['max_zoom']:
                self.zoom_level += 1
                self._force_draw()
        if im.is_key_event(KEYDOWN, K_c):
            #self.p1.bind_entity(self.test1)
            #self.fixed_camera = False
            #self.set_camera_to_entity(self.p1.e)
            self._force_draw()
        if im.is_key_event(KEYDOWN, K_n):
            self.p1.unbind_entity()
            self._force_draw()
        '''
        if im.is_key_event(KEYDOWN, K_g):
            # successfully picked up
            (pickedup, dropped) = self.p1.e.pickup(self.cur_map.tiles[self.p1.e.x][self.p1.e.y])
            for item in pickedup: 
                self.remove_entity_from_map(item)
            for item in dropped:
                self.add_entity_to_map(item, self.p1.e.x, self.p1.e.y)
            self._force_draw()
        '''
        if im.is_key_event(KEYDOWN, K_e):
            self.toggle_expanded_logs()
            self._force_draw()

        '''
        if im.is_key_event(KEYDOWN, K_i):
            if self.p1.e:
                self.i_state.set_entity(self.p1.e)
                pygame.event.post(pygame.event.Event(CONFIG['EVENT_CUSTOM_SWITCH_STATE'], loadstate = self.i_state))
        if im.is_key_event(KEYDOWN, K_g):
            if self.p1.e:
                items = self.p1.e.pickup_all(self.get_player_current_tile())
                for item in items:
                    self.remove_entity_from_map(item)
                self._force_draw()
        '''

        State.input(self, im)

    def get_player_current_tile(self):
        if self.p1.e and self.cur_map:
            return self.cur_map.tiles[self.p1.e.x][self.p1.e.y]

    def add_entity_to_map(self, e, x=-1, y=-1):
        self.entities.append(e)

        if x == -1 and y == -1:
            if e.x:
                x = e.x
            if e.y:
                y = e.y

        self.cur_map.tiles[x][y].set_entity(e)
        e.add_to_map(x, y, self.cur_map)

    # TODO entities should be a key=>value for fast removals (and order drawing data)
    def remove_entity_from_map(self, e):
        self.cur_map.tiles[e.x][e.y].unset_entity(e)
        self.entities.remove(e)

    def set_camera_to_entity(self, e):
        if e and e.alive:
            self._set_camera(
                    e.x - ((CONFIG['map_window_size_x'] / CONFIG['zoom_levels'][self.zoom_level]) / 2),
                    e.y - ((CONFIG['map_window_size_y'] / CONFIG['zoom_levels'][self.zoom_level]) / 2)
                    )
