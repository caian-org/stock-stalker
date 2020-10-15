class Ticker:
    def __init__(self, code, value, updated_at):
        self._code = code
        self._value = value
        self._updated_at = updated_at

    @property
    def code(self):
        return self._code

    @property
    def value(self):
        return self._value

    @property
    def updated_at(self):
        return self._updated_at
