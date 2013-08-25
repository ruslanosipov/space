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

    def draw(self, top_bar, left_pane, right_pane, bottom_bar):
        self.window.fill((0, 0, 0))

        char_seq, color = top_bar
        surface = self.font.render(char_seq, True, color, (0, 0, 0))
        self.window.blit(surface, (0, 0))

        char_seq, color = bottom_bar
        surface = self.font.render(char_seq, True, color, (0, 0, 0))
        self.window.blit(surface, (0, 24 * self.symbol_height))

        for i, line in enumerate(left_pane):
            x = 0
            for char_seq, color in line:
                surface = self.font.render(char_seq, True, color, (0, 0, 0))
                self.window.blit(surface, (x * self.symbol_width,
                                           (i + 1) * self.symbol_height))
                x += len(char_seq)

        for i, line in enumerate(right_pane):
            if len(line):
                x = 23
                for char_seq, color in line:
                    surface = self.font.render(char_seq, 1, color, (0, 0, 0))
                    self.window.blit(surface, (x * self.symbol_width,
                                               (i + 1) * self.symbol_height))
                    x += len(char_seq)

    def update(self):
        pygame.display.update()
