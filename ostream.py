class ostream:
    def __init__(self, file):
        self.file = file

    def __lshift__(self, obj):
        """<< stream operator

        >>> cout = ostream(sys.stdout)
        >>> cerr = ostream(sys.stderr)
        >>> nl = '\\n'

        >>> cout << 1 << " " << 2 << nl
        1 2
        <__main__.ostream object at 0x...>
        """
        self.file.write(str(obj))
        return self


if __name__ == '__main__':
    import doctest

    doctest.testmod(optionflags=doctest.ELLIPSIS)
