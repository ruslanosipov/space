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


def get():
    if not pygame.event.peek(TRACK_EVENTS):
        return
    events = pygame.event.get(TRACK_EVENTS)
    pygame.event.clear(IGNORE_EVENTS)
    for evt in events:
        if evt.type == QUIT:
            return 'quit'
