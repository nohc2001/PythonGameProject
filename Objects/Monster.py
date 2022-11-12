from gameObj import *
from SpaceMath import *
from Camera import*

class Monster(GameObject):
    def __init__(self, location, layer, walkspr, idlespr, attackspr, gm, target):
        global playerobj;
        super().__init__(location, layer, idlespr, gm);
        self.walkspr = walkspr
        self.idlespr = idlespr
        self.attackspr = attackspr;

        self.state = 'idle';
        self.target = target;
        self.attackDelay = vec2(0, 0.2);

        self.attackMaxFrame = 41;
        self.walkMaxFrame = 21;
        self.idleMaxFrame = 31;
        self.presentFrame = 0;
        self.MaxFrame = 0;
        self.FrameUpdateDelta = vec2(0, 0.03)
        
        self.movedir = 1

        self.Speed = 200;
        self.gravity = 0.1;
        self.AddY = 0;
        self.jumpForce = 5;

        self.seekRange = 1000;
        self.chaseRange = 700;
        self.attackRange = 100;

        self.HP = 100;
        self.maxHP = 100;
    
    def update(self, deltaTime):
        if(self.HP <= 0): return;
        self.col.colRT = self.location;

        if(self.col.velocity.y == 0):
            self.AddY = 0;
        self.location.Move(self.col.velocity);

        self.col.velocity = vec2(0, 0);
        #Frame Update
        dist = get_distance(self.target.location.getcenter(), self.location.getcenter());
        if(self.state == 'idle'):
            if(dist < self.chaseRange):
                self.state = 'walk';
        elif(self.state == 'walk'):
            if(dist > self.chaseRange):
                self.state = 'idle';
            if(dist < self.attackRange):
                self.state = 'attack';
                self.FrameUpdateDelta.x = 0;
            
            if(self.target.location.getcenter().x < self.location.getcenter().x):
                self.col.velocity += vec2(-1, 0)
                self.movedir = -1
            else:
                self.col.velocity += vec2(1, 0)
                self.movedir = +1
        elif(self.state == 'attack'):
            if(self.presentFrame + 1 >= self.attackMaxFrame):
                if(dist > self.attackRange):
                    self.state = 'walk';
                    self.presentFrame = 0;
                if(self.target.location.getcenter().x < self.location.getcenter().x):
                    self.movedir = -1
                else:
                    self.movedir = +1
            
            if(self.presentFrame == 25):
                if(self.attackDelay.x > self.attackDelay.y):
                    self.AddHitbox('Monster', self.location, 0.5, 10);
                    self.attackDelay.x = 0;

        self.attackDelay.x += deltaTime;

        self.FrameUpdateDelta.x += deltaTime
        if(self.FrameUpdateDelta.x > self.FrameUpdateDelta.y):
            self.FrameUpdateDelta.x = 0
            if(self.presentFrame + 1 < self.MaxFrame):
                self.presentFrame += 1
            else:
                self.presentFrame = 0
        
        for hb in self.gm.HitboxPool:
            if((hb.isHit == False and hb.tag == 'Player') and hb.colRT.bRectTouchRect(self.location)):
                hb.isHit = True;
                self.HP -= hb.Damage;
                self.col.velocity += vec2(-50 * self.movedir, 0);
                self.AddY = -3;
                self.presentFrame = 0;
                self.state = 'idle';
                
        self.col.velocity = self.col.velocity * self.Speed * deltaTime;
        self.AddY += self.gravity;
        self.col.velocity.y -= self.AddY;
        return 0
    
    def render(self, camera):
        if(self.HP <= 0): return;
        if camera.bObjInCamera(self):
            fpos = camera.WorldPosToScreenPos(self.location.getfpos())
            lpos = camera.WorldPosToScreenPos(self.location.getlpos())
            ObjInScreenRt = rect4(fpos.x, fpos.y, lpos.x, lpos.y)
            
            spr = self.walkspr
            xoffset = 0
            yoffset = 0;
            widmul = 0;
            heimul = 0;
            if(self.state == 'walk'):
                spr = self.walkspr
                xoffset = 0;
                self.MaxFrame = self.walkMaxFrame;
                widmul = 1.5;
                heimul = 1;
                yoffset = 0;
            elif(self.state == 'idle'):
                xoffset = self.location.getwid() / 4
                spr = self.idlespr
                self.MaxFrame = self.idleMaxFrame;
                widmul = 1.5;
                heimul = 1;
                yoffset = 0;
            elif(self.state == 'attack'):
                spr = self.attackspr;
                self.MaxFrame = self.attackMaxFrame;
                widmul = 1.5;
                heimul = 1.3;
                yoffset = self.location.getwid() / 12;
            

            if(self.movedir < 0):
                Wid = spr.w / self.MaxFrame ;
                Hei = spr.h / 2
                spr.clip_draw(int((self.presentFrame) * Wid), 0, int(Wid), int(Hei), ObjInScreenRt.getcenter().x-xoffset, ObjInScreenRt.getcenter().y+yoffset, ObjInScreenRt.getwid()*widmul, ObjInScreenRt.gethei()*heimul)
            else:
                Wid = spr.w / self.MaxFrame ;
                Hei = spr.h / 2
                spr.clip_draw(spr.w - int((self.presentFrame+1) * Wid), int(Hei), int(Wid), int(Hei), ObjInScreenRt.getcenter().x+xoffset, ObjInScreenRt.getcenter().y+yoffset, ObjInScreenRt.getwid()*widmul, ObjInScreenRt.gethei()*heimul)
            #self.spr.clip_draw(Wid*self.presentFrame, 0, Wid, Hei , ObjInScreenRt.getcenter().x, ObjInScreenRt.getcenter().y, ObjInScreenRt.getwid(), ObjInScreenRt.gethei())
            #self.spr.draw(ObjInScreenRt.getcenter().x, ObjInScreenRt.getcenter().y, ObjInScreenRt.getwid(), ObjInScreenRt.gethei());

            GameObject.HPBAR_image.draw(ObjInScreenRt.getcenter().x, ObjInScreenRt.fy - 30, 100, 15);
            GameObject.HP_image.draw(ObjInScreenRt.getcenter().x - (95 - int(95*(self.HP/self.maxHP)))/2, ObjInScreenRt.fy - 30, int(95*(self.HP/self.maxHP)), 12);
        return 0
    
    def event(self, event):
        if(self.HP <= 0): return;
        return 0