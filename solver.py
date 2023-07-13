import pygame
import time
import random

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Set up the display
pygame.init()
WIDTH = 540
HEIGHT = 640
FPS = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku Solver")
clock = pygame.time.Clock()

# Fonts
pygame.font.init()
font_small = pygame.font.SysFont(None, 25)
font_big = pygame.font.SysFont(None, 40)

# Timer
start_time = time.time()
countdown_time = 300  # 5 minutes in seconds
elapsed_time = 0

# Cell dimensions
CELL_SIZE = 50
CELL_PADDING = 4

# Calculate the board dimensions
BOARD_SIZE = CELL_SIZE * 9 + CELL_PADDING * 9
BOARD_POS_X = (WIDTH - BOARD_SIZE) // 2
BOARD_POS_Y = (HEIGHT - BOARD_SIZE - font_big.get_height() - font_small.get_height()) // 2

# Selected cell position
selected = (-1, -1)

# Solve board flag
solve_board = False

# User input mode
input_mode = False
input_counter = 0
input_original = [[0] * 9 for _ in range(9)]


def generate_board():
    # Initialize an empty board
    board = [[0] * 9 for _ in range(9)]

    # Fill the board using backtracking algorithm
    solve(board)

    # Remove random cells to create the puzzle
    empty_cells = random.sample(range(81), 50)  # Adjust the number of empty cells as desired
    for cell in empty_cells:
        row = cell // 9
        col = cell % 9
        board[row][col] = 0

    return board


def solve(bo):
    find = find_empty(bo)
    if not find:
        return True
    else:
        row, col = find

    for i in range(1, 10):
        if valid_check(bo, i, (row, col)):
            bo[row][col] = i

            if solve(bo):
                return True

            bo[row][col] = 0

    return False


def valid_check(bo, num, pos):
    # Row
    for i in range(len(bo[0])):
        if bo[pos[0]][i] == num and pos[1] != i:
            return False

    # Column
    for i in range(len(bo)):
        if bo[i][pos[1]] == num and pos[0] != i:
            return False

    # Check box
    box_x = pos[1] // 3
    box_y = pos[0] // 3
    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if bo[i][j] == num and (i, j) != pos:
                return False

    return True


def draw_grid():
    for i in range(10):
        if i % 3 == 0:
            pygame.draw.line(screen, BLACK, (BOARD_POS_X, BOARD_POS_Y + i * (CELL_SIZE + CELL_PADDING)),
                             (BOARD_POS_X + BOARD_SIZE, BOARD_POS_Y + i * (CELL_SIZE + CELL_PADDING)), 3)
            pygame.draw.line(screen, BLACK, (BOARD_POS_X + i * (CELL_SIZE + CELL_PADDING), BOARD_POS_Y),
                             (BOARD_POS_X + i * (CELL_SIZE + CELL_PADDING), BOARD_POS_Y + BOARD_SIZE), 3)
        else:
            pygame.draw.line(screen, GRAY, (BOARD_POS_X, BOARD_POS_Y + i * (CELL_SIZE + CELL_PADDING)),
                             (BOARD_POS_X + BOARD_SIZE, BOARD_POS_Y + i * (CELL_SIZE + CELL_PADDING)), 1)
            pygame.draw.line(screen, GRAY, (BOARD_POS_X + i * (CELL_SIZE + CELL_PADDING), BOARD_POS_Y),
                             (BOARD_POS_X + i * (CELL_SIZE + CELL_PADDING), BOARD_POS_Y + BOARD_SIZE), 1)


def draw_numbers(board):
    for i in range(9):
        for j in range(9):
            num = str(board[i][j])
            if num != '0':
                pos_x = BOARD_POS_X + j * (CELL_SIZE + CELL_PADDING) + CELL_SIZE // 2
                pos_y = BOARD_POS_Y + i * (CELL_SIZE + CELL_PADDING) + CELL_SIZE // 2
                text_surface = font_big.render(num, True, BLACK)
                text_rect = text_surface.get_rect(center=(pos_x, pos_y))
                screen.blit(text_surface, text_rect)


