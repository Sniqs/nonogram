import pygame
import sys
import pickle

# Screen and block size
SCREEN_TITLE = "Nonogram"
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 1200


# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GREY = (220, 220, 220)
GREY = (190, 190, 190)
DARK_GREY = (119, 119, 119)


# Scale
scale = 1.5
block_size = int(20 * scale)

# Board numbers
numbers_left = [
    [5, -5],
    [3, 5, 3],
    [2, 9, 2],
    [1, 2, 1, 2, 1],
    [1, -11, 1],
    [4, 1, 4],
    [4, 1, 4],
    [-13],
    [6, 6],
    [13],
    [1, 2, 2, 1],
    [-1, 11, 1],
    [2, 9, 2],
    [3, 5, 3],
    [5, 5],
]
numbers_top = [
    [5, 5],
    [3, 5, 3],
    [2, 9, 2],
    [1, -11, 1],
    [1, 1, 6, 2, 1],
    [2, 1, 3, 3],
    [2, 1, 3, 3],
    [-7, 1, 3],
    [2, 1, 3, 3],
    [2, 1, 3, 3],
    [1, 1, 6, 2, 1],
    [1, 11, 1],
    [2, -9, -2],
    [3, 5, 3],
    [5, 5],
]

# Set up the clock
clock = pygame.time.Clock()

