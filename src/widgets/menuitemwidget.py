from src.widgets import LabelWidget
from src.system.resourcemanager import rm
from src.configs import CONFIG

class MenuItemWidget(LabelWidget):
    def __init__(self, x, y, label, select_event=None):
        LabelWidget.__init__(self, x, y, label, select_event)
        self.selected = False

    def draw(self, screen):
        highlight = CONFIG['widget_default_menu_bg_colour'] if self.selected else CONFIG['default_background_colour']
        text = rm.get_font(CONFIG['widget_default_menu_font']).render(self.label, 1, CONFIG['widget_default_menu_font_colour'], highlight)
        screen.blit(text, (
                                    self.x,
                                    self.y,
                                )
                        )
