class Color:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def setFromRGB(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b
        return self

    def get(self):
        return (self.r, self.g, self.b)