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
    
    def getPos(self):
        return (self.position.getX(), self.position.getY(), self.size.getX(), self.size.getY())