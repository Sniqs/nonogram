import pygame
import sys
import pickle

# Screen and block size
SCREEN_TITLE = "Nonogram"
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
# TODO: Fix font scaling when block size changes
BLOCK_SIZE = 20

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GREY = (220, 220, 220)
GREY = (190, 190, 190)
DARK_GREY = (119, 119, 119)

# Board numbers
numbers_left = [
    [5, 5],
    [3, 5, 3],
    [2, 9, 2],
    [1, 2, 1, 2, 1],
    [1, 11, 1],
    [4, 1, 4],
    [4, 1, 4],
    [13],
    [6, 6],
    [13],
    [1, 2, 2, 1],
    [1, 11, 1],
    [2, 9, 2],
    [3, 5, 3],
    [5, 5],
]
numbers_top = [
    [5, 5],
    [3, 5, 3],
    [2, 9, 2],
    [1, 11, 1],
    [1, 1, 6, 2, 1],
    [2, 1, 3, 3],
    [2, 1, 3, 3],
    [7, 1, 3],
    [2, 1, 3, 3],
    [2, 1, 3, 3],
    [1, 1, 6, 2, 1],
    [1, 11, 1],
    [2, 9, 2],
    [3, 5, 3],
    [5, 5],
]

# Set up the clock
clock = pygame.time.Clock()

# Set up font
pygame.font.init()
font = pygame.font.SysFont("Arial", 18)
large_font = pygame.font.SysFont("Arial", 50)


class Game:

    TICK_RATE = 30

    def __init__(self, title, width, height, blocks_horizontally, blocks_vertically):
        """Initializes the class

        Args:
            title (str): Title of the game window
            width (int): Width of the game window
            height (int): Height of the game window
            blocks_horizontally (int): Number of blocks on the board, horizontally
            blocks_vertically (int): Number of blocks on the board, vertically
        """
        self.title = title
        self.width = width
        self.height = height
        self.blocks_horizontally = blocks_horizontally
        self.blocks_vertically = blocks_vertically

        # Set up the display
        self.game_screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)

    def create_blank_board(self):
        """Creates a blank board.

        Returns:
            list: List of all white squares
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
        """Draws the board on screen."""
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
        """Draws the numbers on the left and top of the board."""

        # Drawing the numbers on the left of the board
        pos_y = 200
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

    def show_message(self, message_text):
        """Shows a large message at the center of the screen

        Args:
            message_text (str): Text of the message to display
        """
        text = large_font.render(message_text, True, BLACK)
        rect = self.game_screen.get_rect()
        text_rect = text.get_rect(center=(rect.center))
        bg_rect = text_rect.inflate(BLOCK_SIZE / 4, BLOCK_SIZE / 4)
        pygame.draw.rect(self.game_screen, BLACK, bg_rect)
        pygame.draw.rect(self.game_screen, WHITE, text_rect)
        # self.game_screen.blit(text, bg_rect)
        self.game_screen.blit(text, text_rect)
        pygame.display.update()
        clock.tick(self.TICK_RATE / 60)

    def run_game_loop(self):
        """Runs the main game loop."""
        is_game_over = False

        # Main game loop
        while not is_game_over:

            # Prevent infinite loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_game_over = True

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if load_button.button_clicked(event.pos):
                        try:
                            with open("save_game.txt", "rb") as f:
                                global all_squares
                                all_squares = pickle.load(f)
                                self.draw_board()

                        except:
                            self.show_message("Load unsuccessful")
                        else:
                            self.show_message("Game Loaded")

                    if save_button.button_clicked(event.pos):
                        try:
                            with open("save_game.txt", "wb") as f:
                                pickle.dump(all_squares, f)
                        except:
                            self.show_message("Save unsuccessful")
                        else:
                            self.show_message("Game Saved")

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
            load_button.draw_button(self.game_screen)
            save_button.draw_button(self.game_screen)

            # Update display
            pygame.display.update()
            clock.tick(self.TICK_RATE)


class Button:
    def __init__(self, x_pos, y_pos, button_text):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.button_text = button_text
        self.button = pygame.Rect(
            self.x_pos, self.y_pos, BLOCK_SIZE * 4, BLOCK_SIZE * 2
        )

    def draw_button(self, surface):
        """Draws the button on screen

        Args:
            surface (pygame.Surface): Surface on which to draw the button
        """
        pygame.draw.rect(surface, DARK_GREY, self.button)
        text = font.render(self.button_text, True, WHITE)
        text_rect = text.get_rect(center=(self.button.center))
        surface.blit(text, text_rect)

    def button_clicked(self, event_pos):
        """Checks if button was clicked

        Args:
            event_pos (tuple): Position of the mouse click event

        Returns:
            int: Value indicating if button was clicked
        """

        return self.button.collidepoint(event_pos)


pygame.init()
new_game = Game(SCREEN_TITLE, SCREEN_WIDTH, SCREEN_HEIGHT, 15, 15)
load_button = Button(BLOCK_SIZE / 2, BLOCK_SIZE / 2, "LOAD")
save_button = Button(BLOCK_SIZE * 5, BLOCK_SIZE / 2, "SAVE")
all_squares = new_game.create_blank_board()
new_game.run_game_loop()

# Quit pygame and program
pygame.quit()
sys.exit()
