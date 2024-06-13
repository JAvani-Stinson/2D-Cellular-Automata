import pygame
import random
import os
from datetime import datetime

#initiate pygame
pygame.init()

#Create some colors to reference later
BLACK = (0,0,0)
BLUE = (0, 191, 255)
RED = (220, 20, 60)
GOLD = (255, 215,0)
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
GREEN = (0, 255, 0)
PURPLE = (221, 160, 221)

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
        self.status = 0
    

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
        if cells["{}, {}".format(col, row)].status == 1:
            pygame.draw.rect(screen, GOLD, (*top_left, TILE_SIZE, TILE_SIZE))
        elif cells["{}, {}".format(col, row)].status == 2:
            pygame.draw.rect(screen, RED, (*top_left, TILE_SIZE, TILE_SIZE))
        elif cells["{}, {}".format(col, row)].status == 3:
            pygame.draw.rect(screen, BLUE, (*top_left, TILE_SIZE, TILE_SIZE))
        elif cells["{}, {}".format(col, row)].status == 4:
            pygame.draw.rect(screen, GREEN, (*top_left, TILE_SIZE, TILE_SIZE))
        elif cells["{}, {}".format(col, row)].status == 100:
            pygame.draw.rect(screen, PURPLE, (*top_left, TILE_SIZE, TILE_SIZE))
        
    #draws the lines for the grid
    for row in range(GRID_HEIGHT):
        pygame.draw.line(screen, GREY, (0, row*TILE_SIZE), (WIDTH, row * TILE_SIZE))
    for col in range(GRID_WIDTH):
        pygame.draw.line(screen, GREY, (col * TILE_SIZE, 0), (col * TILE_SIZE, HEIGHT))
    pygame.draw.line(screen, GREY, ((col + 1) * TILE_SIZE, 0), ((col + 1) * TILE_SIZE, HEIGHT))
   
