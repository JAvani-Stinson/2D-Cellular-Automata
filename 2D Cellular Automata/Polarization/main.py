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
LBLUE = (173, 216, 230)

#initial conditions for the playable grid
WIDTH, HEIGHT = 900, 900
TILE_SIZE = 10
GRID_WIDTH = WIDTH // TILE_SIZE
GRID_HEIGHT = HEIGHT // TILE_SIZE
FPS = 60

#makes font and buttons
font = pygame.font. SysFont('Monocraft', 20, bold = True)

black_surf = font.render("Black", True, "white")
black_btn = pygame.Rect(WIDTH+10, 10, 180, 70)

grey_surf = font.render("Grey", True, "white")
grey_btn = pygame.Rect(WIDTH+10, 90, 180, 70)

#initializes the screen and clock
screen = pygame.display.set_mode((WIDTH+200,HEIGHT))

clock = pygame.time.Clock()

#Create a class for the cells by location on grid
class Cell:
    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.status = 0
        self.color = "white"

    def get_energy(self, cells):
        energy = 0
        for place in [(0, -1), (0, 1), (1, 0), (-1, 0)]:
            a, b = place
            if cells["{}, {}".format((self.i + a) % GRID_WIDTH, (self.j + b) % GRID_HEIGHT)].status == 0:
                energy += 0
            elif cells["{}, {}".format((self.i + a) % GRID_WIDTH, (self.j + b) % GRID_HEIGHT) ].status == self.status:
                energy -= 1
            else:
                energy += 1
        return energy
                    
#get energy of the grid
def get_total_energy(cells, positions):
    energy = 0
    for position in positions:
        i, j = position
        energy += cells["{}, {}".format(i, j)].get_energy(cells)
    return energy

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
        color = random.choice([1,2])
        cells["{}, {}".format(col, row)].status = color

    return (positions, cells)

#Visually adds tiles to the grid
def draw_grid(positions, cells):
    for position in positions:
        col, row = position
        top_left = (col * TILE_SIZE, row * TILE_SIZE)

        #specifies the color of a given tile
        if cells["{}, {}".format(col, row)].status == 1:
            pygame.draw.rect(screen, BLACK, (*top_left, TILE_SIZE, TILE_SIZE))
        elif cells["{}, {}".format(col, row)].status == 2:
            pygame.draw.rect(screen, GREY, (*top_left, TILE_SIZE, TILE_SIZE))
    
    #draws the lines for the grid
    pygame.draw.line(screen, GREY, ((GRID_HEIGHT) * TILE_SIZE, 0), ((GRID_HEIGHT) * TILE_SIZE, HEIGHT))

    #adds black button
    pygame.draw.rect(screen, "blue", black_btn)
    screen.blit(black_surf, (black_btn.x + 60, black_btn.y + 23))

    #adds grey button
    pygame.draw.rect(screen, "blue", grey_btn)
    screen.blit(grey_surf, (grey_btn.x + 65, grey_btn.y + 23))

def check_energies(position, orig_status, positions, new_positions, directions, cells):
    col, row = position

    for i in range(len(directions)):
        if directions[i][1] == "left":
            x = (col - 1) % GRID_WIDTH
            y = row
        elif directions[i][1] == "right":
            x = (col + 1) % GRID_WIDTH
            y = row
        elif directions[i][1] == "up":
            y = (row - 1) % GRID_HEIGHT
            x = col
        elif directions[i][1] == "down":
            y = (row + 1) % GRID_HEIGHT
            x = col
        elif directions[i][1] == "leftup":
            x = (col - 1) % GRID_WIDTH
            y = (row - 1) % GRID_HEIGHT
        elif directions[i][1] == "leftdown":
            x = (col - 1) % GRID_WIDTH
            y = (row + 1) % GRID_HEIGHT
        elif directions[i][1] == "rightup":
            x = (col + 1) % GRID_WIDTH
            y = (row - 1) % GRID_HEIGHT
        elif directions[i][1] == "rightdown":
            x = (col + 1) % GRID_WIDTH
            y = (row + 1) % GRID_HEIGHT

        if directions[i][1] != "stay" and (x, y) not in new_positions and (x,y) not in positions:
            cells["{}, {}".format(col, row)].status = 0
            cells["{}, {}".format(x, y)].status = orig_status
            directions[i] = (cells["{}, {}".format(x, y)].get_energy(cells), directions[i][1])
            cells["{}, {}".format(x, y)].status = 0
            cells["{}, {}".format(col, row)].status = orig_status
        
    directions.sort()
    print(directions)

    return directions



