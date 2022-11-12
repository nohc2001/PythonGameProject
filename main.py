import os
from pico2d import *
from Objects.Particles import *
from gameObj import *
from Objects.Player import *
from Objects.MaskyLight import*
from Objects.Monster import*

os.chdir('C:\\Users\\nohc2\\Dev\\PythonGame\\PythonGameProject')
pico2d.open_canvas(WMAX, HMAX)
sys.path.append(r'C:\\Users\\nohc2\\Dev\\PythonGame\\PythonGameProject')

global isRunning
isRunning = True

def EventExecute(event):
    global isRunning
    if event.type == SDL_QUIT:
        close_canvas()
        isRunning = False
        return 0
    
    return 1

global addx
addx = 0
global game_manager
game_manager = GameManager()
global saveClock
global presentClock
saveClock = 0
presentClock = 0
global bgm;
bgm = 0;
LevelEditMode = True;
LevelEdit_PlayMode = False;
moveflow = vec2(0, 1);
rkey, lkey, ukey, dkey = False, False, False, False;
ctrlkey = False;

editSelectIndex = 0;
isSelected = False;

class GameColideData:
    image = pico2d.load_image("Resorceses/GCD.png");
    gradiant = pico2d.load_image("Resorceses/Tile/blocked.png");
    selectedImage = pico2d.load_image("Resorceses/GCDSelected.png");
    tileImages = [];
    tileImages.append(pico2d.load_image("Resorceses/Tile/Tile0.png"));
    tileImages.append(pico2d.load_image("Resorceses/Tile/WoodFloor.png"));
    tileSiz = 100;
    def __init__(self, rt):
        self.RT = rt;
        self.TileImageIndex = -1;
        self.isSelected = False;
        pass;
    
    def sort(self):
        if(self.RT.fx > self.RT.lx):
            self.RT.fx, self.RT.lx = self.RT.lx, self.RT.fx;
        if(self.RT.fy > self.RT.ly):
            self.RT.fy, self.RT.ly = self.RT.ly, self.RT.fy;
        pass
    
    def render(self, camera):
        ts = 100;
        fpos = camera.WorldPosToScreenPos(vec2(min([self.RT.fx, self.RT.lx]), min([self.RT.fy, self.RT.ly])));
        lpos = camera.WorldPosToScreenPos(vec2(max([self.RT.fx, self.RT.lx]), max([self.RT.fy, self.RT.ly])))
        ObjInScreenRt = rect4(fpos.x, fpos.y, lpos.x, lpos.y)
        
        if(self.TileImageIndex < 0):
            if(self.isSelected):
                GameColideData.selectedImage.draw(int(ObjInScreenRt.getcenter().x), int(ObjInScreenRt.getcenter().y), int(ObjInScreenRt.getwid()), int(ObjInScreenRt.gethei()));
            else:
                GameColideData.image.draw(int(ObjInScreenRt.getcenter().x), int(ObjInScreenRt.getcenter().y), int(ObjInScreenRt.getwid()), int(ObjInScreenRt.gethei()));
        else:
            TileImage = GameColideData.tileImages[self.TileImageIndex];

            GameColideData.image.draw(int(ObjInScreenRt.getcenter().x), int(ObjInScreenRt.getcenter().y), int(ObjInScreenRt.getwid()), int(ObjInScreenRt.gethei()));
            yindex = 0;
            while(yindex < ObjInScreenRt.gethei()//ts):
                xindex = 0;
                while(xindex < ObjInScreenRt.getwid()//ts):
                    TileImage.draw(int(ObjInScreenRt.fx + ts/2 + xindex*ts)-1, int(ObjInScreenRt.fy + ts/2 + yindex*ts)-1, ts+2, ts+2);
                    xindex += 1;
                yindex += 1;
            
            #remainRender
            ywid = ObjInScreenRt.gethei() - (ObjInScreenRt.gethei()//ts) * ts;
            xindex = 0;
            while(xindex < ObjInScreenRt.getwid()//ts):
                TileImage.clip_draw(0, 0, 100, int(ywid), int(ObjInScreenRt.fx + ts/2 + xindex*ts)-1, int(ObjInScreenRt.fy + (ObjInScreenRt.gethei()//ts) * ts + ywid/2)-1, ts+2, ywid+2);
                xindex += 1;
            
            xwid = ObjInScreenRt.getwid() - (ObjInScreenRt.getwid()//ts) * ts;
            yindex = 0;
            while(yindex < ObjInScreenRt.gethei()//ts):
                TileImage.clip_draw(0, 0, int(xwid), 100, int(ObjInScreenRt.fx + (ObjInScreenRt.getwid()//ts) * ts + xwid/2)-1, int(ObjInScreenRt.fy + ts/2 + yindex*ts)-1, xwid+2, ts+2);
                yindex += 1;
            
            TileImage.clip_draw(0, 0, int(xwid), int(ywid), int(ObjInScreenRt.fx + (ObjInScreenRt.getwid()//ts) * ts + xwid/2)-1, int(ObjInScreenRt.fy + (ObjInScreenRt.gethei()//ts) * ts + ywid/2)-1, xwid+2, ywid+2);
        
        GameColideData.gradiant.draw(int(ObjInScreenRt.getcenter().x), int(ObjInScreenRt.getcenter().y), int(ObjInScreenRt.getwid())+4, int(ObjInScreenRt.gethei()+4));
        pass;

class GameObjectData:
    images = [];
    images.append(pico2d.load_image("Resorceses/Object/Grass0.png"));
    images.append(pico2d.load_image("Resorceses/Object/Grass1.png"));
    images.append(pico2d.load_image("Resorceses/Object/Grass2.png"));
    images.append(pico2d.load_image("Resorceses/Object/Grass3.png"));
    images.append(pico2d.load_image("Resorceses/Object/Grass4.png"));
    images.append(pico2d.load_image("Resorceses/Object/Tree0.png"));
    images.append(pico2d.load_image("Resorceses/Object/Tree1.png"));
    images.append(pico2d.load_image("Resorceses/Object/Tree2.png"));
    images.append(pico2d.load_image("Resorceses/Object/Tree3.png"));
    images.append(pico2d.load_image("Resorceses/Object/Tree4.png"));
    images.append(pico2d.load_image("Resorceses/Object/Weeds0.png"));
    images.append(pico2d.load_image("Resorceses/Object/Weeds1.png"));
    images.append(pico2d.load_image("Resorceses/Object/Weeds2.png"));
    images.append(pico2d.load_image("Resorceses/Object/Weeds3.png"));
    images.append(pico2d.load_image("Resorceses/Object/Weeds4.png"));

    def __init__(self, rt, sindex, layer) -> None:
        self.sprindex = sindex;
        self.RT = rt;
        self.Layer = layer;
        self.isSelected = False;
        pass

    def sort(self):
        if(self.RT.fx > self.RT.lx):
            self.RT.fx, self.RT.lx = self.RT.lx, self.RT.fx;
        if(self.RT.fy > self.RT.ly):
            self.RT.fy, self.RT.ly = self.RT.ly, self.RT.fy;
        pass

    def render(self, camera):
        self.RT = rect4(self.RT.fx, self.RT.fy, self.RT.fx + 1.5*GameObjectData.images[self.sprindex].w, self.RT.fy + 1.5*GameObjectData.images[self.sprindex].h);
        fpos = camera.WorldPosToScreenPos(vec2(min([self.RT.fx, self.RT.lx]), min([self.RT.fy, self.RT.ly])));
        lpos = camera.WorldPosToScreenPos(vec2(max([self.RT.fx, self.RT.lx]), max([self.RT.fy, self.RT.ly])))
        ObjInScreenRt = rect4(fpos.x, fpos.y, lpos.x, lpos.y)
        GameObjectData.images[self.sprindex].draw(int(ObjInScreenRt.getcenter().x), int(ObjInScreenRt.getcenter().y), int(ObjInScreenRt.getwid()), int(ObjInScreenRt.gethei()));
        pass;

def copy_GCD(GCD):
    gcd = GameColideData(GCD.RT);
    gcd.TileImageIndex = GCD.TileImageIndex;
    return gcd;

def copy_GOD(GOD):
    god = GameObjectData(GOD.RT, GOD.sprindex, GOD.Layer);
    return god;

class EditData:
    
    AddMode = 'ready';
    AddingGCD = GameColideData(rect4(0, 0, 0, 0));
    AddingGOD = GameObjectData(rect4(0, 0, 0, 0), 0, 0);
    addobjiscol = False;
    addTargetLayer = 0;
    def __init__(self) -> None:
        self.GCDArr = [];
        self.GODArr = [];
        pass

    def AddColObj(self, gcd):
        self.GCDArr.append(gcd);
        pass;
    
    def AddObj(self, god):
        self.GODArr.sort(key = lambda c : c.Layer);
        self.GODArr.append(god);
        pass;
    
    def Render(self, camera):
        index = 0;
        EditData.AddingGCD.render(camera);
        while(index < len(self.GCDArr)):
            self.GCDArr[index].render(camera);
            index += 1;
        
        index = 0;
        EditData.AddingGOD.render(camera);
        while(index < len(self.GODArr)):
            self.GODArr[index].render(camera);
            index += 1;
        pass;
    
    def Update(self, delta):
        global rkey, lkey, ukey, dkey, ctrlkey;
        global editSelectIndex, isSelected, MainCamera;
        GameColideData.tileSiz = 100000 / MainCamera.destWH.x;

        if(isSelected == False):
            if(rkey == True):
                MainCamera.MoveTo(MainCamera.destpos + vec2(300 * delta, 0), MainCamera.destWH);
            if(lkey == True):
                MainCamera.MoveTo(MainCamera.destpos + vec2(-300 * delta, 0), MainCamera.destWH);
            if(ukey == True):
                MainCamera.MoveTo(MainCamera.destpos + vec2(0, 300 * delta), MainCamera.destWH);
            if(dkey == True):
                MainCamera.MoveTo(MainCamera.destpos + vec2(0, -300 * delta), MainCamera.destWH);
        else:
            if(EditData.addobjiscol):
                if(ctrlkey == False):
                    if(rkey == True):
                        self.GCDArr[editSelectIndex].RT.Move(vec2(1, 0));
                    if(lkey == True):
                       self.GCDArr[editSelectIndex].RT.Move(vec2(-1, 0));
                    if(ukey == True):
                       self.GCDArr[editSelectIndex].RT.Move(vec2(0, 1));
                    if(dkey == True):
                        self.GCDArr[editSelectIndex].RT.Move(vec2(0, -1));
                else:
                    if(rkey == True):
                        self.GCDArr[editSelectIndex].RT.lx + 10;
                    if(lkey == True):
                        self.GCDArr[editSelectIndex].RT.lx - 10;
                    if(ukey == True):
                        self.GCDArr[editSelectIndex].RT.ly + 10;
                    if(dkey == True):
                        self.GCDArr[editSelectIndex].RT.ly - 10;
            else:
                if(ctrlkey == False):
                    if(rkey == True):
                        self.GODArr[editSelectIndex].RT.Move(vec2(1, 0));
                    if(lkey == True):
                       self.GODArr[editSelectIndex].RT.Move(vec2(-1, 0));
                    if(ukey == True):
                       self.GODArr[editSelectIndex].RT.Move(vec2(0, 1));
                    if(dkey == True):
                        self.GODArr[editSelectIndex].RT.Move(vec2(0, -1));
                else:
                    if(rkey == True):
                        self.GODArr[editSelectIndex].RT.lx + 10;
                    if(lkey == True):
                        self.GODArr[editSelectIndex].RT.lx - 10;
                    if(ukey == True):
                        self.GODArr[editSelectIndex].RT.ly + 10;
                    if(dkey == True):
                        self.GODArr[editSelectIndex].RT.ly - 10;
        pass;
    
    def Event(self, event):
        global rkey, lkey, ukey, dkey, ctrlkey;
        global editSelectIndex, isSelected;
                

        if(event.type == SDL_KEYDOWN):
            if(event.key == SDLK_0):
                MainCamera.destpos = vec2(0, 0);
            
            if(isSelected):
                if(EditData.addobjiscol):
                    if(event.key == SDLK_DELETE):
                        obj = self.GCDArr[editSelectIndex];
                        self.GCDArr.remove(obj);
                        del obj;
                        isSelected = False;
                        editSelectIndex = 0;

                    if(event.key == SDLK_q):
                        if(self.GCDArr[editSelectIndex].TileImageIndex - 1 >= 0):
                            self.GCDArr[editSelectIndex].TileImageIndex -= 1;
                    if(event.key == SDLK_e):
                        if(self.GCDArr[editSelectIndex].TileImageIndex + 1 < len(GameObjectData.images)):
                            self.GCDArr[editSelectIndex].TileImageIndex += 1;
                else:
                    if(event.key == SDLK_DELETE):
                        obj = self.GODArr[editSelectIndex];
                        self.GODArr.remove(obj);
                        del obj;
                        isSelected = False;
                        editSelectIndex = 0;
                    
                    if(event.key == SDLK_q):
                        if(self.GODArr[editSelectIndex].sprindex - 1 >= 0):
                            self.GODArr[editSelectIndex].sprindex -= 1;
                    if(event.key == SDLK_e):
                        if(self.GODArr[editSelectIndex].sprindex + 1 < len(GameObjectData.images)):
                            self.GODArr[editSelectIndex].sprindex += 1;

            if(event.key == SDLK_l):
                self.LoadData("MapSaveFile.txt");
            if(event.key == SDLK_k):
                self.SaveData();
            if(event.key == SDLK_z):
                EditData.addTargetLayer -= 1;
            if(event.key == SDLK_x):
                EditData.addTargetLayer += 1;
            if(event.key == SDLK_o):
                if(EditData.addobjiscol):
                    EditData.addobjiscol = False;
                    EditData.AddMode = 'ready';
                else:
                    EditData.addobjiscol = True;
                    EditData.AddMode = 'ready';

        if(EditData.addobjiscol):
            if(EditData.AddMode == 'ready'):
                if(event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT):
                    EditData.AddMode = 'making';
                    pos = MainCamera.ScreenPosToWorldPos(vec2(event.x, event.y));
                    EditData.AddingGCD.RT = rect4(pos.x, pos.y, 0, 0);
            elif(EditData.AddMode == 'making'):
                pos = MainCamera.ScreenPosToWorldPos(vec2(event.x, event.y));
                EditData.AddingGCD.RT = rect4(EditData.AddingGCD.RT.fx, EditData.AddingGCD.RT.fy, pos.x, pos.y);
                if(event.type == SDL_MOUSEBUTTONUP and event.button == SDL_BUTTON_LEFT):
                    EditData.AddingGCD.sort();
                    self.AddColObj(copy_GCD(EditData.AddingGCD));
                    EditData.AddMode = 'ready';
        else:
            if(EditData.AddMode == 'ready'):
                if(event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT):
                    EditData.AddMode = 'making';
                    pos = MainCamera.ScreenPosToWorldPos(vec2(event.x, event.y));
                    EditData.AddingGOD.RT = rect4(pos.x, pos.y, 0, 0);
            elif(EditData.AddMode == 'making'):
                pos = MainCamera.ScreenPosToWorldPos(vec2(event.x, event.y));
                EditData.AddingGOD.RT = rect4(EditData.AddingGOD.RT.fx, EditData.AddingGOD.RT.fy, pos.x, pos.y);
                if(event.type == SDL_MOUSEBUTTONUP and event.button == SDL_BUTTON_LEFT):
                    EditData.AddingGOD.sort();
                    EditData.AddingGOD.Layer = EditData.addTargetLayer;
                    self.AddObj(copy_GOD(EditData.AddingGOD));
                    EditData.AddMode = 'ready';
        pass;

    def SaveData(self):
        file = open("MapSaveFile.txt", 'w');
        file.write(str(len(self.GCDArr)) + '\n');
        index = 0;
        while(index < len(self.GCDArr)):
            ins = self.GCDArr[index];
            file.write(str(ins.TileImageIndex) + '\n');
            file.write(str(ins.RT.fx) + '\n');
            file.write(str(ins.RT.fy) + '\n');
            file.write(str(ins.RT.lx) + '\n');
            file.write(str(ins.RT.ly) + '\n');
            index += 1;
        
        file.write(str(len(self.GODArr)) + '\n');
        index = 0;
        while(index < len(self.GODArr)):
            ins = self.GODArr[index];
            file.write(str(ins.sprindex) + '\n');
            file.write(str(ins.Layer) + '\n');
            file.write(str(ins.RT.fx) + '\n');
            file.write(str(ins.RT.fy) + '\n');
            file.write(str(ins.RT.lx) + '\n');
            file.write(str(ins.RT.ly) + '\n');
            index += 1;
        pass;

    def LoadData(self, mapfileName):
        index = 0;
        while(index < len(self.GCDArr)):
            del self.GCDArr[index];
            index += 1;
        self.GCDArr.clear();

        index = 0;
        while(index < len(self.GODArr)):
            del self.GODArr[index];
            index += 1;
        self.GODArr.clear();

        file = open(mapfileName, 'r');
        length = int(file.readline());
        index = 0;
        while(index < length):
            ins = GameColideData(rect4(0, 0, 0, 0));
            ins.TileImageIndex = int(file.readline());
            ins.RT.fx = float(file.readline());
            ins.RT.fy = float(file.readline());
            ins.RT.lx = float(file.readline());
            ins.RT.ly = float(file.readline());
            self.GCDArr.append(ins);
            index += 1;

        length = int(file.readline());
        index = 0;
        while(index < length):
            ins = GameObjectData(rect4(0, 0, 0, 0), 0, 0);
            ins.sprindex = int(file.readline());
            ins.Layer = int(file.readline());
            ins.RT.fx = float(file.readline());
            ins.RT.fy = float(file.readline());
            ins.RT.lx = float(file.readline());
            ins.RT.ly = float(file.readline());
            self.GODArr.append(ins);
            index += 1;
        pass;

editdata = EditData();

def init():
    global sprarr, game_manager, bgm, LevelEditMode;

    #sprite init
    sprarr.append(load_image('tica.png')) #0
    sprarr.append(load_image('table_value_2.png')) #1
    sprarr.append(load_image('Resorceses/char_walk.png')) #2
    sprarr.append(load_image('Resorceses/char_idle.png')) #3
    sprarr.append(load_image('Resorceses/Tree0.png')) #4
    sprarr.append(load_image('Resorceses/Grass0.png')) #5
    sprarr.append(load_image('Resorceses/Flower0.png')) #6
    sprarr.append(load_image('Resorceses/dark.png')) #7
    sprarr.append(load_image('Resorceses/Particles/p_fire00.png')) #8
    sprarr.append(load_image('Resorceses/Particles/p_fire01.png')) #9
    sprarr.append(load_image('Resorceses/Particles/p_fire10.png')) #10
    sprarr.append(load_image('Resorceses/Particles/p_fire11.png')) #11
    sprarr.append(load_image('Resorceses/Particles/p_fire20.png')) #12
    sprarr.append(load_image('Resorceses/SpriteSheet/Goblin/goblin_idle.png')) #13
    sprarr.append(load_image('Resorceses/SpriteSheet/Goblin/goblin_walk.png')) #14
    sprarr.append(load_image('Resorceses/SpriteSheet/Goblin/goblin_attack.png')) #15

    fontObj.append(load_font('Resorceses/Font/OK CHAN.ttf')); #1

    if(LevelEditMode):
        return;

    bgm = load_music('Resorceses\Sound\EnterToMagica0.mp3');
    bgm.set_volume(128);
    
    playerobj = Player(rect4(0, 0, 200, 240), 101, sprarr[2], sprarr[3], game_manager)
    playerobj.col.colRT = playerobj.location;
    game_manager.colManager.AddLayer("Player", 20);
    game_manager.colManager.AddObjToCollidLayer("Player", playerobj);

    game_manager.AddObject(playerobj)
    
    monster = Monster(rect4(400, 0, 600, 240), 101, sprarr[14], sprarr[13], sprarr[15], game_manager);
    playerobj.col.colRT = monster.location;
    game_manager.colManager.AddObjToCollidLayer("Player", monster);

    game_manager.AddObject(GameObject(rect4(100, -100, 300, 600), 120, sprarr[4], game_manager))
    game_manager.AddObject(GameObject(rect4(100, -100, 100, 0), 100, sprarr[5], game_manager))
    
    box = GameObject(rect4(300, 100, 400, 200), 100, sprarr[1], game_manager);
    game_manager.AddObject(box);
    box.col = Collider();
    box.col.colRT = box.location;
    game_manager.colManager.AddLayer("Box", 10);
    game_manager.colManager.AddObjToCollidLayer("Box", box);

    floor = GameObject(rect4(-500, -500, 500, -100), 100, sprarr[1], game_manager);
    game_manager.AddObject(floor);
    floor.col = Collider();
    floor.col.colRT = floor.location;
    game_manager.colManager.AddObjToCollidLayer("Box", floor);

    box2 = GameObject(rect4(-400, 100, -300, 200), 100, sprarr[1], game_manager);
    game_manager.AddObject(box2);
    box2.col = Collider();
    box2.col.colRT = box2.location;
    game_manager.colManager.AddObjToCollidLayer("Box", box2);

    game_manager.AddObject(GameObject(rect4(-100, -100, 100, 0), 100, sprarr[5], game_manager))

    masklight = MaskyLight(-10000000, sprarr[7], game_manager, 50, 35, MainCamera);
    masklight.AddLightData(LightData(vec2(0, 0), 200, vec2(500, 500), 10));
    masklight.AddLightData(LightData(vec2(600, 0), 200, vec2(500, 500), 10));
    game_manager.AddObject(masklight);

    game_manager.colManager.AddRelation("Player", "Box");
    
    particle = Particles(rect4(0, 0, 0, 0), vec2(300, 500), vec2(95, 85), 500, 20, vec2(1, 10), vec2(10, 50), 1000, 
        [sprarr[8], sprarr[9], sprarr[10], sprarr[11], sprarr[12]], game_manager);
    game_manager.AddObject(particle);

    bgm.repeat_play();
    return 0

def editplayinit():
    global sprarr, game_manager, bgm, LevelEditMode, playerobj;
    #sprite init

    index = 0;
    while(index < len(game_manager.objPool)):
        del game_manager.objPool[index];
        index += 1;
    game_manager.objPool.clear();

    index = 0;
    while(index < len(game_manager.colManager.Layers)):
        del game_manager.colManager.Layers[index];
        index += 1;
    game_manager.colManager.Layers.clear();

    index = 0;
    while(index < len(sprarr)):
        del sprarr[index];
        index += 1;
    sprarr.clear();

    del bgm;

    sprarr.append(load_image('tica.png')) #0
    sprarr.append(load_image('table_value_2.png')) #1
    sprarr.append(load_image('Resorceses/char_walk.png')) #2
    sprarr.append(load_image('Resorceses/char_idle.png')) #3
    sprarr.append(load_image('Resorceses/Tree0.png')) #4
    sprarr.append(load_image('Resorceses/Grass0.png')) #5
    sprarr.append(load_image('Resorceses/Flower0.png')) #6
    sprarr.append(load_image('Resorceses/dark.png')) #7
    sprarr.append(load_image('Resorceses/Particles/p_fire00.png')) #8
    sprarr.append(load_image('Resorceses/Particles/p_fire01.png')) #9
    sprarr.append(load_image('Resorceses/Particles/p_fire10.png')) #10
    sprarr.append(load_image('Resorceses/Particles/p_fire11.png')) #11
    sprarr.append(load_image('Resorceses/Particles/p_fire20.png')) #12
    sprarr.append(load_image('Resorceses/SpriteSheet/Goblin/goblin_idle.png')) #13
    sprarr.append(load_image('Resorceses/SpriteSheet/Goblin/goblin_walk.png')) #14
    sprarr.append(load_image('Resorceses/SpriteSheet/Goblin/goblin_attack.png')) #15

    fontObj.append(load_font('Resorceses/Font/OK CHAN.ttf')); #1

    bgm = load_music('Resorceses\Sound\EnterToMagica0.mp3');
    bgm.set_volume(128);

    playerobj = Player(rect4(0, 0, 200, 240), 101, sprarr[2], sprarr[3], game_manager)
    playerobj.col.colRT = playerobj.location;
    game_manager.colManager.AddLayer("Player", 20);
    game_manager.colManager.AddObjToCollidLayer("Player", playerobj);

    monster = Monster(rect4(400, 0, 600, 240), 101, sprarr[14], sprarr[13], sprarr[15], game_manager, playerobj);
    playerobj.col.colRT = monster.location;
    game_manager.colManager.AddObjToCollidLayer("Player", monster);

    game_manager.AddObject(playerobj)
    game_manager.AddObject(monster)

    game_manager.colManager.AddLayer("Box", 10);
    index = 0;
    while(index < len(editdata.GCDArr)):
        floor = GameObject(editdata.GCDArr[index].RT, 100, sprarr[1], game_manager);
        game_manager.AddObject(floor);
        floor.col = Collider();
        floor.col.colRT = floor.location;
        game_manager.colManager.AddObjToCollidLayer("Box", floor);
        index += 1;

    game_manager.colManager.AddRelation("Player", "Box");

    bgm.repeat_play();
    pass;

def main():
    init()
    global isRunning, game_manager, saveClock, presentClock, MainCamera, LevelEditMode, LevelEdit_PlayMode, editSelectIndex
    global rkey, lkey, ukey, dkey, isSelected, ctrlkey;

    if(LevelEditMode == False):
        saveClock = pico2d.get_time()
        while(1):
            if(isRunning == False):
                return 0
            
            presentClock = pico2d.get_time()
            deltaTime = presentClock - saveClock

            game_manager.Update(deltaTime)
            MainCamera.Update(deltaTime)

            clear_canvas()

            game_manager.Render(MainCamera)
            #fontObj[0].draw(500, 500, '마법 입문', (0, 0, 0));
            update_canvas()

            events = get_events()
            for event in events:
                EventExecute(event)
                game_manager.Event(event)

            saveClock = presentClock
    else:
        saveClock = pico2d.get_time()
        while(1):
            if(isRunning == False):
                return 0
        
            presentClock = pico2d.get_time()
            deltaTime = presentClock - saveClock

            editdata.Update(deltaTime);
            if(LevelEdit_PlayMode):
                game_manager.Update(deltaTime);
            MainCamera.Update(deltaTime)

            clear_canvas()
            if(LevelEdit_PlayMode):
                game_manager.Render(MainCamera);
            
            editdata.Render(MainCamera);
            fontObj[0].draw(0, 100, 'col : ' + str(editdata.addobjiscol) + ' mode : ' + editdata.AddMode + ' Selection : ' + str(editSelectIndex) + ' Layer : ' + str(EditData.addTargetLayer), (0, 0, 0));
            update_canvas()

            moveflow.x += deltaTime;

            events = get_events()
            for event in events:
                if(LevelEdit_PlayMode):
                    game_manager.Event(event);

                EventExecute(event)

                if(event.type == SDL_KEYDOWN):
                    if(event.key == SDLK_LCTRL):
                        ctrlkey = True;
                if(event.type == SDL_KEYUP):
                    if(event.key == SDLK_LCTRL):
                        ctrlkey = False;
                
                if(LevelEdit_PlayMode == False):
                    if(event.type == SDL_KEYDOWN):
                        if(event.key == SDLK_RIGHT):
                            rkey = True;
                        if(event.key == SDLK_LEFT):
                            lkey = True;
                        if(event.key == SDLK_UP):
                            ukey = True;
                        if(event.key == SDLK_DOWN):
                            dkey = True;
                    if(event.type == SDL_KEYUP):
                        if(event.key == SDLK_RIGHT):
                            rkey = False;
                        if(event.key == SDLK_LEFT):
                            lkey = False;
                        if(event.key == SDLK_UP):
                            ukey = False;
                        if(event.key == SDLK_DOWN):
                            dkey = False;
                    if(event.type == SDL_MOUSEBUTTONDOWN):
                        if(event.button == SDL_BUTTON_RIGHT):
                            if(EditData.addobjiscol):
                                if(isSelected):
                                    editdata.GCDArr[editSelectIndex].isSelected = False;
                            
                                isSelected = False;
                                index = 0;
                                pos = MainCamera.ScreenPosToWorldPos(vec2(event.x, event.y));
                                while(index < len(editdata.GCDArr)):
                                    if(editdata.GCDArr[index].RT.bPosInRect(pos)):
                                        isSelected = True;
                                        editSelectIndex = index;
                                        editdata.GCDArr[index].isSelected = True;
                                        break;
                                    index += 1;
                            else:
                                if(isSelected):
                                    editdata.GODArr[editSelectIndex].isSelected = False;
                            
                                isSelected = False;
                                index = 0;
                                pos = MainCamera.ScreenPosToWorldPos(vec2(event.x, event.y));
                                while(index < len(editdata.GODArr)):
                                    if(editdata.GODArr[index].RT.bPosInRect(pos)):
                                        isSelected = True;
                                        editSelectIndex = index;
                                        editdata.GODArr[index].isSelected = True;
                                        break;
                                    index += 1;

                if(event.type == SDL_KEYDOWN and event.key == SDLK_p):
                    if(LevelEdit_PlayMode):
                        LevelEdit_PlayMode = False;
                    else:
                        editplayinit();
                        LevelEdit_PlayMode = True;
                editdata.Event(event);
                #game_manager.Event(event)
            saveClock = presentClock;

        
    pass;

main()