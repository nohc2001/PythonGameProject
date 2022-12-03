
from random import randint
import random
from gameObj import GameObject
from SpaceMath import *
from Camera import*

class Particles(GameObject):
    def __init__(self, volume, partSpeedMM, AngleRange, gravity, partnum_ps, part_maxtimeMM, part_maxRadiusMM, maxtime, spritelist, gm) -> None:
        self.enable = True;
        self.part_create_volume = volume;
        self.part_speed_minmax = partSpeedMM;
        self.part_maxRadius_minmax = part_maxRadiusMM;
        self.gravity = gravity;
        self.part_dirAngleRange = AngleRange;
        self.part_num_per_sec = partnum_ps;
        self.part_maxtime_minmax = part_maxtimeMM;
        self.flowtime = vec2(0, maxtime);
        self.sprlist = spritelist;
        self.gm = gm;
        self.stacktime = 0;
        self.layer = -10000001;
        self.location = rect4(0, 0, 0, 0);
        self.stackpart = 0;
        pass

    def update(self, deltaTime):
        self.flowtime.x += deltaTime;
        if(self.flowtime.y < self.flowtime.x):
            self.enable = False;
        
        cindex = 0;
        cmax = deltaTime * self.part_num_per_sec;
        self.stackpart += cmax;
        while(cindex < int(self.stackpart)):
            setarange = vec2(math.pi * self.part_dirAngleRange.x/180.0, math.pi * self.part_dirAngleRange.y/180.0);
            part_create_pos = vec2(randint(self.part_create_volume.fx, self.part_create_volume.lx), randint(self.part_create_volume.fy, self.part_create_volume.ly));
            randangle = random.uniform(setarange.x, setarange.y);
            partSpeed = random.uniform(self.part_speed_minmax.x, self.part_speed_minmax.y);
            part_dir = vec2(partSpeed * math.cos(randangle), partSpeed * math.sin(randangle));
            part_radius = random.uniform(self.part_maxRadius_minmax.x, self.part_maxRadius_minmax.y);
            part_maxtime = random.uniform(self.part_maxtime_minmax.x, self.part_maxtime_minmax.y);
            self.gm.AddPart(part_create_pos, part_dir, part_radius, self.gravity, part_maxtime, self.sprlist[random.randint(0, len(self.sprlist)-1)]);
            cindex += 1;
        self.stackpart -= cindex;

    def render(self, camera):
        return 0
    
    def event(self, events):
        return 0
    
    def SetGameManager(self, gameManager):
        self.gm = gameManager
        return 0