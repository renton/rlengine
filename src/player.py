class Player():
    def __init__(self):
        self.had_input = False
        self.e = None

    def bind_entity(self, e):
        if self.e is None or self.get_delay() == 0:
            if self.e:
                self.unbind_entity()
            e.set_ai(False)
            self.e = e

    def unbind_entity(self):
        if self.e is not None and self.get_delay() == 0:
            if self.e:
                self.e.set_ai(True)
                self.e = None

    def move_e(self, map, x, y):
        if self.e:
            # instant moves
            if x == 0 and y == 0:
                # wait
                self.had_input = True
                return

            # actions that cause delay
            if (self.get_delay() == 0):
                target = map.tiles[self.e.x + x][self.e.y + y].get_attackable_target()
                if target:
                    if target.unit_group != self.e.unit_group:
                        self.e.attack(target)
                        self.had_input = True
                    else:
                        # can't attack teammates
                        return
                else:
                    self.had_input = self.e.walk(map, x, y)
    
    def wait_for_input(self):
        self.had_input = False

    def get_delay(self):
        return self.e.delay
