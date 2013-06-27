import pygame
from pygame.locals import *


pygame.init()

TRACK_EVENTS = [
    QUIT,
    KEYDOWN
]
IGNORE_EVENTS = [
    ACTIVEEVENT,
    KEYUP,
    MOUSEMOTION,
    MOUSEBUTTONUP,
    MOUSEBUTTONDOWN,
    JOYAXISMOTION,
    JOYBALLMOTION,
    JOYHATMOTION,
    JOYBUTTONUP,
    JOYBUTTONDOWN,
    VIDEORESIZE,
    VIDEOEXPOSE,
    USEREVENT
]


def get(mode='normal'):
    """
    mode -- str, identical to the way vim mode works (normal, insert)

    Returns tuple (mode, event_name, event_argument)
    """
    if not pygame.event.peek(TRACK_EVENTS):
        return
    events = pygame.event.get(TRACK_EVENTS)
    pygame.event.clear(IGNORE_EVENTS)
    for evt in events:
        if evt.type == KEYDOWN and evt.key == K_ESCAPE:
            mode = 'normal'
            return
        if mode == 'normal':
            if evt.type == QUIT:
                return (mode, 'quit', None)
            if evt.type == KEYDOWN:
                if evt.key == K_SLASH:
                    return ('insert', 'say', '/')
                if evt.key == K_h:
                    return (mode, 'move', (-1, 0))
                if evt.key == K_j:
                    return (mode, 'move', (0, 1))
                if evt.key == K_k:
                    return (mode, 'move', (0, -1))
                if evt.key == K_l:
                    return (mode, 'move', (1, 0))
                if evt.key == K_u:
                    return (mode, 'move', (-1, -1))
                if evt.key == K_i:
                    return (mode, 'move', (1, -1))
                if evt.key == K_n:
                    return (mode, 'move', (-1, 1))
                if evt.key == K_m:
                    return (mode, 'move', (1, 1))
        if mode == 'insert':
            # TODO: simple terminal input emulator
            pass
