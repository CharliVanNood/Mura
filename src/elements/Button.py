from src.utils.vectors import Vector2
from src.utils.color import Color

class Button:
    def __init__(self, x, y, text):
        self.active = False
        self.hover = False

        self.position = Vector2(x, x)
        self.size = Vector2(100, 100)

        self.text = text
        self.color = Color(255, 0, 0)

        self.callback = None
        self.callback_args = []
    
    def getPos(self):
        return (self.position.getX(), self.position.getY(), self.size.getX(), self.size.getY())
    
    def setCallback(self, callback, args=[]):
        self.callback = callback
        self.callback_args = args
        return self

    def runCallback(self):
        if self.callback:
            self.callback(*self.callback_args)
        else:
            print("This button does not have a callback yet")