#chooses random update_set and rule_set
def adjust_grid(cells):
    new_cells = new_cells_obj()
    new_positions = set()
    update_set = set([(random.randrange(0, GRID_HEIGHT), random.randrange(0, GRID_WIDTH)) for _ in range(100)])

    for i in range(GRID_WIDTH):
        for j in range(GRID_HEIGHT):
            if (i, j) not in update_set:
                if cells["{}, {}".format(i, j)].status != 0:
                    new_positions.add((i, j))
                    new_cells["{}, {}".format(i, j)].status = cells["{}, {}".format(i, j)].status

    for position in update_set:
        col, row = position
        status = cells["{}, {}".format(col, row)].status
        neighbors, kernel_sum = get_neighbors(position, cells)

        if status == 1:
            if kernel_sum >= 8:
                new_positions.add((col, row))
                new_cells["{}, {}".format(col, row)].status = 2

            else:
                stay_alive = random.randrange(0, 100)

                if stay_alive <= 75:
                    new_positions.add((col, row))
                    new_cells["{}, {}".format(col, row)].status = 1

                dup_location = random.randrange(0,4)
                if new_cells["{}, {}".format((col - 1) % GRID_WIDTH, row % GRID_HEIGHT)].status == 0 and dup_location == 0:
                    new_positions.add(((col - 1) % GRID_WIDTH, row % GRID_HEIGHT))
                    new_cells["{}, {}".format((col - 1) % GRID_WIDTH, row % GRID_HEIGHT)].status = 1
                elif new_cells["{}, {}".format((col + 1) % GRID_WIDTH, row % GRID_HEIGHT)].status == 0 and dup_location == 1:
                    new_positions.add(((col + 1) % GRID_WIDTH, row % GRID_HEIGHT))
                    new_cells["{}, {}".format((col + 1) % GRID_WIDTH, row % GRID_HEIGHT)].status = 1
                elif new_cells["{}, {}".format(col % GRID_WIDTH, (row + 1) % GRID_HEIGHT)].status == 0 and dup_location == 2:
                    new_positions.add((col % GRID_WIDTH, (row + 1) % GRID_HEIGHT))
                    new_cells["{}, {}".format(col % GRID_WIDTH, (row + 1) % GRID_HEIGHT)].status = 1
                elif new_cells["{}, {}".format(col % GRID_WIDTH, (row - 1) % GRID_HEIGHT)].status == 0 and dup_location == 3:
                    new_positions.add((col % GRID_WIDTH, (row - 1) % GRID_HEIGHT))
                    new_cells["{}, {}".format(col % GRID_WIDTH, (row - 1) % GRID_HEIGHT)].status = 1

        if status == 2:
            if kernel_sum == 21:
                new_positions.add((col, row))
                new_cells["{}, {}".format(col, row)].status = 3
            elif kernel_sum > 15:
                new_positions.add((col, row))
                new_cells["{}, {}".format(col, row)].status = 4
                
            else:
                new_positions.add((col, row))
                new_cells["{}, {}".format(col, row)].status = 2

                dup_location = random.randrange(0,4)
                if dup_location == 0:
                    if new_cells["{}, {}".format((col - 1) % GRID_WIDTH, row % GRID_HEIGHT)].status == 0:
                        new_positions.add(((col - 1) % GRID_WIDTH, row % GRID_HEIGHT))
                        new_cells["{}, {}".format((col - 1) % GRID_WIDTH, row % GRID_HEIGHT)].status = 1
                    elif new_cells["{}, {}".format((col - 1) % GRID_WIDTH, row % GRID_HEIGHT)].status == 1:
                        new_positions.add(((col - 1) % GRID_WIDTH, row))
                        new_cells["{}, {}".format((col - 1) % GRID_WIDTH, row % GRID_HEIGHT)].status = 2
                elif dup_location == 1:
                    if new_cells["{}, {}".format((col + 1) % GRID_WIDTH, row % GRID_HEIGHT)].status == 0:
                        new_positions.add(((col + 1) % GRID_WIDTH, row % GRID_HEIGHT))
                        new_cells["{}, {}".format((col + 1) % GRID_WIDTH, row % GRID_HEIGHT)].status = 1
                    elif new_cells["{}, {}".format((col + 1) % GRID_WIDTH, row % GRID_HEIGHT)].status == 1:
                        new_positions.add(((col + 1) % GRID_WIDTH, row % GRID_HEIGHT))
                        new_cells["{}, {}".format((col + 1) % GRID_WIDTH, row % GRID_HEIGHT)].status = 2
                elif dup_location == 2:
                    if new_cells["{}, {}".format(col % GRID_WIDTH, (row + 1) % GRID_HEIGHT)].status == 0:
                        new_positions.add((col % GRID_WIDTH, (row + 1) % GRID_HEIGHT))
                        new_cells["{}, {}".format(col % GRID_WIDTH, (row + 1) % GRID_HEIGHT)].status = 1
                    elif new_cells["{}, {}".format(col % GRID_WIDTH, (row + 1) % GRID_HEIGHT)].status == 1:
                        new_positions.add((col % GRID_WIDTH, (row + 1) % GRID_HEIGHT))
                        new_cells["{}, {}".format(col % GRID_WIDTH, (row + 1) % GRID_HEIGHT)].status = 2
                elif dup_location == 3:
                    if new_cells["{}, {}".format(col % GRID_WIDTH, (row - 1) % GRID_HEIGHT)].status == 0:
                        new_positions.add((col % GRID_WIDTH, (row - 1) % GRID_HEIGHT))
                        new_cells["{}, {}".format(col % GRID_WIDTH, (row - 1) % GRID_HEIGHT)].status = 1
                    elif new_cells["{}, {}".format(col % GRID_WIDTH, (row - 1) % GRID_HEIGHT)].status == 1:
                        new_positions.add((col % GRID_WIDTH, (row - 1) % GRID_HEIGHT))
                        new_cells["{}, {}".format(col % GRID_WIDTH, (row - 1) % GRID_HEIGHT)].status = 2

        if status == 4:
            new_positions.add((col, row))
            new_cells["{}, {}".format(col, row)].status = 4

            dup_location = random.randrange(0,4)
            if dup_location == 0:
                if new_cells["{}, {}".format((col - 1) % GRID_WIDTH, row % GRID_HEIGHT)].status not in [0, 1, 3]:
                    new_positions.add(((col - 1) % GRID_WIDTH, row % GRID_HEIGHT))
                    new_cells["{}, {}".format((col - 1) % GRID_WIDTH, row % GRID_HEIGHT)].status = 4
            elif dup_location == 1:
                if new_cells["{}, {}".format((col + 1) % GRID_WIDTH, row % GRID_HEIGHT)].status not in [0, 1, 3]:
                    new_positions.add(((col + 1) % GRID_WIDTH, row % GRID_HEIGHT))
                    new_cells["{}, {}".format((col + 1) % GRID_WIDTH, row % GRID_HEIGHT)].status = 4
            elif dup_location == 2:
                if new_cells["{}, {}".format(col % GRID_WIDTH, (row - 1) % GRID_HEIGHT)].status not in [0, 1, 3]:
                    new_positions.add((col % GRID_WIDTH, (row - 1) % GRID_HEIGHT))
                    new_cells["{}, {}".format(col % GRID_WIDTH, (row - 1) % GRID_HEIGHT)].status = 4
            elif dup_location == 3:
                if new_cells["{}, {}".format(col % GRID_WIDTH, (row + 1) % GRID_HEIGHT)].status not in [0, 1, 3]:
                    new_positions.add((col % GRID_WIDTH, (row + 1) % GRID_HEIGHT))
                    new_cells["{}, {}".format(col % GRID_WIDTH, (row + 1) % GRID_HEIGHT)].status = 4

        if status == 3:
            sum3 = 0
            sum4 = 0
            for neighbor in neighbors:
                a, b = neighbor
                if cells["{}, {}".format(a, b)].status == 3:
                    sum3 += 1
                elif cells["{}, {}".format(a, b)].status == 4:
                    sum4 += 1

            if sum3 == 8:
                new_positions.add((col, row))
                new_cells["{}, {}".format(col, row)].status = 100
            

            else:
                new_positions.add((col, row))
                new_cells["{}, {}".format(col, row)].status = 3
                
                if sum4 == 8:
                    for neighbor in neighbors:
                        a, b = neighbor
                        new_positions.add(neighbor)
                        new_cells["{}, {}".format(a, b)].status = 3

        if status == 100:
            new_positions.add((col, row))
            new_cells["{}, {}".format(col, row)].status = 100

    return (new_positions, new_cells)

