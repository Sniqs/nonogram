import pygame
import sys

# Screen and block size
SCREEN_TITLE = "Nonogram"
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
BLOCK_SIZE = 20

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GREY = (220, 220, 220)
GREY = (190, 190, 190)
DARK_GREY = (119, 119, 119)

# Set up the clock
clock = pygame.time.Clock()

# Set up font
pygame.font.init()
font = pygame.font.SysFont("Arial", 18)


class Game:

    TICK_RATE = 30

    def __init__(self, title, width, height, blocks_horizontally, blocks_vertically):
        self.title = title
        self.width = width
        self.height = height
        self.blocks_horizontally = blocks_horizontally
        self.blocks_vertically = blocks_vertically

        # Set up the display
        self.game_screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)

    def create_blank_board(self):
        """Creates a blank board

        Returns:
            list: list of all white squares
        """

        all_squares = []
        for y in range(200, self.blocks_vertically * BLOCK_SIZE + 200, BLOCK_SIZE):
            row = []
            for x in range(
                200, self.blocks_horizontally * BLOCK_SIZE + 200, BLOCK_SIZE
            ):
                square = pygame.Rect(x, y, BLOCK_SIZE - 1, BLOCK_SIZE - 1)
                row.append([square, WHITE])
            all_squares.append(row)
        return all_squares

    def draw_board(self):
        pygame.draw.rect(
            self.game_screen,
            DARK_GREY,
            pygame.Rect(
                199,
                199,
                self.blocks_horizontally * BLOCK_SIZE + 1,
                self.blocks_vertically * BLOCK_SIZE + 1,
            ),
        )

        for row in all_squares:
            for item in row:
                square, color = item
                pygame.draw.rect(self.game_screen, color, square)

    def draw_numbers(self):
        numbers_left = [[1, 2, 3], [15, 3, 2, 5], [2, 4, 2], [3, 8, 12, 5, 25]]
        numbers_top = [[1, 2, 3], [15, 3, 2, 5], [2, 4, 2], [3, 8, 12, 5, 25]]

        pos_y = 200

        # Drawing the numbers on the left of the board
        for i in range(len(numbers_left)):
            pos_x = 200 - (20 * len(numbers_left[i]))
            for j in range(len(numbers_left[i])):
                number = font.render(str(numbers_left[i][j]), True, BLACK)
                if numbers_left[i][j] > 9:
                    self.game_screen.blit(number, (pos_x - 6, pos_y))
                else:
                    self.game_screen.blit(number, (pos_x, pos_y))
                pos_x += 20

            pos_y += 20

        # Drawing the numbers on the top of the board
        pos_x = 200
        pos_y = 200

        for i in range(len(numbers_top)):
            pos_y = 200 - (20 * len(numbers_top[i]))
            for j in range(len(numbers_top[i])):
                number = font.render(str(numbers_top[i][j]), True, BLACK)
                if numbers_top[i][j] > 9:
                    self.game_screen.blit(number, (pos_x, pos_y))
                else:
                    self.game_screen.blit(number, (pos_x + 6, pos_y))
                pos_y += 20

            pos_x += 20

    def run_game_loop(self):
        is_game_over = False
        did_win = False

        # Main game loop
        while not is_game_over:

            # Prevent infinite loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_game_over = True

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # Check which square was clicked and change its color on the list
                    for row in all_squares:
                        for item in row:
                            square, color = item
                            if square.collidepoint(event.pos):
                                if color == WHITE:
                                    item[1] = BLACK
                                else:
                                    item[1] = WHITE

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    # Check which square was clicked and change its color on the list
                    for row in all_squares:
                        for item in row:
                            square, color = item
                            if square.collidepoint(event.pos):
                                if color == WHITE:
                                    item[1] = LIGHT_GREY
                                else:
                                    item[1] = WHITE

            # Redraw screen
            self.game_screen.fill(WHITE)
            self.draw_board()
            self.draw_numbers()

            # Update display
            pygame.display.update()
            clock.tick(self.TICK_RATE)


pygame.init()
new_game = Game(SCREEN_TITLE, SCREEN_WIDTH, SCREEN_HEIGHT, 30, 30)
all_squares = new_game.create_blank_board()
new_game.run_game_loop()

# Quit pygame and program
pygame.quit()
sys.exit()
