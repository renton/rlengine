import pygame

from src.states import MenuState
from config import EVENT_CUSTOM_CREATE_STATE

MAIN_MENU_DRAW_X = 50
MAIN_MENU_DRAW_Y = 50

class MainMenuState(MenuState):
    def __init__(self, screen, player):
        MenuState.__init__(self, screen, player, draw_x = MAIN_MENU_DRAW_X, draw_y = MAIN_MENU_DRAW_Y)

        self.menu.add_menu_item('new campaign', self.exec_new_game)
        self.menu.add_menu_item('continue campaign')
        self.menu.add_menu_item('help')
        self.menu.add_menu_item('options')
        self.menu.add_menu_item('credits')
        self.menu.add_menu_item('exit', self.exec_exit_game)
        self.menu.select(0)

    def exec_new_game(self):
        # special start new game event state?? or create the state here
        pygame.event.post(pygame.event.Event(EVENT_CUSTOM_CREATE_STATE, createstate = None))

    def exec_exit_game(self):
        pygame.event.post(pygame.event.Event(pygame.QUIT))
