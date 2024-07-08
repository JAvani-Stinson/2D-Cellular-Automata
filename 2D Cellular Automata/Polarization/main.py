import pygame
import random
import os
from datetime import datetime
import glob
import matplotlib.pyplot as plt

#initiate pygame
pygame.init()

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

#makes font and buttons
font = pygame.font. SysFont('Monocraft', 20, bold = True)

black_surf = font.render("Black", True, "white")
black_btn = pygame.Rect(WIDTH+10, 90, 180, 70)

grey_surf = font.render("Grey", True, "white")
grey_btn = pygame.Rect(WIDTH+10, 170, 180, 70)

nuc_surf = font.render("Nucleus", True, "white")
nuc_btn = pygame.Rect(WIDTH+10, 10, 180, 70)

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
        self.group = ""

    def get_energy(self, cells):
        energy = 0
        if self.status == 100:
            return 0
        for a in range(-1, 2):
            for b in range(-1, 2):
                if a in [-1, 1] or b in [-1, 1]:
                    try:
                        if self.status == 1 and cells["{}, {}".format(self.i + a, self.j + b)].status == 100:
                            energy -= 40
                        elif cells["{}, {}".format(self.i + a, self.j + b)].status == 0:
                            energy += 0
                        elif cells["{}, {}".format(self.i + a, self.j + b) ].status == self.status:
                            energy -= 15
                        else:
                            energy += 19
                    except:
                        energy += 0

        for a in range(-2, 3):
            for b in range(-2, 3):
                if a in [-2, 2] or b in [-2, 2]:
                    try:
                        if self.status == 1 and cells["{}, {}".format((self.i + a), (self.j + b))].status == 100:
                            energy -= 35
                        elif cells["{}, {}".format((self.i + a), (self.j + b))].status == 0:
                            energy += 0
                        elif cells["{}, {}".format((self.i + a), (self.j + b)) ].status == self.status:
                            energy -= 13
                        else:
                            energy += 17
                    except:
                        energy += 0

        for a in range(-3, 4):
            for b in range(-3, 4):
                if a in [-3, 3] or b in [-3, 3]:
                    try:
                        if self.status == 1 and cells["{}, {}".format((self.i + a) , (self.j + b) )].status == 100:
                            energy -= 30
                        elif cells["{}, {}".format((self.i + a) , (self.j + b) )].status == 0:
                            energy += 0
                        elif cells["{}, {}".format((self.i + a) , (self.j + b) ) ].status == self.status:
                            energy -= 10
                        else:
                            energy += 14
                    except:
                        energy += 0

        for a in range(-4, 5):
            for b in range(-4, 5):
                if a in [-4, 4] or b in [-4, 4]:
                    try:
                        if self.status == 1 and cells["{}, {}".format((self.i + a) , (self.j + b) )].status == 100:
                            energy -= 25
                        elif cells["{}, {}".format((self.i + a) , (self.j + b) )].status == 0:
                            energy += 0
                        elif cells["{}, {}".format((self.i + a) , (self.j + b) ) ].status == self.status:
                            energy -= 7
                        else:
                            energy += 11
                    except:
                        energy += 0
            
        for a in range(-5, 6):
            for b in range(-5, 6):
                if a in [-5, 5] or b in [-5, 5]:
                    try:
                        if self.status == 1 and cells["{}, {}".format((self.i + a) , (self.j + b) )].status == 100:
                            energy -= 20
                        elif cells["{}, {}".format((self.i + a) , (self.j + b) )].status == 0:
                            energy += 0
                        elif cells["{}, {}".format((self.i + a) , (self.j + b) ) ].status == self.status:
                            energy -= 6
                        else:
                            energy += 10
                    except:
                        energy += 0

        for a in range(-6, 7):
            for b in range(-6, 7):
                if a in [-6, 6] or b in [-6, 6]:
                    try:
                        if self.status == 1 and cells["{}, {}".format((self.i + a) , (self.j + b) )].status == 100:
                            energy -= 18
                        elif cells["{}, {}".format((self.i + a) , (self.j + b) )].status == 0:
                            energy += 0
                        elif cells["{}, {}".format((self.i + a) , (self.j + b) ) ].status == self.status:
                            energy -= 5
                        else:
                            energy += 9
                    except:
                        energy += 0

        for a in range(-7, 8):
            for b in range(-7, 8):
                if a in [-7, 7] or b in [-7, 7]:
                    try:
                        if self.status == 1 and cells["{}, {}".format((self.i + a) , (self.j + b) )].status == 100:
                            energy -= 15
                        elif cells["{}, {}".format((self.i + a) , (self.j + b) )].status == 0:
                            energy += 0
                        elif cells["{}, {}".format((self.i + a) , (self.j + b) ) ].status == self.status:
                            energy -= 4
                        else:
                            energy += 8
                    except:
                        energy += 0

        for a in range(-8, 9):
            for b in range(-8, 9):
                if a in [-8, 8] or b in [-8, 8]:
                    try:
                        if self.status == 1 and cells["{}, {}".format((self.i + a) , (self.j + b) )].status == 100:
                            energy -= 12
                        elif cells["{}, {}".format((self.i + a) , (self.j + b) )].status == 0:
                            energy += 0
                        elif cells["{}, {}".format((self.i + a) , (self.j + b) ) ].status == self.status:
                            energy -= 3
                        else:
                            energy += 7
                    except:
                        energy += 0

        for a in range(-9, 10):
            for b in range(-9, 10):
                if a in [-9, 9] or b in [-9, 9]:
                    try:
                        if self.status == 1 and cells["{}, {}".format((self.i + a) , (self.j + b) )].status == 100:
                            energy -= 10
                        elif cells["{}, {}".format((self.i + a) , (self.j + b) )].status == 0:
                            energy += 0
                        elif cells["{}, {}".format((self.i + a) , (self.j + b) ) ].status == self.status:
                            energy -= 2
                        else:
                            energy += 6
                    except:
                        energy += 0 

        for a in range(-10, 11):
            for b in range(-10, 11):
                if a in [-10, 10] or b in [-10, 10]:
                    try:
                        if self.status == 1 and cells["{}, {}".format((self.i + a) , (self.j + b) )].status == 100:
                            energy -= 8
                        elif cells["{}, {}".format((self.i + a) , (self.j + b) )].status == 0:
                            energy += 0
                        elif cells["{}, {}".format((self.i + a) , (self.j + b) ) ].status == self.status:
                            energy -= 1
                        else:
                            energy += 5
                    except:
                        energy += 0 
    
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
def draw_grid(positions, cells, color_groups):
    for position in positions:
        col, row = position
        top_left = (col * TILE_SIZE, row * TILE_SIZE)

        #specifies the color of a given tile
        if not color_groups:
            if cells["{}, {}".format(col, row)].status == 1:
                pygame.draw.rect(screen, BLACK, (*top_left, TILE_SIZE, TILE_SIZE))
            elif cells["{}, {}".format(col, row)].status == 2:
                pygame.draw.rect(screen, GREY, (*top_left, TILE_SIZE, TILE_SIZE))
            elif cells["{}, {}".format(col, row)].status == 100:
                pygame.draw.rect(screen, (255, 192, 203),(*top_left, TILE_SIZE, TILE_SIZE))
        elif color_groups:
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
    
    #draws the lines for the grid
    pygame.draw.line(screen, GREY, ((GRID_HEIGHT) * TILE_SIZE, 0), ((GRID_HEIGHT) * TILE_SIZE, HEIGHT))

    #adds black button
    pygame.draw.rect(screen, "blue", black_btn)
    screen.blit(black_surf, (black_btn.x + 60, black_btn.y + 23))

    #adds grey button
    pygame.draw.rect(screen, "blue", grey_btn)
    screen.blit(grey_surf, (grey_btn.x + 65, grey_btn.y + 23))

    #adds nucleus button
    pygame.draw.rect(screen, "blue", nuc_btn)
    screen.blit(nuc_surf, (nuc_btn.x + 45, nuc_btn.y + 23))

