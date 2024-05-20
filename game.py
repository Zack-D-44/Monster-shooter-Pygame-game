import pygame
from pygame.sprite import Group
from utils import loadSprite
from random import randint
from collections import deque
###add hit wall bullet disaapear

HIT_COLOUR = (255,0,0)

#Class for bullets
class Bullets(pygame.sprite.Sprite):
    def __init__(self):
        #Setting bullet sprite, rect and damage
        pygame.sprite.Sprite.__init__(self)
        sprite = loadSprite('bulletSprite', True)
        self.image = pygame.transform.scale(sprite, (30,30))
        self.rect = self.image.get_rect()
        self.damage = 5
        
        
        
    #Setting bullet movement
    def bulletUpdate(self, screen):
        screen.blit(self.image, self.rect)
        self.rect.x += 5

        if self.rect.x >= 750:
            self.kill()
            

        

        




#Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, player, speed, screen):
        #Setting enemy sprite and rect aswell as other values
        pygame.sprite.Sprite.__init__(self)
        sprite = loadSprite('enemySprite', True)
        self.Originalimage = pygame.transform.scale(sprite, (100, 100))
        self.image = self.Originalimage.copy()
        self.rect = self.image.get_rect()
        self.rect.y = randint(100, 450)
        self.rect.x = 600
        self.health = 50
        self.isHit = False
        self.timeLastHit = 0
        self.hitCoolDown = 100
        self.player = player
        self.speed = speed 

        self.screen = screen
        
    #Enemy movment system
    def updateEnemy(self):
        #Drawing sprite onto screen
        self.screen.blit(self.image, self.rect)
        
        #Calculating vector of enemy pointing from player
        direction = pygame.math.Vector2(self.player.rect.center) - pygame.math.Vector2(self.rect.center)

        #Checking vector length if it does normalise vector in place
        if direction.length() != 0:
            direction.normalize_ip()

        #Moving sprite
        self.rect.x += direction.x * self.speed
        self.rect.y += direction.y * self.speed

        #Applying hit affect if character hit
        if self.isHit:
            self.image.fill(HIT_COLOUR, special_flags=pygame.BLEND_ADD)

        #Enemy hit cooldown
        currentTime = pygame.time.get_ticks()
        if currentTime - self.timeLastHit >= self.hitCoolDown:
            self.isHit = False
            self.timeLastHit = currentTime

        
    


    
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, screen):
        pygame.sprite.Sprite.__init__(self)
        #Loading sprite and setting player attributes
        sprite = loadSprite('playerSprite', True)
        self.image = pygame.transform.scale(sprite, (70, 80))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y =  y
        self.lastBulletShottime = pygame.time.get_ticks()
        self.bulletCoolDown = 100
        self.health = 30
        self.speed = 5
        self.screen = screen
    
    #Shoot bullet function
    def shootBullet(self, bulletsGroup):
        
        #Shooting bullet if cooldown period over
        currentTime = pygame.time.get_ticks()
        if currentTime - self.lastBulletShottime > self.bulletCoolDown:
            
            #Creating bullet object
            bullet = Bullets()
            bullet.rect.midleft = self.rect.midright
            #adding bullet to bullet group and setting last time bullet shot to current time
            bulletsGroup.add(bullet)
            self.lastBulletShottime = currentTime


    def update(self, keys, bulletsGroup):
        #Drawing sprite to screen
        self.screen.blit(self.image, self.rect)

        #Handiling player movement
        if keys[pygame.K_w]:
            if self.rect.top > 0:
                self.rect.y -= self.speed

        if keys[pygame.K_s]:
            if self.rect.bottom < self.screen.get_height():
                self.rect.y += self.speed
        
        if keys[pygame.K_SPACE]:
            self.shootBullet(bulletsGroup)

    
#Class that handles UI
class DrawUIInfo:
    def __init__(self, screen):
        #Initialising font and screen
        self.font = pygame.font.Font(None, 30)
        self.screen = screen
    
    #Renders score text and draws it to screen
    def drawScore(self, score):
        scoreText = self.font.render(f'{score}', True, (255,255,255))
        self.screen.blit(scoreText, (10,10))
        
    #Renders player health text and draws it to screen
    def drawHealth(self,health):
        healthText = self.font.render(f'{health}', True, (255,0,0))
        self.screen.blit(healthText, (360, 10))
        
    def drawRound(self, round):
        roundText = self.font.render(f'{round}', True, (200,21,32))
        self.screen.blit(roundText, (10, 35))

