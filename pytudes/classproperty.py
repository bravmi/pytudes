class classproperty(property):
    def __get__(self, obj, objtype):
        return super().__get__(objtype)


def tests():
    class A:
        @classproperty
        def x(cls):
            return 42

    assert A.x == 42
