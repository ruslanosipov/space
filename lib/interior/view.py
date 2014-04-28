"""Generator of interior view of the spaceship."""

from lib.utl import bresenham
from lib.utl import ignored


def generate_interior_view(
            level,
            coords,
            radius,
            sight,
            visible_tiles,
            pointer=None,
            look=None):
    """Generate an interior view.

    Arguments:
        level -- An instance of lib.interior.level.Level3D.
        coords -- Coordinates in form (x, y).
        radius -- View field radius.
        sight -- Drawing radius.
        visible_tiles -- A list of visible tiles, see find_visible_tiles().
        pointer -- Target pointer.
        look -- Look pointer.

    Returns:
        A list of strings made of characters to be displayed; a dict
        of tuples representing non-standard colors at specific coordinates;
        relative target pointer position; relative look pointer position.
    """
    x0, y0 = coords
    view, colors, rel_pointer, rel_look = [], {}, None, None
    for _ in xrange(0, radius * 2 + 1):
        line = [' ' for _ in xrange(0, radius * 2 + 1)]
        view.append(line)
    for y in xrange(y0 - radius, y0 + radius + 1):
        if y0 - sight <= y <= y0 + sight:
            for x in xrange(x0 - radius, x0 + radius + 1):
                if x0 - sight <= x <= x0 + sight:
                    nx, ny = x - x0 + radius, y - y0 + radius
                    if pointer and (x, y) == pointer:
                        rel_pointer = (nx, ny)
                    if look and (x, y) == look:
                        rel_look = (nx, ny)
                    if (x, y) in visible_tiles:
                        obj = level.get_objects((x, y))[-1]
                        view[ny][nx] = obj.char
                        if not obj.is_default_color:
                            colors[(nx, ny)] = obj.color
    for y, line in enumerate(view):
        view[y] = ''.join(line)
    return view, colors, rel_pointer, rel_look


def find_visible_tiles(level, coords, radius, sight):
    """Find all tiles visible from coords within given sight.

    Arguments:
        level -- An instance of lib.interior.level.Level3D.
        coords -- Coordinates in form (x, y).
        radius -- View field radius.
        sight -- Eyesight radius.

    Returns:
        A list of coordinates.
    """
    x0, y0 = coords
    visible = []
    for y in xrange(y0 - radius, y0 + radius + 1):
        if y0 - sight <= y <= y0 + sight:
            for x in xrange(x0 - radius, x0 + radius + 1):
                if x0 - sight <= x <= x0 + sight:
                    line = bresenham.get_line((x0, y0), (x, y))
                    is_blocker = False
                    for (ix, iy) in line:
                        if not is_blocker and (ix, iy) not in visible:
                            visible.append((ix, iy))
                        with ignored.ignored(IndexError):
                            if level.is_view_blocker((ix, iy)):
                                is_blocker = True
    return visible
