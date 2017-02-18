import pygame
from pygame.locals import *

from config import CONFIG
from src.system.logger import log
from src.system.resourcemanager import rm

class State():
    def __init__(self, screen, player, prev_state = None):
        self.screen = screen
        self.ticks = 0
        self.show_logs = True
        self.show_expanded_logs = False
        self.set_prev_state(prev_state)
        self.fps = 0
        self.p1 = player
        self.bg_colour = CONFIG['default_background_colour']
        self.widgets = []

    def run_mainloop(self):
        self._draw()
        self._step()

    def _force_draw(self):
        self._draw()

    def _draw(self):
        self._before_draw()
        self.draw()
        self._after_draw()

    def _step(self):
        self._before_step()
        self.step()
        self._after_step()

    def _before_step(self):
        pass

    def step(self):
        self.ticks += 1

    def _after_step(self):
        pass

    def _before_draw(self):
        pass

    def draw(self):
        self.screen.fill(self.bg_colour)

    def draw_widgets(self):
        for widget in self.widgets:
            widget.draw(self.screen)

    def add_widget(self, widget):
        self.widgets.append(widget)

    def _after_draw(self):
        self.draw_logs()
        self.draw_widgets()
        self.draw_fps()
        pygame.display.flip()

    def draw_logs(self):
        if self.show_logs:
            count = 0
            num_visible = CONFIG['num_visible_logs_expanded'] if self.show_expanded_logs else CONFIG['num_visible_logs']

            for entry in log.logs:
                if count > num_visible:
                    break
                text = rm.get_sysfont().render(str(entry[0]), 1, CONFIG['log_colours'][entry[1]])
                self.screen.blit(text, (CONFIG['log_draw_x'], CONFIG['log_draw_y'] - (CONFIG['log_line_height'] * count)))
                # TODO last few lines should have transparency
                count += 1

    def set_fps(self, fps):
        self.fps = fps

    def draw_fps(self):
        text = rm.get_font(0).render(str(self.fps), 1, CONFIG['system_font_colour'])
        self.screen.blit(text, (
                                    CONFIG['fps_draw_x'],
                                    CONFIG['fps_draw_y'],
                                )
                        )

    def toggle_expanded_logs(self):
        self.show_expanded_logs = not self.show_expanded_logs

    def input(self, im):
        if im.is_key_event(KEYDOWN, K_ESCAPE):
            if self.prev_state:
                self.close()

    def close(self):
        pygame.event.post(pygame.event.Event(SETTINGS['EVENT_CUSTOM_SWITCH_STATE'], loadstate = self.prev_state))

    def set_prev_state(self, state):
        self.prev_state = state
