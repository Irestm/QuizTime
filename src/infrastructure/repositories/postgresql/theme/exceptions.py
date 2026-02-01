class ThemeNotFound(Exception):
    def __init__(self):
        super().__init__('Theme not found.')