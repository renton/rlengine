import pygame
from pygame.locals import *

LOG_MODE_SYSTEM = 0

EVENT_CUSTOM_SWITCH_STATE = USEREVENT + 2
EVENT_CUSTOM_CREATE_STATE = USEREVENT + 3

CONFIG = {
    # window
    'default_fps'       : 60,
    'fullscreen_mode'   : False,
    'window_x_size'     : 1280,
    'window_y_size'     : 1024,
    'window_name'       : 'rlengine',
    'fps_draw_x'        : 10,
    'fps_draw_y'        : 10,

    # map
    'zoom_levels'           : (1, 2, 4),
    'delay_indicator_colour': (255, 255, 255),


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
    'tileset_path'                      : 'assets/tilesets/',

    # tileset viewer tool
    'tool_tileviewer_max_col_size'      : 48,
    'tool_tileviewer_font_colour'       : (0, 0, 0),

    # anatomy
    'anatomy_types' :  {
            0 : {
                    'name' : 'humanoid',
                    'weapon_slots' : [7, 8],
                    'weapon_swap_slots' : {9 : 7, 10 : 8},
                    'parts' : {
                                0 : {
                                        'name' : 'head',
                                    },
                                1 : {
                                        'name' : 'body',
                                    },
                                2 : {
                                        'name' : 'l.hand',
                                    },
                                3 : {
                                        'name' : 'r.hand',
                                    },
                                4 : {
                                        'name' : 'legs',
                                    },
                                5 : {
                                        'name' : 'l.foot',
                                    },
                                6 : {
                                        'name' : 'r.foot',
                                    },
                                7 : {
                                        'name' : 'l.hand item',
                                    },
                                8 : {
                                        'name' : 'r.hand item',
                                    },
                                9 : {
                                        'name' : 'alt l.hand',
                                    },
                                10 : {
                                        'name' : 'alt r.hand',
                                    },
                                }
                    },
            },

    # units
    'default_player_team'   : 1,

}


CONFIG['map_window_size_x'] = CONFIG['window_x_size'] / CONFIG['tile_size']
CONFIG['map_window_size_y'] = CONFIG['window_y_size'] / CONFIG['tile_size']

CONFIG['min_zoom'] = 0
CONFIG['max_zoom'] = len(CONFIG['zoom_levels'])-1 
