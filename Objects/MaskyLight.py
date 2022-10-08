from math import inf
from gameObj import *
from SpaceMath import *
from Camera import*

class LightData:
    def __init__(self, pos0, radius0, pos1, radius1) -> None:
        self.pos0 = pos0;
        self.radius0 = radius0;
        self.pos1 = pos1;
        self.radius1 = radius1;
        minx = min([self.pos0.x - self.radius0, self.pos1.x - self.radius1]);
        maxx = max([self.pos0.x + self.radius0, self.pos1.x + self.radius1]);
        miny = min([self.pos0.y - self.radius0, self.pos1.y - self.radius1]);
        maxy = max([self.pos0.y + self.radius0, self.pos1.y + self.radius1]);
        self.lightRT = rect4(minx, miny, maxx, maxy);
        pass;

    def bLightDataInCameraRange(self, camera):
        if(camera.Rt.bRectTouchRect(self.lightRT)):
            return True;
        else:
            return False;
        pass;

    def bPosInLightRange(self, ipos):
        if(get_distance(self.pos0, ipos) < self.radius0):
            return True;
        if(get_distance(self.pos1, ipos) < self.radius1):
            return True;

        idir = vec2(self.pos1.y - self.pos0.y, self.pos0.x - self.pos1.x);
        idir_distance = math.sqrt(math.pow(idir.x, 2) + math.pow(idir.y, 2));
        iidir = vec2(idir.x / idir_distance, idir.y / idir_distance);

        idr0 = vec2(iidir.x * self.radius0, iidir.y * self.radius0);
        idr1 = vec2(iidir.x * self.radius1, iidir.y * self.radius1);
        polypos = [vec2(self.pos0.x + idr0.x , self.pos0.y + idr0.y ),
            vec2(self.pos1.x + idr1.x , self.pos1.y + idr1.y ),
            vec2(self.pos1.x - idr1.x , self.pos1.y - idr1.y ),
            vec2(self.pos0.x - idr0.x , self.pos0.y - idr0.y )];

        h = 0;
        index = 0;
        while(index < 4):
            p1 = polypos[index];
            p2 = polypos[(index+1)%4];

            sl = straightLine(p1, p2);
            xx = sl.GetXFromY(ipos.y);
            if(ipos.x < xx and ((p1.y < ipos.y and ipos.y < p2.y) or (p2.y < ipos.y and ipos.y < p1.y))):
                h+=1;
            index += 1;
        
        if(h%2 == 1):
            return True;
        else:
            return False;

class MaskyLight(GameObject):
    def __init__(self, layer, darkspr, gm, wdivide, hdivide, cameraobj):
        self.location = rect4(0, 0, 0, -9999999999);
        self.layer = layer;
        self.darkspr = darkspr;
        self.gm = gm;
        self.wdivide = wdivide;
        self.hdivide = hdivide;
        self.lightDataPool = [];
        self.ldpup = 0;
        self.darkmap = [];

        yindex = 0;
        while(yindex < hdivide):
            arr = [];
            xindex = 0;
            while(xindex < wdivide):
                arr.append(False);
                xindex += 1;
            self.darkmap.append(arr);
            yindex += 1;

        self.cameraObj = cameraobj;
        self.stacktime = 0;
    
    def update(self, deltaTime):
        self.stacktime += deltaTime;
        if(self.stacktime > 0.1):
            self.UpdateDarkMap();
            self.stacktime = 0;
        pass

    def UpdateDarkMap(self):
        wh = vec2(WMAX/self.wdivide, HMAX/self.hdivide);

        lightIndexs = [];
        lindex = 0;
        while(lindex < self.ldpup):
            lightData = self.lightDataPool[lindex];
            if(lightData.bLightDataInCameraRange(self.cameraObj)):
                lightIndexs.append(lindex);
            lindex += 1;

        windex = 0;
        while(windex < self.wdivide):
            hindex = 0;
            while(hindex < self.hdivide):
                ldindex = 0;
                self.darkmap[hindex][windex] = True;
                while(ldindex < len(lightIndexs)):
                    lightData = self.lightDataPool[lightIndexs[ldindex]];
                    if(lightData.bPosInLightRange(self.cameraObj.ScreenPosToWorldPos(vec2(wh.x*windex+wh.x/2, wh.y*hindex+wh.y/2)))):
                        self.darkmap[hindex][windex] = False;
                        break;
                    ldindex += 1;
                hindex += 1;
            windex += 1;
        return 0
    
    def render(self, camera):
        wh = vec2(WMAX/self.wdivide, HMAX/self.hdivide);

        windex = 0;
        while(windex < self.wdivide):
            hindex = 0;
            while(hindex < self.hdivide):
                if(self.darkmap[hindex][windex]):
                    self.darkspr.draw(wh.x*windex, wh.y*hindex, wh.x, wh.y);
                hindex += 1;
            windex += 1;
        return 0
    
    def event(self, event):
        return 0
    
    def AddLightData(self, ldata):
        self.lightDataPool.append(ldata);
        self.ldpup += 1;
    
    def ClearLightData(self):
        self.lightDataPool.clear();
        self.ldpup = 0;
    