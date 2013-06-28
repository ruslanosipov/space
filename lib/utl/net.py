DATA_SEPARATOR = '|'
SEPARATOR_ESC = '\\|'


def net_eval(data):
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
    data = repr(data).replace(DATA_SEPARATOR, SEPARATOR_ESC)
    return data + DATA_SEPARATOR
