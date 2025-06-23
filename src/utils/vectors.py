# The custom vector 2 class for vectors in 2d space
class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        # if clamp is enabled it will make sure the vectors will never become larger or smaller than set
        self.clamp_max = False
        self.clamp_min = False
        self.max_x = 0
        self.max_y = 0
        self.min_x = 0
        self.min_y = 0
    
    def set(self, x, y):
        self.x = x
        self.y = y
        self.checkClamp()
        return self # this return is so it's possible to stack modifiers

    def setX(self, x):
        self.x = x
        self.checkClamp
        return self # this return is so it's possible to stack modifiers

    def setY(self, y):
        self.y = y
        self.checkClamp
        return self # this return is so it's possible to stack modifiers
    
    def setMax(self, x, y):
        self.clamp_max = True
        self.max_x = x
        self.max_y = y
        return self # this return is so it's possible to stack modifiers

    def setMin(self, x, y):
        self.clamp_min = True
        self.min_x = x
        self.min_y = y
        return self # this return is so it's possible to stack modifiers
    
    def get(self):
        return [self.x, self.y]
    
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y

    def add(self, x, y): # adds 2 vectors together
        self.x += x
        self.y += y
        self.checkClamp()
        return self # this return is so it's possible to stack modifiers

    def multiply(self, x, y): # multiplies by vector
        self.x *= x
        self.y *= y
        self.checkClamp()
        return self # this return is so it's possible to stack modifiers
    
    def divide(self, x, y): # divides by vector
        self.x /= x
        self.y /= y
        self.checkClamp()
        return self # this return is so it's possible to stack modifiers
    
    def addVector(self, vector): # adds 2 vectors together
        self.x += vector.x
        self.y += vector.y
        self.checkClamp()
        return self # this return is so it's possible to stack modifiers
    
    def subtractVector(self, vector): # subtracts 2 vectors
        self.x -= vector.x
        self.y -= vector.y
        self.checkClamp()
        return self # this return is so it's possible to stack modifiers
    
    def magnitude(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def checkClamp(self):
        # make sure the value is set within bounds if needed
        if self.clamp_max:
            if self.x > self.max_x: self.x = self.max_x
            if self.y > self.max_y: self.y = self.max_y
        if self.clamp_min:
            if self.x < self.min_x: self.x = self.min_x
            if self.y < self.min_y: self.y = self.min_y
    
    def clone(self):
        return Vector2(self.x, self.y)