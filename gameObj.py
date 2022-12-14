from dataclasses import dataclass
from gc import get_objects
from pico2d import *
from SpaceMath import *
from Camera import *
import ctypes;
import random;

global sprarr;
sprarr = [];
global fontObj;
fontObj = [];

def bRectinRect(rt1, rt2):
    if ((rt1.fx <= rt2.fx and rt2.fx <= rt1.lx) or (rt1.fx <= rt2.lx and rt2.lx <= rt1.lx)) and ((rt1.fy <= rt2.fy and rt2.fy <= rt1.ly) or (rt1.fy <= rt2.ly and rt2.ly <= rt1.ly)):
        return True;
    elif((rt2.fx <= rt1.fx and rt1.fx <= rt2.lx) or (rt2.fx <= rt1.lx and rt1.lx <= rt2.lx)) and ((rt2.fy <= rt1.fy and rt1.fy <= rt2.ly) or (rt2.fy <= rt1.ly and rt1.ly <= rt2.ly)):
        return True;
    else:
        return False;

class Ptr:
    def __init__(self):
        pass

@dataclass(init=True)
class Collider:
    def __init__(self) -> None:
        self.colRT = rect4(0, 0, 0, 0);
        self.velocity = vec2(0, 0);
        pass

@dataclass(init=True)
class Hitbox:
    def __init__(self, rt, tag, maxtime, damage) -> None:
        self.colRT = rt
        self.tag = tag
        self.timeflow = vec2(0, maxtime);
        self.isHit = False;
        self.Damage = 10;
        pass

class Projectile:
    sprlist = None;

    def __init__(self, startPos, dir, tag, damage, gm) -> None:
        if(Projectile.sprlist == None):
            Projectile.sprlist = [];
            Projectile.sprlist.append(load_image('./Resorceses/Particles/arcane.png')); #0
            Projectile.sprlist.append(load_image('./Resorceses/Particles/p_fire00.png')); #1
            Projectile.sprlist.append(load_image('./Resorceses/Particles/p_fire01.png')); #2
            Projectile.sprlist.append(load_image('./Resorceses/Particles/p_fire10.png')); #3
            Projectile.sprlist.append(load_image('./Resorceses/Particles/p_fire11.png')); #4
            Projectile.sprlist.append(load_image('./Resorceses/Particles/p_fire20.png')); #5
            Projectile.sprlist.append(load_image('./Resorceses/Particles/ice0.png')); #6
            Projectile.sprlist.append(load_image('./Resorceses/Particles/ice1.png')); #7
            Projectile.sprlist.append(load_image('./Resorceses/Particles/ice2.png')); #8
            #Projectile.sprlist.append(load_image('Resorceses/Particles/p_fire00.png')); #9
            #Projectile.sprlist.append(load_image('Resorceses/Particles/p_fire00.png')); #10
            #Projectile.sprlist.append(load_image('Resorceses/Particles/p_fire00.png')); #11
            #Projectile.sprlist.append(load_image('Resorceses/Particles/p_fire00.png')); #12

        self.pos = startPos;
        self.dir = dir;
        self.hitbox = Hitbox(rect4(self.pos.x - 10, self.pos.y-10, self.pos.x+10, self.pos.y+10), tag, 100, damage);
        self.partflow = vec2(0, 0.01);
        self.projectflow = vec2(0, 5);
        self.gm = gm;
        pass

    def update(self, delta):
        spr = Projectile.sprlist[0];
        if(self.hitbox.tag == 'Monster'):
            spr = Projectile.sprlist[0];
        elif(self.hitbox.tag == 'Player_Fire'):
            spr = Projectile.sprlist[random.randint(1, 5)];
        elif(self.hitbox.tag == 'Player_Ice'):
            spr = Projectile.sprlist[random.randint(6, 8)];

        self.partflow.x += delta;
        if(self.partflow.y < self.partflow.x):
            self.partflow.x = 0;
            self.gm.AddPart(self.pos, vec2(1, random.randint(-100, 100)), 20, 1000 + random.randint(-500, 500), 1, spr);
        
        self.projectflow.x += delta;
        if(self.projectflow.x > self.projectflow.y):
            self.hitbox.isHit = True;

        self.pos = self.pos + self.dir * delta;
        self.hitbox.colRT = rect4(self.pos.x - 10, self.pos.y-10, self.pos.x+10, self.pos.y+10);
        pass;

