"""Input-to-event converter."""

import pygame


pygame.init()
pygame.key.set_repeat(100, 100)

TRACK_EVENTS = [
    pygame.QUIT,
    pygame.KEYDOWN]

IGNORE_EVENTS = [
    pygame.ACTIVEEVENT,
    pygame.KEYUP,
    pygame.MOUSEMOTION,
    pygame.MOUSEBUTTONUP,
    pygame.MOUSEBUTTONDOWN,
    pygame.JOYAXISMOTION,
    pygame.JOYBALLMOTION,
    pygame.JOYHATMOTION,
    pygame.JOYBUTTONUP,
    pygame.JOYBUTTONDOWN,
    pygame.VIDEORESIZE,
    pygame.VIDEOEXPOSE,
    pygame.USEREVENT]


class Event(object):
    """Input-to-event converter."""

    def __init__(self):
        self.mode = self.prev_mode = 'normal'
        self.prompt = ''
        self.extended_keys = []
        self.temp_mode = None
        self.keys = {
            'dir': {
                'keys': {
                    'b': ('prev', 'arg', (-1, 1)),
                    'h': ('prev', 'arg', (-1, 0)),
                    'j': ('prev', 'arg', (0, 1)),
                    'k': ('prev', 'arg', (0, -1)),
                    'l': ('prev', 'arg', (1, 0)),
                    'n': ('prev', 'arg', (1, 1)),
                    'u': ('prev', 'arg', (1, -1)),
                    'y': ('prev', 'arg', (-1, -1)),
                    'any': ('prev', 'arg', False)},
                'temp': True},
            'eqp': {
                'keys': {
                    'i': ('inv', 'inventory', 1),
                    'u': (None, 'unequip', None),
                    'Q': ('normal', 'reset_right_pane', 1)},
                'temp': False},
            'insert': {
                'keys': {},
                'temp': True},
            'inv': {
                'keys': {
                    'd': (None, 'drop', None),
                    'e': (None, 'equip', None),
                    'E': ('eqp', 'equipment', 1),
                    'Q': ('normal', 'reset_right_pane', 1)},
                'temp': False},
            'look': {
                'keys': {
                    'b': (None, 'look_dir', (-1, 1)),
                    'h': (None, 'look_dir', (-1, 0)),
                    'j': (None, 'look_dir', (0, 1)),
                    'k': (None, 'look_dir', (0, -1)),
                    'l': (None, 'look_dir', (1, 0)),
                    'n': (None, 'look_dir', (1, 1)),
                    'u': (None, 'look_dir', (1, -1)),
                    'y': (None, 'look_dir', (-1, -1)),
                    'Q': ('normal', 'look_done', 1)},
                'temp': False},
            'normal': {
                'keys': {
                    'a': ('dir', 'activate', None),
                    'f': (None, 'int_fire', 1),
                    'i': ('inv', 'inventory', 1),
                    'b': (None, 'move', (-1, 1)),
                    'h': (None, 'move', (-1, 0)),
                    'j': (None, 'move', (0, 1)),
                    'k': (None, 'move', (0, -1)),
                    'l': (None, 'move', (1, 0)),
                    'n': (None, 'move', (1, 1)),
                    'u': (None, 'move', (1, -1)),
                    'y': (None, 'move', (-1, -1)),
                    't': (None, 'target', 1),
                    'v': ('look', 'look', 1),
                    'E': ('eqp', 'equipment', 1),
                    'Q': (None, 'quit', 1),
                    ',': (None, 'pickup', (0, 0)),
                    '/': ('insert', 'say', None)},
                'temp': False},
            'pilot': {
                'keys': {
                    'f': (None, 'ext_fire', 1),
                    'h': (None, 'rotate', 1),
                    'j': (None, 'accelerate', -50),
                    'k': (None, 'accelerate', 50),
                    'l': (None, 'rotate', 0),
                    'Q': ('normal', 'unpilot', 1)},
                'temp': False}}

    def get(self):
        if not pygame.event.peek(TRACK_EVENTS):
            return
        events = pygame.event.get(TRACK_EVENTS)
        pygame.event.clear(IGNORE_EVENTS)
        return self.process(events)

    def process(self, events):
        if self.mode == 'insert':
            return self._process_insert(events)
        return self._process_keys(events)

    def _process_keys(self, events):
        for evt in events:
            if evt.type == pygame.KEYDOWN:
                if evt.unicode in self.keys[self.mode]['keys']:
                    mode, action, arg = \
                        self.keys[self.mode]['keys'][evt.unicode]
                elif 'any' in self.keys[self.mode]['keys']:
                    mode, action, arg = self.keys[self.mode]['keys']['any']
                else:
                    continue
                self._set_mode(mode)
                if mode == 'prev':
                    self.mode = self.prev_mode
                return (action, arg)

    def _process_insert(self, events):
        for evt in events:
            if evt.key == pygame.K_ESCAPE:
                self.mode = self.prev_mode
            elif evt.key == pygame.K_BACKSPACE:
                if len(self.prompt):
                    self.prompt = self.prompt[:-1]
            elif evt.key == pygame.K_RETURN:
                text, self.prompt = self.prompt, ''
                self.mode = self.prev_mode
                return ('arg', text)
            else:
                self.prompt += evt.unicode
        return ('insert_type', self.prompt)

    def _set_mode(self, mode):
        if mode in [None, 'prev']:
            return
        self.prev_mode = self.mode
        self.mode = mode

    #--------------------------------------------------------------------------
    # Extending layout.

    def extend_current_layout(self, action, args):
        def alphabet_generator():
            for letter in ('abcdefghijklmnopqrstuvwxyz'
                           'ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
                yield letter
        alphabet = alphabet_generator()
        self._create_temp_mode(action)
        self._set_mode(self.temp_mode)
        for arg in args:
            letter = alphabet.next()
            self.extended_keys.append(letter)
            self.keys[self.temp_mode]['keys'][letter] = (None, action, arg)
        return self.extended_keys

    def collapse_current_layout(self):
        if self.temp_mode:
            del self.keys[self.temp_mode]
        self.temp_mode = None
        self.extended_keys = []

    def _create_temp_mode(self, mode):
        self.temp_mode = 'temp-' + mode
        self.keys[self.temp_mode] = {
            'keys': {'any': ('prev', 'arg', False)}, 'temp': True}

    #--------------------------------------------------------------------------
    # Accessors.

    def get_mode(self):
        return self.mode

    def get_prompt(self):
        return self.prompt

    def set_mode(self, mode):
        self.prev_mode = self.mode
        self.mode = mode

    def set_prompt(self, prompt):
        self.prompt = prompt
