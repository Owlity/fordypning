import pygame
import math
import sys

# Initialize pygame
pygame.init()


# Clock
clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 36)


# Screen
WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("John Persona 6.2: The Awakening of Persona 2 Rewind Redux Deluxe 8")


BG_COLOR = (30, 30, 30)
BUTTON_COLOR = (70, 130, 180)
HOVER_COLOR = (100, 170, 220)
TEXT_COLOR = (255, 255, 255)

# Font
font = pygame.font.SysFont('serif', 36)

# Button class
class Button:
    def __init__(self, text, x, y, w, h):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)

    def draw(self, surface):
        color = HOVER_COLOR if self.rect.collidepoint(pygame.mouse.get_pos()) else BUTTON_COLOR
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2)

        text_surf = font.render(self.text, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def clicked(self, event):
        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )

# Create buttons
buttons = [
    Button("Play", 200, 120, 200, 50),
    Button("Options", 200, 190, 200, 50),
    Button("Quit", 200, 260, 200, 50)
]

TARGET_COUNT = 0

# Colors
WHITE = (240, 240, 240)
BLUE = (66, 185, 245)
DARK = (30, 30, 30)
GRAY = (128, 128, 128)
GREEN = (0, 128, 0)
GREEND = (0, 80, 0)
Character = (245, 132, 66)
hand = (0, 0, 0, 0.1)
BROWN = (125, 54, 0)
# Square (player)
size = 40
x = WIDTH // 2 - size // 2
y = HEIGHT - size - 50

jump_buffer = 0
jump_buffer_time = 10
click_buffer = 0
click_buffer_time = 10
y_velocity = 0
gravity = 0.8
jump_strength = -17
on_ground = False
double_jump = False
# Ground
ground_y = HEIGHT - 50
wave = 0


player_rect = pygame.Rect(x, y, size, size)
targets = [ #Array
        pygame.Rect(20, 750, 26, 26),
        pygame.Rect(600, 700, 26, 26),
        pygame.Rect(1200, 750, 26, 26),
        pygame.Rect(1720, 480, 26, 26),
        pygame.Rect(1700, 350, 26, 26),
    ]



# Sizes

hand_width = 40
hand_height = 30


# Punch variables
punching = False
hand_offset = 0
hand_speed = 15
max_reach = 170
hand_x_distance = 0
hand_y_distance = 0
# New dash that use hand physics
dash = False
dash_distance = 250
dash_speed = 13
dash_countdown = 0
dash_cooldown = 5
dash_x_distance = 0
dash_y_distance = 0

# sprites
sword = pygame.image.load("sprites\sword.png")
sword = pygame.image.load("sprites\sword.png")

gamescore = 0
# sprites
#image = pygame.image.load('sprite/target.piskel')

