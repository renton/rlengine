from src.widgets import Widget

class LabelWidget(Widget):
    def __init__(self, x, y, label, select_event=None):
        Widget.__init__(self, x, y, select_event)
        self.label = label