def draw_selection():
    if selected != (-1, -1):
        pos_x = BOARD_POS_X + selected[1] * (CELL_SIZE + CELL_PADDING) + CELL_PADDING
        pos_y = BOARD_POS_Y + selected[0] * (CELL_SIZE + CELL_PADDING) + CELL_PADDING
        pygame.draw.rect(screen, BLUE, (pos_x, pos_y, CELL_SIZE, CELL_SIZE), 3)


def draw_timer():
    global elapsed_time
    elapsed_time = int(time.time() - start_time)
    remaining_time = countdown_time - elapsed_time
    if remaining_time <= 0:
        remaining_time = 0

    minutes = remaining_time // 60
    seconds = remaining_time % 60
    timer_text = f"Time Left: {minutes:02d}:{seconds:02d}"
    timer_surface = font_small.render(timer_text, True, BLACK)
    timer_rect = timer_surface.get_rect(center=(WIDTH // 2, BOARD_POS_Y - font_small.get_height() // 2))
    screen.blit(timer_surface, timer_rect)


def find_empty(bo):
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                return (i, j)

    return None


def solve_puzzle():
    global input_mode, input_counter
    input_mode = False
    input_counter = 0


def reset_input():
    global input_counter
    for i in range(9):
        for j in range(9):
            if input_original[i][j] != 0:
                board[i][j] = input_original[i][j]
            else:
                board[i][j] = 0
    input_counter += 1


def check_solution():
    global input_counter
    if input_counter == 3:
        solve(board)
    else:
        reset_input()


# Generate a random board
board = generate_board()

# Main loop
running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                x, y = pygame.mouse.get_pos()
                if BOARD_POS_X <= x <= BOARD_POS_X + BOARD_SIZE and BOARD_POS_Y <= y <= BOARD_POS_Y + BOARD_SIZE:
                    row = (y - BOARD_POS_Y) // (CELL_SIZE + CELL_PADDING)
                    col = (x - BOARD_POS_X) // (CELL_SIZE + CELL_PADDING)
                    selected = (row, col)
                else:
                    selected = (-1, -1)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                solve_puzzle()
            if selected != (-1, -1):
                if not input_mode and board[selected[0]][selected[1]] == 0:
                    input_mode = True
                    input_counter = 0
                    for i in range(9):
                        input_original[i] = board[i].copy()
                elif input_mode and input_counter < 3:
                    if event.unicode.isnumeric():
                        num = int(event.unicode)
                        board[selected[0]][selected[1]] = num
                    elif event.key == pygame.K_BACKSPACE:
                        board[selected[0]][selected[1]] = 0
                    elif event.key == pygame.K_RETURN:
                        check_solution()

    screen.fill(WHITE)

    draw_grid()
    draw_numbers(board)
    draw_selection()
    draw_timer()

    if solve_board:
        solve(board)
        solve_board = False

    # Solve Board Button
    button_width = 200
    button_height = 50
    button_x = (WIDTH - button_width) // 2
    button_y = HEIGHT - button_height - 20
    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
    pygame.draw.rect(screen, GRAY, button_rect)
    solve_text = font_small.render("Solve Board", True, BLACK)
    solve_text_rect = solve_text.get_rect(center=button_rect.center)
    screen.blit(solve_text, solve_text_rect)

    # Check if Solve Board Button is clicked
    mouse_pos = pygame.mouse.get_pos()
    if button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, BLUE, button_rect, 3)
        if pygame.mouse.get_pressed()[0]:  # Left mouse button
            solve_board = True
    else:
        pygame.draw.rect(screen, BLACK, button_rect, 3)

    # User Input Mode Indicator
    if input_mode:
        if input_counter < 3:
            mode_text = font_small.render("User Input Mode (Tries Left: " + str(3 - input_counter) + ")", True, GREEN)
        else:
            mode_text = font_small.render("User Input Mode (Tries Left: 0)", True, BLACK)
        mode_text_rect = mode_text.get_rect(center=(WIDTH // 2, BOARD_POS_Y - font_small.get_height() // 2))
        screen.blit(mode_text, mode_text_rect)

    pygame.display.flip()

    if elapsed_time >= countdown_time or input_counter == 3:
        pygame.time.wait(1000)  # Wait for 1 second before quitting
        running = False

pygame.quit()