#Class that handles player powerups
'''class PowerUps(pygame.sprite.Sprite):
    def __init__(self, screen):
        pygame.sprite.Sprite.__init__(self)
        
        #Setting powerup sprites and rects
        self.screen = screen
        
        
        self.hPowerUpSprite = loadSprite('heartPUpSprite', True)
        self.hPowerUpImage = pygame.transform.scale(self.hPowerUpSprite, (30, 30))
        self.hPowerUpRect = self.hPowerUpImage.get_rect()

        self.fRatePowerUpSprite = loadSprite('fireRatePUpSprite', True)
        self.fRatePowerUpImage = pygame.transform.scale(self.fRatePowerUpSprite, (30,30))
        self.fRatePowerUpRect = self.fRatePowerUpImage.get_rect()
        
        
        self.dPowerUpSprite = loadSprite('damagePUpSprite', True)
        self.dPowerUpImage = pygame.transform.scale(self.dPowerUpSprite, (30,30))
        self.dPowerUpRect = self.dPowerUpImage.get_rect()

        #Setting powerup movement attributes
        self.powerUpMovingDown = True
        self.powerUpMovingUp = False
        self.powerUpSpeed = 2 

        self.spritePostionX = 0
        self.spritePostionY = 0
        
        
        

    def healthPowerUp(self):
        #Randomly selecting sprites postion
        self.hPowerUpRect.x = self.chooseSpritePostion()['X']
        self.hPowerUpRect.y = self.chooseSpritePostion()['Y']

        #Drawing sprite to screen
        self.screen.blit(self.hPowerUpImage, self.hPowerUpRect)

        


    def fireRatePowerUp(self):
        #Randomly selecting sprites position
        self.fRatePowerUpRect.x = self.chooseSpritePostion()['X']
        self.fRatePowerUpRect.y = self.chooseSpritePostion()['Y']

        #Drawing sprite to screen
        self.screen.blit(self.fRatePowerUpImage, self.fRatePowerUpRect)

    def damagePowerUp(self):
        #Randomly selecting sprites postion
        self.dPowerUpRect.x = self.chooseSpritePostion()['X']
        self.dPowerUpRect.y = self.chooseSpritePostion()['Y']

        #Drawing sprite to screen
        self.screen.blit(self.dPowerUpImage, self.dPowerUpRect)

    def chooseSpritePostion(self):
        #Creating a dictionary with two random x and y values that are used to set sprites position
        spritePosition = dict()
        
        #Assigning dictionaries X and Y values
        spritePosition['X'] = randint(300, 700)
        spritePosition['Y'] = randint(10, 400)
        
        #Returning dictionary
        return spritePosition
        


    
    #Handles powerup movment
    def powerUpUpdate(self, powerUpRect, powerUpImage):
        #Changing direction if sprite reaches bottom of screen
        if powerUpRect.y >= 470:
            self.powerUpMovingUp = True
            self.powerUpMovingDown = False
        #Changes direction if sprite reaches top of screen
        elif powerUpRect.y <= 0:
            self.powerUpMovingDown = True
            self.powerUpMovingUp = False

        #Moving sprite upwards
        if self.powerUpMovingUp:
            powerUpRect.y -= self.powerUpSpeed

        #Moving sprite downwards
        elif self.powerUpMovingDown:
            powerUpRect.y += self.powerUpSpeed

        #Drawing sprite 
        self.screen.blit(powerUpImage, powerUpRect)'''
        
        


