import sys
import pygame

from config import CONFIG
from src.system.inputmanager import im
from src.system.resourcemanager import rm
from pygame.locals import *

class Game():
    def __init__(self):
        # init game time
        self.clock = pygame.time.Clock()
        self.fps = CONFIG['default_fps']
        self.playtime = 0.0

        # init screen
        flags = pygame.FULLSCREEN if CONFIG['fullscreen_mode'] else 0
        self.screen = pygame.display.set_mode((CONFIG['window_x_size'], CONFIG['window_y_size']), flags)
        pygame.display.set_caption(CONFIG['window_name'])

        # init mouse
        self.mouse_x, self.mouse_y = (0, 0)

        # set into state
        self._set_cur_state(CONFIG['intro_state'])

    def _set_cur_state(self, state):
        self.cur_state = state

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
              if event.type == pygame.quit:
                  pygame.display.quit()
                  sys.exit()

          # let state handle input
          im.update()
          #self.cur_state.input(self.im)

          keystate = pygame.key.get_pressed()

          # emergency exit
          if keystate[K_q] and (keystate[K_LCTRL] or keystate[K_RCTRL]):
              pygame.display.quit()
              sys.exit()

          #self.cur_state.set_fps(self.clock.get_fps())
          #self.cur_state.run_mainloop()