def check_energies(position, orig_status, positions, new_positions, directions, cells):
    col, row = position

    for i in range(len(directions)):
        if directions[i][1] == "left":
            x = (col - 1)
            y = row
        elif directions[i][1] == "right":
            x = (col + 1)
            y = row
        elif directions[i][1] == "up":
            y = (row - 1)
            x = col
        elif directions[i][1] == "down":
            y = (row + 1)
            x = col
        elif directions[i][1] == "leftup":
            x = (col - 1)
            y = (row - 1)
        elif directions[i][1] == "leftdown":
            x = (col - 1)
            y = (row + 1)
        elif directions[i][1] == "rightup":
            x = (col + 1)
            y = (row - 1)
        elif directions[i][1] == "rightdown":
            x = (col + 1)
            y = (row + 1)

        if directions[i][1] != "stay" and (x, y) not in new_positions and (x,y) not in positions:
            cells["{}, {}".format(col, row)].status = 0
            cells["{}, {}".format(x, y)].status = orig_status
            directions[i] = (cells["{}, {}".format(x, y)].get_energy(cells), directions[i][1])
            cells["{}, {}".format(x, y)].status = 0
            cells["{}, {}".format(col, row)].status = orig_status

        
    directions.sort()

    return directions

#rule_set
def adjust_grid(positions, cells):
    new_positions = set()
    new_cells = new_cells_obj()
            
    for position in positions:
        col, row = position
        orig_status = cells["{}, {}".format(col, row)].status

        if orig_status == 100:
            new_positions.add(position)
            new_cells["{}, {}".format(col, row)].status = 100

        else:
            #initializes some high energies 
            directions = [(1000, "left"), (1000, "right"), (1000, "up"), (1000, "down"), (1000, "leftup"), (1000, "leftdown"), (1000, "rightup"), (1000, "rightdown"), (cells["{}, {}".format(col, row)].get_energy(cells), "stay")]

            if col == 0:
                directions.remove((1000, "left"))
                directions.remove((1000, "leftup"))
                directions.remove((1000, "leftdown"))

            if col == GRID_WIDTH - 1:
                directions.remove((1000, "right"))
                directions.remove((1000, "rightup"))
                directions.remove((1000, "rightdown"))

            if row == 0:
                directions.remove((1000, "up"))
                if col != 0:
                    directions.remove((1000, "leftup"))
                if col != GRID_WIDTH - 1:
                    directions.remove((1000, "rightup"))

            if row == GRID_HEIGHT - 1:
                directions.remove((1000, "down"))
                if col != 0:
                    directions.remove((1000, "leftdown"))
                if col != GRID_WIDTH - 1:
                    directions.remove((1000, "rightdown"))

            #iterates over all possible directions to move to.
            directions = check_energies(position, orig_status, positions, new_positions, directions, cells)
                    
            if directions[0][1] == "left" and ((col - 1), row) not in new_positions and ((col - 1), row) not in positions:
                new_cells["{}, {}".format((col - 1), row)].status = orig_status
                new_positions.add(((col - 1), row))
            elif directions[0][1] == "right" and ((col + 1), row) not in new_positions and ((col + 1), row) not in positions:
                new_cells["{}, {}".format((col + 1), row)].status = orig_status
                new_positions.add(((col + 1), row))
            elif directions[0][1] == "up" and (col, (row - 1)) not in new_positions and (col, (row - 1)) not in positions:
                new_cells["{}, {}".format(col, (row - 1))].status = orig_status
                new_positions.add((col, (row - 1)))
            elif directions[0][1] == "down" and (col, (row + 1)) not in new_positions and (col, (row + 1)) not in positions:
                new_cells["{}, {}".format(col, (row + 1))].status = orig_status
                new_positions.add((col, (row + 1)))
            elif directions[0][1] == "leftup" and ((col - 1), (row - 1)) not in new_positions and ((col - 1), (row - 1)) not in positions:
                new_cells["{}, {}".format((col - 1), (row - 1))].status = orig_status
                new_positions.add(((col - 1), (row - 1)))
            elif directions[0][1] == "leftdown" and ((col - 1), (row + 1)) not in new_positions and ((col - 1), (row + 1)) not in positions:
                new_cells["{}, {}".format((col - 1), (row + 1))].status = orig_status
                new_positions.add(((col - 1), (row + 1)))
            elif directions[0][1] == "rightup" and ((col + 1), (row - 1)) not in new_positions and ((col + 1), (row - 1)) not in positions:
                new_cells["{}, {}".format((col + 1), (row - 1))].status = orig_status
                new_positions.add(((col + 1), (row - 1)))
            elif directions[0][1] == "rightdown" and ((col + 1), (row - 1)) not in new_positions and ((col + 1), (row - 1)) not in positions:
                new_cells["{}, {}".format((col + 1), (row + 1))].status = orig_status
                new_positions.add(((col + 1), (row + 1)))
            else:
                new_cells["{}, {}".format(col, row)].status = orig_status
                new_positions.add(position)

    return (new_positions, new_cells)

