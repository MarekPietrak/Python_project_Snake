import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH = 600
HEIGHT = 400
CELL_SIZE = 20

# Colors
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Fonts
FONT = pygame.font.SysFont('Arial', 25, bold=True)
GAME_OVER_FONT = pygame.font.SysFont('Arial', 50, bold=True)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game')

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# New constants for the timer feature
FOOD_TIMER_EVENT = pygame.USEREVENT + 1
FOOD_TIMER_SECONDS = 5000  # 5 seconds in milliseconds

# Difficulty settings
DIFFICULTIES = {
    'Easy': 0.5,
    'Normal': 1.0,
    'Hard': 3.0,
    'Impossible': 10.0
}

def main_menu():
    difficulties = list(DIFFICULTIES.keys())
    current_difficulty = 1  # Start with Normal

    while True:
        screen.fill(GREEN)
        title_text = FONT.render('Snake Game', True, BLACK)
        start_text = FONT.render('Press ENTER to Start', True, BLACK)
        quit_text = FONT.render('Press ESC to Quit', True, BLACK)
        difficulty_text = FONT.render(f'Difficulty: {difficulties[current_difficulty]}', True, BLACK)
        screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, HEIGHT//2 - 60))
        screen.blit(start_text, (WIDTH//2 - start_text.get_width()//2, HEIGHT//2))
        screen.blit(quit_text, (WIDTH//2 - quit_text.get_width()//2, HEIGHT//2 + 40))
        screen.blit(difficulty_text, (WIDTH//2 - difficulty_text.get_width()//2, HEIGHT//2 + 80))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return difficulties[current_difficulty]
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_LEFT:
                    current_difficulty = (current_difficulty - 1) % len(difficulties)
                if event.key == pygame.K_RIGHT:
                    current_difficulty = (current_difficulty + 1) % len(difficulties)

def game_over(score, difficulty):
    while True:
        screen.fill(GREEN)
        over_text = GAME_OVER_FONT.render('GAME OVER', True, BLACK)
        score_text = FONT.render(f'Score: {score}', True, BLACK)
        restart_text = FONT.render('Press R to Restart', True, BLACK)
        menu_text = FONT.render('Press M for Main Menu', True, BLACK)
        quit_text = FONT.render('Press ESC to Quit', True, BLACK)
        screen.blit(over_text, (WIDTH//2 - over_text.get_width()//2, HEIGHT//2 - 100))
        screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2 - 40))
        screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 20))
        screen.blit(menu_text, (WIDTH//2 - menu_text.get_width()//2, HEIGHT//2 + 60))
        screen.blit(quit_text, (WIDTH//2 - quit_text.get_width()//2, HEIGHT//2 + 100))
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game_loop(difficulty)
                if event.key == pygame.K_m:
                    return  # Return to main menu
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

def pause_menu():
    paused = True
    while paused:
        screen.fill(GREEN)
        pause_text = FONT.render('PAUSED', True, BLACK)
        continue_text = FONT.render('Press C to Continue', True, BLACK)
        menu_text = FONT.render('Press M for Main Menu', True, BLACK)
        screen.blit(pause_text, (WIDTH//2 - pause_text.get_width()//2, HEIGHT//2 - 60))
        screen.blit(continue_text, (WIDTH//2 - continue_text.get_width()//2, HEIGHT//2))
        screen.blit(menu_text, (WIDTH//2 - menu_text.get_width()//2, HEIGHT//2 + 40))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    return 'continue'
                if event.key == pygame.K_m:
                    return 'main_menu'

def game_loop(difficulty):
    # Snake starting position
    snake_pos = [100, 60]
    snake_body = [[100, 60], [80, 60], [60, 60]]
    direction = 'RIGHT'
    change_to = direction

    # Food position
    food_pos = [random.randrange(1, (WIDTH//CELL_SIZE)) * CELL_SIZE,
                random.randrange(1, (HEIGHT//CELL_SIZE)) * CELL_SIZE]
    food_spawn = True

    score = 0
    multiplier = 0
    food_timer_active = False
    timer_start = 0

    # Set game speed based on difficulty
    game_speed = 10 * DIFFICULTIES[difficulty]

    paused = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = not paused  # Toggle pause state
                if not paused:
                    if event.key == pygame.K_UP and direction != 'DOWN':
                        change_to = 'UP'
                    if event.key == pygame.K_DOWN and direction != 'UP':
                        change_to = 'DOWN'
                    if event.key == pygame.K_LEFT and direction != 'RIGHT':
                        change_to = 'LEFT'
                    if event.key == pygame.K_RIGHT and direction != 'LEFT':
                        change_to = 'RIGHT'
            if event.type == FOOD_TIMER_EVENT:
                multiplier = 0
                food_timer_active = False

        if paused:
            pause_result = pause_menu()
            if pause_result == 'continue':
                paused = False
            elif pause_result == 'main_menu':
                return  # Return to main menu
            continue  # Skip the rest of the loop if paused

        direction = change_to

        # Moving the snake
        if direction == 'UP':
            snake_pos[1] -= CELL_SIZE
        elif direction == 'DOWN':
            snake_pos[1] += CELL_SIZE
        elif direction == 'LEFT':
            snake_pos[0] -= CELL_SIZE
        elif direction == 'RIGHT':
            snake_pos[0] += CELL_SIZE

        # Wrap around screen edges
        snake_pos[0] = snake_pos[0] % WIDTH
        snake_pos[1] = snake_pos[1] % HEIGHT

        # Snake body growing mechanism
        snake_body.insert(0, list(snake_pos))
        
        # Check if snake has eaten the food
        if snake_pos == food_pos:
            if food_timer_active:
                multiplier += 1
                score += (1 + multiplier)
            else:
                score += 1
            
            food_spawn = False
            # Reset and start the timer
            pygame.time.set_timer(FOOD_TIMER_EVENT, 0)  # Cancel any existing timer
            pygame.time.set_timer(FOOD_TIMER_EVENT, FOOD_TIMER_SECONDS)
            food_timer_active = True
            timer_start = pygame.time.get_ticks()  # Record the start time
        else:
            snake_body.pop()

        if not food_spawn:
            food_pos = [random.randrange(1, (WIDTH//CELL_SIZE)) * CELL_SIZE,
                        random.randrange(1, (HEIGHT//CELL_SIZE)) * CELL_SIZE]
            food_spawn = True

        # Check for collision with snake body
        for segment in snake_body[1:]:
            if snake_pos == segment:
                game_over(score, difficulty)
                return  # Return to main menu after game over

        # Background
        screen.fill(GREEN)

        # Draw Snake
        for pos in snake_body:
            pygame.draw.rect(screen, BLACK, pygame.Rect(pos[0], pos[1], CELL_SIZE, CELL_SIZE))

        # Draw Food
        pygame.draw.rect(screen, BLACK, pygame.Rect(food_pos[0], food_pos[1], CELL_SIZE, CELL_SIZE))

        # Display Score and Multiplier
        score_text = FONT.render(f'Score: {score}', True, BLACK)
        multiplier_text = FONT.render(f'Multiplier: x{multiplier}', True, BLACK)
        screen.blit(score_text, (10, 10))
        screen.blit(multiplier_text, (10, 40))

        # Display Timer
        if food_timer_active:
            elapsed_time = pygame.time.get_ticks() - timer_start
            remaining_time = max(0, (FOOD_TIMER_SECONDS - elapsed_time) // 1000)
            timer_text = FONT.render(f'Time: {remaining_time}s', True, BLACK)
            screen.blit(timer_text, (WIDTH - 100, 10))

        pygame.display.update()
        clock.tick(game_speed)

if __name__ == '__main__':
    while True:
        selected_difficulty = main_menu()
        game_loop(selected_difficulty)
