import pygame
import random
import time

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Advanced Rhythm Game")
clock = pygame.time.Clock()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLUMN_WIDTH = WIDTH // 5
CHARACTER_SIZE = 100
BOMB_SIZE = 50
MAX_BOMBS_ON_SCREEN = 4

# Colors and background
background_color = (0, 0, 0)
background_image = pygame.image.load("background.png")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Load background music and set parameters
pygame.mixer.music.load("generique.mp3")
pygame.mixer.music.play(-1)
BPM = 120
beat_interval = 60 / BPM
difficulty_increase_interval = 10

# Bomb settings
base_fall_speed = 5
fall_speed_multiplier = 1.1
bomb_spawn_interval = beat_interval * 0.8

# Fonts
font = pygame.font.SysFont("Arial", 24)
large_font = pygame.font.SysFont("Arial", 40)

# Bomb class
class Bomb:
    def __init__(self, column, fall_speed):
        self.x = column * COLUMN_WIDTH + COLUMN_WIDTH // 2 - BOMB_SIZE // 2
        self.y = -BOMB_SIZE
        self.fall_speed = fall_speed
        self.column = column

    def fall(self):
        self.y += self.fall_speed
        return self.y > HEIGHT

    def draw(self):
        pygame.draw.circle(screen, (255, 0, 0), (self.x, int(self.y)), BOMB_SIZE // 2)

# Draw text utility
def draw_text(text, font, color, surface, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    surface.blit(text_surface, text_rect)

# Pause screen
def pause_screen():
    paused = True
    while paused:
        screen.blit(background_image, (0, 0))
        draw_text("PAUSED", large_font, WHITE, screen, WIDTH // 2, HEIGHT // 2 - 50)
        draw_text("Press 'P' to resume", font, WHITE, screen, WIDTH // 2, HEIGHT // 2 + 20)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                paused = False

# Registration screen
def registration_screen():
    user_input = ""
    active = True
    while active:
        screen.fill(BLACK)
        draw_text("Enter your name:", large_font, WHITE, screen, WIDTH // 2, HEIGHT // 2 - 50)
        draw_text(user_input, large_font, WHITE, screen, WIDTH // 2, HEIGHT // 2)
        draw_text("Press ENTER to confirm", font, WHITE, screen, WIDTH // 2, HEIGHT // 2 + 50)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and user_input.strip():
                    return user_input.strip()
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                else:
                    user_input += event.unicode

# Menu screen
def main_menu():
    while True:
        screen.fill(BLACK)
        draw_text("MAIN MENU", large_font, WHITE, screen, WIDTH // 2, HEIGHT // 2 - 50)
        draw_text("Press ENTER to start", font, WHITE, screen, WIDTH // 2, HEIGHT // 2)
        draw_text("Press ESC to quit", font, WHITE, screen, WIDTH // 2, HEIGHT // 2 + 50)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    player_name = registration_screen()  # Appelle la fonction d'enregistrement
                    main_game(player_name)  # Lance le jeu avec le pseudo
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()



# Main game loop
def main_game(player_name):
    column_bombs = {i: [] for i in range(5)}
    last_spawn_time = time.time()
    game_start_time = time.time()
    fall_speed = base_fall_speed
    leaderboard = []

    running = True
    while running:
        screen.fill(background_color)
        screen.blit(background_image, (0, 0))
        draw_text("Press 'P' to pause", font, WHITE, screen, WIDTH // 2, 30)

        current_time = time.time()
        elapsed_time = round(current_time - game_start_time, 1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                pause_screen()

        # Increase difficulty
        if current_time - game_start_time > difficulty_increase_interval:
            fall_speed *= fall_speed_multiplier
            game_start_time = current_time

        # Generate and update bombs
        if time.time() - last_spawn_time >= bomb_spawn_interval:
            available_columns = [col for col, bombs in column_bombs.items() if len(bombs) < 1]
            if available_columns and sum(len(bombs) for bombs in column_bombs.values()) < MAX_BOMBS_ON_SCREEN:
                column = random.choice(available_columns)
                column_bombs[column].append(Bomb(column, fall_speed))
            last_spawn_time = time.time()

        for column, bombs in column_bombs.items():
            bombs[:] = [bomb for bomb in bombs if not bomb.fall()]
            for bomb in bombs:
                bomb.draw()

        draw_text(f"Time: {elapsed_time}s", font, WHITE, screen, WIDTH - 100, 30)
        pygame.display.update()
        clock.tick(60)

    leaderboard.append((player_name, elapsed_time))
    leaderboard.sort(key=lambda x: x[1], reverse=True)
    print("Leaderboard:", leaderboard)

# Game start
player_name = menu_screen()
main_menu(player_name)
pygame.quit()
