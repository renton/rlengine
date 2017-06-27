from config import *

# TODO this should specify what stats are necessary for a class and supply a default value
# these should get initialized and set to default
# should key be the class object name? default_stats_<class name>
CONFIG['default_entity_stats'] = {
            'hp' : 1,
            'max_hp' : 1,
            'move_speed' : 0,
            'tile_id' : 3024,
            'tileset_id' : 0,
            'name' : '',
            'description' : '',
            'indestructable' : False,
            'x' : None,
            'y' : None,
            'cur_map' : None,
            'active' : True,
            'delay' : 0,
            'passable' : False,
            'attackable' : False,
        }

CONFIG['default_unit_stats'] = {
            'alive' : True,
            'swap_alt_delay' : 10,
            'equipment_paradigm_id' : None,
            'unit_group' : -1,
            'ai_radius_vision' : 10,
            'ai_target_ignore_range' : 15,
            'target' : None,
            'corpse_id' : 0,
            'anatomy_id' : 0,
            'attackable' : True,
        }
