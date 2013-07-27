DATA_SEPARATOR = '|'
SEPARATOR_ESC = '\\|'


def net_eval(data):
    """
    >>> net_eval("{'foo': 'bar'}|")
    [{'foo': 'bar'}]
    >>> net_eval("'foo'|'bar'")
    ['foo', 'bar']
    """
    data = data.split(DATA_SEPARATOR)
    if not data[:-1]:
        data.pop()
    valid_data = []
    for package in data:
        if package:
            try:
                package = package.replace(SEPARATOR_ESC, DATA_SEPARATOR)
                valid_data.append(eval(package))
            except (SyntaxError, TypeError):
                print "Invalid package detected"
    return valid_data


def net_repr(data):
    """
    >>> net_repr({'foo': 'bar'})
    "{'foo': 'bar'}|"
    """
    data = repr(data).replace(DATA_SEPARATOR, SEPARATOR_ESC)
    return data + DATA_SEPARATOR