#gathers a cell's Moore neighborhood
def get_neighbors(pos, cells):
    x,y = pos
    neighbors = []
    kernel_sum = 0
    for dx in [-1,0,1]:
        for dy in [-1,0,1]:
            if dx == 0 and dy == 0:
                continue
        
            #adds neighbors to list
            neighbors.append(((x + dx) % GRID_WIDTH, (y + dy) % GRID_HEIGHT))
    
    #computes a kernel sum
    for neighbor in neighbors:
            a, b = neighbor
            kernel_sum += cells["{}, {}".format(a, b)].status

    return (neighbors, kernel_sum)

#saves the images for each grid update
def make_png(screen, num):
    num += 1
    dirvid = '/Users/jstinson/Desktop/2D Cellular Automata/Communicating Colonies/Images'
    fullpath = dirvid + "//" + "%08d.png"%num
    pygame.image.save(screen, fullpath)
    return num

#turns the saved images into a movie
def make_mp4():
    vid_output = '//Users//jstinson//Desktop//2D Cellular Automata/Communicating Colonies//Videos//CA ' + str(datetime.now()) + '.mp4'
    os.system("ffmpeg -r 1 -i '//Users//jstinson//Desktop//2D Cellular Automata/Communicating Colonies//Images//%08d.png' -vcodec mpeg4 -q:v 0 -y '{}'".format(vid_output))

#starts the game
def main():

    #sStarts the game (as Conway) in a paused state and gives the "speed" of play
    running = True
    playing = False
    count = 0
    update_freq = 30
    num = 0

    #creates the cell objects for the grid
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
            
            #updates grid
            (positions, cells) = adjust_grid(cells)
        
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
                        cells["{}, {}".format(col, row)].status = 0

                    #adds cell
                    else:
                        positions.add(pos)
                        cells["{}, {}".format(col, row)].status = 1

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
        screen.fill(WHITE)
        draw_grid(positions, cells)
        pygame.display.update()

    #creates movie when the game is exited
    make_mp4()

    pygame.quit()

if __name__ == "__main__":
    main()
