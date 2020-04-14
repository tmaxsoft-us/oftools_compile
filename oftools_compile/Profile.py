class Profile:

    _section = None
    _options = None

    def __init__(self, section, options):
        self._section = section
        return

    @property
    def section(self):
        return self._section

    @property
    def options(self):
        return self._options