# Set up font
pygame.font.init()
font = pygame.font.SysFont("Arial", int(18 * scale))
large_font = pygame.font.SysFont("Arial", int(50 * scale))


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
        square_fill = "empty"
        for y in range(
            block_size * 10,
            (self.blocks_vertically * block_size) + (block_size * 10),
            block_size,
        ):
            row = []
            for x in range(
                block_size * 10,
                (self.blocks_horizontally * block_size) + (block_size * 10),
                block_size,
            ):
                square = pygame.Rect(x, y, block_size - 1, block_size - 1)
                row.append([square, square_fill])
            all_squares.append(row)
        return all_squares

    def draw_board(self):
        """Draws the board on screen."""
        pygame.draw.rect(
            self.game_screen,
            DARK_GREY,
            pygame.Rect(
                (block_size * 10) - 1,
                (block_size * 10) - 1,
                self.blocks_horizontally * block_size + 1,
                self.blocks_vertically * block_size + 1,
            ),
        )

        for row in all_squares:
            for item in row:
                square, square_fill = item
                if square_fill == "empty":
                    square_image = pygame.image.load("empty.png")
                    image = pygame.transform.scale(
                        square_image, (block_size - 1, block_size - 1)
                    )
                elif square_fill == "black":
                    square_image = pygame.image.load("black.png")
                    image = pygame.transform.scale(
                        square_image, (block_size - 1, block_size - 1)
                    )
                elif square_fill == "dot":
                    square_image = pygame.image.load("dot.png")
                    image = pygame.transform.scale(
                        square_image, (block_size - 1, block_size - 1)
                    )
                elif square_fill == "tentative_black":
                    square_image = pygame.image.load("tentative_black.png")
                    image = pygame.transform.scale(
                        square_image, (block_size - 1, block_size - 1)
                    )
                elif square_fill == "tentative_dot":
                    square_image = pygame.image.load("tentative_dot.png")
                    image = pygame.transform.scale(
                        square_image, (block_size - 1, block_size - 1)
                    )
                pygame.draw.rect(self.game_screen, WHITE, square)
                self.game_screen.blit(image, (square.left, square.top))

    def draw_numbers(self):
        """Draws the numbers on the left and top of the board."""

        # Drawing the numbers on the left of the board
        pos_y = block_size * 10
        for i in range(len(numbers_left)):
            pos_x = (block_size * 10) - (block_size * len(numbers_left[i]))
            for j in range(len(numbers_left[i])):
                number = font.render(str(abs(numbers_left[i][j])), True, BLACK)

                if numbers_left[i][j] < 0:
                    number_rect = number.get_rect(
                        left=pos_x - (block_size * 0.25), top=pos_y
                    )
                    slash_image = pygame.image.load("slash.png")
                    image = pygame.transform.scale(
                        slash_image, (block_size - 1, block_size - 1)
                    )
                    self.game_screen.blit(image, (number_rect.left, number_rect.top))

                if abs(numbers_left[i][j]) > 9:
                    self.game_screen.blit(number, (pos_x - (block_size * 0.25), pos_y))
                else:
                    self.game_screen.blit(number, (pos_x, pos_y))
                pos_x += block_size

            pos_y += block_size

        # Drawing the numbers on the top of the board
        pos_x = block_size * 10
        for i in range(len(numbers_top)):
            pos_y = (block_size * 10) - (block_size * len(numbers_top[i]))
            for j in range(len(numbers_top[i])):
                number = font.render(str(abs(numbers_top[i][j])), True, BLACK)

                if numbers_top[i][j] < 0:
                    number_rect = number.get_rect(left=pos_x, top=pos_y)
                    slash_image = pygame.image.load("slash.png")
                    image = pygame.transform.scale(
                        slash_image, (block_size - 1, block_size - 1)
                    )
                    self.game_screen.blit(image, (number_rect.left, number_rect.top))

                if abs(numbers_top[i][j]) > 9:
                    self.game_screen.blit(number, (pos_x, pos_y))
                else:
                    self.game_screen.blit(number, (pos_x + (block_size * 0.25), pos_y))
                pos_y += block_size

            pos_x += block_size

    def show_message(self, message_text):
        """Shows a large message at the center of the screen

        Args:
            message_text (str): Text of the message to display
        """
        text = large_font.render(message_text, True, BLACK)
        rect = self.game_screen.get_rect()
        text_rect = text.get_rect(center=(rect.center))
        bg_rect = text_rect.inflate(block_size / 4, block_size / 4)
        pygame.draw.rect(self.game_screen, BLACK, bg_rect)
        pygame.draw.rect(self.game_screen, WHITE, text_rect)
        self.game_screen.blit(text, text_rect)
        pygame.display.update()
        clock.tick(self.TICK_RATE / 60)

    def scale_board(self, scale):
        """Changes all global variables necessary to zoom the board in and out

        Args:
            scale (float): Target scale of the board
        """

        global block_size
        global font
        global large_font
        global load_button
        global save_button
        global up_scale_button
        global down_scale_button

        block_size = int(20 * scale)
        font = pygame.font.SysFont("Arial", int(18 * scale))
        large_font = pygame.font.SysFont("Arial", int(50 * scale))
        load_button = Button(block_size / 2, block_size / 2, "LOAD")
        save_button = Button(block_size * 5, block_size / 2, "SAVE")
        up_scale_button = Button(block_size * 9.5, block_size / 2, "+")
        down_scale_button = Button(block_size * 14, block_size / 2, "-")

        i = 0
        j = 0

        for y in range(
            block_size * 10,
            (self.blocks_vertically * block_size) + (block_size * 10),
            block_size,
        ):
            row = []

            for x in range(
                block_size * 10,
                (self.blocks_horizontally * block_size) + (block_size * 10),
                block_size,
            ):
                square = pygame.Rect(x, y, block_size - 1, block_size - 1)
                all_squares[i][j][0] = square
                if j == self.blocks_horizontally - 1:
                    j = 0
                else:
                    j += 1
            i += 1

    def check_number_of_squares(self):
        square_map = []
        filled_squares = []
        filled_row = []
        number = 0

        for row in all_squares:
            row_map = []
            for item in row:
                if item[1] == "black":
                    row_map.append(1)
                else:
                    row_map.append(0)
            square_map.append(row_map)

        # TODO: Add 1s in rows (0 resets count) to get the number of consecutive black squares then compare to numbers_left

        for row in square_map:
            filled_row = []
            for square in row:
                if square == 1:
                    number += 1
                else:
                    if number != 0:
                        filled_row.append(number)
                        number = 0
                    else:
                        continue
            if number != 0:
                filled_row.append(number)
            number = 0
            filled_squares.append(filled_row)

        print(filled_squares)

    def run_game_loop(self):
        """Runs the main game loop."""

        global all_squares
        global scale

        is_game_over = False

        with open("save_game.sav", "rb") as f:  # TODO: remove these two lines
            all_squares = pickle.load(f)

        # Main game loop
        while not is_game_over:

            # Prevent infinite loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_game_over = True

                # Handle mouse click events
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if load_button.button_clicked(event.pos):
                        try:
                            with open("save_game.sav", "rb") as f:
                                all_squares = pickle.load(f)
                                self.scale_board(scale)
                                self.draw_board()

                        except:
                            self.show_message("Load unsuccessful")
                        else:
                            self.show_message("Game Loaded")

                    if save_button.button_clicked(event.pos):
                        try:
                            with open("save_game.sav", "wb") as f:
                                pickle.dump(all_squares, f)
                        except:
                            self.show_message("Save unsuccessful")
                        else:
                            self.show_message("Game Saved")

                    if up_scale_button.button_clicked(event.pos):
                        scale += 0.1
                        self.scale_board(scale)

                    if down_scale_button.button_clicked(event.pos):
                        scale -= 0.1
                        self.scale_board(scale)

                    # Check which square was clicked and change its color on the list
                    for row in all_squares:
                        for item in row:
                            square, square_fill = item
                            if square.collidepoint(event.pos):
                                if square_fill == "empty":
                                    item[1] = "black"
                                elif square_fill == "black":
                                    item[1] = "dot"
                                else:
                                    item[1] = "empty"

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    # Check which square was clicked and change its color on the list
                    for row in all_squares:
                        for item in row:
                            square, square_fill = item
                            if square.collidepoint(event.pos):
                                if square_fill == "empty":
                                    item[1] = "tentative_black"
                                elif square_fill == "tentative_black":
                                    item[1] = "tentative_dot"
                                else:
                                    item[1] = "empty"

            # Redraw screen
            self.game_screen.fill(WHITE)
            self.draw_board()
            self.draw_numbers()
            self.check_number_of_squares()
            load_button.draw_button(self.game_screen)
            save_button.draw_button(self.game_screen)
            up_scale_button.draw_button(self.game_screen)
            down_scale_button.draw_button(self.game_screen)

            # Update display
            pygame.display.update()
            clock.tick(self.TICK_RATE)


class Button:
    def __init__(self, x_pos, y_pos, button_text):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.button_text = button_text
        self.button = pygame.Rect(
            self.x_pos, self.y_pos, block_size * 4, block_size * 2
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
new_game = Game(SCREEN_TITLE, SCREEN_WIDTH, SCREEN_HEIGHT, 5, 5)
load_button = Button(block_size / 2, block_size / 2, "LOAD")
save_button = Button(block_size * 5, block_size / 2, "SAVE")
up_scale_button = Button(block_size * 9.5, block_size / 2, "+")
down_scale_button = Button(block_size * 14, block_size / 2, "-")
all_squares = new_game.create_blank_board()
new_game.run_game_loop()

# Quit pygame and program
pygame.quit()
sys.exit()
