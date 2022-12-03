from gameObj import *
from SpaceMath import *
from Camera import*

class Monster(GameObject):
    sprlist = None;
    soundeffectlist = None;

    def goblin_init(self):
        self.idlespr = Monster.sprlist[0];
        self.walkspr = Monster.sprlist[1];
        self.attackspr = Monster.sprlist[2];

        self.state = 'idle';
       
        self.attackDelay = vec2(0, 0.2);

        self.attackFrame = 25;
        self.attackMaxFrame = 41;
        self.walkMaxFrame = 21;
        self.idleMaxFrame = 31;
        self.presentFrame = 0;
        self.MaxFrame = 0;
        self.FrameUpdateDelta = vec2(0, 0.03)
        
        self.movedir = 1

        self.Speed = 200;
        self.gravity = 2000;
        self.AddY = 0;
        self.jumpForce = 1000;

        self.seekRange = 2000;
        self.chaseRange = 1400;
        self.attackRange = 100;

        self.widmuls = [1.5, 1.5, 1.5];
        self.heimuls = [1, 1, 1.3];
        self.yoffsets = [0, 0, 1/12];
        self.xoffsets = [1/4, 0, 0];

        self.HitType = 'h'; # h : 히트박스 | p : 투사체

        self.HP = 100;
        self.maxHP = 100;
        pass;

    def theif_init(self):
        global sprarr;
        self.idlespr = Monster.sprlist[3];
        self.walkspr = Monster.sprlist[4];
        self.attackspr = Monster.sprlist[5];

        self.state = 'idle';
       
        self.attackDelay = vec2(0, 0.2);

        self.attackFrame = 25;
        self.attackMaxFrame = 41;
        self.walkMaxFrame = 21;
        self.idleMaxFrame = 31;
        self.presentFrame = 0;
        self.MaxFrame = 0;
        self.FrameUpdateDelta = vec2(0, 0.03)
        
        self.movedir = 1

        self.Speed = 200;
        self.gravity = 2000;
        self.AddY = 0;
        self.jumpForce = 1000;

        self.seekRange = 2000;
        self.chaseRange = 1400;
        self.attackRange = 100;

        self.HP = 100;
        self.maxHP = 100;

        self.widmuls = [1, 1, 1.5];
        self.heimuls = [1, 1, 1];
        self.yoffsets = [0, 0, 0];
        self.xoffsets = [1/4, 0, 0];

        self.HitType = 'h';
        pass;

    def blackmage_init(self):
        global sprarr;
        self.idlespr = Monster.sprlist[6];
        self.walkspr = Monster.sprlist[7];
        self.attackspr = Monster.sprlist[8];

        self.state = 'idle';
       
        self.attackDelay = vec2(0, 3);

        self.attackMaxFrame = 41;
        self.walkMaxFrame = 21;
        self.idleMaxFrame = 31;
        self.presentFrame = 0;
        self.MaxFrame = 0;
        self.FrameUpdateDelta = vec2(0, 0.03)
        self.attackFrame = 25;
        
        self.movedir = 1

        self.Speed = 100;
        self.gravity = 2000;
        self.AddY = 0;
        self.jumpForce = 1000;

        self.seekRange = 2000;
        self.chaseRange = 1000;
        self.attackRange = 700;

        self.HP = 50;
        self.maxHP = 50;

        self.widmuls = [1, 1, 1.2];
        self.heimuls = [1, 1, 1.2];
        self.yoffsets = [0, 0, 1/12];
        self.xoffsets = [1/4, 0, 0];

        self.HitType = 'p';
        pass;

    def nefendus_init(self):
        self.idlespr = Monster.sprlist[9];
        self.walkspr = Monster.sprlist[9];
        self.attackspr = Monster.sprlist[10];

        self.state = 'idle';
       
        self.attackDelay = vec2(0, 0.5);

        self.attackMaxFrame = 31;
        self.walkMaxFrame = 31;
        self.idleMaxFrame = 31;
        self.presentFrame = 0;
        self.MaxFrame = 0;
        self.FrameUpdateDelta = vec2(0, 0.03)
        
        self.movedir = 1

        self.attackFrame = 25;

        self.Speed = 0;
        self.gravity = 2000;
        self.AddY = 0;
        self.jumpForce = 1000;

        self.seekRange = 2000;
        self.chaseRange = 2000;
        self.attackRange = 250;

        self.HP = 200;
        self.maxHP = 200;

        self.widmuls = [1, 1, 1.2];
        self.heimuls = [1, 1, 1];
        self.yoffsets = [0, 0, 0];
        self.xoffsets = [0, 0, 0];

        self.HitType = 'h';
        pass;

    def noul_init(self):
        self.idlespr = Monster.sprlist[11];
        self.walkspr = Monster.sprlist[12];
        self.attackspr = Monster.sprlist[13];

        self.state = 'idle';
       
        self.attackDelay = vec2(0, 0.2);

        self.attackMaxFrame = 26;
        self.walkMaxFrame = 21;
        self.idleMaxFrame = 21;
        self.presentFrame = 0;
        self.MaxFrame = 0;
        self.FrameUpdateDelta = vec2(0, 0.03)
        
        self.attackFrame = 17;

        self.movedir = 1

        self.Speed = 200;
        self.gravity = 2000;
        self.AddY = 0;
        self.jumpForce = 1000;

        self.seekRange = 2000;
        self.chaseRange = 1400;
        self.attackRange = 100;

        self.widmuls = [1.5, 2, 1.5];
        self.heimuls = [1, 1, 1.3];
        self.yoffsets = [0, 0, 1/12];
        self.xoffsets = [1/4, 0, 0];

        self.HitType = 'h'; # h : 히트박스 | p : 투사체

        self.HP = 400;
        self.maxHP = 400;
        pass;

    def __init__(self, location, layer, MonsterType, gm, target):
        global playerobj, sprarr;
        self.ismove = False;

        if(Monster.soundeffectlist == None):
            Monster.soundeffectlist = [];
            Monster.soundeffectlist.append(load_wav('Resorceses/Sound/enemy_dead.wav'));

        if(Monster.sprlist == None):
            Monster.sprlist = [];
            Monster.sprlist.append(load_image('Resorceses/SpriteSheet/Goblin/goblin_idle.png')) #0
            Monster.sprlist.append(load_image('Resorceses/SpriteSheet/Goblin/goblin_walk.png')) #1
            Monster.sprlist.append(load_image('Resorceses/SpriteSheet/Goblin/goblin_attack.png')) #2
            Monster.sprlist.append(load_image('Resorceses/SpriteSheet/Theif/thief_idle.png')) #3
            Monster.sprlist.append(load_image('Resorceses/SpriteSheet/Theif/theif_walk.png')) #4
            Monster.sprlist.append(load_image('Resorceses/SpriteSheet/Theif/theif_attack.png')) #5
            Monster.sprlist.append(load_image('Resorceses/SpriteSheet/BlackMage/blackmage_idle.png')) #6
            Monster.sprlist.append(load_image('Resorceses/SpriteSheet/BlackMage/blackmage_walk.png')) #7
            Monster.sprlist.append(load_image('Resorceses/SpriteSheet/BlackMage/blackmage_attack.png')) #8
            Monster.sprlist.append(load_image('Resorceses/SpriteSheet/Nefendus/nefendus_idle.png')) #9
            Monster.sprlist.append(load_image('Resorceses/SpriteSheet/Nefendus/nefendus_attack.png')) #10
            Monster.sprlist.append(load_image('Resorceses/SpriteSheet/Noul/noul_idle.png')) #11
            Monster.sprlist.append(load_image('Resorceses/SpriteSheet/Noul/noul_walk.png')) #12
            Monster.sprlist.append(load_image('Resorceses/SpriteSheet/Noul/noul_attack.png')) #13
            Monster.sprlist.append(load_image('Resorceses/Particles/icee.png')) #14

        super().__init__(location, layer, sprarr[0], gm);
        self.target = target;

        if(MonsterType == 'goblin'):
            self.LeftFirst = False;
            self.goblin_init();
        if(MonsterType == 'thief'):
            self.LeftFirst = True;
            self.theif_init();
        if(MonsterType == 'blackmage'):
            self.LeftFirst = True;
            self.blackmage_init();
        if(MonsterType == 'nefendus'):
            self.LeftFirst = True;
            self.nefendus_init();
        if(MonsterType == 'noul'):
            self.LeftFirst = True;
            self.noul_init();
        
        self.dead = False;

        self.passiveFlow = vec2(0, 0.3);
        self.passive_onFire = 0;
        self.passive_onIce = 0;

        self.pastx = self.location.getcenter().x;
        pass;

    def update(self, deltaTime):
        if(self.dead): return;
        self.col.colRT = self.location;

        if(self.col.velocity.y == 0):
            self.AddY = 0;
        
        
        bejump = False;
        if(self.col.velocity.x == 0 and self.state == 'walk' and self.passive_onIce == False and self.ismove):
            bejump = True;
        self.ismove = False;

        self.location.Move(self.col.velocity);

        self.col.velocity = vec2(0, 0);

        if(self.target.location.getcenter().x < self.location.getcenter().x):
            self.movedir = -1
        else:
            self.movedir = +1

        self.passiveFlow.x += deltaTime;
        if(self.passiveFlow.x > self.passiveFlow.y):
            self.passiveFlow.x = 0;
            if(self.passive_onFire > 0):
                self.passive_onFire -= 1;
                self.onFire();
            
            if(self.passive_onIce > 0):
                self.passive_onIce -= 1;
                

        
        #Frame Update
        dist = get_distance(self.target.location.getcenter(), self.location.getcenter());
        if(self.state == 'idle'):
            if(dist < self.chaseRange):
                self.state = 'walk';
                self.ismove = False;
        elif(self.state == 'walk'):
            if(dist > self.chaseRange):
                self.state = 'idle';
            if(dist < self.attackRange):
                self.state = 'attack';
                self.FrameUpdateDelta.x = 0;
                self.presentFrame = 0
            
            if(self.target.location.getcenter().x < self.location.getcenter().x):
                self.col.velocity += vec2(-1, 0)
                self.movedir = -1
            else:
                self.col.velocity += vec2(1, 0)
                self.movedir = +1
            
            if(bejump):
                self.AddY = -self.jumpForce;
        elif(self.state == 'attack'):
            if(self.presentFrame + 1 >= self.attackMaxFrame):
                if(dist > self.attackRange):
                    self.state = 'walk';
                    self.ismove = False;
                    self.presentFrame = 0;
                if(self.target.location.getcenter().x < self.location.getcenter().x):
                    self.movedir = -1
                else:
                    self.movedir = +1
            
            if(self.presentFrame == self.attackFrame):
                if(self.HitType == 'h'):
                    if(self.attackDelay.x > self.attackDelay.y):
                        self.AddHitbox('Monster', self.location, 0.1, 10);
                        self.attackDelay.x = 0;
                elif(self.HitType == 'p'):
                    if(self.attackDelay.x > self.attackDelay.y):
                        dir = self.target.location.getcenter() - self.location.getcenter();
                        dir = normalized(dir) * 400;
                        self.gm.AddProjectile(self.location.getcenter(), dir, 'Monster', 10);
                        self.attackDelay.x = 0;

        self.attackDelay.x += deltaTime;

        self.FrameUpdateDelta.x += deltaTime
        if(self.FrameUpdateDelta.x > self.FrameUpdateDelta.y):
            self.FrameUpdateDelta.x = self.FrameUpdateDelta.x - self.FrameUpdateDelta.y;
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
                self.ifDead();
        
        for pj in self.gm.ProjectilePool:
            if((pj.hitbox.isHit == False and pj.hitbox.tag == 'Player') and pj.hitbox.colRT.bRectTouchRect(self.location)):
                pj.hitbox.isHit = True;
                self.HP -= pj.hitbox.Damage;
                self.col.velocity += vec2(-50 * self.movedir, 0);
                self.AddY = -3;
                self.presentFrame = 0;
                self.state = 'idle';
                self.ifDead();
            
            if((pj.hitbox.isHit == False and pj.hitbox.tag == 'Player_Fire') and pj.hitbox.colRT.bRectTouchRect(self.location)):
                pj.hitbox.isHit = True;
                self.HP -= pj.hitbox.Damage;
                self.col.velocity += vec2(-50 * self.movedir, 0);
                self.AddY = -3;
                self.presentFrame = 0;
                self.state = 'idle';
                self.passive_onFire = 10;
                self.ifDead();
            
            if((pj.hitbox.isHit == False and pj.hitbox.tag == 'Player_Ice') and pj.hitbox.colRT.bRectTouchRect(self.location)):
                pj.hitbox.isHit = True;
                self.HP -= pj.hitbox.Damage;
                self.col.velocity += vec2(-50 * self.movedir, 0);
                self.AddY = -3;
                self.presentFrame = 0;
                self.state = 'idle';
                self.passive_onIce = 10;
                self.ifDead();
                
        if(self.passive_onIce > 0):
            self.col.velocity.x = 0;
        
        self.col.velocity = self.col.velocity * self.Speed * deltaTime;
        self.AddY += self.gravity * deltaTime;
        self.col.velocity.y -= self.AddY * deltaTime;
        if(self.col.velocity.x != 0):
            self.pastx = self.location.getcenter().x;
            self.ismove = True;
        return 0
    
    def render(self, camera):
        if(self.dead): return;
        if camera.bObjInCamera(self):
            fpos = camera.WorldPosToScreenPos(self.location.getfpos())
            lpos = camera.WorldPosToScreenPos(self.location.getlpos())
            ObjInScreenRt = rect4(fpos.x, fpos.y, lpos.x, lpos.y)
            
            spr = self.walkspr
            xoffset = 0
            yoffset = 0;
            widmul = 0;
            heimul = 0;
            numst = 0;
            if(self.state == 'idle'):
                spr = self.idlespr
                self.MaxFrame = self.idleMaxFrame;
                numst = 0;
            elif(self.state == 'walk'):
                spr = self.walkspr
                self.MaxFrame = self.walkMaxFrame;
                numst = 1;
            elif(self.state == 'attack'):
                spr = self.attackspr;
                self.MaxFrame = self.attackMaxFrame;
                numst = 2;
            
            xoffset = self.location.getwid() * self.xoffsets[numst];
            yoffset = self.location.getwid() * self.yoffsets[numst];
            widmul = self.widmuls[numst];
            heimul = self.heimuls[numst];

            if(self.movedir < 0):
                Wid = spr.w / self.MaxFrame ;
                Hei = spr.h / 2
                if(self.LeftFirst == False):
                    spr.clip_draw(int((self.presentFrame) * Wid), 0, int(Wid), int(Hei), ObjInScreenRt.getcenter().x-xoffset, ObjInScreenRt.getcenter().y+yoffset, ObjInScreenRt.getwid()*widmul, ObjInScreenRt.gethei()*heimul)
                else:
                    spr.clip_draw(int((self.presentFrame) * Wid), int(Hei), int(Wid), int(Hei), ObjInScreenRt.getcenter().x+xoffset, ObjInScreenRt.getcenter().y+yoffset, ObjInScreenRt.getwid()*widmul, ObjInScreenRt.gethei()*heimul)
            else:
                Wid = spr.w / self.MaxFrame ;
                Hei = spr.h / 2
                if(self.LeftFirst == False):
                    spr.clip_draw(spr.w - int((self.presentFrame+1) * Wid), int(Hei), int(Wid), int(Hei), ObjInScreenRt.getcenter().x+xoffset, ObjInScreenRt.getcenter().y+yoffset, ObjInScreenRt.getwid()*widmul, ObjInScreenRt.gethei()*heimul)
                else:
                    spr.clip_draw(spr.w - int((self.presentFrame+1) * Wid), 0, int(Wid), int(Hei), ObjInScreenRt.getcenter().x-xoffset, ObjInScreenRt.getcenter().y+yoffset, ObjInScreenRt.getwid()*widmul, ObjInScreenRt.gethei()*heimul)
                
            #self.spr.clip_draw(Wid*self.presentFrame, 0, Wid, Hei , ObjInScreenRt.getcenter().x, ObjInScreenRt.getcenter().y, ObjInScreenRt.getwid(), ObjInScreenRt.gethei())
            #self.spr.draw(ObjInScreenRt.getcenter().x, ObjInScreenRt.getcenter().y, ObjInScreenRt.getwid(), ObjInScreenRt.gethei());

            if(self.passive_onIce > 0):
                Monster.sprlist[14].draw(int(ObjInScreenRt.getcenter().x), int(ObjInScreenRt.getcenter().y), int(ObjInScreenRt.getwid()), int(ObjInScreenRt.gethei()));
            
            GameObject.HPBAR_image.draw(ObjInScreenRt.getcenter().x, ObjInScreenRt.fy - 30, 100, 15);
            GameObject.HP_image.draw(ObjInScreenRt.getcenter().x - (95 - int(95*(self.HP/self.maxHP)))/2, ObjInScreenRt.fy - 30, int(95*(self.HP/self.maxHP)), 12);
        return 0
    
    def event(self, event):
        if(self.dead): return;
        return 0
    
    def ifDead(self):
        if self.HP <= 0:
            Monster.soundeffectlist[0].play();
            self.gm.AddRootItem(self.location.getcenter() - vec2(-100, 50), 'gold', self.target);
            self.gm.AddRootItem(self.location.getcenter() - vec2(-50, 50), 'gold', self.target);
            self.gm.AddRootItem(self.location.getcenter() - vec2(50, 50), 'gold', self.target);
            self.gm.AddRootItem(self.location.getcenter() - vec2(100, 50), 'health_potion', self.target);
            self.dead = True;
            self.enable = False;
        pass;
    
    def onFire(self):
        self.HP -= 5;
        self.gm.AddPart(self.location.getcenter(), vec2(0, 100), 20, 1000, 1, Projectile.sprlist[random.randint(1, 5)]);
        self.ifDead();
        pass;