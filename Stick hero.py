import pygame
import math
import os
import os.path
from random import randint

#_____________________________________________[GAME_ENGINE CLASSES]_________________________________________#

class Color(object):
    '''A color set.'''
    def __init__(self, custom1 = (0,0,0), custom2 = (0,0,0), custom3 = (0,0,0)):

        self.black = (0,0,0)
        self.white   = (255,255,255)
        self.red     = (255,0,0)
        self.lime    = (0,255,0)
        self.blue    = (0,0,255)
        self.yellow  = (255,255,0)
        self.cyan    = (0,255,255)
        self.magenta = (255,0,255)
        self.silver  = (192,192,192)
        self.gray    = (128,128,128)
        self.maroon  = (128,0,0)
        self.olive   = (128,128,0)
        self.green   = (0,128,0)
        self.purple  = (128,0,128)
        self.teal    = (0,128,128)
        self.navy    = (0,0,128)
        self.custom1 = custom1
        self.custom2 = custom2
        self.custom3 = custom3
color = Color()                                             # Give a name to the module's prefix

class Screen_info(object):
    '''Information on the screen / window.
    Attributes:
        x: Resolution in px.
        y: Resolution in px.
        fps: meaning frame per second, usually 60fps.
        fullscreen: True or False, use the game in fullscreen or not.
        pg: Used by pygame to refer game's window.
    '''
    def __init__(self, x = 0, y = 0, fps = 0, fullscreen = False):
        self.x = x
        self.y = y
        self.fps = fps
        self.fullscreen = fullscreen   
screen = Screen_info()                                      # Give a name to the module's prefix

class Game_info(object):
    '''A menu with customizable options
    Attributes:
        title: Title of the game 
        author: Author / creator of the game.
        year: When the game was created.
        month: When the game was created.
        day: When the game was created.
    '''
    def __init__(self, title = "", author = "", year = 1970, month = 1, day = 1):
        self.title = title
        self.author = author
        self.year = year
        self.month = month
        self.day = day
game_info = Game_info()                                      # Give a name to the module's prefix



#________________________________________[GAME_ENGINE CONFIGURATION]________________________________________#


# [Game informations] #

game_info.title = "Stick HERO"
game_info.author = "DrMint"
game_info.year = 2017
game_info.month = 11
game_info.day = 26



# [Window options]

screen.x, screen.y = 1500, 840
screen.fps = 60
screen.fullscreen = False



# [Pythongame related commands] | Shouldn't have to change them

screen.pg = pygame.display.set_mode((screen.x,screen.y))        # Create a window with a specific size.
pygame.display.set_icon(pygame.image.load('./image/icon.png'))  # Set an icon for the Game (by default : './image/icon.png')
pygame.mixer.pre_init(44100, -16, 1, 512)                       # Custom Audio mixer, without it audio has lattency
pygame.init()                                                   # Allow to use pygame's modules.
pygame.display.set_caption(game_info.title)                     # Change window title (Game title by default)
clock = pygame.time.Clock()                                     # Used by pygame to manage how fast the screen updates


# [Import sound] | Usage: sound['name'] --> pygame.mixer.Sound() #

sound_directory = "./sound/"
sound = {
    'hit_wall'   : pygame.mixer.Sound("./sound/hit_wall.wav"),
    'hit_paddle' : pygame.mixer.Sound("./sound/hit_paddle.wav"),
    'win_sound'  : pygame.mixer.Sound("./sound/win.wav"),
}



# [Import font] | Usage: font['name'] --> pygame.font.Font() #


