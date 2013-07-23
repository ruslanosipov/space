class Level(object):

    #--------------------------------------------------------------------------
    # setup

    def __init__(self, level_definition, obj_definitions):
        """
        >>> o = {'.': 'Floor', '#': 'Door'}
        >>> Level([[['.'], ['#']], [['.'], ['#']]], o)
        <class 'Level'>

        level_definition -- list of lists of lists of chars
        obj_definitions -- dict
        """
        self._load_level(level_definition, obj_definitions)

    def __repr__(self):
        return "<class '%s'>" % self.__class__.__name__

    def _load_level(self, level_definition, obj_definitions):
        """
        level_definition -- list of lists of lists of chars
        obj_definitions -- dict
        """
        level = []
        for y, line in enumerate(level_definition):
            level.append([])
            for x, chars in enumerate(line):
                level[y].append([])
                for char in chars:
                    name = obj_definitions[char]
                    try:
                        module = name.lower()
                        exec("from lib.obj.%s import %s" % (module, name))
                        exec("obj = %s()" % name)
                        level[y][x].append(obj)
                    except ImportError:
                        pass
        self.level = level

    #--------------------------------------------------------------------------
    # object operations

    def add_object(self, (x, y), obj):
        """
        >>> level = Level([[['.']]], {'.': 'Floor'})
        >>> from lib.obj.door import Door
        >>> level.add_object((0, 0), Door())
        >>> level.get_objects((0, 0))
        [<class 'Floor'>, <class 'Door'>]
        >>> level.add_object((7, 9), Door())
        False
        """
        if not 0 <= y < self.get_height() or not 0 <= x < self.get_width(y):
            return False
        self.level[y][x].append(obj)

    def move_object(self, (x0, y0), (x1, y1), obj):
        """
        >>> level = Level([[['.'], ['.']]], {'.': 'Floor'})
        >>> from lib.obj.player import Player
        >>> player = Player('Mike')
        >>> level.add_object((0, 0), player)
        >>> level.move_object((0, 0), (1, 0), player)
        >>> level.get_objects((1, 0))
        [<class 'Floor'>, <class 'Player'> Mike]
        >>> level.move_object((2, 8), (7, 9), player)
        False
        """
        for x, y in [(x0, y0), (x1, y1)]:
            if not (0 <= y < self.get_height() or 0 <= x < self.get_width(y)):
                return False
        self.remove_object((x0, y0), obj)
        self.add_object((x1, y1), obj)

    def remove_object(self, (x, y), obj):
        """
        >>> level = Level([[['.']]], {'.': 'Floor'})
        >>> from lib.obj.door import Door
        >>> door = Door()
        >>> level.add_object((0, 0), door)
        >>> level.remove_object((0, 0), door)
        >>> level.get_objects((0, 0))
        [<class 'Floor'>]
        >>> level.remove_object((0, 0), door)
        False
        >>> level.remove_object((7, 9), door)
        False
        """
        if not 0 <= y < self.get_height() or not 0 <= x < self.get_width(y):
            return False
        if obj not in self.level[y][x]:
            return False
        del self.level[y][x][self.level[y][x].index(obj)]

    #--------------------------------------------------------------------------
    # bulk object accessors

    def get_objects(self, (x, y)):
        """
        >>> level = Level([[['.', '+']]], {'.': 'Floor', '+': 'Door'})
        >>> level.get_objects((0, 0))
        [<class 'Floor'>, <class 'Door'>]
        >>> level.get_objects((7, 9))
        False
        """
        if not 0 <= y < self.get_height() or not 0 <= x < self.get_width(y):
            return False
        if len(self.level[y][x]):
            return self.level[y][x]
        return False

    def is_path_blocker(self, (x, y)):
        """
        >>> level = Level([[['.'], ['#']]], {'.': 'Floor', '#': 'Wall'})
        >>> level.is_path_blocker((7, 8))
        False
        >>> level.is_path_blocker((0, 0))
        False
        >>> level.is_path_blocker((1, 0))
        True
        """
        if not 0 <= y < self.get_height() or not 0 <= x < self.get_width(y):
            return False
        for obj in self.level[y][x]:
            if obj.is_path_blocker():
                return True
        return False

    def is_view_blocker(self, (x, y)):
        """
        >>> level = Level([[['.'], ['#']]], {'.': 'Floor', '#': 'Wall'})
        >>> level.is_view_blocker((7, 8))
        False
        >>> level.is_view_blocker((0, 0))
        False
        >>> level.is_view_blocker((1, 0))
        True
        """
        if not 0 <= y < self.get_height() or not 0 <= x < self.get_width(y):
            return False
        for obj in self.level[y][x]:
            if obj.is_view_blocker():
                return True
        return False

    #--------------------------------------------------------------------------
    # accessors

    def get_height(self):
        """
        >>> o = {'.': 'Floor', '#': 'Door'}
        >>> level = Level([[['.'], ['#']], [['.'], ['#']]], o)
        >>> level.get_height()
        2
        """
        return len(self.level)

    def get_level(self):
        return self.level

    def get_width(self, y):
        """
        >>> o = {'.': 'Floor', '#': 'Door'}
        >>> level = Level([[['.'], ['#']], [['.'], ['#']]], o)
        >>> level.get_width(1)
        2
        >>> level.get_width(7)
        False
        """
        if y >= len(self.level):
            return False
        return len(self.level[y])
