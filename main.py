
import os
from pico2d import *
from gameObj import *
from Objects.Player import *

os.chdir('C:\\Users\\nohc2\\Dev\\PythonGame\\PythonGameProject')
pico2d.open_canvas(800, 600)
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

global MainCamera
MainCamera = Camera(vec2(0, 0), 800, 600, vec2(0, 0), 0.95, vec2(800, 600))

global saveClock
global presentClock
saveClock = 0
presentClock = 0

def init():
    global sprarr
    global game_manager

    #sprite init
    sprarr.append(load_image('tica.png'))

    playerobj = Player(rect4(0, 0, 100, 200), 1, sprarr[0], game_manager)
    game_manager.AddObject(playerobj)
    return 0

def main():
    init()
    global addx
    global isRunning
    global game_manager
    global saveClock
    global presentClock
    global MainCamera

    saveClock = pico2d.get_time()
    while(1):
        if(isRunning == False):
            return 0
        
        presentClock = pico2d.get_time()
        deltaTime = presentClock - saveClock

        game_manager.Update(deltaTime)

        clear_canvas()

        game_manager.Render(MainCamera)

        update_canvas()

        events = get_events()
        for event in events:
            EventExecute(event)
            game_manager.Event(event)

        saveClock = presentClock

main()