class RootItem:
    sprlist = None;

    def __init__(self, pos, itemname, target) -> None:
        if(RootItem.sprlist == None):
            RootItem.sprlist = [];
            RootItem.sprlist.append(load_image('./Resorceses/ItemIcon/gold.png'));
            RootItem.sprlist.append(load_image('./Resorceses/ItemIcon/HealthPotion.png'));
        
        # ???????????? ??????????????? ?????????


        self.target = target;
        
        self.enable = True;
        self.pos = pos;
        self.itemname = itemname;
        self.dropflow = vec2(0, 0.5);
        if(self.itemname == 'health_potion'):
            self.itemid = 1;
        elif(self.itemname == 'gold'):
            self.itemid = 0;
        pass

    def update(self, delta):
        if(self.enable == False):
            return;

        self.dropflow.x += delta;
        if(self.dropflow.y < self.dropflow.x):
            if(bRectinRect(rect4(self.pos.x-20, self.pos.y-20, self.pos.x+20, self.pos.y+20), self.target.location)):
                self.enable = False;
                self.target.AddItem(self.itemid);
        
        pass;
    
    def render(self, camera):
        if(self.enable == False):
            return;

        loc = rect4(self.pos.x-20, self.pos.y-20, self.pos.x+20, self.pos.y+20);
        fpos = camera.WorldPosToScreenPos(loc.getfpos())
        lpos = camera.WorldPosToScreenPos(loc.getlpos())
        ObjInScreenRt = rect4(fpos.x, fpos.y, lpos.x, lpos.y)
        RootItem.sprlist[self.itemid].draw(ObjInScreenRt.getcenter().x, ObjInScreenRt.getcenter().y, ObjInScreenRt.getwid(), ObjInScreenRt.gethei());
        pass;

