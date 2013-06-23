def encode(data):
    """
    data -- list
    """
    return '\n'.join(data)


def decode(data):
    """
    data -- str separated by new line characters
    """
    return data.split('\n')
