import sys
import pygame

from config import CONFIG, EVENT_CUSTOM_SWITCH_STATE, EVENT_CUSTOM_CREATE_STATE
from src.system.inputmanager import im
from src.system.resourcemanager import rm
from src.player import Player
from pygame.locals import *

from src.states import State
from src.custom.states import MainMenuState

from src.map import Map

START_STATE = MainMenuState

class Game():
    def __init__(self):
        # init game time
        self.clock = pygame.time.Clock()
        self.fps = CONFIG['default_fps']
        self.playtime = 0.0

        # init player
        self.p1 = Player()

        # init screen
        flags = pygame.FULLSCREEN if CONFIG['fullscreen_mode'] else 0
        self.screen = pygame.display.set_mode((CONFIG['window_x_size'], CONFIG['window_y_size']), flags)
        pygame.display.set_caption(CONFIG['window_name'])

        # init mouse
        self.mouse_x, self.mouse_y = (0, 0)

        # set into state
        self._set_cur_state(START_STATE(self.screen, self.p1))

        test = Map(True)
        rm.get_tile_by_id(0,0)

    def _set_cur_state(self, state):
        self.cur_state = state

    # TODO pass custom state class here
    def _evoke_new_state(self, state):
        self._set_cur_state(State(self.screen, self.p1))

    def mainloop(self):
        while(1):
          # do not go faster than the framerate
          msec = self.clock.tick(self.fps)
          self.playtime += msec / 1000.0

          # reset im key events
          im.reset_events()
          self.mouse_x, self.mouse_y = pygame.mouse.get_pos()

          # handle events
          for event in pygame.event.get():
            if event.type == EVENT_CUSTOM_SWITCH_STATE:
                self._set_cur_state(event.loadstate)
            if event.type == EVENT_CUSTOM_CREATE_STATE:
                self._evoke_new_state(event.createstate)
            if event.type == pygame.QUIT:
                pygame.display.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                im.set_key_event(event.type, event.key)
            if event.type == pygame.JOYBUTTONDOWN:
                im.set_joy_button_event(event.type, event.button)
            if event.type == pygame.MOUSEBUTTONDOWN:
                im.set_mouse_event(event.type, event.button)

          # let state handle input
          im.update()
          self.cur_state.input(im)

          keystate = pygame.key.get_pressed()

          # emergency exit
          if keystate[K_q] and (keystate[K_LCTRL] or keystate[K_RCTRL]):
              pygame.display.quit()
              sys.exit()

          self.cur_state.set_fps(self.clock.get_fps())
          self.cur_state.run_mainloop()
