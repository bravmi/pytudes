class Point(complex):
    """2-dimensional point

    >>> p = Point(3, 4)
    >>> p
    Point(3.0, 4.0)
    >>> p.x
    3.0

    >>> px, py = p
    >>> px, py
    (3.0, 4.0)

    >>> abs(p)
    5.0
    """

    x = property(lambda p: p.real)
    y = property(lambda p: p.imag)

    def __repr__(self):
        return f'Point({self.x}, {self.y})'

    def __iter__(self):
        yield self.x
        yield self.y


if __name__ == '__main__':
    import doctest

    doctest.testmod()
