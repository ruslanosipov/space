import pygame
from pygame.locals import *


pygame.init()
pygame.key.set_repeat(100, 100)

TRACK_EVENTS = [
    QUIT,
    KEYDOWN]
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
    USEREVENT]


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
        if evt.type == KEYDOWN and evt.key == K_ESCAPE:
            return ('normal', None, None)
        if evt.type == QUIT:
            return (mode, 'quit', None)
        if mode == 'normal':
            if evt.type == KEYDOWN:
                if evt.unicode == 'Q':
                    return (mode, 'quit', None)
                if evt.unicode == '/':
                    return ('insert', 'say', evt.unicode)
                if evt.unicode == 'a':
                    return ('direction', 'activate', 1)
                if evt.unicode == 'v':
                    return ('direction', 'look', 1)
                if evt.unicode == 'h':
                    return (mode, 'move', (-1, 0))
                if evt.unicode == 'j':
                    return (mode, 'move', (0, 1))
                if evt.unicode == 'k':
                    return (mode, 'move', (0, -1))
                if evt.unicode == 'l':
                    return (mode, 'move', (1, 0))
                if evt.unicode == 't':
                    return (mode, 'target', 1)
                if evt.unicode == 'f':
                    return (mode, 'fire', 1)
                if evt.unicode == ',':
                    return (mode, 'pickup', (0, 0))
                if evt.unicode == 'i':
                    return (mode, 'inventory', 1)
                if evt.unicode == 'F':
                    return (mode, 'fly', 1)
        if mode == 'ship':
            if evt.type == KEYDOWN:
                if evt.unicode == 'F':
                    return (mode, 'fly', 1)
        if mode == 'insert':
            if evt.type == KEYDOWN:
                if evt.key == K_BACKSPACE:
                    return (mode, 'backspace', 1)
                if evt.key == K_RETURN:
                    return (mode, 'return', 1)
                return (mode, 'insert', evt.unicode)
        if mode == 'direction':
            if evt.type == KEYDOWN:
                if evt.unicode == 'h':
                    return ('normal', 'arg', (-1, 0))
                if evt.unicode == 'j':
                    return ('normal', 'arg', (0, 1))
                if evt.unicode == 'k':
                    return ('normal', 'arg', (0, -1))
                if evt.unicode == 'l':
                    return ('normal', 'arg', (1, 0))
            return ('normal', 'arg', None)
