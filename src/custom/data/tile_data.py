from src.configs import *

CONFIG['tile_configs'] = {}

CONFIG['tile_configs']['tilesets'] = {
        0 : {
                'name' : '',
                'filename' : 'DungeonCrawl_ProjectUtumnoTileset.png',
                'colorkey' : (0, 0, 0),
            },
}

CONFIG['gametiles'] = {
                            0 : {
                                    'name' : 'default',
                                    'description' : '',
                                    'tileset_id' : 0,
                                    'tile_id' : 3024,
                                    'walkable' : False,
                                    'los_over' : False,
                                },

                            1 : {
                                    'name' : 'stone wall 1',
                                    'description' : '',
                                    'tileset_id' : 0,
                                    'tile_id' : 1069,
                                    'walkable' : False,
                                    'los_over' : False,
                                },

                            2 : {
                                    'name' : 'stone floor 1',
                                    'description' : '',
                                    'tileset_id' : 0,
                                    'tile_id' : 1405,
                                    'walkable' : True,
                                    'los_over' : False,
                                },

                            3 : {
                                    'name' : 'stone tile',
                                    'description' : '',
                                    'tileset_id' : 0,
                                    'tile_id' : 210,
                                    'walkable' : False,
                                    'los_over' : True,
                                },
                            }

def get_tile_data(id):
    if id in CONFIG['gametiles']:
        return CONFIG['gametiles'][id]
    else:
        return CONFIG['gametiles'][0]
