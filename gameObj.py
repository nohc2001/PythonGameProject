from dataclasses import dataclass
from pico2d import *
from SpaceMath import *
from Camera import *
import ctypes;

global sprarr
sprarr = []

class Ptr:
    def __init__(self):
        pass

@dataclass(Init=True)
class Collider:
    def __init__(self) -> None:
        self.colRT = rect4(0, 0, 0, 0);
        self.velocity = vec2(0, 0);
        pass

class ColidLayer:
    def __init__(self, name, priority) -> None:
        self.name = name;
        self.priority = priority;
        self.objList = []; # 이 레이어에 있는 오브젝트들의 id(리스트의 인덱스)
        self.consideringLayer = [];
        pass

    def AddConsideringLayer(self, layerID):
        self.consideringLayer.append(layerID);
        pass

class ColidManager:
    def __init__(self) -> None:
        self.Layers = [];
        self.Relation = [];
        pass

    def SortByPriority(self):
        index = 0;
        while(index < len(self.Layers)):
            kindex = index + 1;
            while(kindex < len(self.Layers)):
                if(self.Layers[kindex].priority > self.Layers[index].priority):
                    ins_layer = self.Layers[kindex];
                    self.Layers[kindex] = self.Layers[index];
                    self.Layers[index] = ins_layer;
                kindex += 1;
            index += 1;

    def AddLayer(self, name, priority):
        self.Layers.append(ColidLayer(name, priority));
        pass

    def AddObjToCollidLayer(self, layer_name, objid):
        index = 0;
        isadd = False;
        while(index < len(self.Layers)):
            if(self.Layers[index].name == layer_name):
                self.Layers[index].objList.append(objid);
                isadd = True;
            index += 1;
        if(isadd == False):
            self.Layers.append(ColidLayer(layer_name, 0));
            index = 0;
            isadd = False;
            while(index < len(self.Layers)):
                if(self.Layers[index].name == layer_name):
                    self.Layers[index].objList.append(objid);
                index += 1;
        pass

    def MoveUpdate(self, deltaTime):
        pass

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
        self.col = Collider() # location을 기준으로 하는 좌표계
    
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
        
        self.colManager = ColidManager();

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
