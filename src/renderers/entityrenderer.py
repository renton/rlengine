import pygame
from config import CONFIG
from src.system.resourcemanager import rm

class EntityRenderer():
    def __init__(self, screen):
        self.screen = screen
        self.display_delay_indicators = True
        self.display_health_indicators = True
        self.shadow_offset = 1

    def draw_entity(self, tiles_to_draw, x, y, zoom_level):

        for sprite in tiles_to_draw:
            self.screen.blit(
                rm.get_tile_by_id(sprite[0], sprite[1], CONFIG['zoom_levels'][zoom_level]),
                (x,y)
            )


    # TODO should be default draw value (not necessarily delay)
    def draw_delay(self, x, y, delay):
        # draw delay
        if self.display_delay_indicators:
            # TODO better algorithm for outlining
            text = rm.get_bold_font(1).render(str(delay), 1, (0,0,0))
            self.screen.blit(text, (
                                        x - self.shadow_offset,
                                        y - self.shadow_offset,
                                    )
                            )

            text = rm.get_bold_font(CONFIG['system_font_default']).render(str(delay), 1, CONFIG['delay_indicator_colour'])
            self.screen.blit(text, (
                                        x,
                                        y,
                                    )
                            )

    # TODO should be default draw bar (not necessarily life)
    def draw_lifebars(self, x, y, zoomed_tile_size, hp, max_hp):
        if self.display_health_indicators:
            pygame.draw.rect(self.screen, CONFIG['lifebar_bg_colour'], (
                x,
                y,
                zoomed_tile_size,
                CONFIG['lifebar_height']),
                0)

            if hp > (max_hp / 2):
                colour = CONFIG['lifebar_fg_colour']
            else:
                if hp > (max_hp / 4):
                    colour = CONFIG['lifebar_fg_warning_colour']
                else:
                    colour = CONFIG['lifebar_fg_danger_colour']

            pygame.draw.rect(self.screen, colour, (
                x,
                y,
                (((float)(hp) / (float)(max_hp)) * (float)(zoomed_tile_size)),
                CONFIG['lifebar_height']),
                0)
