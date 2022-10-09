from dataclasses import dataclass
from pico2d import *
from SpaceMath import *
from Camera import *

global sprarr
sprarr = []

class Ptr:
    def __init__(self):
        a = 1

@dataclass(init=True)
class Part:
    #dir에 speed도 포함.
    def __init__(self, pos, dir, maxradius, gravity, maxtime, sprite) -> None:
        #설정값
        self.enable = True;
        self.pos = pos;
        self.dir = dir;
        self.maxradius = maxradius;
        self.gravity = gravity;
        self.sprite = sprite;
        self.flowtime = vec2(0, maxtime);

        #변화값
        self.yvelocity =0;
        self.radius = 0;
    
    def flowFunc(self, rate):
        #rate는 0~1까지의 실수
        f = 4*math.pow(rate-0.5, 2) + 1;
        return 1/(math.exp(-10*(f-0.5))+1);
    
    def update(self, deltatime):
        self.flowtime.x += deltatime;
        if(self.flowtime.x > self.flowtime.y):
            self.enable = False;
        self.pos += self.dir*deltatime;
        self.dir.y -= self.yvelocity*deltatime;
        self.yvelocity += self.gravity*deltatime;
        self.radius = self.maxradius * self.flowFunc(self.flowtime.x / self.flowtime.y);
        pass

    def render(self, camera):
        loc = rect4(self.pos.x - self.maxradius, self.pos.y - self.maxradius, self.pos.x + self.maxradius, self.pos.y + self.maxradius);
        if(camera.Rt.bRectTouchRect(loc)):
            loc = rect4(self.pos.x - self.radius, self.pos.y - self.radius, self.pos.x + self.radius, self.pos.y + self.radius);
            vf2 = camera.WorldPosToScreenPos(vec2(loc.fx, loc.fy));
            vl2 = camera.WorldPosToScreenPos(vec2(loc.lx, loc.ly));
            loc = rect4(vf2.x, vf2.y, vl2.x, vl2.y);

            self.sprite.draw(loc.fx, loc.fy, loc.getwid(), loc.gethei());
        pass

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
    def __init__(self):
        self.objPool = []
        self.isArrange = False
        
        self.partPool = [];
        self.partMax = 2048;
        self.partup = 0; #고려할 개수

        index = 0;
        while(index < self.partMax):
            self.partPool.append(Part(vec2(0, 0), vec2(0, 0), 0, 0, 0, 0));
            self.partPool[index].enable = False;
            index += 1;
        pass
    
    def AddPart(self, pos, dir, rad, gravity, maxtime, spr):
        if(self.partup + 1 < self.partMax):
            part = Part(pos, dir, rad, gravity, maxtime, spr);
            self.partPool[self.partup] = part;
            self.partup += 1;
        else:
            pindex = 0;
            while(pindex < self.partMax):
                if(self.partPool[pindex].enable == False):
                    part = Part(pos, dir, rad, gravity, maxtime, spr);
                    self.partPool[pindex] = part;
                    break;
                pindex += 1;
        pass

    def Update(self, deltaTime):
        poolLen = len(self.objPool)
        i=0
        while(i < poolLen):
            if(self.objPool[i].layer < 10000000 and self.objPool[i].layer > -10000000):
                self.objPool[i].layer = self.objPool[i].location.fy;

            k = i+1
            while(k < poolLen):
                if self.objPool[i].layer < self.objPool[k].layer:
                    insobj = self.objPool[i]
                    self.objPool[i] = self.objPool[k]
                    self.objPool[k] = insobj
                k += 1
            i += 1
        
        for obj in self.objPool:
            obj.update(deltaTime)
        
        pindex = 0;
        while(pindex < self.partup):
            if(self.partPool[pindex].enable):
                self.partPool[pindex].update(deltaTime);
            else:
                if(pindex == self.partup-1):
                    self.partup -= 1;
            pindex += 1;
        
        pass

    def AddObject(self, obj):
        self.objPool.append(obj)
        self.isArrange = False
        pass
    
    def Render(self, camera):
        obj_index = 0
        poolLen = len(self.objPool)
        while(obj_index < poolLen):
            self.objPool[obj_index].render(camera)
            obj_index += 1

        pindex = 0;
        while(pindex < self.partup):
            if(self.partPool[pindex].enable):
                self.partPool[pindex].render(camera);
            else:
                if(pindex == self.partup-1):
                    self.partup -= 1;
            pindex += 1;
        return 0
    
    def Event(self, event):
        obj_index = 0
        poolLen = len(self.objPool)
        while(obj_index < poolLen):
            self.objPool[obj_index].event(event)
            obj_index += 1
        return 0
