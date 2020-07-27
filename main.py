'''File name: ICS 11 Summative
Author: Rayton Lin
Teacher: Mr.Saleem
Date created: April 29th, 2019
Purpose: Create the main file to run our air hockey game. This main file contains the program for the
                 user interface of the game. From the main menu the user is able to view the rules of the game,
                 quit the program, and continue to the first level. After selecting their level the user will
                 be able to play or quit the game. The player will control their paddle with either the WASD keys or arrow keys. 
                 Throughout the game the user will be able to see their score and time. After the game is over, their score and time will
                 be displayed.
'''
#Imports the pygame module
import pygame
#Imports all local functions from pygame.local
from pygame.locals import *

#Define colors and screen size
red=(255,0,0)
green=(0,255,0)
lgreen=(193,255,193) #Light Green
blue=(0,0,255)
white=(255,255,255)
black=(0,0,0)
#The above are the colours that will be used for the game
 
#Initializes the size of the screen
size=width,height=600,600
#Initializes the clock into a variable
clock=pygame.time.Clock()
 
#Initialize pygame and creates the screen
pygame.init()
screen=pygame.display.set_mode(size)

'''
# Initiates pygame.mixer to allow user to adjust the sound volume
pygame.mixer.init(frequency = 22050, size = -16, channels = 2, buffer = 1024)
'''

#Loading audio
hit = pygame.mixer.Sound("soundsandimages/explosion.ogg")
hit.set_volume(0.5)
pygame.mixer.music.load("soundsandimages/edinstrumental.mp3")
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.15)

#Create the necessary classes and functions
class Block(pygame.sprite.Sprite): #Class for the blocks that will be broken in each level
    #Constructor
    def __init__(self,color):
        super().__init__() #Call the Parent class constructor
 
        #set the two mandatory attributes for a sprite
        self.image=pygame.Surface([24,20])
        self.image.fill(color)
        self.rect=self.image.get_rect()
 
class Ball(pygame.sprite.Sprite): #Class for the ball that will break the blocks.
    #Constructor
    def __init__(self,color):
        super().__init__() #Call the Parent class constructor
 
        #set the two mandatory attributes for a sprite
        self.image=pygame.Surface([10,10])
        self.image.fill(color)
        self.rect=self.image.get_rect()
 
class Paddle(pygame.sprite.Sprite): #Class for the paddle that the player uses to ensure the ball doesn't go past the bottom of the screen.
    #Constructor
    def __init__(self,color):
        super().__init__() #Call the Parent class constructor
 
        #set the two mandatory attributes for a sprite
        self.image=pygame.Surface([80,20])
        self.image.fill(color)
        self.rect=self.image.get_rect()
 
def paddleCollision(tx1,ty1,tx2,ty2,px1,py1,px2,py2): #Function to detect if the cube ball and paddle have collided
    if px2<tx1 or tx2<px1 or py2<ty1 or ty2<py1: #If the cube ball is the the right, left, bottom or top of the paddle, they haven't collided
        return False
    else:
        return True

ballxspeed,ballyspeed=0,0 #Stores the value of the ball's x and y speeds

def ballBlockCollision(tx1,ty1,tx2,ty2,px1,py1,px2,py2): #Function to detect if the cube ball and block have collided, and if so, whether it was on the side or not
    if px2<tx1 or tx2<px1 or py2<ty1 or ty2<py1: #Checks if the cube ball collided on the side of the block or not
        return False
    elif (px2<=tx1+ballxspeed) or (px1-ballxspeed>=tx2): #Checks if they collided on the sides
        return "side" 
    else: #Otherwise, they collided on the top or bottom.
        return True
 
#Define necessary variables
blockCurrentColour=[0,0,255] #Colour of the blocks
lives=3 #The number of lives that the player has throughout the game.
score=0 #The score over the course of the game
framesPlayed=0 #Tracks the number of frames that has been played. 60 frames=1 second.
 
 
def firstScreen():
    font = pygame.font.Font(None, 35) #Initializes the font style
    goToLevel1=True
    run=True
    while run:
        #event loop
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
                goToLevel1=False
            if event.type==pygame.MOUSEBUTTONDOWN:
                run=False
        #draw section
        screen.fill(white)
        textImage = font.render("The goal of this game is to keep a ball bouncing", True, black)
        screen.blit(textImage,[0,00])
        textImage = font.render("using a paddle and the walls to hit and break all", True, black)
        screen.blit(textImage,[0,50])
        textImage = font.render("the blocks on the screen and move onto the next", True, black)
        screen.blit(textImage,[0,100])
        textImage = font.render("level.", True, black)
        screen.blit(textImage,[0,150])
        textImage = font.render("You have 3 lives, and you lose a life", True, black)
        screen.blit(textImage,[0,250])
        textImage = font.render("if you let a ball touch the bottom of the screen.", True, black)
        screen.blit(textImage,[0,300])
        textImage = font.render("To enter the game, press a mouse button.", True, black)
        screen.blit(textImage,[0,400])
        
        pygame.display.flip()
        clock.tick(60)
    if goToLevel1:
        level1() #If the variable stays true, the game moves onto level 1
    else:
        pygame.quit() #Otherwise, the game ends.
 
 
