import pygame
import pygame.math
from board import Board, Reference

# size constants
SIZE = 5
TILE = 50
SPACING = 20
WIDTH = ((SIZE+6)*TILE + (SIZE+5)*SPACING)
HEIGHT = ((SIZE+2)*TILE) + ((SIZE+1)*SPACING)

# setup
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rubik's Race")

# initialize board
board = Board(size=SIZE)
board.shuffle()

reference = Reference(size=SIZE)
reference.shuffle()

# create tiles
player_tiles = [pygame.Surface((TILE, TILE)) for i in range(SIZE**2)]
tile_coordinates = [board.board[i].get_position() for i in range(len(board.board))]
reference_tiles = [pygame.Surface((TILE, TILE)) for i in range(SIZE ** 2)]

# clock
font = pygame.font.SysFont(None, 32)
clock = pygame.time.Clock()
start_time = pygame.time.get_ticks()

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # check for mouse click
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for i in range(len(tile_coordinates)):
                rect = player_tiles[i].get_rect(topleft=tile_coordinates[i])
                if rect.collidepoint(mouse_pos):
                    board.update(i)


    # display tiles
    for i in range(len(player_tiles)):
        # update tile color
        player_tiles[i].fill(board.get_color(i))
        reference_tiles[i].fill(reference.get_color(i))

        # place tiles
        startx = SPACING + TILE
        starty = SPACING + TILE
        x = (SPACING + TILE) * (i % SIZE)
        y = (SPACING + TILE) * (i // SIZE) + starty

        # draw reference tiles
        if i // SIZE != 0 and i // SIZE != SIZE - 1:
            if i % SIZE != 0 and i % SIZE != SIZE - 1:
                screen.blit(reference_tiles[i], (x, y))

        # draw player tiles
        offset = (SIZE)*TILE + (SIZE-1)*SPACING
        tile_coordinates[i] = (x + offset, y)
        screen.blit(player_tiles[i], (tile_coordinates[i]))

    # end game
    if board == reference:
        print('congrats!')
        running = False

    pygame.display.update()
    clock.tick(60)
