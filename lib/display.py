import pygame


class Display(object):

    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Space')
        self.font = pygame.font.Font('dat/fonts/VeraMono.ttf', 20)
        self.symbol_width, self.symbol_height = self.font.size('X')
        # TODO: check if font is monospace by comparing different symbols
        self.columns, self.lines = 80, 25
        screen_width = self.columns * self.symbol_width
        screen_height = self.lines * self.symbol_height
        self.window = pygame.display.set_mode((screen_width, screen_height))

    def draw(self, view):
        """
        view -- 2d list of strings
        """
        self.window.fill((0, 0, 0))
        for i, line in enumerate(view):
            line_len = 0
            for (charset, color) in line:
                surface = self.font.render(charset, True, color, (0, 0, 0))
                width = (line_len) * self.symbol_width
                self.window.blit(surface, (width, i * self.symbol_height))
                line_len += len(charset)

    def update(self):
        pygame.display.update()
