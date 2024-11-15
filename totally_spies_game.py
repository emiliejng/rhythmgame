import pygame
import random
import time

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLUMN_WIDTH = WIDTH // 5
CHARACTER_SIZE = 100

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rhythm Game")

# Fonts
font = pygame.font.SysFont('Arial', 24)
large_font = pygame.font.SysFont('Arial', 40)

# Load background images
background = pygame.image.load("background.jpg")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Load bomb and "You Lose" images
bomb_image = pygame.image.load("bomb.png")
bomb_image = pygame.transform.scale(bomb_image, (50, 50))
you_lose_image = pygame.image.load("you_lose.png")
you_lose_image = pygame.transform.scale(you_lose_image, (WIDTH, HEIGHT))

# Load and play background music
pygame.mixer.music.load("generique.mp3")

# Characters and their corresponding image file names
CHARACTERS = ['Sam', 'Clover', 'Alex', 'Britney', 'Jerry']
CHARACTER_IMAGES = {
    'Sam': 'sam.png',
    'Clover': 'clover.png',
    'Alex': 'alex.png',
    'Britney': 'britney.png',
    'Jerry': 'jerry.png',
}

# Utility function to draw text
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

# Bomb object with image
class Bomb:
    def __init__(self, column, fall_speed):
        self.x = column * COLUMN_WIDTH + COLUMN_WIDTH // 2 - 25
        self.y = -50
        self.column = column
        self.fall_speed = fall_speed

    def fall(self):
        self.y += self.fall_speed
        if self.y > HEIGHT:
            return True
        return False

    def draw(self):
        screen.blit(bomb_image, (self.x, self.y))

# Check for collision between character and bomb
def check_collision(player_position, character_y):
    for bomb in column_bombs[player_position]:
        if bomb.y + 50 > character_y:
            return True
    return False

# Function to generate bombs
def generate_bombs():
    active_bombs = sum(len(bombs) for bombs in column_bombs.values())
    active_columns = sum(1 for bombs in column_bombs.values() if bombs)

    if active_bombs < 4 and active_columns < 3:
        for column in range(5):
            if random.random() < 0.2 and not column_bombs[column]:
                fall_speed = 4
                column_bombs[column].append(Bomb(column, fall_speed))

# Draw the character
def draw_character(character_name, player_position):
    char_image = pygame.image.load(CHARACTER_IMAGES[character_name])
    char_image = pygame.transform.scale(char_image, (CHARACTER_SIZE, CHARACTER_SIZE))
    x = player_position * COLUMN_WIDTH + COLUMN_WIDTH // 2 - CHARACTER_SIZE // 2
    screen.blit(char_image, (x, HEIGHT - CHARACTER_SIZE))

# Main menu with start, register, and leaderboard options
def main_menu():
    menu_running = True
    while menu_running:
        screen.fill(WHITE)
        screen.blit(background, (0, 0))
        
        draw_text("RHYTHM GAME", large_font, BLACK, screen, WIDTH // 2, 100)
        draw_text("1. Start", font, WHITE, screen, WIDTH // 2, 250)
        draw_text("2. Register Now", font, WHITE, screen, WIDTH // 2, 300)
        draw_text("3. Leaderboard", font, WHITE, screen, WIDTH // 2, 350)
        draw_text("Press the corresponding number to select", font, WHITE, screen, WIDTH // 2, 450)

        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    character_selection()
                elif event.key == pygame.K_2:
                    registration_screen()
                elif event.key == pygame.K_3:
                    show_leaderboard()

# Character selection screen
def character_selection():
    clock = pygame.time.Clock()
    selecting = True
    while selecting:
        screen.fill(WHITE)
        screen.blit(background, (0, 0))
        
        x_offset = 50
        for character in CHARACTERS:
            char_image = pygame.image.load(CHARACTER_IMAGES[character])
            char_image = pygame.transform.scale(char_image, (CHARACTER_SIZE, CHARACTER_SIZE))
            screen.blit(char_image, (x_offset, HEIGHT // 2 - CHARACTER_SIZE // 2))
            x_offset += CHARACTER_SIZE + 50

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                x_offset = 50
                for character in CHARACTERS:
                    char_rect = pygame.Rect(x_offset, HEIGHT // 2 - CHARACTER_SIZE // 2, CHARACTER_SIZE, CHARACTER_SIZE)
                    if char_rect.collidepoint(mouse_x, mouse_y):
                        game_loop(character)
                        selecting = False
                        break
                    x_offset += CHARACTER_SIZE + 50

        pygame.display.update()
        clock.tick(FPS)

# Game loop with collision and losing functionality
def game_loop(selected_character):
    global column_bombs
    player_position = 2
    clock = pygame.time.Clock()
    start_time = time.time()
    game_over = False
    column_bombs = {i: [] for i in range(5)}
    pygame.mixer.music.play(-1)
    character_y = HEIGHT - CHARACTER_SIZE

    while not game_over:
        screen.fill(WHITE)
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and player_position > 0:
                    player_position -= 1
                elif event.key == pygame.K_RIGHT and player_position < 4:
                    player_position += 1

        generate_bombs()
        for column in range(5):
            column_bombs[column] = [bomb for bomb in column_bombs[column] if not bomb.fall()]
            for bomb in column_bombs[column]:
                bomb.draw()

        draw_character(selected_character, player_position)

        if check_collision(player_position, character_y):
            game_over = True

        play_time = round(time.time() - start_time, 2)
        draw_text(f"Time: {play_time}s", font, WHITE, screen, WIDTH // 2, 50)

        pygame.display.update()
        clock.tick(FPS)

    pygame.mixer.music.stop()
    show_loss_screen()

# Show the "You Lose" screen with background and indication to press Enter to restart
def show_loss_screen():
    screen.fill(WHITE)
    screen.blit(background, (0, 0))  # Add background image
    screen.blit(you_lose_image, (0, 0))  # Add "You Lose" image on top
    draw_text("Press Enter to play again", font, WHITE, screen, WIDTH // 2, HEIGHT - 50)  # Indication to press Enter
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting = False
                main_menu()

# Start the main menu
main_menu()