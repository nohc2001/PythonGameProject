from gameObj import *
from SpaceMath import *
from Camera import*

class Player(GameObject):
    def __init__(self, location, layer, walkspr, idlespr, attackspr, gm):
        super().__init__(location, layer, idlespr, gm);
        self.walkspr = walkspr
        self.idlespr = idlespr
        self.attackspr = attackspr;
        self.AKeyDown = False
        self.SKeyDown = False
        self.DKeyDown = False
        self.WKeyDown = False

        self.state = 'idle';
        self.attackMaxFrame = 25;
        self.walkMaxFrame = 25;
        self.idleMaxFrame = 21;
        self.presentFrame = 0
        self.FrameUpdateDelta = vec2(0, 0.03)
        self.maxFrame = 0;
        self.movedir = 1

        self.Speed = 300;
        self.gravity = 0.1;
        self.AddY = 0;
        self.jumpForce = 5;

        self.HP = 100;
        self.maxHP = 100;

        self.attackDelay = vec2(0, 0.2);
    
    def update(self, deltaTime):
        if(self.HP <= 0): return;
        self.col.colRT = self.location;
        if(self.col.velocity.y == 0):
            self.AddY = 0;
        self.location.Move(self.col.velocity);

        if(self.state == 'attack'):
            if(self.presentFrame + 1 >= self.attackMaxFrame):
                self.state = 'idle';
            
            if(self.presentFrame == 15):
                if(self.attackDelay.x > self.attackDelay.y):
                    self.AddHitbox('Player', self.location, 0.5, 10);
                    self.attackDelay.x = 0;

        self.attackDelay.x += deltaTime;

        self.FrameUpdateDelta.x += deltaTime
        if(self.FrameUpdateDelta.x > self.FrameUpdateDelta.y):
            self.FrameUpdateDelta.x = 0
            if(self.presentFrame + 1 < self.maxFrame):
                self.presentFrame += 1
            else:
                self.presentFrame = 0
        
        global MainCamera
        self.col.velocity = vec2(0, 0)
        if self.AKeyDown:
            self.col.velocity += vec2(-1, 0)
            self.movedir = -1
        if self.DKeyDown:
            self.col.velocity += vec2(1, 0)
            self.movedir = 1
        if self.WKeyDown:
            if(self.AddY == 0):
                self.AddY = -self.jumpForce;
        
        for hb in self.gm.HitboxPool:
            if((hb.isHit == False and hb.tag == 'Monster') and hb.colRT.bRectTouchRect(self.location)):
                hb.isHit = True;
                self.HP -= hb.Damage;
                self.col.velocity += vec2(-50 * self.movedir, 0);
                self.AddY = -3;

        self.col.velocity = self.col.velocity * self.Speed * deltaTime
        self.AddY += self.gravity;
        self.col.velocity.y -= self.AddY;
        
        camcenter = self.location.getcenter() + self.col.velocity;
        MainCamera.MoveTo(camcenter, vec2(1600, 1200))

        return 0
    
    def render(self, camera):
        if(self.HP <= 0): return;

        if camera.bObjInCamera(self):
            fpos = camera.WorldPosToScreenPos(self.location.getfpos())
            lpos = camera.WorldPosToScreenPos(self.location.getlpos())
            ObjInScreenRt = rect4(fpos.x, fpos.y, lpos.x, lpos.y)

            spr = self.walkspr
            xoffset = 0
            widmul = 1;
            heimul = 1;
            yoffset =0;
            if(self.state == 'walk'):
                spr = self.walkspr
                self.maxFrame = self.walkMaxFrame;
            elif(self.state == 'idle'):
                xoffset = self.location.getwid() / 4
                spr = self.idlespr
                self.maxFrame = self.idleMaxFrame;
            elif(self.state == 'attack'):
                spr = self.attackspr
                self.maxFrame = self.attackMaxFrame;
                widmul = 1.5;
                heimul = 1.3;
                yoffset = self.location.getwid() / 12;

            if(self.movedir < 0):
                Wid = spr.w / self.maxFrame
                Hei = spr.h / 2
                spr.clip_draw(spr.w - int((self.presentFrame+1) * Wid), 0, int(Wid), int(Hei), ObjInScreenRt.getcenter().x-xoffset, ObjInScreenRt.getcenter().y+yoffset, ObjInScreenRt.getwid()*widmul, ObjInScreenRt.gethei()*heimul)
            else:
                Wid = spr.w / self.maxFrame
                Hei = spr.h / 2
                spr.clip_draw(int((self.presentFrame) * Wid), int(Hei), int(Wid), int(Hei), ObjInScreenRt.getcenter().x+xoffset, ObjInScreenRt.getcenter().y+yoffset, ObjInScreenRt.getwid()*widmul, ObjInScreenRt.gethei()*heimul)
            #self.spr.clip_draw(Wid*self.presentFrame, 0, Wid, Hei , ObjInScreenRt.getcenter().x, ObjInScreenRt.getcenter().y, ObjInScreenRt.getwid(), ObjInScreenRt.gethei())
            #self.spr.draw(ObjInScreenRt.getcenter().x, ObjInScreenRt.getcenter().y, ObjInScreenRt.getwid(), ObjInScreenRt.gethei());
            GameObject.HPBAR_image.draw(ObjInScreenRt.getcenter().x + 20*self.movedir, ObjInScreenRt.fy - 30, 100, 15);
            GameObject.HP_image.draw(ObjInScreenRt.getcenter().x - (95 - int(95*(self.HP/self.maxHP)))/2  + 20*self.movedir, ObjInScreenRt.fy - 30, int(95*(self.HP/self.maxHP)), 12);
        return 0
    
    def event(self, event):
        if(self.HP <= 0): return;
        if(event.type == SDL_MOUSEBUTTONDOWN):
            if(self.state != 'attack'):
                self.state = 'attack';
                self.presentFrame = 0;
        if(event.type == SDL_KEYDOWN):
            if event.key == SDLK_a:
                self.state = 'walk'
                self.AKeyDown = True
            if event.key == SDLK_s:
                self.SKeyDown = True
            if event.key == SDLK_d:
                self.state = 'walk'
                self.DKeyDown = True
            if event.key == SDLK_w:
                self.WKeyDown = True
        if(event.type == SDL_KEYUP):
            if event.key == SDLK_a:
                self.state = 'idle'
                self.AKeyDown = False
            if event.key == SDLK_s:
                self.SKeyDown = False
            if event.key == SDLK_d:
                self.state = 'idle'
                self.DKeyDown = False
            if event.key == SDLK_w:
                self.WKeyDown = False
        return 0