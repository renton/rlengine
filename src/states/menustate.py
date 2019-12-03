import pygame
from pygame.locals import *

from src.configs import CONFIG
from src.states import State
from src.widgets import MenuWidget

class MenuState(State):
    def __init__(self, screen, player, draw_x = CONFIG['widget_default_menu_draw_x'], draw_y = CONFIG['widget_default_menu_draw_y']):
        State.__init__(self, screen, player)
        self.menu = MenuWidget(draw_x, draw_y)
        self.add_widget(self.menu)

    def input(self, im):
        if im.is_key_event(KEYDOWN, K_w) or im.is_key_event(KEYDOWN, K_UP):
            self.menu.cycle_last()
            self._force_draw()
        if im.is_key_event(KEYDOWN, K_s) or im.is_key_event(KEYDOWN, K_DOWN):
            self.menu.cycle_next()
            self._force_draw()
        if im.is_key_event(KEYDOWN, K_RETURN) or im.is_key_event(KEYDOWN, K_KP_ENTER):
            if hasattr(self.menu.item_select_event(), '__call__'):
                self.menu.item_select_event()()
                self._force_draw()
