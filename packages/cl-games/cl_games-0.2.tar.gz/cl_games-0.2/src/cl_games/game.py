import sys
import os
import time
import cl_games.input as input
import cl_games.sprites as sprites
class Game:
    """This is the class for the game
        It takes no parameters
        This class is abstract, do not instance it, extend it.
        Just use Game().run() for running it
    """
    sprites = None
    running = True
    title = ""
    sizeX = 40
    sizeY = 20
    wait = 0.02
    clock = 0
    lastFrame = 0
    hud = []
    blank = " "
    input = None
    frameTime = 0
    def __init__(self):
        self.sprites = sprites.SpriteGroup()
        self.running = True
        self.title = ""
        self.sizeX = 40
        self.sizeY = 20
        self.wait = 0.02
        self.clock = 0
        self.lastFrame = 0
        self.hud = []
        self.blank = " "
        self.input = None
        self.frameTime = 0
    def update(self):
        pass
    def renderFrame(self):
        yAxis = []
        yAxis.append("_" * (self.sizeX + 2))
        yAxis.append("|" + (" " * self.sizeX) + "|\r" + ("|" + (" " * (int(self.sizeX / 2) - int(len(self.title) / 2)) + self.title)))
        for y in range(self.sizeY):
            xAxis = ""
            xAxis += "|"
            for x in range(self.sizeX):
                pixel = self.blank
                for sprite in self.sprites:
                    if y in range(int(sprite.posY),int(sprite.posY) + sprite.lenY) and x in range(int(sprite.posX), int(sprite.posX) + sprite.lenX):
                        if sprite.alive == True:
                            disY = y - int(sprite.posY)
                            disX = x - int(sprite.posX)
                            component = sprite.image[disY][disX]
                            pixel = component

                xAxis += pixel
            xAxis += "|"
            yAxis.append(xAxis)
        for index, line in enumerate(self.hud):
            yAxis[index + 2] += '\r' +"|" + line
        yAxis.append("|" + ("_"*self.sizeX) + "|")
        frame = ""
        for line in yAxis:
            frame += "\n" + line
        return frame
    def onFrame(self):
        for sprite in self.sprites:
            if  sprite.alive: sprite.update()
        self.update()
        frame = self.renderFrame()
        os.system('cls' if os.name == 'nt' else 'clear')
        sys.stdout.write(frame)
        sys.stdout.flush()
    def run(self):
        self.running = True
        if self.input is not None:
            self.input.startListening()
        lastFrame = time.time()
        while self.running:
            self.clock = time.time()
            if (self.clock - self.lastFrame) > self.wait:
                self.frameTime = self.clock - self.lastFrame
                self.lastFrame = self.clock
                self.onFrame()
    def addSprite(self, sprite, number=None):
        self.sprites.add(sprite)
