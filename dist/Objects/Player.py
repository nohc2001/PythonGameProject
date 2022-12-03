from gameObj import *
from SpaceMath import *
from Camera import*
import random

class Player(GameObject):
    itemSlot = [0, 0];

    itemsprlist = None;
    playersprlist = None;
    soundEffectlist = None;
    portalLocation = None;
    mapchange = False;

    def __init__(self, location, layer, idlespr, gm):
        if(Player.itemsprlist == None):
            Player.itemsprlist = [];
            Player.itemsprlist.append(load_image('Resorceses/ItemIcon/gold.png'));
            Player.itemsprlist.append(load_image('Resorceses/ItemIcon/HealthPotion.png'));
            Player.itemsprlist.append(load_image('Resorceses/Particles/p_fire01.png'));
            Player.itemsprlist.append(load_image('Resorceses/Particles/ice0.png'));
        
        if(Player.playersprlist == None):
            Player.playersprlist = [];
            Player.playersprlist.append(load_image('Resorceses/char_walk.png')) #0
            Player.playersprlist.append(load_image('Resorceses/char_idle.png')) #1
            Player.playersprlist.append(load_image('Resorceses/SpriteSheet/Player/player_attack.png')) #2
            Player.playersprlist.append(load_image('Resorceses/SpriteSheet/Player/player_attack2.png')) #3
        
        if(Player.soundEffectlist == None):
            Player.soundEffectlist = [];
            Player.soundEffectlist.append(load_wav('Resorceses/Sound/sword0.wav')); #0
            Player.soundEffectlist.append(load_wav('Resorceses/Sound/sword1.wav')); #1
            Player.soundEffectlist.append(load_wav('Resorceses/Sound/sword2.wav')); #2
            Player.soundEffectlist.append(load_wav('Resorceses/Sound/item.wav')); #3
            Player.soundEffectlist.append(load_wav('Resorceses/Sound/enemy_dead.wav')); #4

        super().__init__(location, layer, idlespr, gm);
        self.walkspr = Player.playersprlist[0]
        self.idlespr = Player.playersprlist[1]
        self.attackspr = Player.playersprlist[2];
        self.attack2spr = Player.playersprlist[3];
        self.AKeyDown = False
        self.SKeyDown = False
        self.DKeyDown = False
        self.WKeyDown = False

        self.state = 'idle';
        self.attackMaxFrame = 25;
        self.attack0_delay = vec2(0, 2);
        self.attack2MaxFrame = 29;
        self.walkMaxFrame = 25;
        self.idleMaxFrame = 21;
        self.presentFrame = 0
        self.FrameUpdateDelta = vec2(0, 0.03)
        self.maxFrame = 0;
        self.movedir = 1

        self.Speed = 500;
        self.gravity = 2000;
        self.AddY = 0;
        self.jumpForce = 1000;

        self.HP = 100;
        self.maxHP = 100;

        #self.itemSlot = [0, 0]; # itemid 별로 [gold, health_potion ...]
        self.skillDelay = [vec2(0, 3), vec2(0, 3)];
        self.attackDelay = vec2(0, 0.2);
    
    def update(self, deltaTime):
        global editdata;
        if(self.HP <= 0): return;
        self.col.colRT = self.location;
        if(self.col.velocity.y == 0):
            self.AddY = 0;
        self.location.Move(self.col.velocity);

        self.attack0_delay.x += deltaTime;
        
        if(self.state == 'attack'):
            if(self.presentFrame + 1 >= self.attackMaxFrame):
                self.state = 'idle';
                if(self.AKeyDown or self.DKeyDown):
                    self.state = 'walk';
            
            if(self.presentFrame == 15):
                if(self.attackDelay.x > self.attackDelay.y):
                    self.AddHitbox('Player', self.location, 0.5, 10);
                    self.attackDelay.x = 0;
                    Player.soundEffectlist[random.randint(0, 2)].play();
        if(self.state == 'attack2'):
            if(self.presentFrame + 1 >= self.attack2MaxFrame):
                self.state = 'idle';
            
            if(self.presentFrame == 20):
                if(self.attackDelay.x > self.attackDelay.y):
                    self.AddHitbox('Player', self.location, 0.5, 10);
                    self.attackDelay.x = 0;
                    Player.soundEffectlist[random.randint(0, 2)].play();

        self.attackDelay.x += deltaTime;

        self.FrameUpdateDelta.x += deltaTime
        if(self.FrameUpdateDelta.x > self.FrameUpdateDelta.y):
            self.FrameUpdateDelta.x = self.FrameUpdateDelta.x - self.FrameUpdateDelta.y;
            if(self.presentFrame + 1 < self.maxFrame):
                self.presentFrame += 1
            else:
                self.presentFrame = 0
        
        self.skillDelay[0].x += deltaTime;
        self.skillDelay[1].x += deltaTime;
        
        global MainCamera
        self.col.velocity = vec2(0, 0)
        if(self.state == 'walk'):
            if self.AKeyDown:
                self.col.velocity += vec2(-1, 0)
                self.movedir = -1
            if self.DKeyDown:
                self.col.velocity += vec2(1, 0)
                self.movedir = 1
        
        if self.WKeyDown and self.state != 'attack':
            if(self.AddY == 0):
                self.AddY = -self.jumpForce;
            
        
        for hb in self.gm.HitboxPool:
            if((hb.isHit == False and hb.tag == 'Monster') and hb.colRT.bRectTouchRect(self.location)):
                hb.isHit = True;
                self.HP -= hb.Damage;
                self.col.velocity += vec2(-5 * self.movedir, 0);
                self.AddY = -3;
        
        for pj in self.gm.ProjectilePool:
            if((pj.hitbox.isHit == False and pj.hitbox.tag == 'Monster') and pj.hitbox.colRT.bRectTouchRect(self.location)):
                pj.hitbox.isHit = True;
                self.HP -= pj.hitbox.Damage;
                self.col.velocity += vec2(-5*self.movedir, 0);
                self.AddY = -3;

        self.col.velocity = self.col.velocity * self.Speed * deltaTime
        self.AddY += self.gravity * deltaTime;
        self.col.velocity.y -= self.AddY * deltaTime;
        
        camcenter = self.location.getcenter() + self.col.velocity;
        MainCamera.MoveTo(camcenter, vec2(1600, 1200))


        if(Player.portalLocation.bRectTouchRect(self.location)):
            Player.mapchange = True;
        pass;
    
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
                xoffset = self.location.getwid() / 4
                spr = self.attackspr
                self.maxFrame = self.attackMaxFrame;
                widmul = 1.5;
                heimul = 1.3;
                yoffset = self.location.getwid() / 12;
            elif(self.state == 'attack2'):
                spr = self.attack2spr
                self.maxFrame = self.attack2MaxFrame;
                widmul = 1.8;
                heimul = 1.4;
                yoffset = self.location.getwid() / 6;

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

        Player.itemsprlist[0].draw(100, 50, 50, 50);
        fontObj[0].draw(150, 50, str(Player.itemSlot[0]), [255, 255, 255]);

        Player.itemsprlist[1].draw(100, 100, 50, 50);
        fontObj[1].draw(150, 100, str(Player.itemSlot[1]), [255, 255, 255]);
        fontObj[1].draw(50, 100, '1', [255, 255, 255]);

        Player.itemsprlist[2].draw(300, 100, 50, 50);
        fontObj[1].draw(350, 100, str(int(3 - self.skillDelay[0].x)), [255, 255, 255]);
        fontObj[1].draw(250, 100, 'Q', [255, 255, 255]);

        Player.itemsprlist[3].draw(500, 100, 50, 50);
        fontObj[1].draw(550, 100, str(int(3 - self.skillDelay[1].x)), [255, 255, 255]);
        fontObj[1].draw(450, 100, 'E', [255, 255, 255]);
        return 0
    
    def event(self, event):
        if(self.HP <= 0): return;
        if(event.type == SDL_MOUSEBUTTONDOWN):
            if(self.state != 'attack'):
                if(self.attack0_delay.y < self.attack0_delay.x):
                    self.state = 'attack';
                    self.presentFrame = 0;
                    self.attack0_delay.x = 0;
                elif(self.state != 'attack2'):
                    self.state = 'attack2';
                    self.presentFrame = 0;
        if(event.type == SDL_KEYDOWN):
            if event.key == SDLK_q:
                self.Skill_FireBall();
            if event.key == SDLK_e:
                self.Skill_IceSpear();
            if(self.state != 'attack' or self.state != 'attack2'):
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
            if(event.key == SDLK_1):
                self.UseItem(1);
        if(event.type == SDL_KEYUP):
            if(self.state != 'attack' or self.state != 'attack2'):
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
    
    def AddItem(self, itemid):
        Player.soundEffectlist[3].play();
        Player.itemSlot[itemid] += 1;
        pass;

    def UseItem(self, itemid):
        if(Player.itemSlot[itemid] - 1 >= 0):
            Player.itemSlot[itemid] -= 1;
        else:
            return;
        
        if(itemid == 1):
            if(self.HP + 50 <= self.maxHP):
                self.HP += 50;
            else:
                self.HP = self.maxHP;
        pass;
    
    def Skill_FireBall(self):
        if(self.skillDelay[0].x > self.skillDelay[0].y):
            self.skillDelay[0].x = 0;
            self.gm.AddProjectile(self.location.getcenter(), vec2(self.movedir*1000, 0), 'Player_Fire', 30);
            self.attackDelay.x = 0;
        pass;
    
    def Skill_IceSpear(self):
        if(self.skillDelay[1].x > self.skillDelay[1].y):
            self.skillDelay[1].x = 0;
            self.gm.AddProjectile(self.location.getcenter(), vec2(self.movedir*1000, 0), 'Player_Ice', 30);
            self.attackDelay.x = 0;
        pass;
    
    