def grouping(positions, cells):

    for cell in cells:
        cells[cell].group = ""

    holder = []
    new_groups = []

    for position in positions:
        col, row = position
        group_potential = 0

        neighbors = get_neighbors(position)
        errbody = [position]

        for neighbor in neighbors:
            x, y = neighbor
            if neighbor in positions and cells["{}, {}".format(x, y)].status == cells["{}, {}".format(col, row)].status:
                group_potential += 1
                errbody.append(neighbor)
        
        if group_potential >= 4:
            new_group = set()
            for pos in errbody:
                new_group.add(pos)
                neighbors1 = get_neighbors(pos)
                for neighbor1 in neighbors1:
                    c, d = neighbor1
                    if cells["{}, {}".format(c, d)].status == cells["{}, {}".format(col, row)].status:
                        new_group.add(neighbor1)
            holder.append(new_group)

    while len(holder) > 0:
        first, *rest = holder
        first = set(first)

        lf = -1
        while len(first) > lf:
            lf = len(first)

            rest2 = []
            for r in rest:
                if len(first.intersection(set(r)))>0:
                    first |= set(r)
                else:
                    rest2.append(r)     
            rest = rest2

        new_groups.append(first)
        holder = rest

    for i, group in enumerate(new_groups):
        for pos in group:
            x, y = pos
            cells["{}, {}".format(x, y)].group = i

    return new_groups, cells

