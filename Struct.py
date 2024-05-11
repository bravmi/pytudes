class Struct:
    """A structure that can have any fields defined.

    >>> options = Struct(answer=42, linelen=80, font='courier')
    >>> options.answer
    42
    >>> options.answer = 'plastics'
    >>> vars(options)
    {'answer': 'plastics', 'linelen': 80, 'font': 'courier'}
    """

    def __init__(self, **entries):
        self.__dict__.update(entries)

    def __repr__(self):
        args = ['%s=%s' % (k, repr(v)) for (k, v) in vars(self).items()]
        return 'Struct({})'.format(', '.join(args))


def update(x, **entries):
    if hasattr(x, 'update'):
        x.update(entries)
    else:
        x.__dict__.update(entries)
    return x


if __name__ == '__main__':
    import doctest

    doctest.testmod()
