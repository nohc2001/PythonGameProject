import os
from pico2d import *
from Objects.Particles import *
from gameObj import *
from Objects.Player import *
from Objects.MaskyLight import*

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

class GameColideData:
    image = pico2d.load_image("Resorceses/GCD.png");
    def __init__(self, rt):
        self.RT = rt;
        pass;
    
    def sort(self):
        if(self.RT.fx > self.RT.lx):
            self.RT.fx, self.RT.lx = self.RT.lx, self.RT.fx;
        if(self.RT.fy > self.RT.ly):
            self.RT.fy, self.RT.ly = self.RT.ly, self.RT.fy;
        pass
    
    def render(self, camera):
        fpos = camera.WorldPosToScreenPos(self.RT.getfpos())
        lpos = camera.WorldPosToScreenPos(self.RT.getlpos())
        ObjInScreenRt = rect4(fpos.x, fpos.y, lpos.x, lpos.y)
        GameColideData.image.draw(int(ObjInScreenRt.getcenter().x), int(ObjInScreenRt.getcenter().y), int(ObjInScreenRt.getwid()), int(ObjInScreenRt.gethei()));
        pass;

def copy_GCD(GCD):
    gcd = GameColideData(GCD.RT);
    return gcd;

class EditData:
    AddMode = 'ready';
    AddingGCD = GameColideData(rect4(0, 0, 0, 0));
    def __init__(self) -> None:
        self.GCDArr = [];
        pass

    def AddObj(self, gcd):
        self.GCDArr.append(gcd);
        pass;
    
    def Render(self, camera):
        index = 0;
        #EditData.AddingGCD.render(camera);
        while(index < len(self.GCDArr)):
            self.GCDArr[index].render(camera);
            index += 1;
        pass;
    
    def Event(self, event):
        if(EditData.AddMode == 'ready'):
            if(event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT):
                EditData.AddMode = 'making';
                pos = MainCamera.ScreenPosToWorldPos(vec2(event.x, event.y));
                EditData.AddingGCD.RT = rect4(pos.x, pos.y, 0, 0);
        elif(EditData.AddMode == 'making'):
            if(event.type == SDL_MOUSEBUTTONUP and event.button == SDL_BUTTON_LEFT):
                pos = MainCamera.ScreenPosToWorldPos(vec2(event.x, event.y));
                EditData.AddingGCD.RT = rect4(EditData.AddingGCD.RT.fx, EditData.AddingGCD.RT.fy, pos.x, pos.y);
                EditData.AddingGCD.sort();
                self.AddObj(copy_GCD(EditData.AddingGCD));
                EditData.AddMode = 'ready';
        pass;

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

editdata = EditData();
moveflow = vec2(0, 0.1);
def main():
    init()
    global isRunning, game_manager, saveClock, presentClock, MainCamera, LevelEditMode

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
        rkey, lkey, ukey, dkey = False, False, False, False;
        saveClock = pico2d.get_time()
        while(1):
            if(isRunning == False):
                return 0
        
            presentClock = pico2d.get_time()
            deltaTime = presentClock - saveClock

            #game_manager.Update(deltaTime)
            MainCamera.Update(deltaTime/1000.0)

            clear_canvas()

            #game_manager.Render(MainCamera)
            #fontObj[0].draw(500, 500, '마법 입문', (0, 0, 0));
            editdata.Render(MainCamera);
            update_canvas()

            moveflow.x += deltaTime/1000.0;

            events = get_events()
            for event in events:
                EventExecute(event)
                if(event.type == SDL_KEYDOWN and event.key == SDLK_RIGHT):
                    rkey = True;
                    MainCamera.MoveTo(MainCamera.destpos + vec2(100, 0), MainCamera.destWH);
                if(event.type == SDL_KEYDOWN and event.key == SDLK_LEFT):
                    lkey = True;
                    MainCamera.MoveTo(MainCamera.destpos + vec2(-100, 0), MainCamera.destWH);
                if(event.type == SDL_KEYDOWN and event.key == SDLK_UP):
                    ukey = True;
                    MainCamera.MoveTo(MainCamera.destpos + vec2(0, 100), MainCamera.destWH);
                if(event.type == SDL_KEYDOWN and event.key == SDLK_DOWN):
                    
                    MainCamera.MoveTo(MainCamera.destpos + vec2(0, -100), MainCamera.destWH);
                editdata.Event(event);
                #game_manager.Event(event)

        saveClock = presentClock;
    pass;

main()