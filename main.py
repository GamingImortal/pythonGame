import pygame
from PIL import Image

#  Setup 
pygame.init()
WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ralph's BrickGame")

PLAYER_WIDTH, PLAYER_HEIGHT = 50, 50



BG = Image.open("./tools/thanos.gif")
frames = []

try:
    while True:
        frame = BG.copy().convert("RGBA")
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

    pygame.draw.rect(WIN, (255, 0, 0), player)





# Game Loop 
def game():
    clock = pygame.time.Clock()
    frame_index = 0
    run = True

    player = pygame.Rect(200,HEIGHT-PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)

    while run:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                run = False
                break
        

       
        frame_index = (frame_index + 1) % len(frames)
        WIN.blit(frames[frame_index], (0, 0))   

        draw(player)

        pygame.display.update()
        clock.tick(10)  

       

    pygame.quit()


if __name__ == "__main__":
    game()
