import math
import pygame
import random

#Create some colors to reference later
BLACK = (0,0,0)
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
LBLUE = (173, 216, 230)

#initial conditions for the playable grid
WIDTH, HEIGHT = 900, 900
TILE_SIZE = 20
GRID_WIDTH = WIDTH // TILE_SIZE
GRID_HEIGHT = HEIGHT // TILE_SIZE
FPS = 60

pygame.init()

#makes font and buttons
font = pygame.font.SysFont('Monocraft', 20, bold = True)

black_surf = font.render("Black", True, "white")
black_btn = pygame.Rect(WIDTH+10, 170, 180, 70)

grey_surf = font.render("Grey", True, "white")
grey_btn = pygame.Rect(WIDTH+10, 250, 180, 70)

nuc_surf = font.render("Nucleus", True, "white")
nuc_btn = pygame.Rect(WIDTH+10, 10, 180, 70)

pp_surf = font.render("Polarity", True, "white")
pp_surf_contin = font.render("Protein", True, "white")
pp_btn = pygame.Rect(WIDTH+10, 90, 180, 70)

#initializes the screen and clock
screen = pygame.display.set_mode((WIDTH+200,HEIGHT))

clock = pygame.time.Clock()

#Generates a random play grid
def gen(num, grids):

    #creates a copy of cell objects
    cells = new_cells_obj(grids)

    #randomly generation positions within grid restraints
    positions = set([(random.randrange(0, GRID_HEIGHT), random.randrange(0, GRID_WIDTH)) for _ in range(num)])
    polarity_proteins = set([(random.randrange(0, GRID_HEIGHT), random.randrange(0, GRID_WIDTH)) for _ in range(num - 4)])

    #updates the new cell objects
    for position in positions:
        (col, row) = position
        color = random.choice([1,2])
        cells["{}, {}".format(col, row)].status = color
    
    for pp in polarity_proteins:
        (col, row) = pp
        type = random.choice([1,2])
        if type == 1:
            cells["{}, {}".format(col, row)].polarity_protein_A = True
        else:
            cells["{}, {}".format(col, row)].polarity_protein_B = True

    positions = positions.union(polarity_proteins)
    return (positions, cells)

#Visually adds tiles to the grid
def draw_grid(positions, cells, sanity_checks, color_groups, color_grids, split_cells, grids):
    
    if color_grids:
        colors = iter([(255, 192, 203),
                  BLACK, 
                  GREY, 
                  (18, 123, 203), 
                  (150, 100, 38),
                  (200, 0, 100), 
                  (0, 0, 240), 
                  (30, 0, 0), 
                  (189, 18, 244), 
                  (0, 194, 0), 
                  (111, 111, 254)])
        
        for grid in grids:
            color = next(colors)
            for position in grid.positions:
                col, row = position
                top_left = (col * TILE_SIZE, row * TILE_SIZE)
                pygame.draw.rect(screen, color, (*top_left, TILE_SIZE, TILE_SIZE))
    
    for position in positions:
        col, row = position
        top_left = (col * TILE_SIZE, row * TILE_SIZE)

        #specifies the color of a given tile
        if not color_grids:
            if color_groups:
                if cells["{}, {}".format(col, row)].group == 0:
                    pygame.draw.rect(screen, BLACK, (*top_left, TILE_SIZE, TILE_SIZE))
                elif cells["{}, {}".format(col, row)].group == 1:
                    pygame.draw.rect(screen, GREY, (*top_left, TILE_SIZE, TILE_SIZE))
                elif cells["{}, {}".format(col, row)].group == 2:
                    pygame.draw.rect(screen, (255, 192, 203),(*top_left, TILE_SIZE, TILE_SIZE))
                elif cells["{}, {}".format(col, row)].group == 3:
                    pygame.draw.rect(screen, (18, 123, 203),(*top_left, TILE_SIZE, TILE_SIZE))
                elif cells["{}, {}".format(col, row)].group == 4:
                    pygame.draw.rect(screen, (150, 100, 38),(*top_left, TILE_SIZE, TILE_SIZE))
                elif cells["{}, {}".format(col, row)].group == 5:
                    pygame.draw.rect(screen, (200, 0, 100),(*top_left, TILE_SIZE, TILE_SIZE))
                elif cells["{}, {}".format(col, row)].group == 6:
                    pygame.draw.rect(screen, (0, 0, 240),(*top_left, TILE_SIZE, TILE_SIZE))
                elif cells["{}, {}".format(col, row)].group == 7:
                    pygame.draw.rect(screen, (30, 0, 0),(*top_left, TILE_SIZE, TILE_SIZE))
                elif cells["{}, {}".format(col, row)].group == 8:
                    pygame.draw.rect(screen, (189, 18, 244),(*top_left, TILE_SIZE, TILE_SIZE))
                elif cells["{}, {}".format(col, row)].group == 9:
                    pygame.draw.rect(screen, (0, 194, 0),(*top_left, TILE_SIZE, TILE_SIZE))
                elif cells["{}, {}".format(col, row)].group == 10:
                    pygame.draw.rect(screen, (111, 111, 254),(*top_left, TILE_SIZE, TILE_SIZE))
            else:
                if cells["{}, {}".format(col, row)].status == 1:
                    pygame.draw.rect(screen, BLACK, (*top_left, TILE_SIZE, TILE_SIZE))
                elif cells["{}, {}".format(col, row)].status == 2:
                    pygame.draw.rect(screen, GREY, (*top_left, TILE_SIZE, TILE_SIZE))

                if cells["{}, {}".format(col, row)].centrosome_pos:
                    pygame.draw.rect(screen, (0, 100, 0), (*top_left, TILE_SIZE, TILE_SIZE))
                elif cells["{}, {}".format(col, row)].centrosome_neg:
                    pygame.draw.rect(screen, (0, 200, 0), (*top_left, TILE_SIZE, TILE_SIZE))
                elif cells["{}, {}".format(col, row)].nucleus:
                    pygame.draw.rect(screen, (255, 192, 203), (*top_left, TILE_SIZE, TILE_SIZE))
                elif cells["{}, {}".format(col, row)].polarity_protein_A:
                    pygame.draw.rect(screen, (100, 0, 0), (*top_left, TILE_SIZE, TILE_SIZE))
                elif cells["{}, {}".format(col, row)].polarity_protein_B:
                    pygame.draw.rect(screen, (200, 0, 0), (*top_left, TILE_SIZE, TILE_SIZE))
       
    if sanity_checks:
        for pos in positions:
            col, row = pos
            top_left = (col * TILE_SIZE, row * TILE_SIZE)
            pygame.draw.rect(screen, BLACK, (*top_left, TILE_SIZE, TILE_SIZE))

    #separates menu from cells
    pygame.draw.line(screen, GREY, ((GRID_HEIGHT) * TILE_SIZE, 0), ((GRID_HEIGHT) * TILE_SIZE, HEIGHT))

    #makes the lines that divide each cell
    for (horizontal_start, horizontal_stop, vertical_start, vertical_stop) in split_cells:
        pygame.draw.line(screen, GREY, ((horizontal_start) * TILE_SIZE, (vertical_start) * TILE_SIZE), ((horizontal_stop) * TILE_SIZE, (vertical_stop) * TILE_SIZE), 2)

    #adds black button
    pygame.draw.rect(screen, "blue", black_btn)
    screen.blit(black_surf, (black_btn.x + 60, black_btn.y + 23))

    #adds grey button
    pygame.draw.rect(screen, "blue", grey_btn)
    screen.blit(grey_surf, (grey_btn.x + 65, grey_btn.y + 23))

    #adds nucleus button
    pygame.draw.rect(screen, "blue", nuc_btn)
    screen.blit(nuc_surf, (nuc_btn.x + 45, nuc_btn.y + 23))

    #add Polarity Protein Button
    pygame.draw.rect(screen, "blue", pp_btn)
    screen.blit(pp_surf, (pp_btn.x + 38, pp_btn.y + 10))
    screen.blit(pp_surf_contin, (pp_btn.x + 45, pp_btn.y + 40))

