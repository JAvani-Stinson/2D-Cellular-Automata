import pygame
import random
import os
from datetime import datetime
import glob

#initiate pygame
pygame.init()

#Create some colors to reference later
BLACK = (0,0,0)
WHITE = (255, 255, 255)
GREY = (128, 128, 128)

#initial conditions for the playable grid
WIDTH, HEIGHT = 800, 800
TILE_SIZE = 20
GRID_WIDTH = WIDTH // TILE_SIZE
GRID_HEIGHT = HEIGHT // TILE_SIZE
FPS = 60

#initializes the screen and clock
screen = pygame.display.set_mode((WIDTH+200,HEIGHT))

clock = pygame.time.Clock()

#Create a class for the cells by location on grid
class Cell:
    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.cyto_determ = [(0, "a"), (0, "b"), (0, "c"), (0, "d"), (0, "e")]
        self.type = ""
        self.replications = 0

#resets the cell objects for the grid that can be used to clear the old
def new_cells_obj():
    cells = {}
    for i in range(GRID_WIDTH):
        for j in range(GRID_HEIGHT):
            cells["{}, {}".format(i, j)] = Cell(i, j)
    return cells


#Generates a random play grid
def gen(num):

    #creates a copy of cell objects
    cells = new_cells_obj()

    #randomly generation positions within grid restraints
    positions = set([(random.randrange(0, GRID_HEIGHT), random.randrange(0, GRID_WIDTH)) for _ in range(num)])

    #updates the new cell objects
    for position in positions:
        (col, row) = position
        cells["{}, {}".format(col, row)].status = 1

    return (positions, cells)

#Visually adds tiles to the grid
def draw_grid(positions, cells):
    for position in positions:
        col, row = position
        top_left = (col * TILE_SIZE, row * TILE_SIZE)

        #specifies the color of a given tile
        x = sorted(cells["{}, {}".format(col, row)].cyto_determ)
        if x[0][1] == "a":
            pygame.draw.rect(screen, (0,0,200), (*top_left, TILE_SIZE, TILE_SIZE))
        elif x[0][1] == "b":
            pygame.draw.rect(screen, (0, 12, 80), (*top_left, TILE_SIZE, TILE_SIZE))
        elif x[0][1] == "c":
            pygame.draw.rect(screen, (12, 120, 5), (*top_left, TILE_SIZE, TILE_SIZE))
        elif x[0][1] == "d":
            pygame.draw.rect(screen, (190, 200, 210), (*top_left, TILE_SIZE, TILE_SIZE))
        elif x[0][1] == "e":
            pygame.draw.rect(screen, (95, 0, 142), (*top_left, TILE_SIZE, TILE_SIZE))
        else:
            pygame.draw.rect(screen, (255, 255, 255), (*top_left, TILE_SIZE, TILE_SIZE))
    
    #draws the lines for the grid
    for row in range(GRID_HEIGHT):
        pygame.draw.line(screen, GREY, (0, row*TILE_SIZE), (WIDTH, row * TILE_SIZE))
    for col in range(GRID_WIDTH):
        pygame.draw.line(screen, GREY, (col * TILE_SIZE, 0), (col * TILE_SIZE, HEIGHT))
    pygame.draw.line(screen, GREY, ((col + 1) * TILE_SIZE, 0), ((col + 1) * TILE_SIZE, HEIGHT))

