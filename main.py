'''

#import pygame
from PIL import Image


pygame.init()
WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ralph's BrickGame")

PLAYER_WIDTH, PLAYER_HEIGHT = 50, 50



BG = Image.open("./tools/thanos.gif")
fire = Image.open("./tools/fireGif.gif")
frames = []

try:
    while True:
        frame = BG.copy().convert("RGBA")
        frame2 = fire.copy().convert("RGBA")
        mode = frame.mode
        size = frame.size
        data = frame.tobytes()

        pygame_image = pygame.image.fromstring(data, size, mode)
        pygame_image = pygame.transform.scale(pygame_image, (WIDTH, HEIGHT))
        frames.append(pygame_image)

        BG.seek(BG.tell() + 1)
except EOFError:
    pass  

def draw(player):

    pygame.draw.rect(WIN, (255, 0, 0), player, border_radius= 50)


def draw2(projectiles):

    pygame.draw.polygon(WIN, (255, 0, 0),[(300, 300), (325, 400), (350, 300)],5)

    try:
        while True:
            frame = BG.copy().convert("RGBA")
            frame2 = fire.copy().convert("RGBA")
            mode = frame.mode
            size = frame.size
            data = frame.tobytes()

            pygame_image2 = pygame.image.fromstring(data, size, mode)
            pygame_image2 = pygame.transform.scale(pygame_image2, projectiles)
            frames.append(pygame_image2)

            BG.seek(BG.tell() + 1)
    except EOFError:
        pass



# Game Loop 
def game():
    clock = pygame.time.Clock()
    frame_index = 0
    run = True

    player = pygame.Rect(200,HEIGHT-PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    projectiles = pygame.Rect(400, HEIGHT-PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)

    while run:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                run = False
                break
        

       
        frame_index = (frame_index + 1) % len(frames)
        WIN.blit(frames[frame_index], (0, 0))   

        draw(player)
        draw2(projectiles)

        pygame.display.update()
        clock.tick(10)  

       

    pygame.quit()


if __name__ == "__main__":
    game()

'''
import time

import pygame
from PIL import Image, ImageSequence
pygame.font.init()

# Setup
pygame.init()
WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ralph's BrickGame")

PLAYER_WIDTH, PLAYER_HEIGHT = 50, 50
PROJECTILE_WIDTH, PROJECTILE_HEIGHT = 15, 40
PLAYER_SPEED = 5

FONT = pygame.font.SysFont("comicsans",30)

# ------------------------------
# Load and prep background GIF
# ------------------------------


BG = Image.open("./tools/thanos.gif")
bg_frames = []
for frame in ImageSequence.Iterator(BG):
    frame = frame.convert("RGBA")
    pygame_frame = pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode)
    pygame_frame = pygame.transform.scale(pygame_frame, (WIDTH, HEIGHT))
    bg_frames.append(pygame_frame)

# ------------------------------
# Load and prep fire GIF
# ------------------------------
fire = Image.open("./tools/fireGif.gif")
fire_frames = []
for frame in ImageSequence.Iterator(fire):
    frame = frame.convert("RGBA")
    pygame_frame = pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode)
    pygame_frame = pygame.transform.scale(pygame_frame, (PROJECTILE_WIDTH, PROJECTILE_HEIGHT))
    fire_frames.append(pygame_frame)



def elapsed(elapsed_time):


    time_text = FONT.render(f"Time:{round(elapsed_time)}s",1,"white")
    WIN.blit(time_text,(10,10))
def draw_player(player):
    pygame.draw.rect(WIN, (255, 0, 0), player, border_radius=50)

def draw_projectile(projectile, fire_frame):
    # Optional projectile outline
    pygame.draw.polygon(WIN, (255, 0, 0),
                        [(projectile.centerx, projectile.top),
                         (projectile.left, projectile.bottom),
                         (projectile.right, projectile.bottom)], 2)
    # Draw the fire animation in the projectile area
    WIN.blit(fire_frame, projectile.topleft)


# ------------------------------
# Game loop
# ------------------------------
def game():
    clock = pygame.time.Clock()
    fire_frame_idx = 0
    bg_frame_idx = 0
    run = True

    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    projectile = pygame.Rect(400, HEIGHT - PLAYER_HEIGHT - 150, PROJECTILE_WIDTH, PROJECTILE_HEIGHT)


    bounce_y = 0
    bounce_direction = -1  # up first
    bounce_range = 10
    bounce_speed = 4

    clock = pygame.time.Clock()

    start_time = time.time()



    while run:

        clock.tick(60)
        elapsed_time = time.time()- start_time
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                run = False
                break


        bg_frame_idx = (bg_frame_idx + 1) % len(bg_frames)
        WIN.blit(bg_frames[bg_frame_idx], (0, 0))

        # --- Automatic jump bounce ---
        bounce_y += bounce_direction * bounce_speed
        if abs(bounce_y) >= bounce_range:
            bounce_direction *= -1  # reverse bounce direction

        # Draw entities with bounce offset
        elapsed(elapsed_time)
        draw_player(pygame.Rect(player.x, player.y + bounce_y, PLAYER_WIDTH, PLAYER_HEIGHT))
        draw_projectile(projectile, fire_frames[fire_frame_idx])

        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_SPEED >= 0:
            player.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] and player.x + PLAYER_SPEED + PLAYER_WIDTH <= WIDTH:
            player.x += PLAYER_SPEED

        # Update frame indices
        fire_frame_idx = (fire_frame_idx + 1) % len(fire_frames)

        pygame.display.update()
        clock.tick(30)

    pygame.quit()



if __name__ == "__main__":
    game()