class ColidLayer:
    def __init__(self, name, priority) -> None:
        self.name = name;
        self.priority = priority;
        self.objList = []; # ??? ???????????? ?????? ?????????????????? id(???????????? ?????????)
        self.consideringLayer = []; # ??? ????????? ?????? ?????? ???????????? ??????????????? ???????????? ???????????? ?????????.
        self.bSelfCollid = False;
        pass

    def AddConsideringLayer(self, layer):
        self.consideringLayer.append(layer);
        pass

    def MoveUpdate(self, deltaTime):
        if(self.bSelfCollid):
            i = 0;
            while(i < len(self.objList)):
                k = i+1;
                while(k < len(self.objList)):
                    get_objects()
                    obj1 = self.objList[objindex];
                    obj2 = self.objList[o_objindex];
                    self.TwoObjUpdate(obj1, obj2, False);
                    k += 1;
                i += 1;

        index = 0;
        while(index < len(self.consideringLayer)):
            olayer = self.consideringLayer[index];
            objindex = 0;
            while(objindex < len(self.objList)):
                o_objindex = 0;
                while(o_objindex < len(olayer.objList)):
                    obj1 = self.objList[objindex];
                    obj2 = olayer.objList[o_objindex];
                    self.TwoObjUpdate(obj1, obj2, True);
                    o_objindex += 1;
                objindex += 1;
            index += 1;
        pass

    def TwoObjUpdate(self, obj1, obj2, secondFrozen):
        if(secondFrozen == False):
            rt1m = obj1.col.colRT;
            rt1m.Move(obj1.col.velocity);

            rt2m = obj2.col.colRT;
            rt2m.Move(obj2.col.velocity);

            if(bRectinRect(rt1m, rt2m) == False):
                return False;
            
            nomoveCount = 0;
            col1 = obj1.col;
            col2 = obj2.col;
            if (obj1.col.velocity.x == 0 and obj2.col.velocity.x == 0):
                left_col = Collider();
                right_col = Collider();

                b = col1.colRT.getCenter().x > col2.colRT.getCenter().x;
                if(b):
                    left_col = col2;
                    right_col = col1;
                else:
                    left_col = col1;
                    right_col = col2;
                
                leftX = 0;
                rightX = 0;
                lvx = 0;
                rvx = 0;
                b = left_col.velocity.x != 0;
                if(b):
                    leftX = left_col.colRT.lx + left_col.velocity.x;
                    rightX = right_col.colRT.fx;
                    lvx = 0;
                    rvx = -right_col.velocity.x;
                else:
                    leftX = left_col.colRT.lx ;
                    rightX = right_col.colRT.fx + right_col.velocity.x;
                    lvx = left_col.velocity;
                    rvx = 0;

                CenterX = (lvx * rightX + rvx * leftX) / (lvx + rvx);

                leftVelX = CenterX - leftX;
                rightVelX = CenterX - rightX;

                leftRT = rect4();
                rightRT = rect4();

                if(lvx != 0):
                    leftRT = left_col.colRT + left_col.velocity * (leftVelX / lvx);
                else:
                    leftRT = left_col.colRT;
                if(rvx != 0):
                    rightRT = right_col.colRT + right_col.velocity * (rightVelX / rvx);
                else:
                    rightRT = right_col.colRT;
                
                if ((leftRT.fy < rightRT.fy and rightRT.fy < leftRT.ly) or (leftRT.fy < rightRT.ly and rightRT.ly < leftRT.ly)) or ((rightRT.fy < leftRT.fy and leftRT.fy < rightRT.ly) or (rightRT.fy < leftRT.ly and leftRT.ly < rightRT.ly)):
                    if(lvx != 0):
                        left_col.velocity = left_col.velocity * (leftVelX / lvx);
                    if(rvx != 0):
                        right_col.velocity = right_col.velocity * (rightVelX / rvx);
                else:
                    nomoveCount += 1;
            else:
                left_col = Collider();
                right_col = Collider();

                b = col1.colRT.getCenter().x > col2.colRT.getCenter().x;
                if(b):
                    left_col = col2;
                    right_col = col1;
                else:
                    left_col = col1;
                    right_col = col2;
                
                leftX = left_col.colRT.lx;
                rightX = right_col.colRT.fx;
                if (leftX <= rightX):

                    lvx = left_col.velocity.x;
                    rvx = -right_col.velocity.x;
                    CenterX = (lvx * rightX + rvx * leftX) / (lvx + rvx);
                    
                    leftVelX = CenterX - leftX;
                    rightVelX = CenterX - rightX;

                    leftRT = rect4();
                    rightRT = rect4();
                    if(lvx != 0):
                        leftRT = left_col.colRT + left_col.velocity * (leftVelX / lvx);
                    else:
                        leftRT = left_col.colRT;
                    
                    if(rvx != 0):
                        rightRT = right_col.colRT + right_col.velocity * (rightVelX / rvx);
                    else:
                        rightRT = right_col.colRT;

                    if((leftRT.fy < rightRT.fy and rightRT.fy < leftRT.ly) or (leftRT.fy < rightRT.ly and rightRT.ly < leftRT.ly)) or ((rightRT.fy < leftRT.fy and leftRT.fy < rightRT.ly) or (rightRT.fy < leftRT.ly and leftRT.ly < rightRT.ly)):
                        if(lvx != 0):
                            left_col.velocity = left_col.velocity * (leftVelX / lvx);
                        else:
                            left_col.velocity = left_col.velocity;

                        if(rvx != 0):
                            right_col.velocity = right_col.velocity * (rightVelX / rvx);
                        else:
                            right_col.velocity = right_col.velocity;
                    else:
                        nomoveCount += 1;
                else:
                    nomoveCount += 1;

            if (obj1.col.velocity.y == 0 and obj2.col.velocity.y == 0):
                top_col = Collider();
                bottom_col = Collider();

                b = col1.colRT.getCenter().y > col2.colRT.getCenter().y;
                if(b):
                    top_col = col2;
                    bottom_col = col1;
                else:
                    top_col = col1;
                    bottom_col = col2;
                
                topY = 0;
                bottomY = 0;
                tvy = 0;
                bvy = 0;
                b = top_col.velocity.y != 0;
                if(b):
                    topY = top_col.colRT.ly + top_col.velocity.y;
                    bottomY = bottom_col.colRT.fy;
                    tvy = 0;
                    bvy = -bottom_col.velocity.y;
                else:
                    topY = top_col.colRT.ly;
                    bottomY = bottom_col.colRT.fy + bottom_col.velocity.y;
                    tvy = top_col.velocity.y;
                    bvy = 0;

                CenterY = (tvy * bottomY + bvy * topY) / (tvy + bvy);

                topVelY = CenterY - topY;
                bottomVelY = CenterY - bottomY;

                topRT = rect4();
                bottomRT = rect4();

                if(tvy != 0):
                    topRT = top_col.colRT + top_col.velocity * (topVelY / tvy);
                else:
                    topRT = top_col.colRT;
                if(bvy != 0):
                    bottomRT = bottom_col.colRT + bottom_col.velocity * (bottomVelY / bvy);
                else:
                    bottomRT = bottom_col.colRT;
                
                if ((topRT.fx < bottomRT.fx and bottomRT.fx < topRT.lx) or (topRT.fx < bottomRT.lx and bottomRT.lx < topRT.lx)) or ((bottomRT.fx < topRT.fx and topRT.fx < bottomRT.lx) or (bottomRT.fx < topRT.lx and topRT.lx < bottomRT.lx)):
                    if(tvy != 0):
                        top_col.velocity = top_col.velocity * (topVelY / tvy);
                    if(bvy != 0):
                        bottom_col.velocity = bottom_col.velocity * (bottomVelY / bvy);
                else:
                    nomoveCount += 1;
            else:
                top_col = Collider();
                bottom_col = Collider();

                b = col1.colRT.getCenter().y > col2.colRT.getCenter().y;
                if(b):
                    top_col = col2;
                    bottom_col = col1;
                else:
                    top_col = col1;
                    bottom_col = col2;
                
                topY = top_col.colRT.ly;
                bottomY = bottom_col.colRT.fy;
                if (topY <= bottomY):
                    tvy = top_col.velocity.y;
                    bvy = -bottom_col.velocity.y;
                    CenterY = (tvy * bottomY + bvy * topY) / (tvy + bvy);
                    
                    topVelY = CenterY - topY;
                    bottomVelY = CenterY - bottomY;

                    topRT = rect4();
                    bottomRT = rect4();
                    if(tvy != 0):
                        topRT = top_col.colRT + top_col.velocity * (topVelY / tvy);
                    else:
                        topRT = top_col.colRT;
                    
                    if(bvy != 0):
                        bottomRT = bottom_col.colRT + bottom_col.velocity * (bottomVelY / bvy);
                    else:
                        bottomRT = bottom_col.colRT;

                    if((topRT.fx < rightRT.fx and rightRT.fx < topRT.lx) or (topRT.fx < rightRT.lx and rightRT.lx < topRT.lx)) or ((rightRT.fx < leftRT.fx and leftRT.fx < rightRT.lx) or (rightRT.fx < leftRT.lx and leftRT.lx < rightRT.lx)):
                        if(tvy != 0):
                            top_col.velocity = top_col.velocity * (topVelY / tvy);
                        else:
                            top_col.velocity = top_col.velocity;

                        if(bvy != 0):
                            bottom_col.velocity = bottom_col.velocity * (bottomVelY / bvy);
                        else:
                            bottom_col.velocity = bottom_col.velocity;
                    else:
                        nomoveCount += 1;
                else:
                    nomoveCount += 1;

            if (nomoveCount >= 2):
                col1.velocity = vec2(0, 0);
                col2.velocity = vec2(0, 0);
        else:
            rt1m = copy_rect4(obj1.col.colRT);
            rt1m.Move(obj1.col.velocity);

            rt2m = obj2.col.colRT;

            if(bRectinRect(rt1m, rt2m) == False):
                #print("col : false");
                return False;
            else:
                #print("col : true");
                rt1m = copy_rect4(obj1.col.colRT);
                rt1m.Move(vec2(obj1.col.velocity.x, 0));
                if(bRectinRect(rt1m, rt2m) == False):
                    obj1.col.velocity = vec2(obj1.col.velocity.x, 0);
                    return True;
                rt1m = copy_rect4(obj1.col.colRT);
                rt1m.Move(vec2(0, obj1.col.velocity.y));
                if(bRectinRect(rt1m, rt2m) == False):
                    obj1.col.velocity = vec2(0, obj1.col.velocity.y);
                    return True;
                obj1.col.velocity = vec2(0, 0);
                return True;
        pass

