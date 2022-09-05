from asyncio.windows_events import NULL
import os
from time import clock_gettime
from pico2d import *
from time import *
from gameObj import *

os.chdir('C:\\Users\\nohc2\\Dev\\PythonGame')
pico2d.open_canvas(800, 600)

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

def main():
    global addx
    global isRunning
    global game_manager
    global saveClock
    global presentClock

    saveClock = clock_gettime(time.CLOCK_REALTIME)
    while(1):
        if(isRunning == False):
            return 0
        
        presentClock = clock_gettime(time.CLOCK_REALTIME)
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