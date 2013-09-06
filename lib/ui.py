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
        self.inventory = None
        self.is_pilot_mode = False
        self.oscillator = 0
        self.mode = 'chat'

    def compose(self):
        self.oscillator = self.oscillator + 1 if self.oscillator < 50 else 0

        top_bar = self._compose_top_status_bar()

        left_pane = self._compose_view_pane()

        right_pane = getattr(self, '_compose_%s_pane' % self.mode)()

        bottom_bar = self._compose_bottom_status_bar()

        return top_bar, left_pane, right_pane, bottom_bar

    #--------------------------------------------------------------------------
    # composing panes

    def _compose_bottom_status_bar(self):
        bottom_status_bar = self.evt_mode_desc + self.bottom_status_bar
        return (bottom_status_bar, UI_COLOR)

    def _compose_chat_pane(self):
        pane = []
        for y in xrange(0, len(self.view_field)):
            if len(self.chat_log) >= y + 1:
                msg, msg_type = self.chat_log[y]
                pane.append([(' ' + msg, MSG_COLORS[msg_type])])
            elif y == len(self.view_field) - 1:
                pane.append([(' > ' + self.prompt, UI_COLOR)])
            else:
                pane.append([])
        return pane

    def _compose_equipment_pane(self):
        pane = []
        y = 0
        for k, v in self.equipment.items():
            pane.append([(' %s: %s' % (k, v), UI_COLOR)])
            y += 1
        n = len(self.view_field)
        for y in xrange(y, n):
            if y == n - 1:
                pane.append([(' > ' + self.prompt, UI_COLOR)])
            else:
                pane.append([])
        return pane

    def _compose_inventory_pane(self):
        pane = []
        y = 0
        if not len(self.inventory):
            pane.append([('Your inventory is empty...', UI_COLOR)])
            y += 1
        for item in self.inventory:
            pane.append([(item, UI_COLOR)])
            y += 1
        n = len(self.view_field)
        for y in xrange(y, n):
            if y == n - 1:
                pane.append([(' > ' + self.prompt, UI_COLOR)])
            else:
                pane.append([])
        return pane

    def _compose_top_status_bar(self):
        return (self.top_status_bar, UI_COLOR)

    def _compose_view_pane(self):
        pane = []
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
            pane.append(l)
        return pane

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

    def set_inventory(self, inventory):
        self.inventory = inventory

    def set_look_pointer(self, look_pointer):
        self.look_pointer = look_pointer
        self.oscillator = 0

    def set_mode(self, mode='chat'):
        self.mode = mode

    def set_prompt(self, prompt):
        self.prompt = prompt

    def set_target(self, target):
        self.target = target
        self.oscillator = 0

    def set_top_status_bar(self, top_status_bar):
        self.top_status_bar = top_status_bar

    def set_view_field(self, view_field):
        self.view_field = view_field
