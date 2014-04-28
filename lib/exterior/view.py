"""Exterior (space) view generator."""


def generate_exterior_view(
        level,
        coords,
        radius,
        sight,
        pointer=None):
    """Generate an exterior view.

    Arguments:
        level -- An instance of lib.exterior.level.Level5D.
        coords -- Coordinates in form (p, q, x, y).
        radius -- View field radius.
        sight -- Drawing radius.
        pointer -- Spaceship's pointer.

    Returns:
        A list of strings made of characters to be displayed; a dict
        of tuples representing non-standard colors at specific coordinates.
    """
    # TODO: Replace this with cleaner and/or more efficient algorithm.
    p, q, x0, y0 = coords
    view, colors = [], {}
    for _ in xrange(0, radius * 2 + 1):
        line = [' ' for _ in xrange(0, radius * 2 + 1)]
        view.append(line)
    ny = 0
    for y in xrange(y0 - radius, y0 + radius + 1):
        nx = 0
        if y0 - sight <= y <= y0 + sight:
            for x in xrange(x0 - radius, x0 + radius + 1):
                if x0 - sight <= x <= x0 + sight:
                    if pointer and (p, q, x, y) == pointer:
                        view[ny][nx] = '+'
                    else:
                        obj = level.get_objects((p, q, x, y))[-1]
                        view[ny][nx] = obj.char
                        if not obj.is_default_color:
                            colors[(nx, ny)] = obj.color
                nx += 1
        ny += 1
    for y, line in enumerate(view):
        view[y] = ''.join(line)
    return view, colors
