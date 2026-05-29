import pygame
import math
import sys

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 1880, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Square")

# Clock
clock = pygame.time.Clock()


# Colors
WHITE = (240, 240, 240)
BLUE = (0, 150, 255)
DARK = (30, 30, 30)
GRAY = (128, 128, 128)
GREEN = (0, 128, 0)
Character = (245, 132, 66)
HAND_COLOR = (0, 150, 200)

# Square (player)
size = 40
x = WIDTH // 2 - size // 2
y = HEIGHT - size - 50

# hand Sizes
hand_width = 20
hand_height = 10

y_velocity = 0
gravity = 0.8
jump_strength = -17
on_ground = False
double_jump = False
# Ground
ground_y = HEIGHT - 50
wave = 0

# Punch variables
punching = False
hand_offset = 0
hand_speed = 13
max_reach = 170
hand_x_distance = 0
hand_y_distance = 0



# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and on_ground:
                y_velocity = jump_strength
                on_ground = False
                double_jump = True
            elif  event.key == pygame.K_w and double_jump:
                y_velocity = jump_strength
                on_ground = False
                double_jump = False
            if event.key == pygame.K_s and on_ground == False:
                y_velocity += 10.5   # extra downward force
   
        # Apply gravity
    y_velocity += gravity
    y += y_velocity

    # Collision with ground
    if y + size >= ground_y:
        y = ground_y - size
        y_velocity = 0
        on_ground = True
        double_jump = False


    #trig
    if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1. and not punching:
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
    hand_x_distance = math.cos(wave) * hand_offset
    hand_y_distance = math.sin(wave) * hand_offset
            
    # Punch animation
    if punching:
        
        hand_offset += hand_speed

        if hand_offset >= max_reach:
            hand_speed = -hand_speed

        if hand_offset <= 0:
            hand_offset = 0
            hand_speed = abs(hand_speed)
            punching = False
    # Hand (punching part)
    hand_x = x + size // 2 + hand_x_distance
    hand_y = y + size // 2 + hand_y_distance

    # Draw
    screen.fill(BLUE)

    # Ground
    pygame.draw.rect(screen, GREEN, (0, ground_y, WIDTH, HEIGHT - ground_y))

    # Square
    pygame.draw.rect(screen, Character, (x, y, size, size))

    # Square settings

    speed = 6


    # Key presses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        x -= speed
    if keys[pygame.K_d]:
        x += speed
   

    # Keep square on screen
    square_x = max(0, min(WIDTH - size, x))
    square_y = max(0, min(HEIGHT - size, y))

    pygame.draw.rect(
        screen,
        Character,
        (hand_x, hand_y, hand_width, hand_height)
    )

    pygame.display.flip()
    clock.tick(60)
   