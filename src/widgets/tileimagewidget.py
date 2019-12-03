from src.widgets import Widget
from src.configs import CONFIG

class TileImageWidget(Widget):
    def __init__(self, x, y, select_event=None):
        Widget.__init__(self, x, y, select_event)
        self.tileset_id = None
        self.tile_id = None

    def set_tile(self, tileset_id, tile_id):
        self.tileset_id = tileset_id
        self.tile_id = tile_id

    def draw(self, screen):
        if self.tileset_id is not None and self.tile_id is not None:
            screen.blit(
                    rm.get_tile_by_id(self.tileset_id, self.tile_id, CONFIG['zoom_levels'][-1]), (
                        self.x,
                        self.y,
                        )
                    )
