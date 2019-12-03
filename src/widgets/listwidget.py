from src.widgets import Widget
from src.configs import CONFIG

class ListWidget(Widget):
    def __init__(self, x, y, select_event=None):
        Widget.__init__(self, x, y, select_event)
        self.data = {}

    def add_data(self, data):
        self.data = data

    def clear_data(self):
        self.data = {}

    def draw(self, screen):
        count = 0
        for k,v in self.data.items():
            text = rm.get_font(CONFIG['system_font_default']).render(str(k) + " : " + str(v), 1, CONFIG['system_font_colour'])
            screen.blit(text, (
                                        self.x,
                                        self.y + (CONFIG['widget_list_line_spacing'] * count),
                                    )
                            )
            count += 1
