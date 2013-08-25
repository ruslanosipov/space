MSG_COLORS = {
    0: (100, 255, 100),
    1: (100, 100, 100),
    2: (200, 200, 200),
    3: (200, 0, 0)}
UI_COLOR = (100, 100, 100)


class UI(object):
    global MSG_COLORS
    global UI_COLOR

    def __init__(self):
        self.view_field = ''
        self.colors = {}
        self.chat_log = []
        self.prompt = ''
        self.evt_mode_desc = ''
        self.bottom_status_bar = ''
        ver = 'v0.3.1-alpha'
        self.top_status_bar = ' ' * (80 - len(ver)) + ver
        self.target = None
        self.look_pointer = None
        self.equipment = None
        self.is_pilot_mode = False
        self.oscillator = 0

    def compose(self):
        self.oscillator = self.oscillator + 1 if self.oscillator < 50 else 0

        top_status_bar = (self.top_status_bar, UI_COLOR)

        # left pane
        view_field = []
        for y, line in enumerate(self.view_field):
            l = []
            for x, char in enumerate(line):
                if (x, y) in self.colors.keys():
                    color = self.colors[(x, y)]
                else:
                    color = self.default_colors[char]
                if self.oscillator < 25:
                    if (x, y) == self.target:
                        char = 'x'
                        color = self.default_colors[char]
                    elif (x, y) == self.look_pointer:
                        char = 'l'
                        color = self.default_colors[char]
                if len(l) and l[-1][1] == color:
                    l[-1][0] += char
                else:
                    l.append([char, color])
            view_field.append(l)

        # right pane
        side_pane = []
        if self.equipment:
            pass
        else:
            for y in xrange(0, len(view_field)):
                if len(self.chat_log) >= y + 1:
                    msg, msg_type = self.chat_log[y]
                    side_pane.append([[' ' + msg, MSG_COLORS[msg_type]]])
                elif y == len(self.view_field) - 1:
                    side_pane.append([[' > ' + self.prompt, UI_COLOR]])
                else:
                    side_pane.append([])

        bottom_status_bar = self.evt_mode_desc + self.bottom_status_bar
        bottom_status_bar = (bottom_status_bar, UI_COLOR)

        return top_status_bar, view_field, side_pane, bottom_status_bar

    #--------------------------------------------------------------------------
    # accessors

    def get_prompt(self):
        return self.prompt

    def set_bottom_status_bar(self, bottom_status_bar):
        self.bottom_status_bar = bottom_status_bar

    def set_chat_log(self, chat_log):
        self.chat_log = chat_log

    def set_colors(self, colors):
        self.colors = colors

    def set_default_colors(self, int_colors, ext_colors):
        self.default_colors = self.int_colors = int_colors
        self.ext_colors = ext_colors

    def set_pilot_mode(self):
        if self.is_pilot_mode:
            self.default_colors = self.ext_colors
        else:
            self.default_colors = self.int_colors

    def set_evt_mode_desc(self, evt_mode_desc):
        self.evt_mode_desc = evt_mode_desc + (24 - len(evt_mode_desc)) * ' '

    def set_equipment(self, equipment):
        self.equipment = equipment

    def set_look_pointer(self, look_pointer):
        self.look_pointer = look_pointer
        self.oscillator = 0

    def set_prompt(self, prompt):
        self.prompt = prompt

    def set_target(self, target):
        self.target = target
        self.oscillator = 0

    def set_top_status_bar(self, top_status_bar):
        self.top_status_bar = top_status_bar

    def set_view_field(self, view_field):
        self.view_field = view_field
