class Point(object):
    def __init__(self, x, y, z, state):
        self._x = x
        self._y = y
        self._z = z
        self._state = state

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def z(self):
        return self._z

    @property
    def xzy(self):
        return (self._x, self._z, self._y)

    @property
    def state(self):
        return self._state

    def _about(self, a, b):
        return abs(a-b) <= max(abs(a), abs(b)) * 0.01

    def __eq__(self, other):
        return (self._about(self._x, other._x) and
                self._about(self._y, other._y) and
                self._about(self._z, other._z) and
                self._about(self._state, other._state))

    def __repr__(self):
        return "(%s, %s, %s) Laser: %s" % (self._x, self._y, self._z, self._state)
