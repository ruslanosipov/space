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
    for evt in events:
        if evt.type == pygame.KEYDOWN and evt.key == pygame.K_ESCAPE:
            return ('normal', None, None)
        if evt.type == pygame.QUIT:
            return (mode, 'quit', None)
        if mode == 'normal':
            if evt.type == pygame.KEYDOWN:
                if evt.unicode == 'Q':
                    return (mode, 'quit', None)
                if evt.unicode == '/':
                    return ('insert', 'say', evt.unicode)
                if evt.unicode == 'a':
                    return ('direction', 'activate', 1)
                if evt.unicode == 'v':
                    return ('direction', 'look', 1)
                if evt.key == pygame.K_LEFT:
                    return (mode, 'move', (-1, 0))
                if evt.key == pygame.K_DOWN:
                    return (mode, 'move', (0, 1))
                if evt.key == pygame.K_UP:
                    return (mode, 'move', (0, -1))
                if evt.key == pygame.K_RIGHT:
                    return (mode, 'move', (1, 0))
                if evt.unicode == 't':
                    return (mode, 'target', 1)
                if evt.unicode == 'f':
                    return (mode, 'int_fire', 1)
                if evt.unicode == ',':
                    return (mode, 'pickup', (0, 0))
                if evt.unicode == 'i':
                    return (mode, 'inventory', 1)
        if mode == 'pilot':
            if evt.type == pygame.KEYDOWN:
                if evt.unicode == 'Q':
                    return ('normal', 'unpilot', 1)
                if evt.key == pygame.K_LEFT:
                    return (mode, 'rotate', 1)
                if evt.key == pygame.K_RIGHT:
                    return (mode, 'rotate', 0)
                if evt.key == pygame.K_UP:
                    return (mode, 'accelerate', 0.1)
                if evt.key == pygame.K_DOWN:
                    return (mode, 'accelerate', -0.1)
                if evt.unicode == 'f':
                    return (mode, 'ext_fire', 1)
        if mode == 'insert':
            if evt.type == pygame.KEYDOWN:
                if evt.key == pygame.K_BACKSPACE:
                    return (mode, 'backspace', 1)
                if evt.key == pygame.K_RETURN:
                    return (mode, 'return', 1)
                return (mode, 'insert', evt.unicode)
        if mode == 'direction':
            if evt.type == pygame.KEYDOWN:
                if evt.key == pygame.K_LEFT:
                    return ('normal', 'arg', (-1, 0))
                if evt.key == pygame.K_DOWN:
                    return ('normal', 'arg', (0, 1))
                if evt.key == pygame.K_UP:
                    return ('normal', 'arg', (0, -1))
                if evt.key == pygame.K_RIGHT:
                    return ('normal', 'arg', (1, 0))
            return ('normal', 'arg', None)