#rule_set for Conway's Game of Life
def adjust_grid(positions, cells):
    update_set = set([(random.randrange(0, GRID_HEIGHT), random.randrange(0, GRID_WIDTH)) for _ in range(100)])
    dup_location = random.randrange(4)
    new_positions = set()
    new_cells = dict(cells)

    for position in positions:
        new_positions.add(position)

    for position in positions:
        col, row = position
        if position in update_set:
            if cells["{}, {}".format(col, row)].replications != 0 and cells["{}, {}".format(col, row)].cyto_determ != 0:
                x = cells["{}, {}".format(col, row)].cyto_determ
                cyto_split_a =  random.randrange(0, x[0][0] + 1)
                cyto_split_b =  random.randrange(0, x[1][0] + 1)
                cyto_split_c =  random.randrange(0, x[2][0] + 1)
                cyto_split_d =  random.randrange(0, x[3][0] + 1)
                cyto_split_e =  random.randrange(0, x[4][0] + 1)

                if dup_location == 0 and (col - 1, row) not in positions and (col - 1, row) not in new_positions:
                    new_positions.add((col - 1, row))
                    new_positions.add((col, row))
                    new_cells["{}, {}".format(col-1, row)].cyto_determ = [(cyto_split_a, "a"), (cyto_split_b, "b"), (cyto_split_c, "c"), (cyto_split_d, "d"), (cyto_split_e, "e")]
                    new_cells["{}, {}".format(col, row)].cyto_determ = [(x[0][0] - cyto_split_a, "a"), (x[1][0] - cyto_split_b, "b"), (x[2][0] - cyto_split_c, "c"), (x[3][0] - cyto_split_d, "d"), (x[4][0] - cyto_split_e, "e")]
                    new_cells["{}, {}".format(col, row)].replications = cells["{}, {}".format(col, row)].replications - 1
                    new_cells["{}, {}".format(col-1, row)].replications = new_cells["{}, {}".format(col, row)].replications
                
                elif dup_location == 1 and (col + 1, row) not in positions and (col + 1, row) not in new_positions:
                    new_positions.add((col + 1, row))
                    new_positions.add((col, row))
                    new_cells["{}, {}".format(col + 1, row)].cyto_determ = [(cyto_split_a, "a"), (cyto_split_b, "b"), (cyto_split_c, "c"), (cyto_split_d, "d"), (cyto_split_e, "e")]
                    new_cells["{}, {}".format(col, row)].cyto_determ = [(x[0][0] - cyto_split_a, "a"), (x[1][0] - cyto_split_b, "b"), (x[2][0] - cyto_split_c, "c"), (x[3][0] - cyto_split_d, "d"), (x[4][0] - cyto_split_e, "e")]
                    new_cells["{}, {}".format(col, row)].replications = cells["{}, {}".format(col, row)].replications - 1
                    new_cells["{}, {}".format(col + 1, row)].replications = new_cells["{}, {}".format(col, row)].replications

                elif dup_location == 2 and (col, row - 1) not in positions and (col, row - 1) not in new_positions:
                    new_positions.add((col, row - 1))
                    new_positions.add((col, row))
                    new_cells["{}, {}".format(col, row - 1)].cyto_determ = [(cyto_split_a, "a"), (cyto_split_b, "b"), (cyto_split_c, "c"), (cyto_split_d, "d"), (cyto_split_e, "e")]
                    new_cells["{}, {}".format(col, row)].cyto_determ = [(x[0][0] - cyto_split_a, "a"), (x[1][0] - cyto_split_b, "b"), (x[2][0] - cyto_split_c, "c"), (x[3][0] - cyto_split_d, "d"), (x[4][0] - cyto_split_e, "e")]
                    new_cells["{}, {}".format(col, row)].replications = cells["{}, {}".format(col, row)].replications - 1
                    new_cells["{}, {}".format(col, row  - 1)].replications = new_cells["{}, {}".format(col, row)].replications

                elif dup_location == 3 and (col, row + 1) not in positions and (col, row + 1) not in new_positions:
                    new_positions.add((col, row + 1))
                    new_positions.add((col, row))
                    new_cells["{}, {}".format(col, row + 1)].cyto_determ = [(cyto_split_a, "a"), (cyto_split_b, "b"), (cyto_split_c, "c"), (cyto_split_d, "d"), (cyto_split_e, "e")]
                    new_cells["{}, {}".format(col, row)].cyto_determ = [(x[0][0] - cyto_split_a, "a"), (x[1][0] - cyto_split_b, "b"), (x[2][0] - cyto_split_c, "c"), (x[3][0] - cyto_split_d, "d"), (x[4][0] - cyto_split_e, "e")]
                    new_cells["{}, {}".format(col, row)].replications = cells["{}, {}".format(col, row)].replications - 1
                    new_cells["{}, {}".format(col, row  + 1)].replications = new_cells["{}, {}".format(col, row)].replications
    
    return (new_positions, new_cells)

