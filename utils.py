#helper methods for code
from pygame.image import load
from pathlib import Path

#method that deals with loading sprites
def loadSprite(name, withAlpha=True):
    #creating the file path
    #__file__ is python constant that equates to path of source file in this case utils parent equates to dir that file is found in after slash is the path of file we want to access so it will go parent/assets/sprites/file.png
    filename = Path(__file__).parent / Path("assets/sprites/" + name + ".png")
    #resolve creates the path load is pygame module that loads sprite
    sprite = load(filename.resolve())

    #checks if we want to use alpha transparency
    if withAlpha:
        #returning with transparency
        return sprite.convert_alpha()
    
    #returning without alpha transparency
    return sprite.convert()