def shifting(positions, groups, cells):
    amalg = set()
    new_cells = new_cells_obj()
    new_positions = set()

    for cell in cells:
        if cells[cell].status == 100:
            new_positions.add((cells[cell].i, cells[cell].j))
            new_cells["{}, {}".format(cells[cell].i, cells[cell].j)].status = 100
            amalg.add((cells[cell].i, cells[cell].j))

    for group in groups:
        amalg = amalg.union(group)

    for group in groups:

        can_move = True

        orig_point = next(iter(group))
        a, b = orig_point
        orig_status = cells["{}, {}".format(a, b)].status

        directions = ["left", "right", "up", "down", "leftup", "leftdown", "rightup", "rightdown", "stay"]

        for pos in group:
            x, y = pos
            if x == 0:
                if "left" in directions:
                    directions.remove("left")
                if "leftup" in directions:
                    directions.remove("leftup")
                if "leftdown" in directions:
                    directions.remove("leftdown")

            if x == GRID_WIDTH - 1:
                if "right" in directions:
                    directions.remove("right")
                if "rightup" in directions:
                    directions.remove("rightup")
                if "rightdown" in directions:
                    directions.remove("rightdown")

            if y == 0:
                if "up" in directions:
                    directions.remove("up")
                if "leftup" in directions:
                    directions.remove("leftup")
                if "rightup" in directions:
                    directions.remove("rightup")

            if y == GRID_HEIGHT - 1:
                if "down" in directions:
                    directions.remove("down")
                if "rightdown" in directions:
                    directions.remove("rightdown")
                if "leftdown" in directions:
                    directions.remove("leftdown")

        direction = random.choice(directions)

        if direction == "left":
            for point in group:
                x, y = point
                if ((x - 1) , y) in new_positions: 
                    can_move = False
            if can_move:
                for point in group:
                    x, y = point
                    new_positions.add(((x - 1) , y))
                    new_cells["{}, {}".format((x - 1) , y)].status = orig_status
            else:
                for point in group:
                    x, y = point
                    new_positions.add((x, y))
                    new_cells["{}, {}".format(x, y)].status = orig_status

        elif direction == "right":
            for point in group:
                x, y = point
                if ((x + 1) , y) in new_positions: 
                    can_move = False
            if can_move:
                for point in group:
                    x, y = point
                    new_positions.add(((x + 1) , y))
                    new_cells["{}, {}".format((x + 1) , y)].status = orig_status
            else:
                for point in group:
                    x, y = point
                    new_positions.add((x, y))
                    new_cells["{}, {}".format(x, y)].status = orig_status

        elif direction == "up":
            for point in group:
                x, y = point
                if (x, (y - 1) ) in new_positions: 
                    can_move = False
            if can_move:
                for point in group:
                    x, y = point
                    new_positions.add((x, (y - 1) ))
                    new_cells["{}, {}".format(x, (y - 1) )].status = orig_status
            else:
                for point in group:
                    x, y = point
                    new_positions.add((x, y))
                    new_cells["{}, {}".format(x, y)].status = orig_status

        elif direction == "down":
            for point in group:
                x, y = point
                if (x, (y + 1) ) in new_positions: 
                    can_move = False
            if can_move:
                for point in group:
                    x, y = point
                    new_positions.add((x, (y + 1) ))
                    new_cells["{}, {}".format(x, (y + 1) )].status = orig_status
            else:
                for point in group:
                    x, y = point
                    new_positions.add((x, y))
                    new_cells["{}, {}".format(x, y)].status = orig_status

        elif direction == "leftup":
            for point in group:
                x, y = point
                if ((x - 1) , (y - 1) ) in new_positions: 
                    can_move = False
            if can_move:
                for point in group:
                    x, y = point
                    new_positions.add(((x - 1) , (y - 1) ))
                    new_cells["{}, {}".format((x - 1) , (y - 1) )].status = orig_status
            else:
                for point in group:
                    x, y = point
                    new_positions.add((x, y))
                    new_cells["{}, {}".format(x, y)].status = orig_status

        elif direction == "leftdown":
            for point in group:
                x, y = point
                if ((x - 1) , (y + 1) ) in new_positions: 
                    can_move = False
            if can_move:
                for point in group:
                    x, y = point
                    new_positions.add(((x - 1) , (y + 1) ))
                    new_cells["{}, {}".format((x - 1) , (y + 1) )].status = orig_status
            else:
                for point in group:
                    x, y = point
                    new_positions.add((x, y))
                    new_cells["{}, {}".format(x, y)].status = orig_status

        elif direction == "rightup":
            for point in group:
                x, y = point
                if ((x + 1) , (y - 1) ) in new_positions: 
                    can_move = False
            if can_move:
                for point in group:
                    x, y = point
                    new_positions.add(((x + 1) , (y - 1) ))
                    new_cells["{}, {}".format((x + 1) , (y - 1) )].status = orig_status
            else:
                for point in group:
                    x, y = point
                    new_positions.add((x, y))
                    new_cells["{}, {}".format(x, y)].status = orig_status

        elif direction == "rightdown":
            for point in group:
                x, y = point
                if ((x + 1) , (y + 1) ) in new_positions: 
                    can_move = False
            if can_move:
                for point in group:
                    x, y = point
                    new_positions.add(((x + 1) , (y + 1) ))
                    new_cells["{}, {}".format((x + 1) , (y + 1) )].status = orig_status
            else:
                for point in group:
                    x, y = point
                    new_positions.add((x, y))
                    new_cells["{}, {}".format(x, y)].status = orig_status

        else:
            for point in group:
                x, y = point
                new_positions.add((x, y))
                new_cells["{}, {}".format(x, y)].status = orig_status

    for pos in positions:
        if pos not in amalg:

            x, y = pos
            orig_status = cells["{}, {}".format(x, y)].status

            directions = ["left", "right", "up", "down", "leftup", "leftdown", "rightup", "rightdown", "stay"]

            if x == 0:
                for dir in directions:
                    if dir == "left":
                        directions.remove("left")
                    if dir == "leftdown":
                        directions.remove("leftdown")
                    if dir == "left":
                        directions.remove("leftup")

            if x == GRID_WIDTH - 1:
                for dir in directions:
                    if dir == "right":
                        directions.remove("right")
                    if dir == "rightdown":
                        directions.remove("rightdown")
                    if dir == "left":
                        directions.remove("rightup")
            if y == 0:
                for dir in directions:
                    if dir == "up":
                        directions.remove("up")
                    if dir == "leftup":
                        directions.remove("leftup")
                    if dir == "rightup":
                        directions.remove("rightup")

            if y == GRID_HEIGHT - 1:
                for dir in directions:
                    if dir == "down":
                        directions.remove("down")
                    if dir == "leftdown":
                        directions.remove("leftdown")
                    if dir == "rightdown":
                        directions.remove("rightdown")

            random.shuffle(directions)

            unplaced = True
            i = 0

            while unplaced:
                try:
                    if directions[i] == "left":
                        if ((x - 1) , y) not in new_positions:
                            unplaced = False
                            new_positions.add(((x - 1) , y))
                            new_cells["{}, {}".format((x - 1) , y)].status = orig_status

                    elif directions[i] == "right":
                        if ((x + 1) , y) not in new_positions:
                            unplaced = False
                            new_positions.add(((x + 1) , y))
                            new_cells["{}, {}".format((x + 1) , y)].status = orig_status

                    elif directions[i] == "up":
                        if (x, (y - 1) ) not in new_positions:
                            unplaced = False
                            new_positions.add((x, (y - 1) ))
                            new_cells["{}, {}".format(x, (y - 1) )].status = orig_status
                    
                    elif directions[i] == "down":
                        if (x, (y + 1) ) not in new_positions:
                            unplaced = False
                            new_positions.add((x, (y + 1) ))
                            new_cells["{}, {}".format(x, (y + 1) )].status = orig_status

                    elif directions[i] == "leftup":
                        if ((x - 1) , (y - 1) ) not in new_positions:
                            unplaced = False
                            new_positions.add(((x - 1) , (y - 1) ))
                            new_cells["{}, {}".format((x - 1) , (y - 1) )].status = orig_status

                    elif directions[i] == "leftdown":
                        if ((x - 1) , (y + 1) ) not in new_positions:
                            unplaced = False
                            new_positions.add(((x - 1) , (y + 1) ))
                            new_cells["{}, {}".format((x - 1) , (y + 1) )].status = orig_status
            
                    elif directions[i] == "rightup":
                        if ((x + 1) , (y - 1) ) not in new_positions:
                            unplaced = False
                            new_positions.add(((x + 1) , (y - 1) ))
                            new_cells["{}, {}".format((x + 1) , (y - 1) )].status = orig_status

                    elif directions[i] == "rightdown":
                        if ((x + 1) , (y + 1) ) not in new_positions:
                            unplaced = False
                            new_positions.add(((x + 1) , (y + 1) ))
                            new_cells["{}, {}".format((x + 1) , (y + 1) )].status = orig_status
                    else:
                        if (x, y) not in new_positions:
                            unplaced = False
                            new_positions.add((x, y))
                            new_cells["{}, {}".format(x, y)].status = orig_status
                except:
                    new_positions.add((x, y))
                    new_cells["{}, {}".format(x, y)].status = orig_status
                    unplaced = False

                i += 1

    return (new_positions, new_cells)

