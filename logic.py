import pygame
import sys

'''Game Constants'''
# screen_info = pygame.display.Info() # Get info about the display

# Define game window size using monitor stats
WIDTH = 1500
HEIGHT = 740
CELL_SIZE = 10

# Grid size
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE

# Colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ORANGE = (255, 165, 0)

# Tracking cell stats
TOTAL_LIVE_CELLS = 0



# Initialize pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT)) # Display object to draw on
pygame.display.set_caption("Game of Life - press q to stop")

# Set up on-screen counters
font = pygame.font.Font(None, 36) # None for default font, 36 for font size


''' Functions '''

# Initialize the grid to store the state(alive or dead) of each cell, represented as a two-dimensional list.
def return_empty_grid():
    return [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

# Update the grid each frame - implementing game of life rules.
def update_grid(grid):
    new_grid = return_empty_grid() # Create a new grid to hold the next state

    # Game of Life Automata Rules
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            num_live_neighbors = count_live_neighbors(grid, x, y)
            cell = grid[y][x]
            if cell == 1 and num_live_neighbors in (2, 3):
                new_grid[y][x] = 1 # Cell survives
            elif cell == 0 and num_live_neighbors == 3:
                new_grid[y][x] = 1 # Cell becomes alive
            else:
                new_grid[y][x] = 0 # Cell dies or remains dead
    return new_grid

# Return how many cell neighbours are alive as an integer.
def count_live_neighbors(grid, x, y):
    # Calculate the number of live neighbors around the cell at (x, y)
    count = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            nx, ny = x + j, y + i
            if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT:
                count += grid[ny][nx]
    return count

# Draw each alive cell by iterating over the grid squares and checking if alive.
def draw_cells(grid):
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            color = ORANGE if grid[y][x] == 1 else BLACK # Draw orange coloured cells
            pygame.draw.rect(screen, color, rect, 0)  # Fill the cell with the color

# Let the user setup the initial grid configuration by placing squares.
def setup_grid(grid):
    setup = True
    drawing = False
    while setup:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Allow player to quit the game before setup complete
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                drawing = True
            elif event.type == pygame.MOUSEBUTTONUP:
                drawing = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    setup = False  # Exit setup and start the simulation when space bar is pressed

            if drawing and (event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONDOWN):
                # Get mouse position and determine which cell it corresponds to
                x, y = event.pos
                grid_x = x // CELL_SIZE
                grid_y = y // CELL_SIZE

                # Toggle the cell state
                if 0 <= grid_x < GRID_WIDTH and 0 <= grid_y < GRID_HEIGHT:
                    grid[grid_y][grid_x] = 1


        screen.fill(BLACK)
        draw_cells(grid)
        pygame.display.flip()

# Main loop.
def main():
    clock = pygame.time.Clock()
    running = True
    grid = return_empty_grid()  # Initialize the grid

    # Allow user to set up the initial state
    setup_grid(grid)

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q: #Check if "q" is pressed
                    running = False # Stop the simulation

        grid = update_grid(grid)  # Update the grid
        screen.fill(BLACK)
        draw_cells(grid)  # Draw the updated grid
        pygame.display.flip() # Draw updated screen
        clock.tick(50)  # Update 50 times per second

    pygame.quit()
    sys.exit()




main()

if __name__ == '__main__':
    main()