import cl_games.sprites as sprites
from cl_games.game import Game

def sprite_collide(main_sp, group):
    retval = []
    for sprite in group:
        if has_collided(main_sp, sprite):
            retval.append(sprite)
    return retval

def group_collide(group1, group2):
    retval = []
    for sprite1 in group1:
        for sprite2 in group2:
            if has_collided(sprite1, sprite2):
                retval.append([sprite1, sprite2])
    return retval

def has_collided(sprite1, sprite2):
    if sprite1.alive == True and sprite2.alive == True:
        if (sprite1.posX > (sprite2.posX + sprite2.lenX)) or ((sprite1.lenX + sprite1.posX) < sprite2.posX) or (sprite1.posY > (sprite2.posY + sprite2.lenY)) or ((sprite1.lenY + sprite1.posY) < sprite2.posY):
            return False
        else:
            return True
    else:
        return False
