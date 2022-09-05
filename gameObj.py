from pico2d import *
from SpaceMath import *
from Camera import *
global sprarr
sprarr = [
    load_image('tica.png') # 0
]

class Ptr:
    def __init__(self):
        return 0

class GameObject:
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
    
    def SetGameManager(self, gameManager):
        self.gm = gameManager
        return 0

class GameManager(Ptr):
    def __init__(self, objPool, isArrange):
        self.objPool = []
        self.isArrange = False
    
    def Update(self, deltaTime):
        if self.isArrange == False:
            #arrange by layer
            poolLen = len(self.objPool)
            i=0
            while(i < poolLen):
                k = i+1
                while(k < poolLen):
                    if self.objPool[i].layer > self.objPool[k].layer:
                        insobj = self.objPool[i]
                        self.objPool[i] = self.objPool[k]
                        self.objPool[k] = insobj
                    k += 1
                i += 1

            self.isArrange = True
        
        for obj in self.objPool:
            obj.update(deltaTime)
    
    def AddObject(self, obj):
        self.objPool.__add__(obj)
        self.isArrange = False
    
    def Render(self, camera):
        obj_index = 0
        poolLen = len(self.objPool)
        while(obj_index < poolLen):
            self.objPool[obj_index].render(camera)
            obj_index += 1
        return 0
    
    def Event(self, event):
        obj_index = 0
        poolLen = len(self.objPool)
        while(obj_index < poolLen):
            self.objPool[obj_index].event(event)
            obj_index += 1
        return 0