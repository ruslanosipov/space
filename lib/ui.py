MSG_COLORS = {
    0: (100, 255, 100),
    1: (100, 100, 100),
    2: (200, 200, 200),
    3: (200, 0, 0)}
UI_COLOR = (100, 100, 100)
SECONDARY_UI_COLOR = (165,  42,  42)


class UI(object):
    global MSG_COLORS
    global UI_COLOR

    def __init__(self):
        self.view_field = ''
        self.colors = {}
        self.chat_log = []
        self.prompt = ''
        self.evt_mode_desc = 24 * ' '
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
                pane.append([(' i', SECONDARY_UI_COLOR),
                             ('nventory ', UI_COLOR),
                             ('u', SECONDARY_UI_COLOR),
                             ('nequip ', UI_COLOR),
                             ('Q', SECONDARY_UI_COLOR),
                             ('uit', UI_COLOR)])
            else:
                pane.append([])
        return pane

    def _compose_inventory_pane(self):
        pane = []
        y = 0
        if not len(self.inventory):
            pane.append([('Your inventory is empty...', UI_COLOR)])
            y += 1
        for item, qty in self.inventory.items():
            if qty > 1:
                item = "%s (%d)" % (item, qty)
            pane.append([(item, UI_COLOR)])
            y += 1
        n = len(self.view_field)
        for y in xrange(y, n):
            if y == n - 1:
                pane.append([(' d', SECONDARY_UI_COLOR),
                             ('rop ', UI_COLOR),
                             ('e', SECONDARY_UI_COLOR),
                             ('quip ', UI_COLOR),
                             ('E', SECONDARY_UI_COLOR),
                             ('quipment ', UI_COLOR),
                             ('Q', SECONDARY_UI_COLOR),
                             ('uit', UI_COLOR)])
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
                char, color = self._draw_element(x, y, char)
                if len(l) and l[-1][1] == color:
                    l[-1][0] += char
                else:
                    l.append([char, color])
            pane.append(l)
        return pane

    def _draw_element(self, x, y, char):
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
        return char, color

    #--------------------------------------------------------------------------
    # accessors

    def set_default_colors(self, int_colors, ext_colors):
        self.default_colors = self.int_colors = int_colors
        self.ext_colors = ext_colors

    def toggle_pilot_mode(self):
        if self.is_pilot_mode:
            self.default_colors = self.int_colors
            self.is_pilot_mode = False
        else:
            self.default_colors = self.ext_colors
            self.is_pilot_mode = True

    @evt_mode_desc.setter
    def evt_mode_desc(self, value):
        self.evt_mode_desc = value + (24 - len(value)) * ' '

    @look_pointer.setter
    def look_pointer(self, value):
        self.look_pointer = value
        self.oscillator = 0

    @target.setter
    def target(self, value):
        self.target = value
        self.oscillator = 0
