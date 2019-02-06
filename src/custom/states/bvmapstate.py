import pygame

from config import EVENT_CUSTOM_CREATE_STATE

from src.map import Map
from src.entities import UnitEntity
from src.states import MapState

class BvMapState(MapState):
    def __init__(self, screen, player, room_id=None):
        MapState.__init__(self, screen, player)
        # TODO init room settings from room_data with room_id

        self.set_map(Map(True))

        test2 = UnitEntity(0)
        test2.set_unit_group(3)
        test1 = UnitEntity(0)
        test1.set_unit_group(3)

        test3 = UnitEntity(0)
        test3.set_unit_group(2)
        test4 = UnitEntity(0)
        test4.set_unit_group(2)

        self.add_entity_to_map(test2, 6, 6)
        self.add_entity_to_map(test1, 5, 5)
        self.add_entity_to_map(test3, 12, 12)
        self.add_entity_to_map(test4, 14, 14)

        #self.p1.bind_entity(test2)
        self.set_follow_camera(test1)

        #self.i_state = InventoryState(self.screen, self.p1, self)

        self._force_draw()
