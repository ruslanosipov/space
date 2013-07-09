class Spaceship:

    def __init__(self, (x, y)):
        self.x, self.y = x, y
        self.targets = [
            (0, -2),
            (1, -2),
            (2, -1),
            (2, 0),
            (2, 1),
            (1, 2),
            (0, 2),
            (-1, 2),
            (-2, 1),
            (-2, 0),
            (-2, -1),
            (-1, -2)]
        self.target = self.targets[0]
        self.target_index = 0

    def rotate_target(self, reverse=False):
        i = 1 if not reverse else -1
        if self.target_index == len(self.targets) - 1 and not reverse:
            self.target_index = 0
        elif self.target_index == 0 and reverse:
            self.target_index = len(self.targets) - 1
        else:
            self.target_index += i
        self.target = self.targets[self.target_index]

    def get_coordinates(self):
        return (self.x, self.y)

    def get_target(self):
        dx, dy = self.target
        return (self.x + dx, self.y + dy)