# Game loop
while True:

    text = font.render(str(gamescore) + " targets", True, WHITE)
 
    textrect = text.get_rect()

    if jump_buffer > 0:
        jump_buffer -= 1

    if jump_buffer > 0 and on_ground:
        y_velocity = jump_strength
        on_ground = False
        double_jump = True
        jump_buffer = 0

    elif jump_buffer > 0 and double_jump:
        y_velocity = jump_strength
        on_ground = False
        double_jump = False
        jump_buffer = 0

    if click_buffer > 0:
        click_buffer -= 1

    if click_buffer > 0 and not punching:
        mousePos = pygame.mouse.get_pos()
        #gets the position of the mouse
        adjecent = mousePos[0] - x 
        opposite = mousePos[1] - y
        #gets the vertical and horizontal axis difference via x2-x1 and y2-y1
        #print(mousePos, adjecent, opposite)
        wave =  math.atan2(opposite, adjecent ) 
        #gets the angle of the punch through right angle trigenometry
        #print(wave)
        max_height = (math.tan(wave))*max_reach
        #uses trig to find out the height with the angle and lenght
        (math.tan(wave))*max_reach == max_height
        print(max_height)
        punching = True
        click_buffer = 0


    for event in pygame.event.get():
       
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
          
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w or event.key == pygame.K_SPACE: 
                jump_buffer = jump_buffer_time
              
            if event.key == pygame.K_s and on_ground == False:
                y_velocity += 15.5   # extra downward force
   

    #restart button
    # if event.type == pygame.KEYDOWN:
    #    if event.key == pygame.K_r:
    #       pygame.QUIT
    #      pygame.init()
 
 


    #trig
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and not punching:
                click_buffer = click_buffer_time 

                
    swordscale = pygame.transform.rotate(sword,(-60 * wave)-45)
    swordscale = pygame.transform.scale (swordscale, (64, 64))
    # Punch animation
    if punching:
        
        hand_offset += hand_speed

        hand_x_distance = (math.cos(wave)-0.15) * hand_offset
        hand_y_distance = (math.sin(wave)-0.25) * hand_offset
        if hand_offset >= max_reach:
            hand_speed = -hand_speed

        if hand_offset <= 0:
            hand_offset = 0
            hand_speed = abs(hand_speed)
            punching = False

    # Hand (punching part)
    hand_x = x + size // 2 + hand_x_distance
    hand_y = y + size // 2 + hand_y_distance

  
    

    if dash_countdown > 0:
    
        dash_countdown-=1

    # Grapple
    #if event.type == pygame.MOUSEBUTTONDOWN:
    #     if event.button == 3:
    #        if dash_countdown <= 0:
     #           dash_countdown = dash_cooldown*60
     #           print("right")

    
    
   
       


    # Apply gravity
    y_velocity += gravity
    y += y_velocity

    # Collision with ground
    if y + size >= ground_y:
        y = ground_y - size
        y_velocity = 0
        on_ground = True
        double_jump = False

    # Draw
    screen.fill(GREEND) 

    # Ground
    pygame.draw.rect(screen, GREEN, (0, ground_y, WIDTH, HEIGHT - ground_y))
    

    
    platforms = [ #Array
        pygame.Rect(20, 800, 400, 30),
        pygame.Rect(600, 750, 200, 30),
        pygame.Rect(1200, 800, 400, 30),
        pygame.Rect(1600, 400, 250, 30),
        pygame.Rect(1600, 400, 30, 250),
    ]
    for platform in platforms:
        if y + size >= platform.top and y+size <= platform.bottom:
            if x < platform.right and x > platform.left:
                y = platform.top - size
                y_velocity = 0
                on_ground = True
                double_jump = False
        pygame.draw.rect(screen, BROWN, platform)

    # Square
    pygame.draw.rect(screen, Character, (x, y, size, size))

    # Square settings

    speed = 5



    for target in targets:
        pygame.draw.rect(screen, DARK, target)
        #collide = pygame.Rect.colliderect(hand, target)  
    # if target.colliderect(hand):
    #    pygame.draw.rect(screen, Character, target)
    #ø    print ("collide")
    # Key presses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        x -= speed
    if keys[pygame.K_d]:
        x += speed




    # Keep square on screen
    square_x = max(0, min(WIDTH - size, x))
    square_y = max(0, min(HEIGHT - size, y))

  
    ticks=pygame.time.get_ticks()
    millis=ticks%1000
    seconds=int(ticks/1000 % 60)
    minutes=int(ticks/60000 % 24)
    out='{minutes:02d}:{seconds:02d}:{millis}'.format(minutes=minutes, millis=millis, seconds=seconds)
    print(out)
   
    screen.blit(swordscale, (hand_x - 10, hand_y -20 ))
    for target in targets:
        handRect = pygame.Rect(hand_x, hand_y, hand_width, hand_height)
        if target.colliderect(handRect):
            gamescore += 1
            print (gamescore)
            targets.pop(targets.index(target))

    text2 = font.render(str(out), True, WHITE)
    textrect2 = text2.get_rect()
    textrect2.center = (WIDTH/2, 50)
    screen.blit(text, textrect)
    screen.blit(text2, textrect2)  
    pygame.display.update()
    pygame.display.flip()

    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            pygame.quit()
            quit()

    clock.tick(60)
 

   
    







