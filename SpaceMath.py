from ast import operator

class vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        v2 = vec2(0, 0)
        v2.x = self.x + other.x
        v2.y = self.y + other.y
        return v2
    
    def __sub__(self, other):
        v2 = vec2(0, 0)
        v2.x = self.x - other.x
        v2.y = self.y - other.y
        return v2
    
    def __mul__(self, other):
        v2 = vec2(0, 0)
        v2.x = self.x * other
        v2.y = self.y * other
        return v2
    
    def __truediv__(self, other):
        if other != 0:
            v2 = vec2(0, 0)
            v2.x = self.x / other
            v2.y = self.y / other
            return v2
        else:
            v2 = vec2(0, 0)
            v2.x = 0
            v2.y = 0
            return v2

class rect4:
    def __init__(self, fx, fy, lx, ly):
        self.fx = fx
        self.fy = fy
        self.lx = lx
        self.ly = ly
    
    def getwid(self):
        return self.lx - self.fx
    
    def gethei(self):
        return self.ly - self.fy
    
    def getcenter(self):
        return vec2((self.lx + self.fx) / 2, (self.ly + self.fy) / 2)
    
    def getfpos(self):
        return vec2(self.fx, self.fy)
    
    def getlpos(self):
        return vec2(self.lx, self.ly)

    def bPosInRect(self, v2):
        if(self.fx < v2.x and v2.x < self.lx) and (self.fy < v2.y and v2.y < self.ly):
            return True
        else :
            return False

    def bRectInRect(self, smallRt):
        if self.bPosInRect(vec2(smallRt.fx, smallRt.fy)) and self.bPosInRect(vec2(smallRt.lx, smallRt.ly)):
            return True
        else:
            return False
    
    def bRectTouchRect(self, smallRt):
        if(self.fx < smallRt.lx and smallRt.fx < self.lx) and (self.fy < smallRt.ly and smallRt.fy < self.ly):
            return True
        else :
            return False
    
    def Move(self, v2):
        self.fx += v2.x
        self.lx += v2.x
        self.fy += v2.y
        self.ly += v2.y
