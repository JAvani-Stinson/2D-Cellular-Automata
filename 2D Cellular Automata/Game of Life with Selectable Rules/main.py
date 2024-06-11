import pygame
import random
import os
from datetime import datetime

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

#font, content, and dimensions of the rule buttons
font = pygame.font. SysFont('Georgia', 20, bold = True)

conway_surf = font.render("Conway's Game", True, "white")

conway_surf_contin = font.render("of Life", True, "white")
conway_btn = pygame.Rect(WIDTH+10, 10, 180, 70)

brian_surf = font.render("Brian's Brain", True, "white")
brian_btn = pygame.Rect(WIDTH+10, 90, 180, 70)

fred_surf = font.render("Fredkin", True, "white")
fred_btn = pygame.Rect(WIDTH+10, 170, 180, 70)

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
    
    def bring_to_life(self):
        self.status = 1
        self.color = "black"

    #for Brian's Brain
    def dying(self):
        self.status = -1
        self.color = "grey"

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
            pygame.draw.rect(screen, BLACK, (*top_left, TILE_SIZE, TILE_SIZE))
        elif cells["{}, {}".format(col, row)].status == -1:
            pygame.draw.rect(screen, GREY, (*top_left, TILE_SIZE, TILE_SIZE))
    
    #draws the lines for the grid
    for row in range(GRID_HEIGHT):
        pygame.draw.line(screen, GREY, (0, row*TILE_SIZE), (WIDTH, row * TILE_SIZE))
    for col in range(GRID_WIDTH):
        pygame.draw.line(screen, GREY, (col * TILE_SIZE, 0), (col * TILE_SIZE, HEIGHT))
    pygame.draw.line(screen, GREY, ((col + 1) * TILE_SIZE, 0), ((col + 1) * TILE_SIZE, HEIGHT))
    
    #Adds conway's button
    pygame.draw.rect(screen, "blue", conway_btn)
    screen.blit(conway_surf, (conway_btn.x + 10, conway_btn.y + 10))
    screen.blit(conway_surf_contin, (conway_btn.x + 57, conway_btn.y + 35))

    #adds Brian's button
    pygame.draw.rect(screen, "blue", brian_btn)
    screen.blit(brian_surf, (brian_btn.x + 20, brian_btn.y + 23))

    #add fredkin's button
    pygame.draw.rect(screen, "blue", fred_btn)
    screen.blit(fred_surf, (fred_btn.x + 50, fred_btn.y + 23))

#rule_set for Fredkin
def fredkin_adjust_grid(positions, cells):
    all_neighbors = set()
    new_positions = set()

    #gets the neighbors of the living cells
    for position in positions:
        neighbors = get_neighbors(position)
        all_neighbors.update(neighbors)

        neighbors = list(filter(lambda x: x in positions, neighbors))

        #checks if a living cells had 2 or 3 living neighbors to make it living on new grid
        if len(neighbors) % 2 == 1:
            new_positions.add(position)
    
    #checks the neighbor's neighbors
    for position in all_neighbors:
        neighbors = get_neighbors(position)

        neighbors = list(filter(lambda x: x in positions, neighbors))

        #if that neighbor had 3 living cells as neighbors, it brings it alive on the new grid
        if len(neighbors) % 2 == 1:
            new_positions.add(position)

    #resets the cells
    cells = new_cells_obj()

    #updates the objects for the living cells
    for position in new_positions:
        col, row = position
        cells["{}, {}".format(col, row)].status = 1

    return (new_positions, cells)



