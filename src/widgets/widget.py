class Widget():
    def __init__(self, x, y, select_event=None):
        self.select_event = select_event
        self.x = x
        self.y = y

    def get_select_event(self):
        if select_event:
            return self.select_event()
        return False

    def draw(self, screen):
        pass