#gathers a cell's Von Neumann neighborhood
def get_neighbors(pos):
    x,y = pos
    neighbors = []
    potential_neighbors = [(-1, 0), (1, 0), (0, 1), (0, -1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

    if x == 0:
        potential_neighbors.remove((-1, 0))
        potential_neighbors.remove((-1, 1))
        potential_neighbors.remove((-1, -1))
    if x == GRID_WIDTH - 1:
        potential_neighbors.remove((1, 0))
        potential_neighbors.remove((1, 1))
        potential_neighbors.remove((1, -1))
    if y == 0:
        potential_neighbors.remove((0, -1))
        if (1, -1) in potential_neighbors:
            potential_neighbors.remove((1, -1))
        if (-1, -1) in potential_neighbors:
            potential_neighbors.remove((-1, -1))
    if y == GRID_HEIGHT - 1:
        potential_neighbors.remove((0, 1))
        if (-1, 1) in potential_neighbors:
            potential_neighbors.remove((-1, 1))
        if (1, 1) in potential_neighbors:
            potential_neighbors.remove((1, 1))

    for position in potential_neighbors:
        dx, dy = position
        #adds neighbors to list
        neighbors.append(((x + dx) , (y + dy) ))

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

def plot_it(x_coord, y_coord):
    plt.plot(x_coord, y_coord)
    plt.xlabel("Timesteps (matches with video increments in base 60)")
    plt.ylabel("Overall Grid Enerfy")
    plot_output = '//Users//jstinson//Desktop//2D Cellular Automata/Polarization//Plots//CA ' + str(datetime.now()) + '.png'
    plt.savefig(plot_output)
    plt.show()

#starts the game
def main():

    #sStarts the game (as Conway) in a paused state and gives the "speed" of play
    running = True
    playing = False

    count = 0
    update_freq = 30

    shift_count = 0
    shift_freq = 140

    num = 0
    time = 0
    x_coord = []
    y_coord = []

    #initializes a grouping mechanism as a list of sets
    color_groups = False
    groups = []

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
            shift_count += 1

        #updates the game according to "speed" set priorly
        if count >= update_freq:
            count = 0

            y_coord.append(get_total_energy(cells, positions))
            x_coord.append(time)
            time += 1

            #takes picture
            num = make_png(screen, num)
            
            #determines the rule_set
            positions, cells = adjust_grid(positions, cells)
            groups, cells = grouping(positions, cells)

            blackies = 0 
            grey = 0
            pink = 0

            for cell in cells:
                if cells[cell].status == 1:
                    blackies += 1
                elif cells[cell].status == 2:
                    grey += 1
                elif cells[cell].status == 100:
                    pink += 1

            print("{}: blacks - {}, grey - {}, pink - {}".format(time, blackies, grey, pink))

        if shift_count >= shift_freq:
            shift_count = 0

            y_coord.append(get_total_energy(cells, positions))
            x_coord.append(time)
            time += 1

            #takes picture
            num = make_png(screen, num)
            
            #determines the rule_set
            positions, cells = shifting(positions, groups, cells)

            blackies = 0 
            grey = 0
            pink = 0

            for cell in cells:
                if cells[cell].status == 1:
                    blackies += 1
                elif cells[cell].status == 2:
                    grey += 1
                elif cells[cell].status == 100:
                    pink += 1

            print("shifting at {}: blacks - {}, grey - {}, pink - {}".format(time, blackies, grey, pink))

        #initializes a way to see if the game is progressing
        if playing:
            status = "Playing"
        else:
            status = "Paused"

        #shows player what the rules are and if the game is proceeding
        pygame.display.set_caption("{}: Add color {}, Color Groups = {}".format(status, add_color, color_groups))

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

                if nuc_btn.collidepoint(event.pos):
                    add_color = "nuc"

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
                        elif add_color == "nuc":
                            cells["{}, {}".format(col, row)].status = 100

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
                    (positions, cells) = gen(random.randrange(3, 5) * GRID_WIDTH)
                    print("new generation")

                #toggles grouping
                if event.key == pygame.K_k:
                    color_groups = not color_groups

        #displays everything
        screen.fill(LBLUE)
        draw_grid(positions, cells, color_groups)
        pygame.display.update()

    #creates movie when the game is exited
    make_mp4()

    #makes and saves the chart
    plot_it(x_coord, y_coord)

    #empties images folder
    files = glob.glob('/Users/jstinson/Desktop/2D Cellular Automata/Polarization/Images/*')
    for f in files:
        os.remove(f)

    pygame.quit()

if __name__ == "__main__":
    main()