#rule_set for brian's brain
def brian_adjust_grid(positions, cells):
    all_neighbors = set()
    new_positions = set()
    
    #makes new dict of cell objects for the new grid
    new_cells = new_cells_obj()

    #update cells that were already initialized
    for cell in cells:
        #living > dying
        if cells[cell].status == 1:
            new_cells["{}, {}".format(cells[cell].i, cells[cell ].j)].status = -1
        #dying > dead
        elif cells[cell].status == -1:
            new_cells["{}, {}".format(cells[cell].i, cells[cell ].j)].status = 0

    #adds dying cells to new_positions (adds formerly living cells to new grid)
    for cell in new_cells:
        if new_cells[cell].status == -1:
            new_positions.add((new_cells[cell].i, new_cells[cell].j))

    #gets the neighbors for the formerly living cells
    for position in positions:
        neighbors = get_neighbors(position)
        all_neighbors.update(neighbors)

    #starts to update the neighbors if necessary
    for pos in all_neighbors:
        i, j = pos
        #gets the neighbor's neighbors
        neigh = get_neighbors(pos)
        live_neighbors = 0

        #checks the number of living cells that neighbor had around it
        for neighbor in neigh:
            col, row = neighbor
            if cells["{}, {}".format(col, row)].status == 1:
                live_neighbors += 1
            
        #Adds new living cells according to "come alive" condition
        if live_neighbors == 2:
            new_positions.add(pos)
            new_cells["{}, {}".format(i, j)].status = 1
        
    return (new_positions, new_cells)

#rule_set for Conway's Game of Life
def conway_adjust_grid(positions, cells):
    all_neighbors = set()
    new_positions = set()

    #gets the neighbors of the living cells
    for position in positions:
        neighbors = get_neighbors(position)
        all_neighbors.update(neighbors)

        neighbors = list(filter(lambda x: x in positions, neighbors))

        #checks if a living cells had 2 or 3 living neighbors to make it living on new grid
        if len(neighbors) in [2,3]:
            new_positions.add(position)
    
    #checks the neighbor's neighbors
    for position in all_neighbors:
        neighbors = get_neighbors(position)

        neighbors = list(filter(lambda x: x in positions, neighbors))

        #if that neighbor had 3 living cells as neighbors, it brings it alive on the new grid
        if len(neighbors) == 3:
            new_positions.add(position)

    #resets the cells
    cells = new_cells_obj()

    #updates the objects for the living cells
    for position in new_positions:
        col, row = position
        cells["{}, {}".format(col, row)].status = 1

    return (new_positions, cells)

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
    dirvid = '/Users/jstinson/Desktop/2D Cellular Automata/Game of Life with Selectable Rules/Images'
    fullpath = dirvid + "//" + "%08d.png"%num
    pygame.image.save(screen, fullpath)
    return num

#turns the saved images into a movie
def make_mp4():
    vid_output = '//Users//jstinson//Desktop//2D Cellular Automata/Game of Life with Selectable Rules//Videos//CA ' + str(datetime.now()) + '.mp4'
    os.system("ffmpeg -r 1 -i '//Users//jstinson//Desktop//2D Cellular Automata/Game of Life with Selectable Rules//Images//%08d.png' -vcodec mpeg4 -q:v 0 -y '{}'".format(vid_output))

#starts the game
def main():

    #sStarts the game (as Conway) in a paused state and gives the "speed" of play
    running = True
    playing = False
    count = 0
    update_freq = 30
    num = 0
    rule_set = "Conway's Game of Life"

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
            
            #determines the rule_set
            if rule_set == "Conway's Game of Life":
                (positions, cells) = conway_adjust_grid(positions, cells)
            elif rule_set == "Brian's Brain":
                (positions, cells) = brian_adjust_grid(positions, cells)
            elif rule_set == "Fredkin":
                (positions, cells) = fredkin_adjust_grid(positions, cells)
        
        #initializes a way to see if the game is progressing
        if playing:
            status = "Playing"
        else:
            status = "Paused"

        #shows player what the rules are and if the game is proceeding
        pygame.display.set_caption("{}: {}".format(rule_set, status))

        #checks for clicks
        for event in pygame.event.get():
            
            #quits game
            if event.type == pygame.QUIT:
                running = False

            #checks to see if the player clicked the button to change rules
            if event.type == pygame.MOUSEBUTTONDOWN:
                if conway_btn.collidepoint(event.pos):
                    rule_set = "Conway's Game of Life"

                if brian_btn.collidepoint(event.pos):
                    rule_set = "Brian's Brain"

                if fred_btn.collidepoint(event.pos):
                    rule_set = "Fredkin"

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
