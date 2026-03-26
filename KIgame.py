import pygame
import math
import sys

pygame.init()
clock = pygame.time.Clock()

WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gravity Square")

BLUE       = (66, 185, 245)
GREEN      = (0, 128, 0)
Character  = (245, 132, 66)
ROPE_COLOR = (180, 140, 80)

font = pygame.font.SysFont(None, 36)

# ── Player ────────────────────────────────────────────────────────────────────
size = 40
x = float(WIDTH  // 2 - size // 2)
y = float(HEIGHT - size - 50)
x_velocity  = 0.0
y_velocity  = 0.0
gravity     = 0.8
jump_strength = -17
on_ground   = False
double_jump = False
speed       = 5
MAX_VEL     = 28.0          # terminal velocity cap so it doesn't go crazy

ground_y = HEIGHT - 50

# ── Jump buffer ───────────────────────────────────────────────────────────────
jump_buffer      = 0
jump_buffer_time = 10

# ── Punch ─────────────────────────────────────────────────────────────────────
click_buffer      = 0
click_buffer_time = 10
punching        = False
hand_offset     = 0
hand_speed      = 15
max_reach       = 170
wave            = 0.0
hand_x_distance = 0.0
hand_y_distance = 0.0
hand_width  = 20
hand_height = 10

# ── Grapple ───────────────────────────────────────────────────────────────────
grappling        = False
grapple_target_x = 0.0
grapple_target_y = 0.0
grapple_wave     = 0.0

GRAPPLE_REACH      = 500        # max hypotenuse reach
GRAPPLE_PULL       = 2.2        # acceleration added toward target per frame
GRAPPLE_ARRIVE_DIST = 40        # how close before auto-release
GRAPPLE_MAX_FRAMES  = 60        # safety: auto-release after 1 second

dash_countdown  = 0
dash_cooldown   = 5             # seconds
grapple_timer   = 0

# ── Game loop ─────────────────────────────────────────────────────────────────
while True:

    # ── Jump buffer ────────────────────────────────────────────────────────────
    if jump_buffer > 0:
        jump_buffer -= 1

    if jump_buffer > 0 and on_ground:
        y_velocity  = jump_strength
        on_ground   = False
        double_jump = True
        jump_buffer = 0
    elif jump_buffer > 0 and double_jump:
        y_velocity  = jump_strength
        on_ground   = False
        double_jump = False
        jump_buffer = 0

    # ── Click buffer → punch ───────────────────────────────────────────────────
    if click_buffer > 0:
        click_buffer -= 1

    if click_buffer > 0 and not punching:
        mousePos = pygame.mouse.get_pos()
        wave     = math.atan2(mousePos[1] - y, mousePos[0] - x)
        punching = True
        click_buffer = 0

    # ── Events ─────────────────────────────────────────────────────────────────
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_w, pygame.K_SPACE):
                jump_buffer = jump_buffer_time
            if event.key == pygame.K_s and not on_ground:
                y_velocity += 10.5

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and not punching:
                click_buffer = click_buffer_time

            # ── RIGHT-CLICK → grapple ──────────────────────────────────────
            if event.button == 3 and dash_countdown <= 0 and not grappling:
                mousePos = pygame.mouse.get_pos()

                cx = x + size // 2
                cy = y + size // 2

                grapple_wave     = math.atan2(mousePos[1] - cy, mousePos[0] - cx)
                grapple_target_x = cx + math.cos(grapple_wave) * GRAPPLE_REACH
                grapple_target_y = cy + math.sin(grapple_wave) * GRAPPLE_REACH

                # Clamp inside screen
                grapple_target_x = max(0, min(WIDTH,  grapple_target_x))
                grapple_target_y = max(0, min(HEIGHT, grapple_target_y))

                grappling      = True
                grapple_timer  = 0
                dash_countdown = dash_cooldown * 60

    # ── Punch animation ────────────────────────────────────────────────────────
    if punching:
        hand_offset += hand_speed
        hand_x_distance = math.cos(wave) * hand_offset
        hand_y_distance = math.sin(wave) * hand_offset
        if hand_offset >= max_reach:
            hand_speed = -hand_speed
        if hand_offset <= 0:
            hand_offset = 0
            hand_speed  = abs(hand_speed)
            punching    = False

    hand_x = x + size // 2 + hand_x_distance
    hand_y = y + size // 2 + hand_y_distance

    # ── Grapple pull (velocity-based) ──────────────────────────────────────────
    if grappling:
        grapple_timer += 1

        cx = x + size // 2
        cy = y + size // 2
        dx = grapple_target_x - cx
        dy = grapple_target_y - cy
        dist = math.hypot(dx, dy)

        if dist < GRAPPLE_ARRIVE_DIST or grapple_timer >= GRAPPLE_MAX_FRAMES:
            # ── Release: player keeps all velocity → propels forward ──────────
            grappling = False
        else:
            # Pull force in grapple direction, gravity still applies normally
            pull_angle = math.atan2(dy, dx)
            x_velocity += math.cos(pull_angle) * GRAPPLE_PULL
            y_velocity += math.sin(pull_angle) * GRAPPLE_PULL

            # Cap velocity so it stays controllable
            speed_now = math.hypot(x_velocity, y_velocity)
            if speed_now > MAX_VEL:
                x_velocity = (x_velocity / speed_now) * MAX_VEL
                y_velocity = (y_velocity / speed_now) * MAX_VEL

    # ── Cooldown ───────────────────────────────────────────────────────────────
    if dash_countdown > 0:
        dash_countdown -= 1

    # ── Gravity (always on — even during grapple for arc feel) ─────────────────
    y_velocity += gravity
    y += y_velocity
    x += x_velocity

    # ── Horizontal movement (WASD still steers mid-air) ───────────────────────
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        x -= speed
    if keys[pygame.K_d]:
        x += speed

    # ── Ground collision ───────────────────────────────────────────────────────
    if y + size >= ground_y:
        y          = float(ground_y - size)
        y_velocity = 0.0
        x_velocity *= 0.75       # ground friction bleeds off horizontal speed
        on_ground  = True
        double_jump = False
        if grappling:            # ground cancels grapple
            grappling = False

    # ── Keep on screen ─────────────────────────────────────────────────────────
    if x < 0:
        x = 0.0
        x_velocity = 0.0
    if x + size > WIDTH:
        x = float(WIDTH - size)
        x_velocity = 0.0

    # ── Draw ───────────────────────────────────────────────────────────────────
    screen.fill(BLUE)

    pygame.draw.rect(screen, GREEN, (0, ground_y, WIDTH, HEIGHT - ground_y))

    platforms = [
        pygame.Rect(20,  800, 400, 40),
        pygame.Rect(600, 750, 200, 30),
    ]
    for platform in platforms:
        if y + size >= platform.top and y + size <= platform.bottom:
            if x < platform.right and x + size > platform.left:
                y          = float(platform.top - size)
                y_velocity = 0.0
                x_velocity *= 0.75
                on_ground  = True
                double_jump = False
                if grappling:
                    grappling = False
        pygame.draw.rect(screen, GREEN, platform)

    # Grapple rope + target dot
    if grappling:
        pygame.draw.line(
            screen, ROPE_COLOR,
            (int(x + size // 2), int(y + size // 2)),
            (int(grapple_target_x), int(grapple_target_y)), 3
        )
        pygame.draw.circle(screen, ROPE_COLOR,
                           (int(grapple_target_x), int(grapple_target_y)), 6)

    # HUD
    if dash_countdown > 0:
        screen.blit(font.render(f"Grapple CD: {dash_countdown // 60 + 1}s", True, (255, 80, 80)), (20, 20))
    else:
        screen.blit(font.render("Grapple READY  [RMB]", True, (80, 255, 80)), (20, 20))

    vel_text = font.render(f"vel  x:{x_velocity:+.1f}  y:{y_velocity:+.1f}", True, (220, 220, 220))
    screen.blit(vel_text, (20, 55))

    # Player + hand
    pygame.draw.rect(screen, Character, (int(x), int(y), size, size))
    pygame.draw.rect(screen, GREEN,     (int(hand_x), int(hand_y), hand_width, hand_height))

    pygame.display.flip()
    clock.tick(60)