"""Context helper to ignore exceptions."""

import contextlib


@contextlib.contextmanager
def ignored(*exceptions):
    """Context helper to ignore exceptions."""
    try:
        yield
    except exceptions:
        pass
