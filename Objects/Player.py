from gameObj import *
from SpaceMath import *
from Camera import*

class Player(GameObject):
    def __init__(self, location, layer, spr, gm):
        self.location = location
        self.layer = layer
        self.spr = spr
        self.gm = gm
        self.AKeyDown = False
        self.SKeyDown = False
        self.DKeyDown = False
        self.WKeyDown = False
        self.Speed = 1
    
    def update(self, deltaTime):
        global MainCamera
        moveDelta = vec2(0, 0)
        if self.AKeyDown:
            moveDelta += vec2(-1, 0)
        if self.SKeyDown:
            moveDelta += vec2(0, -1)
        if self.DKeyDown:
            moveDelta += vec2(1, 0)
        if self.WKeyDown:
            moveDelta += vec2(0, 1)
        moveDelta = moveDelta * self.Speed
        self.location.Move(moveDelta)
        camcenter = self.location.getcenter() + moveDelta*10
        MainCamera.MoveTo(camcenter, vec2(1600, 1200))
        return 0
    
    def render(self, camera):
        if camera.bObjInCamera(self):
            fpos = camera.WorldPosToScreenPos(self.location.getfpos())
            lpos = camera.WorldPosToScreenPos(self.location.getlpos())
            ObjInScreenRt = rect4(fpos.x, fpos.y, lpos.x, lpos.y)
            self.spr.draw(ObjInScreenRt.getcenter().x, ObjInScreenRt.getcenter().y, ObjInScreenRt.getwid(), ObjInScreenRt.gethei());
        return 0
    
    def event(self, event):
        if(event.type == SDL_KEYDOWN):
            if event.key == SDLK_a:
                self.AKeyDown = True
            if event.key == SDLK_s:
                self.SKeyDown = True
            if event.key == SDLK_d:
                self.DKeyDown = True
            if event.key == SDLK_w:
                self.WKeyDown = True
        if(event.type == SDL_KEYUP):
            if event.key == SDLK_a:
                self.AKeyDown = False
            if event.key == SDLK_s:
                self.SKeyDown = False
            if event.key == SDLK_d:
                self.DKeyDown = False
            if event.key == SDLK_w:
                self.WKeyDown = False
        return 0
    