class Borg:
    __shared_state = {}

    def __init__(self):
        self.__dict__ = self.__shared_state


def tests():
    b1 = Borg()
    b2 = Borg()
    b1.x = 5

    assert b1 is not b2
    assert b2.x == 5


if __name__ == '__main__':
    pass
