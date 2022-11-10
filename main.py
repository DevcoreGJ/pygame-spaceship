import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First Game!") #Title of game window

#---------------------------CONSTANT VARIABLES DEFINED-----------------------------

WHITE = (255,255,255) #SEE FILL
BLACK = (000,000,000) #BORDER COLOUR, see pygame.draw.rect...
RED = (255,000,000)
YELLOW = (255,255,000)

FPS = 60 #FRAME LOCK SEE TICK

VEL = 5 #VELOCITY FOR PLAYER MOVEMENT, SEE KEYBINDINGS

BULLETS_VEL = 7 #deliberately faster than character, see BULLET SHOT MECHANIC

MAX_BULLETS = 3 #See bullet shot mechanics

SPACESHIP_WIDTH, SPACESHIP_HEIGHT=55, 40 #SEE RED &/OR YELLOW
#CREATING NEW CUSTOM EVENT
#NUMBERS INDICATE THE EVENT CODE
YELLOW_HIT = pygame.USEREVENT + 1 #EVENT 1, WHEN YELLOW GETS HIT
RED_HIT = pygame.USEREVENT + 2 #EVENT 2, WHEN RED GETS HIT  

#WIDTH = 900 / 2 = 450 IN MIDDLE OF SCREEN - 10, 5 FROM BOTH SIDES
BORDER = pygame.Rect(WIDTH//2, 0, 10, HEIGHT) #see pygame.draw.rect, // for int divide, no floats

#-------------------------------------SOUND FX-------------------------------------
BULLETS_HIT_SOUND = pygame.mixer.Sound(
    os.path.join('Assets', 'Grenade+1.mp3'))
BULLETS_FIRE_SOUND = pygame.mixer.Sound(
    os.path.join('Assets', 'Gun+Silencer.mp3'))
#-------------------------------------FONT-----------------------------------------

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)
#----------------------------------------------------------------------------------

#------------------------------------LOAD IN RAW IMAGE-----------------------------
YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_yellow.png'))#locates spaceship, see def draw_window

RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_red.png'))#locates spaceship, see def draw_window

SPACE_IMAGE = pygame.image.load(
    os.path.join('Assets', 'space.png'))
#----------------------------------------------------------------------------------

#-----------------------------------Used Yellow/Red spaceship assett-------------------
#YELLOW/Red_SPACESHIP_IMAGE is too big and needs to be resized before drawn in.
#Define YELLOW/RED_SPACESHIP as YELLOW/RED_SPACESHIP_IMAGE and transform initially its scale
#You can use the constant variables above as then the height and width is already set
#Tack on the the rotate transformation ahead of the already scaled transformation
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH,SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH,SPACESHIP_HEIGHT)), 270)

SPACE = pygame.transform.scale(
    SPACE_IMAGE, (WIDTH, HEIGHT))
#transform contains rotate, scale and location

#replaced with draw_window(args):
#def draw_window(): #method to print to screen what is loaded in above.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
#works in stack order. What is drawn first will be underneath the next object.
    #object 1 background colour
    WIN.blit(SPACE, (0, 0))#bg now a png of space declared above
    #
    #WIN.fill(WHITE) #bg fill = const var white
    # OLD BLANK/WHITE BACKGROUND COLOUR
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^   
#REPLACED BY REDUCED SIZED IMAGE
    #WIN.blit(YELLOW_SPACESHIP_IMAGE, (300, 100)) #draw spaceship at these coordinates see 
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#replaced with yellow.x...
#WIN.blit(YELLOW_SPACESHIP, (300, 100))
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    pygame.draw.rect(WIN, BLACK, BORDER) # see constant black

#font
    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
    # dynamically place the health counter on screen
    WIN.blit(red_health_text,(WIDTH -  red_health_text.get_width() - 10, - 10))
    WIN.blit(yellow_health_text, (10, + 10))  
#object 2 yellow spaceship image asset    
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y)) #see def main yellow rectangle

    #replaced with red.x...
    #WIN.blit(RED_SPACESHIP, (700, 100))
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#object 3 red spaceship image asset
    WIN.blit(RED_SPACESHIP, (red.x, red.y)) #see def main red rectangle    

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update() #forces objects to update

def yellow_handle_movement(keys_pressed, yellow):
#---------------------------------(left) yellow spaceship keybindings----------------   
    #assign WASD keys for (left) spaceship yellow
    # not the best practice but allows simulataneous key entry    
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:        #key a = LEFT
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x:        #key D = RIGHT
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0 :       #key a = UP
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 15:        #key a = DOWN
        yellow.y += VEL
#----------------------------------------------------------------------------------------