#rule_set for Conway's Game of Life
def adjust_grid(positions, cells):
    new_positions = set()
    new_cells = new_cells_obj()
            
    for position in positions:
        col, row = position

        #initializes some high energies 
        directions = [(100, "left"), (100, "right"), (100, "up"), (100, "down"), (100, "leftup"), (100, "leftdown"), (100, "rightup"), (100, "rightdown"), (cells["{}, {}".format(col, row)].get_energy(cells), "stay")]
        
        orig_status = cells["{}, {}".format(col, row)].status

        #iterates over all possible directions to move to.
        directions = check_energies(position, orig_status, positions, new_positions, directions, cells)
                
        if directions[0][1] == "left":
            new_positions.add(((col - 1) % GRID_WIDTH, row))
            new_cells["{}, {}".format((col - 1) % GRID_WIDTH, row)].status = orig_status
        elif directions[0][1] == "right":
            new_positions.add(((col + 1) % GRID_WIDTH, row))
            new_cells["{}, {}".format((col + 1) % GRID_WIDTH, row)].status = orig_status
        elif directions[0][1] == "up":
            new_positions.add((col, (row - 1) % GRID_HEIGHT))
            new_cells["{}, {}".format(col, (row - 1) % GRID_HEIGHT)].status = orig_status
        elif directions[0][1] == "down":
            new_positions.add((col, (row + 1) % GRID_HEIGHT))
            new_cells["{}, {}".format(col, (row + 1) % GRID_HEIGHT)].status = orig_status
        elif directions[0][1] == "leftup":
            new_positions.add(((col - 1) % GRID_WIDTH, (row - 1) % GRID_HEIGHT))
            new_cells["{}, {}".format((col - 1) % GRID_WIDTH, (row - 1) % GRID_HEIGHT)].status = orig_status
        elif directions[0][1] == "leftdown":
            new_positions.add(((col - 1) % GRID_WIDTH, (row + 1) % GRID_HEIGHT))
            new_cells["{}, {}".format((col - 1) % GRID_WIDTH, (row + 1) % GRID_HEIGHT)].status = orig_status
        elif directions[0][1] == "rightup":
            new_positions.add(((col + 1) % GRID_WIDTH, (row - 1) % GRID_HEIGHT))
            new_cells["{}, {}".format((col + 1) % GRID_WIDTH, (row - 1) % GRID_HEIGHT)].status = orig_status
        elif directions[0][1] == "rightdown":
            new_positions.add(((col + 1) % GRID_WIDTH, (row - 1) % GRID_HEIGHT))
            new_cells["{}, {}".format((col + 1) % GRID_WIDTH, (row - 1) % GRID_HEIGHT)].status = orig_status
        else:
            new_positions.add(position)
            new_cells["{}, {}".format(col, row)].status = orig_status

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
    dirvid = '/Users/jstinson/Desktop/2D Cellular Automata/Polarization/Images'
    fullpath = dirvid + "//" + "%08d.png"%num
    pygame.image.save(screen, fullpath)
    return num

#turns the saved images into a movie
def make_mp4():
    vid_output = '//Users//jstinson//Desktop//2D Cellular Automata/Polarization//Videos//CA ' + str(datetime.now()) + '.mp4'
    os.system("ffmpeg -r 1 -i '//Users//jstinson//Desktop//2D Cellular Automata/Polarization//Images//%08d.png' -vcodec mpeg4 -q:v 0 -y '{}'".format(vid_output))

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

    #initializes a color to add
    add_color = "black"

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
            positions, cells = adjust_grid(positions, cells)
        
        #initializes a way to see if the game is progressing
        if playing:
            status = "Playing"
        else:
            status = "Paused"

        #shows player what the rules are and if the game is proceeding
        pygame.display.set_caption("{}: Add color {}".format(status, add_color))

        #checks for clicks
        for event in pygame.event.get():
            
            #quits game
            if event.type == pygame.QUIT:
                running = False

            #checks to see if the player clicked the button to change chosen color
            if event.type == pygame.MOUSEBUTTONDOWN:
                if black_btn.collidepoint(event.pos):
                    add_color = "black"

                if grey_btn.collidepoint(event.pos):
                    add_color = "grey"

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
                        if add_color == "black":
                            cells["{}, {}".format(col, row)].status = 1
                        elif add_color == "grey":
                            cells["{}, {}".format(col, row)].status = 2

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
                    (positions, cells) = gen(random.randrange(10, 15) * GRID_WIDTH)

        #displays everything
        screen.fill(LBLUE)
        draw_grid(positions, cells)
        pygame.display.update()

    #creates movie when the game is exited
    make_mp4()

    #empties images folder
    files = glob.glob('/Users/jstinson/Desktop/2D Cellular Automata/Polarization/Images/*')
    for f in files:
        os.remove(f)

    pygame.quit()

if __name__ == "__main__":
    main()