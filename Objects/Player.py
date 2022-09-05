from gameObj import *

class Player(GameObject):
    def __init__(self, location, layer):
        self.location = [0, 0, 0, 0]
        self.layer = 0
    
    def update(self, deltaTime):
        return 0
    
    def render(self, camera):
        return 0
    
    def event(self, event):
        return 0