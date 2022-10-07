from gameObj import *
from SpaceMath import *
from Camera import*

class LightData:
    def __init__(self, pos0, radius0, pos1, radius1) -> None:
        self.pos0 = pos0;
        self.radius0 = radius0;
        self.pos1 = pos1;
        self.radius1 = radius1;
        pass;

    def bPosInLightRange(self, ipos):
        distance0 = get_distance(self.pos0, ipos);
        if(distance0 < self.radius0):
            return True;
        distance1 = get_distance(self.pos1, ipos);
        if(distance1 < self.radius1):
            return True;

        dir = vec2(self.pos1.x - self.pos0.x, self.pos1.y - self.pos0.y);
        idir = vec2(dir.y, -dir.x);
        idir_distance = math.sqrt(math.pow(idir.x, 2) + math.pow(idir.y, 2));
        iidir = vec2(idir.x / idir_distance, idir.y / idir_distance);

        polypos = [];
        polypos[0] = vec2(self.pos0.x + iidir.x * self.radius0 , self.pos0.y + iidir.y * self.radius0 );
        polypos[1] = vec2(self.pos1.x + iidir.x * self.radius1 , self.pos1.y + iidir.y * self.radius1 );
        polypos[2] = vec2(self.pos1.x - iidir.x * self.radius1 , self.pos1.y - iidir.y * self.radius1 );
        polypos[3] = vec2(self.pos0.x - iidir.x * self.radius0 , self.pos0.y - iidir.y * self.radius0 );

        h = 0;
        index = 0;
        while(index < 4):
            p1 = vec2(0, 0);
            p2 = vec2(0, 0);
            if(index == 3):
                p1 = polypos[index];
                p2 = polypos[0];
            else:
                p1 = polypos[index];
                p2 = polypos[index+1];

            sl = straightLine(p1, p2);
            xx = sl.GetYFromX(ipos.y);
            if(ipos.x < xx and ((p1.y < ipos.y and ipos.y < p2.y) or (p2.y < ipos.y and ipos.y < p1.y))):
                h+=1;
        
        if(h%2 == 1):
            return True;
        else:
            return False;

class MaskyLight(GameObject):
    def __init__(self, layer, darkspr, gm, wdivide, hdivide):
        self.layer = layer;
        self.darkspr = darkspr;
        self.gm = gm;
        self.wdivide = wdivide;
        self.hdivide = hdivide;
        self.lightDataPool = [];
        self.ldpup = 0;
    
    def update(self, deltaTime):
        pass
    
    def render(self, camera):
        wh = vec2(WMAX/self.wdivide, HMAX/self.hdivide);

        windex = 0;
        while(windex < self.wdivide):
            hindex = 0;
            while(hindex < self.hdivide):
                self.darkspr.draw(wh.x*windex, wh.y*hindex, wh.x, wh.y);
                hindex += 1;
            windex += 1;
        return 0
    
    def event(self, event):
        return 0
    
    def AddLightData(self, ldata):
        self.lightDataPool[self.ldpup] = ldata;
        self.ldpup += 1;
    
    def ClearLightData(self):
        self.lightDataPool.clear();
        self.ldpup = 0;
    