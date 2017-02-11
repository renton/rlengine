import pygame

class InputManager():

    # ==XBOX GUIDE==
    # button
    # 0 - A
    # 1 - B
    # 2 - X
    # 3 - Y
    # axis
    # 0 - left analog - x 
    # 1 - left analog - y
    # 2 - LS pressure
    # 3 - right analog - x
    # 4 - right analog - y
    # 5 - RS pressure

    def __init__(self):

        self.joypad_enabled = False

        self.MOUSEBUTTONLEFT = 1
        self.MOUSEBUTTONCENTER = 2
        self.MOUSEBUTTONRIGHT = 3

        # init keyboard
        self.keystate = {}
        self.keyevents = {}

        # init mouse
        self.mousestate = {}
        self.mouse_x,self.mouse_y = (0,0)
        self.moustevents = {}

        self.joysticks = []
        self.joybuttonevents = {}
        if self.joypad_enabled:
            # init joypads
          pygame.joystick.init()
          for j_input in [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]:
              j_input.init()

              # not sure how expensive getting numbutton type calls are, so store in memory
              self.joysticks.append({
                  'obj':j_input,
                  'num_axes':j_input.get_numaxes(),
                  'num_buttons':j_input.get_numbuttons(),
                  'axisstates':{},
                  'buttonstates':{}
              })

    def _fetch_inputs(self):
        self.keystate = pygame.key.get_pressed()
        self.mousestate = pygame.mouse.get_pressed()
        self.mouse_x,self.mouse_y = pygame.mouse.get_pos()
        self._fetch_joypad_inputs()

    def update(self):
        self._fetch_inputs()

    # TODO going to have to compile dev version of pygame to fix stdout bug
    def _fetch_joypad_inputs(self):
        for joystick in self.joysticks:
            #axis
            for i in range(joystick['num_axes']):
                joystick['axisstates'][i] = joystick['obj'].get_axis(i)

            #buttons
            for i in range(joystick['num_buttons']):
                 joystick['buttonstates'][i] = joystick['obj'].get_button(i)

    def reset_events(self):
        self.keyevents = {}
        self.joybuttonevents = {}
        self.mouseevents = {}

    # ======================================================================
    #   JOY EVENTS
    # ======================================================================
    def set_joy_button_event(self,event,button):
        if event not in self.joybuttonevents:
            self.joybuttonevents[event] = {}
        self.joybuttonevents[event][button] = 1

    def is_joy_button_event(self,event,button):
        return (event in self.joybuttonevents and button in self.joybuttonevents[event])

    def is_joy_button_pressed(self,joy_id,button_id):
        return self.joysticks[joy_id]['buttonstates'][button_id] == 1

    # ======================================================================
    #   KEY EVENTS
    # ======================================================================
    def set_key_event(self,event,key):
        if event not in self.keyevents:
            self.keyevents[event] = {}
        self.keyevents[event][key] = 1

    def is_key_event(self, event, key):
        return (event in self.keyevents and key in self.keyevents[event])

    # ======================================================================
    #   MOUSE EVENTS
    # ======================================================================
    def is_lmouse_pressed(self):
        return self.is_mouse_event(pygame.MOUSEBUTTONDOWN, self.MOUSEBUTTONLEFT)

    def is_cmouse_pressed(self):
        return self.is_mouse_event(pygame.MOUSEBUTTONDOWN, self.MOUSEBUTTONCENTER)

    def is_rmouse_pressed(self):
        return self.is_mouse_event(pygame.MOUSEBUTTONDOWN, self.MOUSEBUTTONRIGHT)

    def is_mouse_event(self, event, button):
        return (event in self.mouseevents and button in self.mouseevents[event])

    def set_mouse_event(self, event, button):
        if event not in self.mouseevents:
            self.mouseevents[event] = {}
        self.mouseevents[event][button] = 1

im = InputManager()
