import pygame
import sys

# Screen size
SCREEN_TITLE = "Nonogram"
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
BLOCK_WIDTH = 50
BLOCK_HEIGHT = 50


# Colors
WHITE_COLOR = (255, 255, 255)
BLACK_COLOR = (0, 0, 0)

# Set up the clock
clock = pygame.time.Clock()

# Set up font
pygame.font.init()
font = pygame.font.SysFont("comicsans", 75)

class Game:
    TICK_RATE = 60

    tile_map = [[1, 1, 1, 1], [1, 0, 0, 0], [1, 0, 1, 0], [1, 0, 0, 0]]


    def __init__ (self, title, width, height):
        self.title = title
        self.width = width
        self.height = height

        # Set up the display
        self.game_screen = pygame.display.set_mode((width, height))
        self.game_screen.fill(WHITE_COLOR)
        pygame.display.set_caption(title)

    def get_tile_color(self, tile_contents):
        if tile_contents == 0:
            tile_color = WHITE_COLOR
        if tile_contents == 1:
            tile_color = BLACK_COLOR
        return tile_color

      
    def draw_map(self, game_screen, tile_map):
        for j, tile in enumerate(tile_map):
            for i, tile_contents in enumerate(tile):
                myrect = pygame.Rect(i*BLOCK_WIDTH+100, j*BLOCK_HEIGHT+100, BLOCK_WIDTH, BLOCK_HEIGHT)
                pygame.draw.rect(game_screen, self.get_tile_color(tile_contents), myrect)
        
    def run_game_loop(self):
        is_game_over = False
        did_win = False
        

        # Main game loop
        while not is_game_over:

            # Prevent infinite loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_game_over = True

                # Detect key press
                elif event.type == pygame.KEYDOWN:

                    # Set direction to up when pressing "w"
                    if event.key == pygame.K_w:
                        direction = 1

                    # Set direction to down when pressing "w"
                    elif event.key == pygame.K_s:
                        direction = -1


                # Stop movement when key released
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_w or event.key == pygame.K_s:
                        direction = 0


               

            # Redraw blank screen
            self.game_screen.fill(WHITE_COLOR)
            self.draw_map(self.game_screen, self.tile_map)
            
          

        

            # Update display
            pygame.display.update()
            clock.tick(self.TICK_RATE)







pygame.init()

new_game = Game(SCREEN_TITLE, SCREEN_WIDTH, SCREEN_HEIGHT)
new_game.run_game_loop()








# Quit pygame and program
pygame.quit()
sys.exit()
