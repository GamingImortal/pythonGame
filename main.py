import random
import time
import pygame
from PIL import Image, ImageSequence

pygame.font.init()
pygame.init()


WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ralph's BrickGame")

PLAYER_WIDTH, PLAYER_HEIGHT = 50, 50
PROJECTILE_WIDTH, PROJECTILE_HEIGHT = 15, 40
PLAYER_SPEED = 15
STAR_WIDTH = 10
STAR_HEIGHT = 14
STAR_VEL = 9

FONT = pygame.font.SysFont("comicsans", 30)


BG = Image.open("./tools/spaaaace.gif")
bg_frames = []
for frame in ImageSequence.Iterator(BG):
    frame = frame.convert("RGBA")
    pygame_frame = pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode)
    pygame_frame = pygame.transform.scale(pygame_frame, (WIDTH, HEIGHT))
    bg_frames.append(pygame_frame)


fire = Image.open("./tools/fireGif.gif")
fire_frames = []
for frame in ImageSequence.Iterator(fire):
    frame = frame.convert("RGBA")
    pygame_frame = pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode)
    pygame_frame = pygame.transform.scale(pygame_frame, (PROJECTILE_WIDTH, PROJECTILE_HEIGHT))
    fire_frames.append(pygame_frame)


def elapsed(elapsed_time):
    time_text = FONT.render(f"Time:{round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (10, 10))

def draw_player(player, stars):
    pygame.draw.rect(WIN, (225, 225, 225), player, border_radius=50)
    for star in stars:
        pygame.draw.rect(WIN, "white", star)

def draw_projectile(projectile, fire_frame):

    pygame.draw.polygon(WIN, (255, 0, 0),
                        [(projectile.centerx, projectile.top),
                         (projectile.left, projectile.bottom),
                         (projectile.right, projectile.bottom)], 2)
    # Draw fire animation
    WIN.blit(fire_frame, projectile.topleft)

# ------------------------------
# Game function
# ------------------------------
def game():
    clock = pygame.time.Clock()
    fire_frame_idx = 0
    bg_frame_idx = 0
    run = True

    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)

    # Initialize projectile at random top position
    projectile = pygame.Rect(random.randint(0, WIDTH - PROJECTILE_WIDTH), -PROJECTILE_HEIGHT, PROJECTILE_WIDTH, PROJECTILE_HEIGHT)

    star_add_increment = 2000
    star_count = 0
    stars = []
    hit = False
    start_time = time.time()

    while run:
        star_count += clock.tick(15)
        if star_count > star_add_increment:
            for _ in range(8):
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                stars.append(star)
            star_add_increment = max(200, star_add_increment - 50)
            star_count = 0

        elapsed_time = time.time() - start_time

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                run = False
                break


        if hit:
            lost_text = FONT.render("You lost you big headed loser", 1, "white")
            WIN.blit(lost_text, (WIDTH / 2 - lost_text.get_width() / 2, HEIGHT / 2 - lost_text.get_height() / 2))
            pygame.display.update()
            pygame.time.delay(4000)
            break

        bg_frame_idx = (bg_frame_idx + 1) % len(bg_frames)
        WIN.blit(bg_frames[bg_frame_idx], (0, 0))

        elapsed(elapsed_time)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_SPEED >= 0:
            player.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] and player.x + PLAYER_SPEED + PLAYER_WIDTH <= WIDTH:
            player.x += PLAYER_SPEED

        for star in stars[:]:
            star.y += STAR_VEL
            if star.y > HEIGHT:
                stars.remove(star)
            elif star.colliderect(player):
                stars.remove(star)
                hit = True
                break


            for i in range(1):
                projectile.y += 8
                if projectile.y > HEIGHT:
                    projectile.y = -PROJECTILE_HEIGHT
                    projectile.x = random.randint(0, WIDTH - PROJECTILE_WIDTH)
                if projectile.colliderect(player):
                    hit = True

        draw_player(player, stars)
        draw_projectile(projectile, fire_frames[fire_frame_idx])

        fire_frame_idx = (fire_frame_idx + 1) % len(fire_frames)

        pygame.display.update()
        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    game()
