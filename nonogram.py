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
font = pygame.font.SysFont("comicsans", 75)

class Game:

    TICK_RATE = 30

    def __init__ (self, title, width, height, blocks_horizontally, blocks_vertically):
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
            for x in range(200, self.blocks_horizontally * BLOCK_SIZE + 200, BLOCK_SIZE):
                rect = pygame.Rect(x, y, BLOCK_SIZE-1, BLOCK_SIZE-1)
                row.append([rect, WHITE])            
            all_squares.append(row)
        return all_squares
        
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
                    # check which rect was clicked and change its color on list
                    for row in all_squares:
                        for item in row:
                            rect, color = item
                            if rect.collidepoint(event.pos):
                                if color == WHITE:
                                    item[1] = BLACK
                                else:
                                    item[1] = WHITE


                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    # check which rect was clicked and change its color on list
                    for row in all_squares:
                        for item in row:
                            rect, color = item
                            if rect.collidepoint(event.pos):
                                if color == WHITE:
                                    item[1] = LIGHT_GREY
                                else:
                                    item[1] = WHITE
                              

            # Redraw screen
            self.game_screen.fill(WHITE)
            pygame.draw.rect(self.game_screen, DARK_GREY, pygame.Rect(199, 199, self.blocks_horizontally * BLOCK_SIZE + 1, self.blocks_vertically * BLOCK_SIZE + 1))
            
            for row in all_squares:
                for item in row:
                    rect, color = item
                    pygame.draw.rect(self.game_screen, color, rect)
            
          

        

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