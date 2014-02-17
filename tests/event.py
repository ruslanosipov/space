import unittest
import pygame

from lib.event import Event


def _unicode_events(chars):
    events = []
    for char in chars:
        event = pygame.event.Event(
            pygame.KEYDOWN, unicode=char, key=None, mod=None)
        events.append(event)
    return events


def _key_events(keys):
    events = []
    for key in keys:
        event = pygame.event.Event(
            pygame.KEYDOWN, unicode=None, key=key, mod=None)
        events.append(event)
    return events


class TestEventGet(unittest.TestCase):

    def setUp(self):
        pygame.init()
        self.event = Event()

    def tearDown(self):
        pygame.quit()

    def test_simple_quit_action_called_by_unicode(self):
        events = _unicode_events(['Q'])
        self.assertEqual(self.event.process(events), ('quit', 1))
        self.assertEqual(self.event.get_mode(), 'normal')

    def test_activate_action_temporarily_switches_mode(self):
        events = _unicode_events(['a'])
        self.assertEqual(self.event.process(events), ('activate', None))
        self.assertNotEqual(self.event.get_mode(), 'normal')
        events = _unicode_events(['j'])
        self.assertEqual(self.event.process(events), ('arg', (0, 1)))
        self.assertEqual(self.event.get_mode(), 'normal')

    def test_dir_mode_is_exited_by_pressing_wrong_key(self):
        events = _unicode_events(['a'])
        self.event.process(events)
        self.event.process(events)
        self.assertEqual(self.event.get_mode(), 'normal')

    def test_insert_mode_adds_characters_to_the_prompt(self):
        self.event.process(_unicode_events(['/']))
        self.assertEqual(self.event.get_mode(), 'insert')
        self.assertEqual(
            self.event.process(_unicode_events(['h'])),
            ('insert_type', 'h'))
        self.assertEqual(
            self.event.process(_unicode_events(['i'])),
            ('insert_type', 'hi'))

    def test_insert_mode_adds_multiple_characters_at_once(self):
        self.event.process(_unicode_events(['/']))
        self.assertEqual(
            self.event.process(_unicode_events(['h', 'i'])),
            ('insert_type', 'hi'))

    def test_insert_mode_backspace_erases_character(self):
        self.event.process(_unicode_events(['/']))
        self.event.process(_unicode_events(['h', 'i']))
        self.assertEqual(
            self.event.process(_key_events([pygame.K_BACKSPACE])),
            ('insert_type', 'h'))

    def test_backspace_does_not_erase_non_existent_characters(self):
        self.event.process(_unicode_events(['/']))
        self.assertEqual(
            self.event.process(_key_events([pygame.K_BACKSPACE])),
            ('insert_type', ''))

    def test_escape_exits_insert_mode_keeps_the_prompt(self):
        self.event.process(_unicode_events(['/']))
        self.event.process(_unicode_events(['h', 'i']))
        self.assertEqual(
            self.event.process(_key_events([pygame.K_ESCAPE])),
            ('insert_type', 'hi'))
        self.assertEqual(self.event.get_mode(), 'normal')
        self.assertEqual(
            self.event.process(_unicode_events(['/'])),
            ('say', None))
        self.assertEqual(
            self.event.process(_unicode_events(['!'])),
            ('insert_type', 'hi!'))

    def test_insert_mode_can_be_exited_with_return_key(self):
        self.event.process(_unicode_events(['/']))
        self.event.process(_unicode_events(['h', 'i']))
        self.assertEqual(
            self.event.process(_key_events([pygame.K_RETURN])),
            ('arg', 'hi'))
        self.assertEqual(self.event.get_mode(), 'normal')
        self.event.process(_unicode_events(['/']))
        self.assertEqual(
            self.event.process(_unicode_events([])),
            ('insert_type', ''))

    def test_insert_mode_exit_returns_back_to_a_previous_mode(self):
        self.event.process(_unicode_events(['E']))
        self.assertEqual(self.event.get_mode(), 'eqp')
        self.event.process(_unicode_events(['e']))
        self.event.process(_key_events([pygame.K_RETURN]))
        self.assertEqual(self.event.get_mode(), 'eqp')

    def test_equipment_mode_returns_back_to_normal_mode(self):
        self.event.process(_unicode_events(['E']))
        self.assertEqual(self.event.get_mode(), 'eqp')
        self.event.process(_unicode_events(['e']))
        self.event.process(_key_events([pygame.K_RETURN]))
        self.assertEqual(self.event.get_mode(), 'eqp')
        self.event.process(_unicode_events(['Q']))
        self.assertEqual(self.event.get_mode(), 'normal')


class TestExtendLayout(unittest.TestCase):

    def setUp(self):
        pygame.init()
        self.event = Event()

    def tearDown(self):
        pygame.quit()

    def test_extended_layout_in_inventory(self):
        self.event.process(_unicode_events(['i']))
        self.assertEqual(self.event.get_mode(), 'inv')
        items = ['pants', 'hat']
        keys = self.event.extend_current_layout('equip', items)
        self.assertEqual(keys, ['a', 'b'])
        action = self.event.process(_unicode_events([keys[0]]))
        self.assertEqual(action, ('equip', items[0]))

    def test_exteneded_layout_can_be_collapsed(self):
        self.event.process(_unicode_events(['i']))
        keys = self.event.extend_current_layout('equip', ['pants', 'hat'])
        self.event.process(_unicode_events(['Q']))
        self.event.collapse_current_layout()
        action = self.event.process(_unicode_events([keys[0]]))
        self.assertEqual(action, ('activate', None))

    def test_extedned_layout_resets_on_every_call(self):
        self.event.process(_unicode_events(['i']))
        items = ['pants', 'hat']
        keys = self.event.extend_current_layout('equip', items)
        self.assertEqual(keys, ['a', 'b'])
        self.event.process(_unicode_events(['Q']))
        self.event.collapse_current_layout()
        self.event.process(_unicode_events(['i']))
        keys = self.event.extend_current_layout('equip', items)
        self.assertEqual(keys, ['a', 'b'])