def red_handle_movement(keys_pressed, red):
    #--------------------------------(right) red spaceship keybindings-------------------
    #assign arrows for right spaceship red
    # not the best practice but allows simulataneous key entry    
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:   #key LEFT = LEFT
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL  + red.width < WIDTH:       #key RIGHT = RIGHT
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:                           #key UP = UP
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 15:  #key DOWN = DOW
        red.y += VEL

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets: # for every bullet fired from the yellow bullets
        bullet.x += BULLETS_VEL # follow the bullet velocity along the positive x-axis
        if red.colliderect(bullet): # to check if (yellow) has had direct collision with the bullet
        
        #CONSTANT CREATED AT TOP OF DOCUMENT FOR AN EVENT TO DETERMINE WHAT HAPPENS WHEN HIT    
            pygame.event.post(pygame.event.Event(RED_HIT))   
            yellow_bullets.remove(bullet)#remove the bullet on collision
        elif bullet.x >  WIDTH:
            yellow_bullets.remove(bullet)
    for bullet in red_bullets: # for every bullet fired from the yellow bullets
        bullet.x -= BULLETS_VEL # follow the bullet velocity along the positive x-axis
        if yellow.colliderect(bullet): # to check if (yellow) has had direct collision with the bullet
        
        #CONSTANT CREATED AT TOP OF DOCUMENT FOR AN EVENT TO DETERMINE WHAT HAPPENS WHEN HIT    
            pygame.event.post(pygame.event.Event(YELLOW_HIT))   
            red_bullets.remove(bullet)#remove the bullet on collision
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()/2, HEIGHT//2 - draw_text.get_height()//2))

    pygame.display.update()
    pygame.time.delay(5000)

#-----------------------------------------------------------------------------------------
def main():
    #make it possible to replace draw_window YELLOW_SPACESHIP, RED_SPACESHIP 
    #coordinate args with yellow, red (var names below).x and .y
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT) # define player character
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT) # define player character
    
    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)#limits our framerate
        #constant FPS defined as 60
        #60 is the average refresh rate of standard monitors.
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #  in top right of window
                run = False
                pygame.quit()

            #each player has a limited number of bullets
            #strategic not spammy

            #new key pressed method
#------------------------------------------#BULLET SHOT MECHNIC-----------------------------------
            #keybindings
            if event.type == pygame.KEYDOWN: # alt to if keys_pressed[pygame.<insertkeyhere>]
                #YELLOW BULLET
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS: #click left control for yellow ship to shoot
                    #maximum 3 bullets can be on the screen at one time.
                    #PHYSICS
                    bullet = pygame.Rect(
                        yellow.x + yellow.width, yellow.y + yellow.height//2 -2, 10, 5)#yellow bullet physics. must have // for int divide
                    yellow_bullets.append(bullet)#yellow bullet array starts at zero each shot append 1 bullet
                    BULLETS_FIRE_SOUND.play()

                #RED BULLET PHYSICS
                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:#click right control for red ship to shoot
                    #maximum 3 bullets can be on the screen at one time.
                    #PHYSICS
                    bullet  = pygame.Rect(
                        red.x, red.y + red.height//2 - 2, 10, 5)#red bullet physics, must have // for int divide
                    red_bullets.append(bullet)#red bullet array starts at zero each shot append 1 bullet
                    BULLETS_FIRE_SOUND.play()
            
            if event.type == RED_HIT:
                red_health-= 1
                BULLETS_HIT_SOUND.play()
            
            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLETS_HIT_SOUND.play()
        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Wins!"
        
        if yellow_health <=0:
            winner_text = "Red Wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break

#demo of player yellow and reds bullet button functionality
        #print(red_bullets, yellow_bullets)
# when either left or right ctrl is clicked the console prints
# out a response

#---------------------------------------------------------------------------------------------
#----------------------------dummy code for example of movement-------------------------------                
        #red.x += 1 
        #adds 1 to red x coordinate
        #bound to clock.tick which limits our framerate.
        #red will move 60 pixels per second which is what we have locked
        #frames per second at.
#-----------------------------call event handlers-----------------------------------------------
        keys_pressed = pygame.key.get_pressed() #during while 60 times a second, which keys 
        #pushed down output response, recognises long holds
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)
        
        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)

    main()        
#-------------------------------------------------------------------------------------------
if __name__ == "__main__": #main file run
    main() #name of file

#--------------------------Chris' pro feedback----------------------------------------------
# Chris' advice if there is something you want updating fairly regularly put it on 
# a timer, updating the timer fairy regularly at something at for example 0.1 seconds.
#ticks can:
#pull down your framerate under load.
#can inadvertantly bring allow access to entire class

#timers are better because they can be controlled and are a deliberate object
#you can kill off or have simulataneous timers that can be controlled.

# look in to do once, or pygame equiv
# setting framerate on timer at "begin play"
#------------------------------------------------------------------------------------
