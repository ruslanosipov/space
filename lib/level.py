"""Game level - either a spaceship interior or space."""

import importlib

from lib.utl import ignored


class NonexistentObjectDefinition(Exception):
    """Object is missing definition module."""


class ObjectDefinitionMissing(Exception):
    """Object is missing definition in one of the dat/*.txt files."""


class Level(object):
    """Game level - either a spaceship interior or space."""

    #--------------------------------------------------------------------------
    # Setup.

    def __init__(self, level_definition, obj_definitions):
        self.level = []
        self._load_level(level_definition, obj_definitions)

    def __repr__(self):
        return "<class '%s'>" % self.__class__.__name__

    def _load_level(self, level_definition, obj_definitions, extras=None):
        if extras is None:
            extras = {}
        level = []
        for y, line in enumerate(level_definition):
            level.append([])
            for x, chars in enumerate(line):
                level[y].append([])
                for char in chars:
                    if (x, y) in extras.keys() and extras[(x, y)][0] == char:
                        name = extras[(x, y)][1]
                    else:
                        try:
                            name = obj_definitions[char]
                        except KeyError:
                            raise ObjectDefinitionMissing
                    module = name.lower()
                    try:
                        module = importlib.import_module("lib.obj.%s" % module)
                    except ImportError:
                        raise NonexistentObjectDefinition
                    obj = getattr(module, name)()
                    with ignored.ignored(AttributeError):
                        _ = obj.coords
                        obj.coords = (x, y)
                    with ignored.ignored(AttributeError):
                        _ = obj.interior
                        obj.interior = self
                    level[y][x].append(obj)
        self.level = level

    #--------------------------------------------------------------------------
    # Object operations.

    def add_object(self, (x, y), obj, position=0):
        if not 0 <= y < self.get_height() or not 0 <= x < self.get_width(y):
            raise IndexError("coordinates can not be outside the level")
        if position > 0:
            position = - position
            self.level[y][x].insert(position, obj)
        else:
            self.level[y][x].append(obj)

    def move_object(self, (x0, y0), (x1, y1), obj):
        for x, y in [(x0, y0), (x1, y1)]:
            if not (0 <= y < self.get_height() or 0 <= x < self.get_width(y)):
                raise IndexError("coordinates can not be outside the level")
        self.remove_object((x0, y0), obj)
        self.add_object((x1, y1), obj)

    def remove_object(self, (x, y), obj):
        if not 0 <= y < self.get_height() or not 0 <= x < self.get_width(y):
            raise IndexError("coordinates can not be outside the level")
        del self.level[y][x][self.level[y][x].index(obj)]

    #--------------------------------------------------------------------------
    # Bulk object accessors.

    def get_objects(self, (x, y)):
        if not 0 <= y < self.get_height() or not 0 <= x < self.get_width(y):
            raise IndexError("coordinates can not be outside the level")
        return self.level[y][x]

    def is_path_blocker(self, (x, y)):
        if not 0 <= y < self.get_height() or not 0 <= x < self.get_width(y):
            raise IndexError("coordinates can not be outside the level")
        for obj in self.level[y][x]:
            if obj.is_path_blocker:
                return True
        return False

    def is_view_blocker(self, (x, y)):
        if not 0 <= y < self.get_height() or not 0 <= x < self.get_width(y):
            raise IndexError("coordinates can not be outside the level")
        for obj in self.level[y][x]:
            if obj.is_view_blocker:
                return True
        return False

    #--------------------------------------------------------------------------
    # Accessors.

    def get_height(self):
        return len(self.level)

    def get_width(self, y):
        return len(self.level[y])
