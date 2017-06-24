import pygame
from pygame.locals import *

LOG_MODE_SYSTEM = 0

EVENT_CUSTOM_SWITCH_STATE = USEREVENT + 2
EVENT_CUSTOM_CREATE_STATE = USEREVENT + 3

CONFIG = {
    # window
    'default_fps'       : 60,
    'fullscreen_mode'   : False,
    'window_x_size'     : 800,
    'window_y_size'     : 600,
    'window_name'       : 'rlengine',
    'fps_draw_x'        : 10,
    'fps_draw_y'        : 10,

    # map
    'zoom_levels'       : (1, 2, 4),

    # game
    'intro_state'               : None,
    'tile_size'                 : 32,
    'default_background_colour' : (0, 0, 0),
    'sample_map_x_size'         : 20,
    'sample_map_y_size'         : 20,

    # assets
    'asset_path'            : 'assets/',

    # fonts
    'font_path'             : 'fonts/',
    'system_fonts'          : {
                                0 : ('DejaVuSans.ttf', 20),
                                1 : ('DejaVuSans.ttf', 18),
                            },
    'system_font_default'   : 0,
    'system_font_size'      : 20,
    'system_font_colour'    : (255, 255, 255),

    # logging
    'log_store_max'             : 100,
    'num_visible_logs'          : 8,
    'num_visible_logs_expanded' : 35,
    'log_draw_x'                : 20,
    'log_draw_y'                : 560,
    'log_line_height'           : 20,
    'log_colours'               : {
                                    LOG_MODE_SYSTEM : (255, 255, 255),
                                },

    # widget
    'widget_list_line_spacing'          : 40,
    'widget_default_menu_font_colour'   : (255, 255, 255),
    'widget_default_menu_bg_colour'     : (100, 100, 100),
    'widget_default_menu_font'          : 0,
    'widget_default_menu_line_spacing'  : 40,
    'widget_default_menu_draw_x'        : 50,
    'widget_default_menu_draw_y'        : 50,

    # tilests
    'tileset_path'                      : 'assets/tilesets/'

}
