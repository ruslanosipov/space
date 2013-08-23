def get_line((x, y), (x1, y1), length=False):
    """
    Draw line from (x, y) to (x1, y1). Returns a list.
    """
    steep = 0
    line = []
    dx = abs(x1 - x)
    if (x1 - x) > 0:
        sx = 1
    else:
        sx = -1
    dy = abs(y1 - y)
    if (y1 - y) > 0:
        sy = 1
    else:
        sy = -1
    if dy > dx:
        steep = 1
        x, y = y, x
        dx, dy = dy, dx
        sx, sy = sy, sx
    d = (2 * dy) - dx
    if not length:
        for i in range(0, dx):
            if steep:
                line.append((y, x))
            else:
                line.append((x, y))
            while d >= 0:
                y = y + sy
                d = d - (2 * dx)
            x = x + sx
            d = d + (2 * dy)
        line.append((x1, y1))
        return line
    for i in range(0, length):
        if steep:
            line.append((y, x))
        else:
            line.append((x, y))
        while d >= 0:
            y = y + sy
            d = d - (2 * dx)
        x = x + sx
        d = d + (2 * dy)
    return line