class ColidManager:
    def __init__(self) -> None:
        self.Layers = [];
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
        index = 0;
        while(index < len(self.Layers)):
            self.Layers[index].MoveUpdate(deltaTime);
            index += 1;
        pass

    def AddRelation(self, name1, name2):
        index = 0;
        layer1 = self.Layers[0];
        layer2 = self.Layers[1];
        while(index < len(self.Layers)):
            if(self.Layers[index].name == name1):
                layer1 = self.Layers[index];
            
            if(self.Layers[index].name == name2):
                layer2 = self.Layers[index];
            index += 1;
        
        layer1.AddConsideringLayer(layer2);
        pass;
    

@dataclass(init=True)
class Part:
    #dir??? speed??? ??????.
    def __init__(self, pos, dir, maxradius, gravity, maxtime, sprite) -> None:
        #?????????
        self.enable = True;
        self.pos = pos;
        self.dir = dir;
        self.maxradius = maxradius;
        self.gravity = gravity;
        self.sprite = sprite;
        self.flowtime = vec2(0, maxtime);

        #?????????
        self.yvelocity =0;
        self.radius = 0;
    
    def flowFunc(self, rate):
        #rate??? 0~1????????? ??????
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

            rate = math.pow(1 - (self.flowtime.x / self.flowtime.y), 3);
            self.sprite.draw(loc.fx, loc.fy, loc.getwid()*rate, loc.gethei()*rate);
        pass