def level1():
    global lives,score,framesPlayed,ballxspeed,ballyspeed #Makes the variables global so you can update them from inside the function
    remainingMobs=10 #Stores the number of remaining blocks to determine if the level is completed
 
    #Create sprite groups and some block objects
    allSprites=pygame.sprite.Group()
    mobs=pygame.sprite.Group()
    player=Paddle(red)
    allSprites.add(player)
    ball=Ball(black)
    allSprites.add(ball)
    #Sets the ball speed to the initial amounts.
    ballxspeed=3
    ballyspeed=3
    #Create 10 mobs and add them to the sprites' group
    for i in range(10):
        mob=Block(blockCurrentColour)
        blockCurrentColour[2]-=25
        if blockCurrentColour[2]<100:
            blockCurrentColour[2]%=255
        #The above 3 lines ensures adjacent blocks are not the same color, making them easier to tell apart.
        mob.rect.x=200+20*i
        mob.rect.y=50
        #Sets the placement of the blocks.
           
        allSprites.add(mob)
        mobs.add(mob)
     
   
 
    font=pygame.font.Font(None,20) #Initializes the font
 
    #Create variables determining the next screen
    goToLevel2=False
    goToLoseScreen=False
 
    #main game loop
    run=True
    while run:
        #event loop
        for event in pygame.event.get():
            if event.type==pygame.QUIT: 
                run=False
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_p:#Skips the level to go to level 2
                    goToLevel2=True
                    run=False
                if event.key==pygame.K_w or event.key==pygame.K_UP: 
                    ballyspeed-=1 #Makes the ball go more upwards than before.
                    ballyspeed=max(ballyspeed,-20) #Ensures the ball doesn't go past a certain speed.
                if event.key==pygame.K_s or event.key==pygame.K_DOWN:
                    ballyspeed+=1 #Makes the ball go more downwards than before.
                    ballyspeed=min(ballyspeed,20) #Ensures the ball doesn't go past a certain speed.
                if event.key==pygame.K_d or event.key==pygame.K_RIGHT:
                    ballxspeed+=1 #Makes the ball go more rightwards than before.
                    ballxspeed=min(ballxspeed,20) #Ensures the ball doesn't go past a certain speed.
                if event.key==pygame.K_a or event.key==pygame.K_LEFT:
                    ballxspeed-=1 #Makes the ball go mroe leftwards than before.
                    ballxspeed=max(ballxspeed,-20) #Ensures the ball doesn't go past a certain speed.
                   
        #game logic
        framesPlayed+=1
        mouseX=pygame.mouse.get_pos()[0]
        mouseY=height-20 #mouseX and mouseY set the location of the paddle.
        ball.rect.x+=ballxspeed
        ball.rect.y+=ballyspeed
        #Updates the position of the cube ball.
        if ball.rect.right>=width:
            ball.rect.right=width
            ballxspeed*=(-1) #The ball will bounce off the wall
        elif ball.rect.left<=0:
            ball.rect.left=0
            ballxspeed*=(-1) #The ball will bounce off the wall
        if ball.rect.top<=0:
            ball.rect.top=0
            ballyspeed*=(-1)
        if paddleCollision(player.rect.x,player.rect.y,player.rect.right,player.rect.bottom,ball.rect.x,ball.rect.y,ball.rect.right,ball.rect.bottom):
            ballyspeed=-abs(ballyspeed) #The ball will bounce off the paddle.
 
        if ball.rect.y>player.rect.bottom: #The ball is under the paddle.
            lives-=1 #The player will lose a life
            ball.rect.x=0 
            ball.rect.y=0 #The ball respawns.
            ballxspeed=3
            ballyspeed=3
        player.rect.centerx=mouseX
        player.rect.centery=mouseY
        #Updates the position of the paddle.
        mob_hit_list=pygame.sprite.spritecollide(ball,mobs,True)
        for mob in range(len(mob_hit_list)):
            hitMob=mob_hit_list[mob]
            remainingMobs-=1
            score+=1
            if mob==0:
                ballyspeed*=(-1)
                if ballBlockCollision(hitMob.rect.x,hitMob.rect.y,hitMob.rect.right,hitMob.rect.bottom,ball.rect.x,ball.rect.y,ball.rect.right,ball.rect.bottom)=="side":
                    ballxspeed*=(-1)
                hit.play()
        if lives<=0:
            goToLoseScreen=True #The player lost the game
            run=False
        elif remainingMobs==0:
            goToLevel2=True #The player beat the level
            run=False
        #draw section
        screen.fill(lgreen)
               
       
        textImage=font.render("Current Score: %s"%(score),True,black)
        screen.blit(textImage,[0,0])
        textImage=font.render("Current Level: 1",True,black)
        screen.blit(textImage,[225,0])
        textImage=font.render("Current Number of Lives: %s"%(lives),True,black)
        screen.blit(textImage,[400,0])
        textImage=font.render("Time Played: %s seconds"%(framesPlayed//60),True,black)
        screen.blit(textImage,[0,10])
        allSprites.draw(screen)
       
        pygame.display.flip() #Updates the screen
        clock.tick(60) #Ensures the game plays at 60 frames per second.
    if goToLevel2: #If true, the player beat the level and the second level is put up.
        level2()
    elif goToLoseScreen: #If the player loses the level, the lose screen is put up.
        loseScreen()
    else:
        pygame.quit() #If the player exits the game, the game ends.
 
def level2():
    global lives,score,framesPlayed,ballxspeed,ballyspeed #Makes the variables global so you can update them from inside the function
    remainingMobs=50 #Stores the number of remaining blocks to determine if the level is completed
 
    #create sprite groups and some block objects
    allSprites=pygame.sprite.Group()
    mobs=pygame.sprite.Group()
    player=Paddle(red)
    allSprites.add(player)
    ball=Ball(black)
    ball.rect.x=0
    ball.rect.y=400
    allSprites.add(ball)
    #Sets the ball speed to the initial amounts.
    ballxspeed=3
    ballyspeed=3
    #Create 50 mobs and add them to the sprites' group
    for i in range(50):
        mob=Block(blockCurrentColour)
        if i<25:
            mob.rect.x=(i) * 24
            mob.rect.y=30
        elif i<31:
            mob.rect.x=(i-25) * 24
            mob.rect.y=70
        elif i<37:
            mob.rect.x=600-((i-30) * 24)
            mob.rect.y=70
        else:
            mob.rect.x=(i-31)%24 * 24
            mob.rect.y=110
        #The above sets the position of the blocks.
        blockCurrentColour[2]-=25
        if blockCurrentColour[2]<100:
            blockCurrentColour[2]%=255
        #The above ensures each color of block is different from an adjacent block, making them easier to tell apart.
        allSprites.add(mob)
        mobs.add(mob)
     
    font=pygame.font.Font(None,20) #Initializes the font
 
    #Create variables determining the next screen
    goToWinScreen=False
    goToLoseScreen=False
 
    #main game loop
    run=True
    while run:
        #event loop
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
            if event.key==pygame.K_w or event.key==pygame.K_UP: 
                    ballyspeed-=1 #Makes the ball go more upwards than before.
                    ballyspeed=max(ballyspeed,-20) #Ensures the ball doesn't go past a certain speed.
                if event.key==pygame.K_s or event.key==pygame.K_DOWN:
                    ballyspeed+=1 #Makes the ball go more downwards than before.
                    ballyspeed=min(ballyspeed,20) #Ensures the ball doesn't go past a certain speed.
                if event.key==pygame.K_d or event.key==pygame.K_RIGHT:
                    ballxspeed+=1 #Makes the ball go more rightwards than before.
                    ballxspeed=min(ballxspeed,20) #Ensures the ball doesn't go past a certain speed.
                if event.key==pygame.K_a or event.key==pygame.K_LEFT:
                    ballxspeed-=1 #Makes the ball go mroe leftwards than before.
                    ballxspeed=max(ballxspeed,-20) #Ensures the ball doesn't go past a certain speed.
        #game logic
        framesPlayed+=1
        mouseX=pygame.mouse.get_pos()[0]
        mouseY=height-20 #mouseX and mouseY set the location of the paddle.
        ball.rect.x+=ballxspeed
        ball.rect.y+=ballyspeed
        #The two variables above update the position of the cube ball.
        if ball.rect.right>=width:
            ball.rect.right=width
            ballxspeed*=(-1) #The ball will bounce off the wall
        elif ball.rect.left<=0:
            ball.rect.left=0
            ballxspeed*=(-1) #The ball will bounce off the wall
        if ball.rect.top<=0:
            ball.rect.top=0
            ballyspeed*=(-1)
        if paddleCollision(player.rect.x,player.rect.y,player.rect.right,player.rect.bottom,ball.rect.x,ball.rect.y,ball.rect.right,ball.rect.bottom):
            ballyspeed=-abs(ballyspeed) #The ball will bounce off the paddle.
 
        if ball.rect.y>player.rect.bottom: #The ball is under the paddle.
            lives-=1 #The player will lose a life
            ball.rect.x=0 
            ball.rect.y=0 #The ball respawns.
            ballxspeed=3
            ballyspeed=3
        player.rect.centerx=mouseX
        player.rect.centery=mouseY
        #Updates the position of the paddle.
        mob_hit_list=pygame.sprite.spritecollide(ball,mobs,True)
        for mob in range(len(mob_hit_list)):
            hitMob=mob_hit_list[mob]
            remainingMobs-=1
            score+=1
            if mob==0:
                ballyspeed*=(-1) #The ball bounces off the block.
                if ballBlockCollision(hitMob.rect.x,hitMob.rect.y,hitMob.rect.right,hitMob.rect.bottom,ball.rect.x,ball.rect.y,ball.rect.right,ball.rect.bottom)=="side":
                    ballxspeed*=(-1) #The cube ball hit the side of the block, so it bounces off.
                hit.play() #Plays the sound when a block gets hit.
 
        if lives==0:
            goToLoseScreen=True #The player lost the game.
            run=False
        elif remainingMobs==0:
            goToWinScreen=True #The player beat the level.
            run=False
        #draw section
        screen.fill(lgreen)
        textImage=font.render("Current Score: %s"%(score),True,black)
        screen.blit(textImage,[0,0])
        textImage=font.render("Current Level: 2",True,black)
        screen.blit(textImage,[225,0])
        textImage=font.render("Current Number of Lives: %s"%(lives),True,black)
        screen.blit(textImage,[400,0])
        textImage=font.render("Time Played: %s seconds"%(framesPlayed//60),True,black)
        screen.blit(textImage,[0,10])
        allSprites.draw(screen)
     
        pygame.display.flip() #Updates the screen.
        clock.tick(60) #Ensures the game plays at 60 frames per second.
    if goToWinScreen:
        winScreen() #The player beat all the levels and won the game, so the win screen is brought up.
    elif goToLoseScreen:
        loseScreen() #The player lost the level, so the lose screen is brought up.
    else:
        pygame.quit() #The player exited the game, so the game ends.
 
def winScreen():
    global lives
    global score
    global framesPlayed
    font = pygame.font.Font(None, 35) #The font is initialized
    goToLevel1=True
    run=True
    while run:
        #event loop
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
                goToLevel1False
            if event.type==pygame.MOUSEBUTTONDOWN:
                run=False
        #draw section
        screen.fill(green)
        textImage = font.render("YOU HAVE WON THE GAME! Final Score: %s" %(score), True, black)
        screen.blit(textImage,[50,200])
        textImage = font.render("Final Time: %s seconds" %(framesPlayed//60), True, black)
        screen.blit(textImage,[175,300])
        textImage = font.render("To replay the game, press a mouse button.", True, black)
        screen.blit(textImage,[50,400])
        pygame.display.flip() #Updates the screen.
        clock.tick(60) #Ensures the game plays at 60 frames per second.
    if goToLevel1:
        lives=3
        score=0
        level1() #The game is restarted.
    else:
        pygame.quit() #The player exited the game, so the game ends.
 
def loseScreen():
    global lives
    global score
    global framesPlayed
    font = pygame.font.Font(None, 35)
    goToLevel1=True
    run=True
    while run:
        #event loop
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
                goToLevel1=False
            if event.type==pygame.MOUSEBUTTONDOWN:
                run=False
        #draw screen
        screen.fill(red)
        textImage = font.render("YOU HAVE LOST THE GAME! Final Score: %s" %(score), True, black)
        screen.blit(textImage,[50,200])
        textImage = font.render("Final Time: %s seconds" %(framesPlayed//60), True, black)
        screen.blit(textImage,[175,300])
        textImage = font.render("To replay the game, press a mouse button.", True, black)
        screen.blit(textImage,[50,400])
        pygame.display.flip() #Updates the screen.
        clock.tick(60) #Ensures the game plays at 60 frames per second.
    if goToLevel1:
        lives=3
        score=0
        framesPlayed=0
        level1() #The game is restarted
    else:
        pygame.quit() #The player exited the game, so the game ends.
firstScreen() #The player starts at the initial screen with the title of the game and the instructions.
