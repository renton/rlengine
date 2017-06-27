from src.entities import Entity
from src.system.logger import log
from random import randint, choice
from sets import Set
from src.algos import *
from config import CONFIG

# TODO move some of the long SETTINGS key strings into their own functions in either classes or settings file
# TODO might not need to equip whole item... just durability and some other things

class UnitEntity(Entity):
    def __init__(self, e_id):
        Entity.__init__(self, e_id)

        self.alive                  = True
        self.swap_alt_delay         = 10
        self.equipment_paradigm_id  = None
        self.unit_group             = -1
        self.ai_radius_vision       = 10
        self.ai_target_ignore_range = 15
        self.target                 = None
        self.corpse_id              = 0
        self.anatomy_id             = 0
        self.attackable             = True

        # TODO this gets past in as param to build specific units
        self._load_data({})

        self.statuses = {}
        self.skills = {}
        self.traits = {}
        self.equipped = {}
        self.anatomy = {}

        self.tileset_id = 0
        self.tile_id = 963

        self._load_equipment_slots()

    def _decorator_is_alive(func):
        def func_wrapper(*args):
            if args[0].alive:
                return func(*args)
            else:
                return False
        return func_wrapper

    @_decorator_is_alive
    def step(self, map):
        Entity.step(self, map)

    def equip(self, item, slot):
        # apply stats + skills + statuses
        # TODO make sure this item is able to equip in this slot
        # TODO make sure this character actually has this slot in their anatomy
        result_items = ([], [])
        if item.u_id in self.inventory:
            if self.is_slot_equipped(slot):
                removed_item = self.unequip(slot)
                result_items[1].append(removed_item)
            self.equipped[slot] = item
            result_items[0].append(item)
        return result_items

    def unequip(self, slot):
        # remove stats + skills + statuses
        if self.is_slot_equipped(slot):
            tmp = self.equipped[slot] 
            self.equipped[slot] = None
            return tmp
        return None

    def is_slot_equipped(self, slot):
        return self.equipped[slot] != None

    def pickup_item(self, item):
        self.inventory[item.u_id] = item
        item.set_owner(self)

    def drop_item(self, item):
        item.clear_owner()
        del self.inventory[item.u_id]

    def _load_equipment_slots(self):
        self.equipped = {}
        if self.equipment_paradigm_id != None:
            dataset = CONFIG['anatomy_types'][self.anatomy_id]['parts']
            for k,v in dataset.items():
                self.equipped[v['name']] = None

    def swap_alt(self):
        if self.equipment_paradigm_id is not None:
            take_off = {}
            for i in CONFIG['anatomy_types'][self.anatomy_id]['weapon_slots']:
                take_off[i] = self.unequip[i]
            for k,v in CONFIG['anatomy_types'][self.anatomy_id]['weapon_swap_slots']:
                self.equip(self.equipped[k], v)
                self.equip(take_off[v], k)
            self.adjust_delay(self.swap_alt_delay)

    def get_current_weapons(self):
        weps = []
        if self.equipment_paradigm_id is not None:
            for i in CONFIG['equipment_anatomy'][self.anatomy_id]['weapon_slots']:
                if i in self.equipped:
                    weps.append(self.equipped[i])
        return weps

    def _generate_status_icon(self):
        pass

    @_decorator_is_alive
    def take_damage(self, dmg):
        Entity.take_damage(self, dmg)
        if self.hp <= 0:
            self._die()

    def get_unit_group(self):
        return self.unit_group

    def set_unit_group(self, unit_group):
        self.unit_group = unit_group

    def _die(self):
        self.alive = False
        is_ally = (self.unit_group == CONFIG['default_player_team'])
        #log.add_log(self.name + ' has died', LOG_MODE_ALLY_DEATH if is_ally else LOG_MODE_ENEMY_DEATH)
        self.remove_from_map()

    def attack(self, e):
        pass

    @_decorator_is_alive
    def step(self, map):
        if self.delay > 0:
            self.adjust_delay(-1)
        self._ai(map)

    # TODO sub in AI module classes
    @_decorator_is_alive
    def _ai(self, map):
        if not self.ai:
            return

        if (self.delay <= 0):
            targets = Set()
            # if there is an adjacent entity, it takes precendence
            for i in range(3):
                for j in range(3):
                    target = map.tiles[(i - 1) + self.x][(j - 1) + self.y].get_attackable_target()
                    if target and target != self and (target.unit_group != self.unit_group or target.unit_group == -1):
                        targets.add(target)

            if targets:
                target = choice(list(targets))
                self.attack(target)
                return 
            else:
                # check if target is too far way
                if self.get_target():
                    if abs(self.x - self.target.x) >= self.ai_target_ignore_range or abs(self.y - self.target.y) >= self.ai_target_ignore_range:
                        self.unset_target()

                # find targets in range
                if not self.get_target():
                    for i in range(self.ai_radius_vision * 2):
                        for j in range(self.ai_radius_vision * 2):
                            if ((i - self.ai_radius_vision) + self.x) < len(map.tiles) and ((j - self.ai_radius_vision) + self.y) < len(map.tiles[i]):
                                target = map.tiles[(i - self.ai_radius_vision) + self.x][(j - self.ai_radius_vision) + self.y].get_attackable_target()
                                if target and target != self and (target.unit_group != self.unit_group or target.unit_group == -1):
                                    targets.add(target)

                    # pick a target
                    if targets:
                        self.set_target(choice(list(targets)))

                else:
                    if self.get_target():
                        # approach target
                        delta_x = 0
                        delta_y = 0
                        if self.x > self.target.x:
                            delta_x = -1
                        if self.x < self.target.x:
                            delta_x = 1
                        if self.y > self.target.y:
                            delta_y = -1
                        if self.y < self.target.y:
                            delta_y = 1

                        if map.is_walkable(self.x + delta_x, self.y + delta_y):
                            self.walk(map, delta_x, delta_y)
                            return 

                # random movement
                can_move = False
                open_spots = []
                for i in range(3):
                    for j in range(3):
                        tile = map.tiles[(i - 1) + self.x][(j - 1) + self.y]
                        if tile.can_move():
                            open_spots.append(((i - 1), (j - 1)))
                if open_spots:
                    delta_x, delta_y = choice(open_spots)
                    self.walk(map, delta_x, delta_y)
                else:
                    self.walk(map, 0, 0)

    def get_target(self):
        if self.target and not self.target.alive:
            self.unset_target()
        return self.target

    def set_target(self, e):
        self.target = e

    def unset_target(self):
        self.target = None

    def get_armor_for_part(self, part):
        armors = []
        for slot,item in self.equipped.items():
            if hasattr(item, 'anatomy_defence'):
                if part in item.anatomy_defence:
                    armors.append((slot, item))
        return armors

    '''
    def take_body_part_dmg(self, part, dmg, attack_type):
        # apply bone defense vs raw damage
        dmg = dmg - (roll(2, SETTINGS['anatomy_types'][self.anatomy_id]['parts'][part]['def']) / 2)

        # apply weak_vs damage for attack_type + part
        if attack_type in SETTINGS['anatomy_types'][self.anatomy_id]['parts'][part]['weak_vs']:
            dmg = dmg * SETTINGS['anatomy_types'][self.anatomy_id]['parts'][part]['weak_vs'][attack_type]

        self.anatomy[part]['hp'] -= dmg
        if self.anatomy[part]['hp'] < 0:
            self.anatomy[part]['hp'] = 0
        # calculate stat penalties, injuries etc.
        # calculate bleed % and amount

        # TODO SHOULD WE KEEP THIS???
        # TODO should hp damage only be taken if part hp is under a threshold??? make constant
        if self.anatomy[part]['hp'] < 75:
            self.take_damage(SETTINGS['anatomy_types'][self.anatomy_id]['parts'][part]['e_hp_mod'] * dmg)
    '''

    '''
    def get_part_hp(self, part):
        return self.anatomy[part]['hp']
    '''

    def take_equipment_damage_at_slot(self, slot, dmg):
        self.equipped[slot].durability -= dmg
        if self.equipped[slot].durability <= 0:
            self.destroy_equipment_at_slot(slot)

    def destroy_equipment_at_slot(self, slot):
        # TODO also take out of inventory
        del self.equipped[slot]

    def pickup(self, tile):
        # move item from ground to inventory 
        pass

    def pickup_all(self, tile):
        items = []
        for k,v in tile.get_entities().items():
            if hasattr(v, 'is_item') and v.is_item:
                items.append(v)
                self.pickup_item(v)
        return items
