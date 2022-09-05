from gameObj import *

class Player(GameObject):
    def __init__(self, location, layer, spr, gm):
        self.location = location
        self.layer = layer
        self.spr = spr
        self.gm = gm
    
    def update(self, deltaTime):
        return 0
    
    def render(self, camera):
        if camera.bObjInCamera(self):
            fpos = camera.WorldPosToScreenPos(self.location.getfpos())
            lpos = camera.WorldPosToScreenPos(self.location.getlpos())
            ObjInScreenRt = rect4(fpos.x, fpos.y, lpos.x, lpos.y)
            self.spr.draw(ObjInScreenRt.getcenter().x, ObjInScreenRt.getcenter().y, ObjInScreenRt.getwid(), ObjInScreenRt.gethei());
        return 0
    
    def event(self, events):
        return 0
    