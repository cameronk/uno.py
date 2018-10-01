class Card:
    def __init__(self, number, color, id):
        self._number = number
        self._color = color
        self._id = id

    def __repr__(self):
        return "|{} {}|".format(self._color, self._number)

    @property
    def color(self):
        return self._color

    @property
    def number(self):
        return self._number
