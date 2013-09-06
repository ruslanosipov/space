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


def get(mode='normal'):
    """
    mode -- str, identical to the way vim mode works (normal, insert,
    direction)

    Returns tuple (mode, event_name, event_argument)
    """
    if not pygame.event.peek(TRACK_EVENTS):
        return
    events = pygame.event.get(TRACK_EVENTS)
    pygame.event.clear(IGNORE_EVENTS)
    if mode == 'insert':
        text = ""
        for evt in events:
            if evt.type == pygame.KEYDOWN:
                if evt.key == pygame.K_ESCAPE:
                    return ('normal', None, None, None)
                if evt.key == pygame.K_BACKSPACE:
                    return (mode, 'backspace', 1, None)
                if evt.key == pygame.K_RETURN:
                    return (mode, 'return', 1, 'str')
                text += evt.unicode
        return (mode, 'insert', text, 'str')
    for evt in events:
        if evt.type == pygame.QUIT:
            return (mode, 'quit', None, None)
        if mode == 'normal':
            if evt.type == pygame.KEYDOWN:
                if evt.unicode == 'Q':
                    return (mode, 'quit', None, None)
                if evt.unicode == '/':
                    return ('insert', 'say', evt.unicode, 'str')
                if evt.unicode == 'a':
                    return ('direction', 'activate', 1, 'int')
                if evt.unicode == 'v':
                    return ('look', 'look', 1, 'int')
                if evt.key == pygame.K_LEFT:
                    return (mode, 'move', (-1, 0), 'tuple_of_int')
                if evt.key == pygame.K_DOWN:
                    return (mode, 'move', (0, 1), 'tuple_of_int')
                if evt.key == pygame.K_UP:
                    return (mode, 'move', (0, -1), 'tuple_of_int')
                if evt.key == pygame.K_RIGHT:
                    return (mode, 'move', (1, 0), 'tuple_of_int')
                if evt.unicode == 't':
                    return (mode, 'target', 1, 'int')
                if evt.unicode == 'f':
                    return (mode, 'int_fire', 1, 'int')
                if evt.unicode == ',':
                    return (mode, 'pickup', (0, 0), 'tuple_of_int')
                if evt.unicode == 'i':
                    return (mode, 'inventory', 1, 'int')
                if evt.unicode == 'E':
                    return ('equipment', 'equipment', 1, 'int')
        if mode == 'pilot':
            if evt.type == pygame.KEYDOWN:
                if evt.unicode == 'Q':
                    return ('normal', 'unpilot', 1, 'int')
                if evt.key == pygame.K_LEFT:
                    return (mode, 'rotate', 1, 'int')
                if evt.key == pygame.K_RIGHT:
                    return (mode, 'rotate', 0, 'int')
                if evt.key == pygame.K_UP:
                    return (mode, 'accelerate', 100, 'int')
                if evt.key == pygame.K_DOWN:
                    return (mode, 'accelerate', -100, 'int')
                if evt.unicode == 'f':
                    return (mode, 'ext_fire', 1, 'int')
        if mode == 'direction':
            if evt.type == pygame.KEYDOWN:
                if evt.key == pygame.K_LEFT:
                    return ('normal', 'arg', (-1, 0), 'tuple_of_int')
                if evt.key == pygame.K_DOWN:
                    return ('normal', 'arg', (0, 1), 'tuple_of_int')
                if evt.key == pygame.K_UP:
                    return ('normal', 'arg', (0, -1), 'tuple_of_int')
                if evt.key == pygame.K_RIGHT:
                    return ('normal', 'arg', (1, 0), 'tuple_of_int')
                if evt.unicode == '.':
                    return ('normal', 'arg', (0, 0), 'tuple_of_int')
            return ('normal', 'arg', None, None)
        if mode == 'look':
            if evt.type == pygame.KEYDOWN:
                if evt.key == pygame.K_LEFT:
                    return ('look', 'look_dir', (-1, 0), 'tuple_of_int')
                if evt.key == pygame.K_DOWN:
                    return ('look', 'look_dir', (0, 1), 'tuple_of_int')
                if evt.key == pygame.K_UP:
                    return ('look', 'look_dir', (0, -1), 'tuple_of_int')
                if evt.key == pygame.K_RIGHT:
                    return ('look', 'look_dir', (1, 0), 'tuple_of_int')
                if evt.key == pygame.K_ESCAPE or evt.unicode == 'Q':
                    return ('normal', 'look_done', 1, 'int')
        if mode == 'equipment':
            if evt.type == pygame.KEYDOWN:
                if evt.unicode == 'e':
                    return ('insert', 'equip', 1, 'int')
                if evt.unicode == 'u':
                    return ('insert', 'unequip', 1, 'int')
                if evt.unicode == 'd':
                    return ('insert', 'drop', 1, 'int')
                if evt.unicode == 'i':
                    return ('inventory', 'inventory', 1, 'int')
                if evt.key == pygame.K_ESCAPE or evt.unicode == 'Q':
                    return ('normal', None, None, None)
        if mode == 'inventory':
            if evt.type == pygame.KEYDOWN:
                if evt.unicode == 'E':
                    return ('equipment', 'equipment', 1, 'int')
                if evt.key == pygame.K_ESCAPE or evt.unicode == 'Q':
                    return ('normal', None, None, None)
