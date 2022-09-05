from SpaceMath import *

class Camera:
    def __init__(self, center, Width, Height, destpos, powrate, screenWH):
        self.center = center
        self.Width = Width
        self.Height = Height
        self.destpos = destpos
        self.destWH = vec2(Width, Height)
        self.powrate = powrate
        self.Rt = rect4(self.center.x-self.Width/2, self.center.y-self.Height/2, self.center.x+self.Width/2, self.center.y+self.Height/2)
        self.screenWH = screenWH
    
    def MoveTo(self, destPos, destwh):
        self.destpos = destPos
        self.destWH = destwh
        return 0
    
    def Update(self, deltaTime):
        result = self.destpos * (1-self.powrate) + self.center * self.powrate
        self.center += (result - self.center) * deltaTime

        result = self.destWH * (1-self.powrate) + vec2(self.Width, self.Height) * self.powrate
        self.Width += (result.x - self.Width) * deltaTime
        self.Height += (result.y - self.Height) * deltaTime

        self.Rt = rect4(self.center.x-self.Width/2, self.center.y-self.Height/2, self.center.x+self.Width/2, self.center.y+self.Height/2)
        return 0
    
    def bObjInCamera(self, obj):
        if self.Rt.bRectTouchRect(obj.location):
            return True
        else:
            return False
    
    def WorldPosToScreenPos(self, v2):
        rpos = vec2(0, 0)
        rpos.x = self.screenWH.x * (v2.x - self.Rt.fx) / self.Width
        rpos.y = self.screenWH.y * (v2.y - self.Rt.fy) / self.Height
        return rpos

global MainCamera
MainCamera = Camera(vec2(0, 0), 800, 600, vec2(0, 0), 0.75, vec2(800, 600))