font_directory = "./font/"                                  # By default, font_directory = "./font/"
font = {

    'title'   : pygame.font.Font(font_directory + "game_font.ttf", min(screen.x, screen.y) // 4  ),
    'h1'      : pygame.font.Font(font_directory + "game_font.ttf", min(screen.x, screen.y) // 15 ),
    'h2'      : pygame.font.Font(font_directory + "game_font.ttf", min(screen.x, screen.y) // 25 ),
    'score'   : pygame.font.Font(font_directory + "game_font.ttf", min(screen.x, screen.y) // 5 ),
    'hscore'   : pygame.font.Font(font_directory + "game_font.ttf", min(screen.x, screen.y) // 15 ),
}


# [Import images]

background = []
for i in range(9):
    background += [pygame.image.load('./image/parallax' + str(i) + '.png').convert_alpha()]

chara = []
for i in range(13):
    chara += [pygame.image.load('./image/chr' + str(i) + '.png').convert_alpha()]


#________________________________________[GAME FONCTIONS]________________________________________#

def test_if_in_range():

    global ladder_lenght, ladder_width, next_plateforme_x, next_plateforme_width, current_plateforme_x, current_plateforme_width
    
    ladder_end_pos = current_plateforme_x - ladder_width + current_plateforme_width + ladder_lenght

    if ladder_end_pos >= next_plateforme_x and ladder_end_pos <= next_plateforme_x + next_plateforme_width:
        return True
    else:
        return False


def test_if_in_perfect():

    global ladder_lenght, ladder_width, next_plateforme_x, next_plateforme_width, current_plateforme_x, current_plateforme_width
    
    ladder_end_pos = current_plateforme_x - ladder_width + current_plateforme_width + ladder_lenght

    if ladder_end_pos >= next_plateforme_x + (next_plateforme_width - perfect_width) / 2 and ladder_end_pos <= next_plateforme_x + (next_plateforme_width + perfect_width) / 2:
        return True
    else:
        return False

def parralax():

    global background_surface, background, bx
    
    for i in range(8):
        coef = (8 - i)**2 // 4 + 1
        background_surface.blit(background[i], (-bx / coef + 3500 * ((bx / coef) // 3500),0))
        background_surface.blit(background[i], (-bx / coef + 3500 * ((bx / coef) // 3500 + 1),0))

    return

#________________________________________[GAME CONFIGURATION]________________________________________#

current_plateforme_x = 0
next_plateforme_x = 0
plateforme_height = 0.3 * screen.y

if screen.x > screen.y:
    default_plateforme_width = screen.x * 0.05
else:
    default_plateforme_width = screen.x * 0.15
    
current_plateforme_width = default_plateforme_width

if screen.x > screen.y:
    generator_plateforme_width = [default_plateforme_width, 0.20 * screen.x]
else:
    generator_plateforme_width = [default_plateforme_width, 0.40 * screen.x]

generator_borders = 0.05 * screen.x
generator_plateforme_pos = [current_plateforme_x + current_plateforme_width + generator_borders, min(screen.x - current_plateforme_x - current_plateforme_width, screen.y - plateforme_height)]



ladder_width = 8
grow_speed = 8
#transition_speed = 5
perfect_width = 0.2 * default_plateforme_width


#________________________________________________[GAME]______________________________________________#

ladder_lenght = 0


background_surface = pygame.Surface((screen.x, screen.y))

for i in range(8):
    background_surface.blit(background[i], (0,0))


done = False
generate = True
grow = False
transition = False
smooth_transition_speed = 0
smooth_angle_speed = 0
ladder_transition = False
falling_ladder = False
angle_ladder = math.pi / 2
score = 0
combo = 0
hscore = 0
color_score = color.black
bx = 0
save_pos = 0

running_man = False
running_begin = current_plateforme_x + current_plateforme_width - ladder_width * 2 - 75
running_pos = running_begin
running_frame = 0
running_end = 0
running_step = 200 / 13
chara_surface = chara[running_frame]

plateforme_appearing = False
next_plateforme_height = 0

while not done:
    if generate == True:
        next_plateforme_x = randint(generator_plateforme_pos[0], generator_plateforme_pos[1])
        next_plateforme_width = randint(generator_plateforme_width[0], generator_plateforme_width[1])
        generate = False
        plateforme_appearing = True
        next_plateforme_height = 0

    if plateforme_appearing == True:
        next_plateforme_height += (plateforme_height - next_plateforme_height) // 5 + 1
        if next_plateforme_height == plateforme_height:
            plateforme_appearing = False
        
    
    # --- Quit game if cross clicked
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            
    # --- Detect Player input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and transition == False and ladder_lenght < screen.y - plateforme_height and ladder_transition == False and falling_ladder == False:
        if grow == False:
            grow = True
        else:
            ladder_lenght += grow_speed
    else:
        if grow == True:
            grow = False
            ladder_transition = True
            
    if ladder_transition == True:
        smooth_angle_speed += 0.5 
        if angle_ladder - (math.pi / 1000 * smooth_angle_speed) < 0:
            angle_ladder = 0
            ladder_transition = False
            

            if test_if_in_range() == True:
                running_man = True
                transition = True
                running_end = next_plateforme_x + next_plateforme_width - ladder_width * 2 - 75
                save_pos = next_plateforme_x
                smooth_angle_speed = 0

                score += 1
                if test_if_in_perfect() == True:
                    combo += 1
                    score += combo
                    color_score = color.red
                else:
                    combo = 0
                    color_score = color.black
                if score > hscore:hscore = score

            else:
                color_score = color.black
                falling_ladder = True
                combo = 0
                score = 0
                parralax()
        else:
            angle_ladder -= math.pi / 1000 * smooth_angle_speed

    if running_man == True:
        if running_pos + running_step < running_end:
            chara_surface = chara[running_frame % 12 + 1]
            running_frame += 1
            running_pos += running_step
        else:
            running_pos = running_end
            running_frame = 0
            chara_surface = chara[0]
            running_man = False


    if falling_ladder == True:
        if angle_ladder < - math.pi / 2:
            falling_ladder = False
            smooth_angle_speed = 0
            ladder_lenght = 0
            angle_ladder = math.pi / 2
        else:
            smooth_angle_speed += 0.5
            angle_ladder -= math.pi / 1000 * smooth_angle_speed

        
    if transition == True:
        if next_plateforme_x > - (next_plateforme_width - default_plateforme_width):    

            t = (save_pos - next_plateforme_x) / (abs(-(next_plateforme_width - default_plateforme_width)) + save_pos)
            
            smooth_transition_speed = - (abs(-(next_plateforme_width - default_plateforme_width)) + save_pos) / 3 * (-1 + t) * t + 0.2
            
            font['score'] = pygame.font.Font(font_directory + "game_font.ttf", min(screen.x, screen.y) // int((- 10 * (-1 + (t/2)) * (t/2) + 0.1 + 2)))
            current_plateforme_x -= smooth_transition_speed
            next_plateforme_x -= smooth_transition_speed
            running_pos -= smooth_transition_speed
            running_end -= smooth_transition_speed
            bx += smooth_transition_speed / 2
        else:
            transition = False
            current_plateforme_x = 0
            current_plateforme_width = default_plateforme_width
            smooth_transition_speed = 0
            if running_man == False: running_pos = running_begin
            generate = True
            ladder_lenght = 0
            angle_ladder = math.pi / 2
            
        

    # --- Game code

    # --- Drawing code

    
    screen.pg.blit(background_surface, ((0,0)))
    
    if ladder_lenght > 0:

        if transition == True:
            parralax()

        if transition == True or falling_ladder == True:   
            score_surface = font['score'].render(str(score), False, color_score)
            hscore_surface = font['hscore'].render('Best  ' + str(hscore), False, color.black)
            background_surface.blit(score_surface, ((screen.x - score_surface.get_width()) / 2 + 10, screen.y / 10))
            background_surface.blit(hscore_surface, ((screen.x - hscore_surface.get_width()) / 2, screen.y / 20))
        
        point1 = (current_plateforme_x + current_plateforme_width - ladder_width, screen.y - plateforme_height - math.cos(angle_ladder) * ladder_width * 0.6)
        point2 = (current_plateforme_x + current_plateforme_width - ladder_width + ladder_lenght * math.cos(angle_ladder), screen.y - plateforme_height - (ladder_lenght) * math.sin(angle_ladder)- math.cos(angle_ladder) * ladder_width * 0.6)

        pygame.draw.line(screen.pg, color.black, point1, point2, int(ladder_width * 1.5))
    
    pygame.draw.rect(screen.pg, color.black, [current_plateforme_x, screen.y - plateforme_height, current_plateforme_width, plateforme_height])
    pygame.draw.rect(screen.pg, color.black, [next_plateforme_x, screen.y - next_plateforme_height, next_plateforme_width, next_plateforme_height])
    pygame.draw.rect(screen.pg, color.red, [next_plateforme_x + (next_plateforme_width - perfect_width) / 2, screen.y - next_plateforme_height, perfect_width, next_plateforme_height * 0.01])

    screen.pg.blit(chara_surface, ((running_pos, screen.y - plateforme_height - 97)))

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()        

    # --- Limit to 60 frames per second
    clock.tick(screen.fps)



# Close the window and quit.
pygame.quit()