class GameObject:
    HPBAR_image = None;
    HP_image = None;

    def __init__(self, location, layer, spr, gm):
        self.location = location
        self.layer = layer
        self.spr = spr
        self.gm = gm
        self.visible = True;
        self.col = Collider() # location??? ???????????? ?????? ?????????
        self.enable = True;
    
    def update(self, deltaTime):
        return 0
    
    def render(self, camera):
        if(self.visible == False): return;
        #if camera.bObjInCamera(self):
        if True:
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
    
    def AddHitbox(self, Tag, rt, maxtime, damage):
        hb = Hitbox(rt, Tag, maxtime, damage);
        self.gm.HitboxPool.append(hb);

class GameManager(Ptr):
    def __init__(self):
        self.objPool = []
        self.isArrange = False
        
        self.colManager = ColidManager();

        self.partPool = [];
        self.partMax = 2048;
        self.partup = 0; #????????? ??????

        self.HitboxPool = [];

        self.ProjectilePool = [];

        self.RootItemPool = [];

        index = 0;
        while(index < self.partMax):
            self.partPool.append(Part(vec2(0, 0), vec2(0, 0), 0, 0, 0, 0));
            self.partPool[index].enable = False;
            index += 1;
        pass

    def AddPart(self, pos, dir, rad, gravity, maxtime, spr):
        global MainCamera;
        if(MainCamera.Rt.bPosInRect(pos) == False):
            return;

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

    def AddProjectile(self, startPos, dir, tag, damage):
        pj = Projectile(startPos, dir, tag, damage, self);
        self.ProjectilePool.append(pj);
        pass;

    def AddRootItem(self, pos, itemname, target):
        ri = RootItem(pos, itemname, target);
        self.RootItemPool.append(ri);
        pass;

    def Update(self, deltaTime):
        poolLen = len(self.objPool)
        i=0
        while(i < poolLen):
            k = i+1
            while(k < poolLen):
                if self.objPool[i].layer < self.objPool[k].layer:
                    insobj = self.objPool[i]
                    self.objPool[i] = self.objPool[k]
                    self.objPool[k] = insobj
                k += 1
            i += 1
        
        self.colManager.MoveUpdate(deltaTime);

        for obj in self.objPool:
            obj.update(deltaTime)

            if(obj.enable == False):
                self.objPool.remove(obj);
                del obj;

        pindex = 0;
        while(pindex < self.partup):
            if(self.partPool[pindex].enable):
                self.partPool[pindex].update(deltaTime);
            else:
                if(pindex == self.partup-1):
                    self.partup -= 1;
            pindex += 1;
        
        for hb in self.HitboxPool:
            hb.timeflow.x += deltaTime;
            if(hb.timeflow.x > hb.timeflow.y):
                hb.isHit = True;
            
            if(hb.isHit):
                self.HitboxPool.remove(hb);
                del hb;
        
        for pj in self.ProjectilePool:
            pj.hitbox.timeflow.x += deltaTime;
            if(pj.hitbox.timeflow.x > pj.hitbox.timeflow.y):
                pj.hitbox.isHit = True;
            
            pj.update(deltaTime);
            
            if(pj.hitbox.isHit):
                self.ProjectilePool.remove(pj);
                del pj;
        
        for ri in self.RootItemPool:
            ri.update(deltaTime);
            
            if(ri.enable == False):
                self.RootItemPool.remove(ri);
                del ri;
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

        
        for ri in self.RootItemPool:
            ri.render(camera);

        return 0
    
    def Event(self, event):
        obj_index = 0
        poolLen = len(self.objPool)
        while(obj_index < poolLen):
            self.objPool[obj_index].event(event)
            obj_index += 1
        return 0