#gathers a cell's Moore neighborhood
def get_neighbors(pos):
    x,y = pos
    neighbors = []
    for dx in [-1,0,1]:
        for dy in [-1,0,1]:
            if dx == 0 and dy == 0:
                continue
        
            #adds neighbors to list
            neighbors.append(((x + dx) % GRID_WIDTH, (y + dy) % GRID_HEIGHT))

    return neighbors

#saves the images for each grid update
def make_png(screen, num):
    num += 1
    dirvid = '/Users/jstinson/Desktop/2D Cellular Automata/Cytoplasmic Determinants/Images'
    fullpath = dirvid + "//" + "%08d.png"%num
    pygame.image.save(screen, fullpath)
    return num

#turns the saved images into a movie
def make_mp4():
    vid_output = '//Users//jstinson//Desktop//2D Cellular Automata/Cytoplasmic Determinants//Videos//CA ' + str(datetime.now()) + '.mp4'
    os.system("ffmpeg -r 1 -i '//Users//jstinson//Desktop//2D Cellular Automata/Cytoplasmic Determinants//Images//%08d.png' -vcodec mpeg4 -q:v 0 -y '{}'".format(vid_output))

#starts the game
def main():

    #sStarts the game (as Conway) in a paused state and gives the "speed" of play
    running = True
    playing = False
    count = 0
    update_freq = 30
    num = 0
    
    #initialized a dictionary of cell objects for the grid
    cells = new_cells_obj()

    #initializes positions
    positions = set()

    #the actual game code
    while running:

        #internal clock
        clock.tick(FPS)

        #checks if the game is no longer paused
        if playing:
            count += 1

        #updates the game according to "speed" set priorly
        if count >= update_freq:
            count = 0

            #takes picture
            num = make_png(screen, num)
            
            #determines the rule_set
            (positions, cells) = adjust_grid(positions, cells)

        #initializes a way to see if the game is progressing
        if playing:
            status = "Playing"
        else:
            status = "Paused"

        #shows player what the rules are and if the game is proceeding
        pygame.display.set_caption("{}".format(status))

        #checks for clicks
        for event in pygame.event.get():
            
            #quits game
            if event.type == pygame.QUIT:
                running = False

            #allows players to add positions with clicks on grid
            if event.type == pygame.MOUSEBUTTONDOWN:

                #translates pixel to grid space (col, row)
                x, y = pygame.mouse.get_pos()
                if x <= WIDTH and y <= HEIGHT:
                    col = x // TILE_SIZE
                    row = y // TILE_SIZE
                    pos = (col, row)
                
                    #checks if cell is already there to remove
                    if pos in positions:
                        positions.remove(pos)
                        cells["{}, {}".format(col, row)].cyto_determ = 0
                        cells["{}, {}".format(col, row)].type = ""

                    #adds cell
                    else:
                        positions.add(pos)
                        cells["{}, {}".format(col, row)].cyto_determ = [(1000,"a"), (1000,"b"), (1000,"c"), (1000,"d"), (1000,"e")]
                        cells["{}, {}".format(col, row)].type = "egg"
                        cells["{}, {}".format(col, row)].replications = 5

            #checks for button presses
            if event.type == pygame.KEYDOWN:

                #allows to pause and play the game
                if event.key == pygame.K_SPACE:
                    playing = not playing

                #clears the board by emptying positions and reseting cells
                if event.key == pygame.K_c:
                    positions = set()
                    cells = new_cells_obj()
                    playing = False
                    count = 0

                #generates a random set of positions
                if event.key == pygame.K_g:
                    (positions, cells) = gen(random.randrange(2, 5) * GRID_WIDTH)

        #displays everything
        screen.fill((255, 255, 0))
        draw_grid(positions, cells)
        pygame.display.update()

    #creates movie when the game is exited
    make_mp4()

    #clears images folder
    files = glob.glob('/Users/jstinson/Desktop/2D Cellular Automata/Cytoplasmic Determinants/Images/*')
    for f in files:
        os.remove(f)

    pygame.quit()

if __name__ == "__main__":
    main()