class theGame:
    #initialise display 
    def __init__(self):
        #initialising pygame and pygame fonts
        pygame.init()
        pygame.font.init()
        #Setting display caption
        pygame.display.set_caption('The game')

        #creating screen variable
        self.screen = pygame.display.set_mode((740, 493))#x,y
        #load background setting false because we don't need alpha transparency
        self.background = loadSprite("gameBackground", False)
        
        #creating player and adding it to the player sprite group
        self.player = Player(50, 150, self.screen)
        self.playerGroup = pygame.sprite.Group()
        self.playerGroup.add(self.player)

        
        #creating powerups object and creating a health powerup
        #self.powerUps = PowerUps(self.screen)
        #self.powerUps.healthPowerUp()
        
        #Initialising enemies        
        self.enemies = pygame.sprite.Group()
        self.enemyDamage = 5
        self.enemiesKilled = 0
        self.enemySpeed = 2.5
        self.createEnemies()
        
        #Creating bullet sprite group
        self.bullets = pygame.sprite.Group()
        
        #Drawing ui info to screen
        self.uiInfo = DrawUIInfo(self.screen)
        self.uiInfo.drawScore(0)
        self.uiInfo.drawHealth(self.player.health)

        self.round = 1

    
    #Handling random powerup spawns
    def chooseRandomPowerUp(self):
        #list of power ups with their rects and images
        listOfPowerUps = [[self.powerUps.hPowerUpRect, self.powerUps.hPowerUpImage],[self.powerUps.dPowerUpRect, self.powerUps.dPowerUpImage], [self.powerUps.fRatePowerUpRect, self.powerUps.fRatePowerUpImage]]

        #Randomly chosing which powerup from the list
        powerUpChoice = listOfPowerUps[randint(0,2)]

        #Creating dict 
        powerUpChoiceDict = dict()

        #Setting the rect and image of chosen powerup as values in the dict
        powerUpChoiceDict['Rect'] = listOfPowerUps[powerUpChoice, 0]
        powerUpChoiceDict['Image'] = listOfPowerUps[powerUpChoice, 1]
        
        return powerUpChoiceDict
    

    #Random enemy spawn mechanic
    def createEnemies(self):
        #For value between 1 and 5 spawn enemy, change these values to set max and min enemy spawns
        for _ in range(randint(1,5)):
            enemy = Enemy(self.player, self.enemySpeed, self.screen)
            self.enemies.add(enemy)
            '''if self.enemiesKilled % 10 == 0:##not working come back to later
                self.enemySpeed += 0.1  
                self.player.speed += 1
                print(self.player.speed, self.enemySpeed)'''

    



    #The game loop
    def gameLoop(self):
        #Creating a clock
        clock = pygame.time.Clock()
        #Setting spawn timer to zero
        spawnTimer = 0
        
        while True:
            #Handling if game shutdown 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                #Handling shooting bullets
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.player.shootBullet(self.bullets)
            
        
            #self.powerUps.powerUpUpdate(self.screen, self.powerUps.hPowerUpRect, self.powerUps.hPowerUpImage)
            #Getting pressed keys and updating player based on them
            keys = pygame.key.get_pressed()
            self.player.update(keys, self.bullets)

            #Handling enemy bullet collisions
            
            bulletEnemyCollisions = pygame.sprite.groupcollide(self.bullets, self.enemies, True, False)
            for bullet, hitEnemies in bulletEnemyCollisions.items():
                #reducing health of enemy by 5 when it is hit
                for enemy in hitEnemies:
                    enemy.health -= 5
                    #removing enemy if health is 0
                    if enemy.health <= 0:
                        self.enemies.remove(enemy)
                        #Counting how many enemies killed
                        self.enemiesKilled += 1
                    if self.enemiesKilled/10 == self.round:
                        self.player.health += 10
                        self.player.speed += 1
                        self.enemySpeed += 1
                        self.round += 1
                        self.enemies.empty()
                        self.uiInfo.drawRound(self.round)
                        
                        
                    else:
                        #Setting enemy is hit to activate its hit effect
                        enemy.isHit = True

            #Handling enemies collisions with players
            playerEnemyCollisions = pygame.sprite.groupcollide(self.enemies, self.playerGroup, True, False)
            for enemies, hitPlayer in playerEnemyCollisions.items():
                for enemy in hitPlayer:
                    #reducing player health by enemy damage if the player is hit
                    self.player.health -= self.enemyDamage
                    #Updating UI information
                    self.uiInfo.drawHealth(self.player.health)
                    #Ending game if player health equals 0
                    if self.player.health <= 0:
                        quit()

            
                    
            
            #Updating enemies
            for enemy in self.enemies:
                enemy.updateEnemy()
            
            spawnTimer += clock.get_rawtime() 

            #Spawning new enemies every
            if spawnTimer >= 300:
                self.createEnemies()
                spawnTimer = 0
            
            #Looping through bullets in bullet sprite group and updating there position
            for bullet in self.bullets:
                bullet.bulletUpdate(self.screen)

            #Drawing all of the sprites with method that handles sprite drawing
            self.draw()
            
            clock.tick(60)
            pygame.display.flip()
    
            
    
    #draws objects
    def draw(self):
        #blit means transferring bytes from one buffer to another
        #in this case background attribute initialised when class created going to be blitted to screen surface
        #Drawinng all of the sprites to the positions that they are required in
        self.screen.blit(self.background, (0,0))
        self.screen.blit(self.player.image, self.player.rect)
        self.enemies.draw(self.screen)
        self.bullets.draw(self.screen)
        self.uiInfo.drawScore(self.enemiesKilled)
        self.uiInfo.drawHealth(self.player.health)
        self.uiInfo.drawRound(self.round)
        #self.powerUps.powerUpUpdate(self.powerUps.hPowerUpRect, self.powerUps.hPowerUpImage)
        
        #self.powerUps.powerUpUpdate(self.powerUps.fRatePowerUpRect, self.powerUps.fRatePowerUpImage)
        
        #self.powerUps.powerUpUpdate(self.powerUps.dPowerUpRect, self.powerUps.dPowerUpImage)
        
        
        
