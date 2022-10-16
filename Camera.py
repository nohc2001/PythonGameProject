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
        if(self.Rt.fx > self.Rt.lx):
            nn = self.Rt.lx;
            self.Rt.lx = self.Rt.fx;
            self.Rt.fx = nn;
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
    
    def ScreenPosToWorldPos(self, wpos):
        v2 = vec2(0, 0);
        v2.x = wpos.x * self.Width / self.screenWH.x + self.Rt.fx;
        v2.y = wpos.y * self.Height / self.screenWH.y + self.Rt.fy;
        return v2;
    
    def WorldLenToScreenLen(self, len):
        rate = ((self.screenWH.x / self.Width) + (self.screenWH.y / self.Height)) / 2
        return len * rate;

global MainCamera
global WMAX, HMAX
WMAX = 1000;
HMAX = 700;
MainCamera = Camera(vec2(0, 0), 2*WMAX, 2*HMAX, vec2(0, 0), 0.01, vec2(WMAX, HMAX))