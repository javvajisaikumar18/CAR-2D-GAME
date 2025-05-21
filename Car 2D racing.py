import pygame
import sys
import random
from pytmx.util_pygame import load_pygame
import pytmx

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 800, 640
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Car Game")
clock = pygame.time.Clock()

# Load Assets
bg_music = 'bg_music car.mp3'
crash_sound = 'crash car sound.wav'
car_sprites = pygame.image.load("car spirit.png").convert_alpha()
obstacle_img = pygame.image.load("obstacle car.png").convert_alpha()
tmx_data = load_pygame("car_tile.tmx")  # No leading space!

# Load Sounds
pygame.mixer.music.load(bg_music)
pygame.mixer.music.play(-1)
crash_sfx = pygame.mixer.Sound(crash_sound)

# Car Sprite Animation Setup
CAR_FRAME_WIDTH, CAR_FRAME_HEIGHT = 64, 128
car_frames = [car_sprites.subsurface((i * CAR_FRAME_WIDTH, 0, CAR_FRAME_WIDTH, CAR_FRAME_HEIGHT)) for i in range(2)]
car_index = 0
car_anim_timer = 0

# Car Initial Position
car_x = 400
car_y = 480
car_speed = 5

# Obstacle
obstacle_x = random.randint(100, 700)
obstacle_y = -100
obstacle_speed = 5

# Score
score = 0
font = pygame.font.SysFont(None, 36)

# Game State
game_state = "start"

# Draw Tile Map
def draw_map():
    for layer in tmx_data.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                tile = tmx_data.get_tile_image_by_gid(gid)
                if tile:
                    screen.blit(tile, (x * tmx_data.tilewidth, y * tmx_data.tileheight))

# Utility to show text
def show_text(text, size, x, y, color=(255, 255, 255)):
    f = pygame.font.SysFont(None, size)
    t = f.render(text, True, color)
    screen.blit(t, (x, y))

# Start Menu
def start_menu():
    screen.fill((0, 0, 0))
    show_text("🚗 Car Game", 72, 260, 200)
    show_text("Press SPACE to Start", 40, 270, 300)
    pygame.display.flip()

# Game Over Screen
def game_over():
    crash_sfx.play()
    screen.fill((0, 0, 0))
    show_text("Game Over!", 60, 300, 250, (255, 0, 0))
    show_text(f"Score: {score}", 40, 340, 320)
    show_text("Press R to Restart", 36, 300, 380)
    pygame.display.flip()

# Reset Game State
def reset_game():
    global car_x, car_y, obstacle_x, obstacle_y, obstacle_speed, score
    car_x = 400
    car_y = 480
    obstacle_x = random.randint(100, 700)
    obstacle_y = -100
    obstacle_speed = 5
    score = 0

# Game Loop
running = True
while running:
    clock.tick(60)

    if game_state == "start":
        start_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_state = "play"
                reset_game()

    elif game_state == "gameover":
        game_over()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                game_state = "play"
                reset_game()

    elif game_state == "play":
        screen.fill((0, 0, 0))
        draw_map()

        # Animate car
        car_anim_timer += 1
        if car_anim_timer % 10 == 0:
            car_index = (car_index + 1) % len(car_frames)

        # Draw car and obstacle
        screen.blit(car_frames[car_index], (car_x, car_y))
        screen.blit(obstacle_img, (obstacle_x, obstacle_y))
        show_text(f"Score: {score}", 30, 10, 10)

        # Controls
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and car_x > 0:
            car_x -= car_speed
        if keys[pygame.K_RIGHT] and car_x < WIDTH - CAR_FRAME_WIDTH:
            car_x += car_speed

        # Obstacle logic
        obstacle_y += obstacle_speed
        if obstacle_y > HEIGHT:
            obstacle_y = -100
            obstacle_x = random.randint(100, 700)
            score += 1
            obstacle_speed += 0.2

        # Collision detection
        car_rect = pygame.Rect(car_x, car_y, CAR_FRAME_WIDTH, CAR_FRAME_HEIGHT)
        obstacle_rect = pygame.Rect(obstacle_x, obstacle_y, CAR_FRAME_WIDTH, CAR_FRAME_HEIGHT)
        if car_rect.colliderect(obstacle_rect):
            game_state = "gameover"

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()

pygame.quit()
