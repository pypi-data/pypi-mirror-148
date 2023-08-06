class Sprite:
    """Sprite Class"""
    groups = []
    posX = 0
    posY = 0
    lenX = 0
    lenY = 0
    image = []
    alive = True
    def __init__(self, game):
        self.game = game
        self.groups = []
        self.posX = 0
        self.posY = 0
        self.lenX = 0
        self.lenY = 0
        self.image = []
    def update(self):
        pass
    def setLengthToImage(self):
        self.lenY = len(self.image)
        self.lenX = len(self.image[0])
    def kill(self):
        self.alive = False
        for sg in self.groups:
            sg.takeout(self)
class SpriteGroup:
    """docstring for SpriteGroup."""
    sprites = []
    def __init__(self):
        super(SpriteGroup, self).__init__()
        self.sprites = []
    def add(self, sprite):
        self.sprites.append(sprite)
        sprite.groups.append(self)
    def __iter__(self):
        return iter(self.sprites)
    def takeout(self, sprite):
        if sprite in self.sprites:
            self.sprites.remove(sprite)
        if self in sprite.groups:
            sprite.groups.remove(self)