#resets the cell objects for the grid that can be used to clear the old
def new_cells_obj(grids):
    cells = {}
    for i in range(GRID_WIDTH):
        for j in range(GRID_HEIGHT):
            cells["{}, {}".format(i, j)] = Cell(i, j)
            for grid in grids:
                if (i, j) in grid.positions:
                    cells["{}, {}".format(i, j)].grid = grid
    return cells

#Create a class for te grid
class Grid:
    def __init__(self, max_wid, min_wid, max_len, min_len):
        self.Max_Width = max_wid
        self.Min_Width = min_wid
        self.Max_Length = max_len
        self.Min_Length = min_len

        self.time = 0
        self.splitting = False
        self.separating_nuclei_pos = False
        self.separating_nuclei_neg = False
        self.pos_ready_divide = False
        self.neg_ready_divide = False

        self.nucleus = set()
        self.pp = set()

        self.centrosome_pos = ()
        self.centrosome_neg = ()
        self.centrosome_pos_direction = ""
        self.pos_nuclei = set()
        self.neg_nuclei = set()

        self.positions = set()
        for i in range(self.Min_Width, self.Max_Width + 1):
            for j in range(self.Min_Length, self.Max_Length + 1):
                self.positions.add((i, j))

        if len(self.positions) <= 40:
            self.can_divide = False
        else:
            self.can_divide = True

#Create a class for the cells by location on grid
class Cell:
    def __init__(self, i, j):
        self.i = i
        self.j = j

        self.status = 0

        self.nucleus = False
        self.polarity_protein_A = False
        self.polarity_protein_B = False
        self.centrosome_pos = False
        self.centrosome_neg = False

        self.group = ""
        self.grid = ""

    def get_energy(self, positions, cells, distance_scaler):
        energy = 0
        for pos in positions:

            if pos != (self.i, self.j) and pos in self.grid.positions:
                x, y = pos
                other = cells["{}, {}".format(x, y)]

                distance = math.sqrt((x - self.i)**2 + (y - self.j)**2)
                strength = 1/distance * distance_scaler

                if self.status == 1:
                    if other.status == 1:
                        rate = -20
                    elif other.status == 2:
                        rate = 20
                    else:
                        rate = 0

                elif self.status == 2:
                    if other.status == 1:
                        rate = 20
                    elif other.status == 2:
                        rate = -20
                    else:
                        rate = 0

                else:
                    rate = 0

                energy += strength * rate
            
        return energy

    