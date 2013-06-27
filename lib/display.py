import pygame


class Display:
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
        level -- 2d list of strings
        """
        for i, line in enumerate(view):
            surface = self.font.render(line, True, (255, 255, 255), (0, 0, 0))
            self.window.blit(surface, (0, i * self.symbol_height))

    def update(self):
        pygame.display.update()
