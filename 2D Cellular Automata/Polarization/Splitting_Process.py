import math
import random
from Classes_and_Grids import Grid

p_to_c_match_rate = -30
p_to_c_differ_rate = 10

def move_pp_A(positions, cells, distance_scaler, pp_attraction_factor, pp_repulsion_factor):
    proteins = set()
    on_membrane = set()

    #adds all the polarity protein positions to a set for later use
    for pos in positions:
        col, row = pos
        if cells["{}, {}".format(col, row)].polarity_protein_A or cells["{}, {}".format(col, row)].polarity_protein_B:
            proteins.add(pos)

    for protein in proteins:
        col, row = protein
        grid = cells["{}, {}".format(col, row)].grid
        if col == grid.Min_Width or col == grid.Max_Width or row == grid.Min_Length or row == grid.Max_Length:
            on_membrane.add(protein)

    for protein in proteins:
        col, row = protein
        grid = cells["{}, {}".format(col, row)].grid
        me = cells["{}, {}".format(col, row)]

        if me.polarity_protein_A:

            if col == grid.Min_Width or col == grid.Max_Width or row == grid.Min_Length or row == grid.Max_Length:
                possible_moves = [(float("inf"), "left"), (float("inf"), "right"), (float("inf"), "up"), (float("inf"), "down"), (float("inf"), "stay")]
                
                if col == grid.Min_Width and row == grid.Min_Length:
                    possible_moves.remove((float("inf"), "left"))
                    possible_moves.remove((float("inf"), "up"))
                elif col == grid.Min_Width and row == grid.Max_Length:
                    possible_moves.remove((float("inf"), "left"))
                    possible_moves.remove((float("inf"), "down"))
                elif col == grid.Max_Width and row == grid.Min_Length:
                    possible_moves.remove((float("inf"), "right"))
                    possible_moves.remove((float("inf"), "up"))
                elif col == grid.Max_Width and row == grid.Max_Length:
                    possible_moves.remove((float("inf"), "right"))
                    possible_moves.remove((float("inf"), "down"))
                elif col == grid.Max_Width or col == grid.Min_Width:
                    possible_moves.remove((float("inf"), "right"))
                    possible_moves.remove((float("inf"), "left"))
                elif row == grid.Max_Length or row == grid.Min_Length:
                    possible_moves.remove((float("inf"), "up"))
                    possible_moves.remove((float("inf"), "down"))

                possible_moves = pp_energy_A(protein, cells, on_membrane, grid, possible_moves, distance_scaler, pp_attraction_factor, pp_repulsion_factor)

                if possible_moves[0][1] == "left":
                    me.polarity_protein_A = False
                    cells["{}, {}".format(col - 1, row)].polarity_protein_A = True
                    positions.add((col - 1, row))
                    on_membrane.remove((col, row))
                    on_membrane.add((col - 1, row))
                    if me.status == 0 and me.nucleus == False and me.polarity_protein_B == False:
                        positions.remove((col, row))
                elif possible_moves[0][1] == "right":
                    me.polarity_protein_A = False
                    cells["{}, {}".format(col + 1, row)].polarity_protein_A = True
                    positions.add((col + 1, row))
                    on_membrane.remove((col, row))
                    on_membrane.add((col + 1, row))
                    if me.status == 0 and me.nucleus == False and me.polarity_protein_B == False:
                        positions.remove((col, row))
                elif possible_moves[0][1] == "up":
                    me.polarity_protein_A = False
                    cells["{}, {}".format(col, row - 1)].polarity_protein_A = True
                    positions.add((col, row - 1))
                    on_membrane.remove((col, row))
                    on_membrane.add((col, row - 1))
                    if me.status == 0 and me.nucleus == False and me.polarity_protein_B == False:
                        positions.remove((col, row))
                elif possible_moves[0][1] == "down":
                    me.polarity_protein_A = False
                    cells["{}, {}".format(col, row + 1)].polarity_protein_A = True
                    positions.add((col, row + 1))
                    on_membrane.remove((col, row))
                    on_membrane.add((col, row + 1))
                    if me.status == 0 and me.nucleus == False and me.polarity_protein_B == False:
                        positions.remove((col, row))

                elif possible_moves[0][1] == "stay":
                    me.polarity_protein_A = True

            else:
                to_border = [(abs(col - grid.Min_Width), "left"), 
                            (abs(grid.Max_Width - col), "right"), 
                            (abs(row - grid.Min_Length), "up"), 
                            (abs(grid.Max_Length - row), "down")]
                to_border.sort()

                if to_border[0][1] == "left" and cells["{}, {}".format(col - 1, row)].polarity_protein_A == False:
                    me.polarity_protein_A = False
                    cells["{}, {}".format(col - 1, row)].polarity_protein_A = True
                    positions.add((col - 1, row))
                    if me.status == 0 and me.nucleus == False and me.polarity_protein_B == False:
                        positions.remove((col, row))
                elif to_border[0][1] == "right" and cells["{}, {}".format(col + 1, row)].polarity_protein_A == False:
                    me.polarity_protein_A = False
                    cells["{}, {}".format(col + 1, row)].polarity_protein_A = True
                    positions.add((col + 1, row))
                    if me.status == 0 and me.nucleus == False and me.polarity_protein_B == False:
                        positions.remove((col, row))
                elif to_border[0][1] == "up" and cells["{}, {}".format(col, row - 1)].polarity_protein_A == False:
                    me.polarity_protein_A = False
                    cells["{}, {}".format(col, row - 1)].polarity_protein_A = True
                    positions.add((col, row - 1))
                    if me.status == 0 and me.nucleus == False and me.polarity_protein_B == False:
                        positions.remove((col, row))
                elif to_border[0][1] == "down" and cells["{}, {}".format(col, row + 1)].polarity_protein_A == False:
                    me.polarity_protein_A = False
                    cells["{}, {}".format(col, row + 1)].polarity_protein_A = True
                    positions.add((col, row + 1))
                    if me.status == 0 and me.nucleus == False and me.polarity_protein_B == False:
                        positions.remove((col, row))
        
    return positions, cells

def move_pp_B(positions, cells, distance_scaler, pp_attraction_factor, pp_repulsion_factor):
    proteins = set()
    on_membrane = set()

    #adds all the polarity protein positions to a set for later use
    for pos in positions:
        col, row = pos
        if cells["{}, {}".format(col, row)].polarity_protein_A or cells["{}, {}".format(col, row)].polarity_protein_B:
            proteins.add(pos)

    for protein in proteins:
        col, row = protein
        grid = cells["{}, {}".format(col, row)].grid
        if col == grid.Min_Width or col == grid.Max_Width or row == grid.Min_Length or row == grid.Max_Length:
            on_membrane.add(protein)

    for protein in proteins:
        col, row = protein
        grid = cells["{}, {}".format(col, row)].grid
        me = cells["{}, {}".format(col, row)]

        if me.polarity_protein_B:

            if col == grid.Min_Width or col == grid.Max_Width or row == grid.Min_Length or row == grid.Max_Length:
                possible_moves = [(float("inf"), "left"), (float("inf"), "right"), (float("inf"), "up"), (float("inf"), "down"), (float("inf"), "stay")]
                
                if col == grid.Min_Width and row == grid.Min_Length:
                    possible_moves.remove((float("inf"), "left"))
                    possible_moves.remove((float("inf"), "up"))
                elif col == grid.Min_Width and row == grid.Max_Length:
                    possible_moves.remove((float("inf"), "left"))
                    possible_moves.remove((float("inf"), "down"))
                elif col == grid.Max_Width and row == grid.Min_Length:
                    possible_moves.remove((float("inf"), "right"))
                    possible_moves.remove((float("inf"), "up"))
                elif col == grid.Max_Width and row == grid.Max_Length:
                    possible_moves.remove((float("inf"), "right"))
                    possible_moves.remove((float("inf"), "down"))
                elif col == grid.Max_Width or col == grid.Min_Width:
                    possible_moves.remove((float("inf"), "right"))
                    possible_moves.remove((float("inf"), "left"))
                elif row == grid.Max_Length or row == grid.Min_Length:
                    possible_moves.remove((float("inf"), "up"))
                    possible_moves.remove((float("inf"), "down"))

                possible_moves = pp_energy_B(protein, cells, on_membrane, grid, possible_moves, distance_scaler, pp_attraction_factor, pp_repulsion_factor)

                if possible_moves[0][1] == "left":
                    me.polarity_protein_B = False
                    cells["{}, {}".format(col - 1, row)].polarity_protein_B= True
                    positions.add((col - 1, row))
                    on_membrane.remove((col, row))
                    on_membrane.add((col - 1, row))
                    if me.status == 0 and me.nucleus == False and me.polarity_protein_A == False:
                        positions.remove((col, row))
                elif possible_moves[0][1] == "right":
                    me.polarity_protein_B = False
                    cells["{}, {}".format(col + 1, row)].polarity_protein_B = True
                    positions.add((col + 1, row))
                    on_membrane.remove((col, row))
                    on_membrane.add((col + 1, row))
                    if me.status == 0 and me.nucleus == False and me.polarity_protein_A == False:
                        positions.remove((col, row))
                elif possible_moves[0][1] == "up":
                    me.polarity_protein_B = False
                    cells["{}, {}".format(col, row - 1)].polarity_protein_B = True
                    positions.add((col, row - 1))
                    on_membrane.remove((col, row))
                    on_membrane.add((col, row - 1))
                    if me.status == 0 and me.nucleus == False and me.polarity_protein_A == False:
                        positions.remove((col, row))
                elif possible_moves[0][1] == "down":
                    me.polarity_protein_B = False
                    cells["{}, {}".format(col, row + 1)].polarity_protein_B = True
                    positions.add((col, row + 1))
                    on_membrane.remove((col, row))
                    on_membrane.add((col, row + 1))
                    if me.status == 0 and me.nucleus == False and me.polarity_protein_A == False:
                        positions.remove((col, row))

                elif possible_moves[0][1] == "stay":
                    me.polarity_protein_B = True
            else:
                to_border = [(abs(col - grid.Min_Width), "left"), 
                            (abs(grid.Max_Width - col), "right"), 
                            (abs(row - grid.Min_Length), "up"), 
                            (abs(grid.Max_Length - row), "down")]
                to_border.sort()

                if to_border[0][1] == "left" and cells["{}, {}".format(col - 1, row)].polarity_protein_B == False:
                    me.polarity_protein_B = False
                    cells["{}, {}".format(col - 1, row)].polarity_protein_B = True
                    positions.add((col - 1, row))
                    if me.status == 0 and me.nucleus == False and me.polarity_protein_A == False:
                        positions.remove((col, row))
                elif to_border[0][1] == "right" and cells["{}, {}".format(col + 1, row)].polarity_protein_B == False:
                    me.polarity_protein_B = False
                    cells["{}, {}".format(col + 1, row)].polarity_protein_B = True
                    positions.add((col + 1, row))
                    if me.status == 0 and me.nucleus == False and me.polarity_protein_A == False:
                        positions.remove((col, row))
                elif to_border[0][1] == "up" and cells["{}, {}".format(col, row - 1)].polarity_protein_B == False:
                    me.polarity_protein_B = False
                    cells["{}, {}".format(col, row - 1)].polarity_protein_B = True
                    positions.add((col, row - 1))
                    if me.status == 0 and me.nucleus == False and me.polarity_protein_A == False:
                        positions.remove((col, row))
                elif to_border[0][1] == "down" and cells["{}, {}".format(col, row + 1)].polarity_protein_B == False:
                    me.polarity_protein_B = False
                    cells["{}, {}".format(col, row + 1)].polarity_protein_B = True
                    positions.add((col, row + 1))
                    if me.status == 0 and me.nucleus == False and me.polarity_protein_A == False:
                        positions.remove((col, row))

    return positions, cells

def pp_energy_A(pos, cells, on_membrane, grid, possible_moves, distance_scaler, pp_attraction_factor, pp_repulsion_factor):
    x, y = pos

    for i, move in enumerate(possible_moves):
        if move[1] == "left" and not cells["{}, {}".format(x - 1, y)].polarity_protein_A:
            c = x - 1
            d = y
            energy = 0
            direction = "left"
        elif move[1] == "right" and not cells["{}, {}".format(x + 1, y)].polarity_protein_A:
            c = x + 1
            d = y
            energy = 0
            direction = "right"
        elif  move[1] == "up" and not cells["{}, {}".format(x, y - 1)].polarity_protein_A:
            c = x
            d = y - 1
            energy = 0
            direction = "up"
        elif move[1] == "down" and not cells["{}, {}".format(x, y + 1)].polarity_protein_A:
            c = x
            d = y + 1
            energy = 0
            direction = "down"
        else:
            c = x
            d = y
            energy = 0
            direction = "stay"
            
        for protein in on_membrane:
            if protein in cells["{}, {}".format(x, y)].grid.positions:
                a, b = protein

                if (c == grid.Max_Width and a == grid.Min_Width) or (c == grid.Min_Width and a == grid.Max_Width):
                    potential = [abs(d - grid.Max_Length) + abs(b - grid.Max_Length), abs(d - grid.Min_Length) + abs(b - grid.Min_Length)]
                    potential.sort()
                    y_distance = potential[0]
                else:
                    y_distance = abs(d - b)
                if (d == grid.Max_Length and b == grid.Min_Length) or (d == grid.Min_Width and b == grid.Max_Length):
                    potential = [abs(c - grid.Max_Width) + abs(a - grid.Max_Width), abs(c - grid.Min_Width) + abs(a - grid.Min_Width)]
                    potential.sort()
                    x_distance = potential[0]
                else:
                    x_distance = abs(c - a)

                distance = x_distance + y_distance
                if distance != 0:
                    strength = 1/math.sqrt(distance) * distance_scaler
                    if cells["{}, {}".format(a, b)].polarity_protein_A:
                        energy += strength * pp_attraction_factor
                    if cells["{}, {}".format(a, b)].polarity_protein_B:
                        energy += strength * pp_repulsion_factor
                else:
                    distance = 1
                    strength = 1/math.sqrt(distance) * distance_scaler
                    if cells["{}, {}".format(a, b)].polarity_protein_A:
                        energy += strength * pp_attraction_factor
                    if cells["{}, {}".format(a, b)].polarity_protein_B:
                        energy += strength * pp_repulsion_factor

        possible_moves[i] = (energy, direction)

    possible_moves.sort()

    return possible_moves

def pp_energy_B(pos, cells, on_membrane, grid, possible_moves, distance_scaler, pp_attraction_factor, pp_repulsion_factor):
    x, y = pos

    for i, move in enumerate(possible_moves):
        if move[1] == "left" and not cells["{}, {}".format(x - 1, y)].polarity_protein_B:
            c = x - 1
            d = y
            energy = 0
            direction = "left"
        elif move[1] == "right" and not cells["{}, {}".format(x + 1, y)].polarity_protein_B:
            c = x + 1
            d = y
            energy = 0
            direction = "right"
        elif  move[1] == "up" and not cells["{}, {}".format(x, y - 1)].polarity_protein_B:
            c = x
            d = y - 1
            energy = 0
            direction = "up"
        elif move[1] == "down" and not cells["{}, {}".format(x, y + 1)].polarity_protein_B:
            c = x
            d = y + 1
            energy = 0
            direction = "down"
        else:
            c = x
            d = y
            energy = 0
            direction = "stay"
            
        for protein in on_membrane:
            if protein != (x, y):
                a, b = protein

                if (c == grid.Max_Width and a == grid.Min_Width) or (c == grid.Min_Width and a == grid.Max_Width):
                    potential = [abs(d - grid.Max_Length) + abs(b - grid.Max_Length), abs(d - grid.Min_Length) + abs(b - grid.Min_Length)]
                    potential.sort()
                    y_distance = potential[0]

                else:
                    y_distance = abs(d - b)

                if (d == grid.Max_Length and b == grid.Min_Length) or (d == grid.Min_Width and b == grid.Max_Length):
                    potential = [abs(c - grid.Max_Width) + abs(a - grid.Max_Width), abs(c - grid.Min_Width) + abs(a - grid.Min_Width)]
                    potential.sort()
                    x_distance = potential[0]

                else:
                    x_distance = abs(c - a)

                distance = x_distance + y_distance

                if distance != 0:
                    strength = 1/math.sqrt(distance) * distance_scaler
                    if cells["{}, {}".format(a, b)].polarity_protein_B:
                        energy += strength * pp_attraction_factor
                    if cells["{}, {}".format(a, b)].polarity_protein_A:
                        energy += strength * pp_repulsion_factor
                else:
                    distance = 1
                    strength = 1/math.sqrt(distance) * distance_scaler
                    if cells["{}, {}".format(c, d)].polarity_protein_B:
                        energy += strength * pp_attraction_factor
                    if cells["{}, {}".format(c, d)].polarity_protein_A:
                        energy += strength * pp_repulsion_factor
                    
        possible_moves[i] = (energy, direction)


    possible_moves.sort()

    return possible_moves

def double_nucleus(positions, cells, grids):
    for grid in grids:
        if grid.time > 700 and grid.splitting == False and grid.can_divide == True:
            grid.splitting = True

            if grid.centrosome_pos:
                a, b = grid.centrosome_pos
                cells["{}, {}".format(a, b + 1)].nucleus = True
                cells["{}, {}".format(a + 1, b + 1)].nucleus = True
                cells["{}, {}".format(a + 1, b)].nucleus = True
                grid.nucleus.add((a + 1, b + 1))
                grid.nucleus.add((a, b + 1))
                grid.nucleus.add((a + 1, b))
                positions.add((a, b + 1))
                positions.add((a + 1, b + 1))
                positions.add((a + 1, b))
                cells["{}, {}".format(a + 1, b + 1)].centrosome_neg = True
                grid.centrosome_neg = (a + 1, b + 1)

            elif grid.centrosome_neg:
                a, b = grid.centrosome_neg
                cells["{}, {}".format(a, b - 1)].nucleus = True
                cells["{}, {}".format(a - 1, b - 1)].nucleus = True
                cells["{}, {}".format(a - 1, b)].nucleus = True
                grid.nucleus.add((a - 1, b - 1))
                grid.nucleus.add((a, b - 1))
                grid.nucleus.add((a - 1, b))
                positions.add((a, b - 1))
                positions.add((a - 1, b - 1))
                positions.add((a - 1, b))
                cells["{}, {}".format(a - 1, b - 1)].centrosome_pos = True
                grid.centrosome_pos = (a - 1, b - 1)
            
            get_centrosome_directions(cells, grid)

    return positions, cells

def get_centrosome_directions(cells, grid):
    if grid.centrosome_pos[0] > grid.centrosome_neg[0]:
        right_start = grid.centrosome_pos[0]
        left_start = grid.centrosome_neg[0]
    else:
        right_start = grid.centrosome_neg[0]
        left_start = grid.centrosome_pos[0]

    if grid.centrosome_pos[1] > grid.centrosome_neg[1]:
        down_start = grid.centrosome_pos[1]
        up_start = grid.centrosome_neg[1]
    else:
        down_start = grid.centrosome_neg[1]
        up_start = grid.centrosome_pos[1]

    up = 0
    down = 0
    left = 0
    right = 0

    for pp in grid.pp:
        x, y = pp
        if x >= right_start:
            if cells["{}, {}".format(x, y)].polarity_protein_A:
                right += 1
        elif x <= left_start:
            if cells["{}, {}".format(x, y)].polarity_protein_A:
                left += 1
        if y >= down_start:
            if cells["{}, {}".format(x, y)].polarity_protein_A:
                down += 1
        elif y <= up_start:
            if cells["{}, {}".format(x, y)].polarity_protein_A:
                up += 1

    directions = sorted([(left, "left"), (right, "right"), (up, "up"), (down, "down")])
    directions.reverse()

    if directions[0][0] == directions[1][0]:
        direction_pos = random.choice([directions[0][1], directions[1][1]])
    else:
        direction_pos = directions[0][1]
    
    grid.centrosome_pos_direction = direction_pos

    if grid.centrosome_pos_direction == "right":
        a, b = grid.centrosome_pos
        cells["{}, {}".format(a, b)].centrosome_pos = False
        cells["{}, {}".format(a + 1, b)].centrosome_pos = True
        grid.centrosome_pos = (a + 1, b)

        c, d = grid.centrosome_neg
        cells["{}, {}".format(c, d)].centrosome_neg = False
        cells["{}, {}".format(c - 1, d)].centrosome_neg = True
        grid.centrosome_neg = (c - 1, d)

    if grid.centrosome_pos_direction == "down":
        a, b = grid.centrosome_pos
        cells["{}, {}".format(a, b)].centrosome_pos = False
        cells["{}, {}".format(a, b + 1)].centrosome_pos = True
        grid.centrosome_pos = (a, b + 1)

        c, d = grid.centrosome_neg
        cells["{}, {}".format(c, d)].centrosome_neg = False
        cells["{}, {}".format(c, d - 1)].centrosome_neg = True
        grid.centrosome_neg = (c, d - 1)

    if grid.centrosome_pos_direction == "left":
        edge = float("inf")
        for nucleus in grid.nucleus:
            if nucleus[0] <= edge:
                edge = nucleus[0]
        for nucleus in grid.nucleus:
            if nucleus[0] == edge:
                grid.pos_nuclei.add(nucleus)
            else:
                grid.neg_nuclei.add(nucleus)
    elif grid.centrosome_pos_direction == "right":
        edge = float("-inf")
        for nucleus in grid.nucleus:
            if nucleus[0] >= edge:
                edge = nucleus[0]
        for nucleus in grid.nucleus:
            if nucleus[0] == edge:
                grid.pos_nuclei.add(nucleus)
            else:
                grid.neg_nuclei.add(nucleus)
    elif grid.centrosome_pos_direction == "up":
        edge = float("inf")
        for nucleus in grid.nucleus:
            if nucleus[1] <= edge:
                edge = nucleus[1]
        for nucleus in grid.nucleus:
            if nucleus[1] == edge:
                grid.pos_nuclei.add(nucleus)
            else:
                grid.neg_nuclei.add(nucleus)
    elif grid.centrosome_pos_direction == "down":
        edge = float("-inf")
        for nucleus in grid.nucleus:
            if nucleus[1] >= edge:
                edge = nucleus[1]
        for nucleus in grid.nucleus:
            if nucleus[1] == edge:
                grid.pos_nuclei.add(nucleus)
            else:
                grid.neg_nuclei.add(nucleus)
 
    return

def get_centrosome_energy_pos(grid, cells):
    i, j = grid.centrosome_pos
    energy = 0

    for protein in grid.pp:
        x, y = protein
        other = cells["{}, {}".format(x, y)]

        distance = math.sqrt((x - i)**2 + (y - j)**2)
        if distance != 0:
            strength = 1/distance * 10
        else:
            strength = 10

        if other.polarity_protein_A:
            rate = p_to_c_match_rate
        if other.polarity_protein_B:
            rate = p_to_c_differ_rate

        energy += strength * rate
    
    return energy

def get_centrosome_energy_neg(grid, cells):
    i, j = grid.centrosome_neg
    energy = 0

    for protein in grid.pp:
        x, y = protein
        other = cells["{}, {}".format(x, y)]

        distance = math.sqrt((x - i)**2 + (y - j)**2)
        if distance != 0:
            strength = 1/distance * 10
        else:
            strength = 10

        if other.polarity_protein_B:
            rate = p_to_c_match_rate
        if other.polarity_protein_A:
            rate = p_to_c_differ_rate

        energy += strength * rate
    
    return energy


def move_centrosomes(positions, cells, grids, centrosome_threshold):
    for grid in grids:
        if grid.splitting:
            a, b = grid.centrosome_pos
            c, d = grid.centrosome_neg

            if get_centrosome_energy_pos(grid, cells) > centrosome_threshold and not grid.separating_nuclei_pos:
                if grid.centrosome_pos_direction == "left" and a > .20 * abs(grid.Max_Width - grid.Min_Width) // 1 + grid.Min_Width:
                    cells["{}, {}".format(a, b)].centrosome_pos = False
                    cells["{}, {}".format(a - 1, b)].centrosome_pos = True
                    positions.add((a - 1, b))
                    if not cells["{}, {}".format(a, b)].nucleus and not cells["{}, {}".format(a, b)].status and not cells["{}, {}".format(a, b)].polarity_protein_A and not cells["{}, {}".format(a, b)].polarity_protein_B and not cells["{}, {}".format(a, b)].centrosome_neg:
                        positions.remove((a, b))
                    if a - 1 <= .20 * abs(grid.Max_Width - grid.Min_Width) // 1 + grid.Min_Width or a <= .20 * abs(grid.Max_Width - grid.Min_Width) // 1 + grid.Min_Width:
                        grid.separating_nuclei_pos = True
                elif grid.centrosome_pos_direction == "right" and a < .80 * abs(grid.Max_Width - grid.Min_Width) // 1 + grid.Min_Width:
                    cells["{}, {}".format(a, b)].centrosome_pos = False
                    cells["{}, {}".format(a + 1, b)].centrosome_pos = True
                    positions.add((a + 1, b))
                    if not cells["{}, {}".format(a, b)].nucleus and not cells["{}, {}".format(a, b)].status and not cells["{}, {}".format(a, b)].polarity_protein_A and not cells["{}, {}".format(a, b)].polarity_protein_B and not cells["{}, {}".format(a, b)].centrosome_neg:
                        positions.remove((a, b))
                    if a + 1 >= .80 * abs(grid.Max_Width - grid.Min_Width) // 1 + grid.Min_Width or a >= .80 * abs(grid.Max_Width - grid.Min_Width) // 1 + grid.Min_Width:
                        grid.separating_nuclei_pos = True
                elif grid.centrosome_pos_direction == "up" and b > .20 * abs(grid.Max_Length - grid.Min_Length) // 1 + grid.Min_Length:
                    cells["{}, {}".format(a, b)].centrosome_pos = False
                    cells["{}, {}".format(a, b - 1)].centrosome_pos = True
                    positions.add((a, b - 1))
                    if not cells["{}, {}".format(a, b)].nucleus and not cells["{}, {}".format(a, b)].status and not cells["{}, {}".format(a, b)].polarity_protein_A and not cells["{}, {}".format(a, b)].polarity_protein_B and not cells["{}, {}".format(a, b)].centrosome_neg:
                        positions.remove((a, b))
                    if b - 1 <= .20 * abs(grid.Max_Length - grid.Min_Length) // 1 + grid.Min_Length or b <= .20 * abs(grid.Max_Length - grid.Min_Length) // 1 + grid.Min_Length:
                        grid.separating_nuclei_pos = True
                elif grid.centrosome_pos_direction == "down" and b < .80 * abs(grid.Max_Length - grid.Min_Length) // 1 + grid.Min_Length:
                    cells["{}, {}".format(a, b)].centrosome_pos = False
                    cells["{}, {}".format(a, b + 1)].centrosome_pos = True
                    positions.add((a, b + 1))
                    if not cells["{}, {}".format(a, b)].nucleus and not cells["{}, {}".format(a, b)].status and not cells["{}, {}".format(a, b)].polarity_protein_A and not cells["{}, {}".format(a, b)].polarity_protein_B and not cells["{}, {}".format(a, b)].centrosome_neg:
                        positions.remove((a, b))
                    if b + 1 >= .80 * abs(grid.Max_Length - grid.Min_Length) // 1 + grid.Min_Length or b >= .80 * abs(grid.Max_Length - grid.Min_Length) // 1 + grid.Min_Length:
                        grid.separating_nuclei_pos = True
                else:
                    grid.separating_nuclei_pos = True
            else:
                grid.separating_nuclei_pos = True

            if get_centrosome_energy_neg(grid, cells) > centrosome_threshold and not grid.separating_nuclei_neg:
                if grid.centrosome_pos_direction == "left" and c < .80 * abs(grid.Max_Width - grid.Min_Width) // 1 + grid.Min_Width:
                    cells["{}, {}".format(c, d)].centrosome_neg = False
                    cells["{}, {}".format(c + 1, d)].centrosome_neg = True
                    positions.add((c + 1, d))
                    if not cells["{}, {}".format(c, d)].nucleus and not cells["{}, {}".format(c, d)].status and not cells["{}, {}".format(c, d)].polarity_protein_A and not cells["{}, {}".format(c, d)].polarity_protein_B and not cells["{}, {}".format(c, d)].centrosome_neg:
                        positions.remove((c, d))
                    if c + 1 >= .80 * abs(grid.Max_Width - grid.Min_Width) // 1 + grid.Min_Width or c >= .80 * abs(grid.Max_Width - grid.Min_Width) // 1 + grid.Min_Width:
                        grid.separating_nuclei_neg = True
                elif grid.centrosome_pos_direction == "right" and c > .20 * abs(grid.Max_Width - grid.Min_Width) // 1 + grid.Min_Width:
                    cells["{}, {}".format(c, d)].centrosome_neg = False
                    cells["{}, {}".format(c - 1, d)].centrosome_neg = True
                    positions.add((c - 1, d))
                    if not cells["{}, {}".format(c, d)].nucleus and not cells["{}, {}".format(c, d)].status and not cells["{}, {}".format(c, d)].polarity_protein_A and not cells["{}, {}".format(c, d)].polarity_protein_B and not cells["{}, {}".format(c, d)].centrosome_neg:
                        positions.remove((c, d))
                    if c - 1 <= .20 * abs(grid.Max_Width - grid.Min_Width) // 1 + grid.Min_Width or c <= .20 * abs(grid.Max_Width - grid.Min_Width) // 1 + grid.Min_Width:
                        grid.separating_nuclei_neg = True
                elif grid.centrosome_pos_direction == "up" and d < .80 * abs(grid.Max_Length - grid.Min_Length) // 1 + grid.Min_Length:
                    cells["{}, {}".format(c, d)].centrosome_neg = False
                    cells["{}, {}".format(c, d + 1)].centrosome_neg = True
                    positions.add((c, d + 1))
                    if not cells["{}, {}".format(c, d)].nucleus and not cells["{}, {}".format(c, d)].status and not cells["{}, {}".format(c, d)].polarity_protein_A and not cells["{}, {}".format(c, d)].polarity_protein_B and not cells["{}, {}".format(c, d)].centrosome_neg:
                        positions.remove((c, d))
                    if d + 1 >= .80 * abs(grid.Max_Length - grid.Min_Length) // 1 + grid.Min_Length or d >= .80 * abs(grid.Max_Length - grid.Min_Length) // 1 + grid.Min_Length:
                        grid.separating_nuclei_neg = True
                elif grid.centrosome_pos_direction == "down" and d > .20 * abs(grid.Max_Length - grid.Min_Length) // 1 + grid.Min_Length:
                    cells["{}, {}".format(c, d)].centrosome_neg = False
                    cells["{}, {}".format(c, d - 1)].centrosome_neg = True
                    positions.add((c, d - 1))
                    if not cells["{}, {}".format(c, d)].nucleus and not cells["{}, {}".format(c, d)].status and not cells["{}, {}".format(c, d)].polarity_protein_A and not cells["{}, {}".format(c, d)].polarity_protein_B and not cells["{}, {}".format(c, d)].centrosome_neg:
                        positions.remove((c, d))
                    if d - 1 <= .20 * abs(grid.Max_Length - grid.Min_Length) // 1 + grid.Min_Length or d <= .20 * abs(grid.Max_Length - grid.Min_Length) // 1 + grid.Min_Length:
                        grid.separating_nuclei_neg = True
                else:
                    grid.separating_nuclei_neg = True
            else:
                grid.separating_nuclei_neg = True
    
    return positions, cells

def move_nuclei(positions, cells, grids):
    for grid in grids:
        if grid.separating_nuclei_pos and grid.separating_nuclei_neg:

            for nucleus in grid.pos_nuclei:
                if nucleus == grid.centrosome_pos:
                    grid.pos_ready_divide = True

            for nucleus in grid.neg_nuclei:
                if nucleus == grid.centrosome_neg:
                    grid.neg_ready_divide = True

            new_pos = set()
            new_neg = set()
            if grid.centrosome_pos_direction == "left":
                if not grid.pos_ready_divide:
                    for nucleus in grid.pos_nuclei:
                        x, y = nucleus
                        positions.add((x - 1, y))
                        cells["{}, {}".format(x - 1, y)].nucleus = True
                        cells["{}, {}".format(x, y)].nucleus = False
                        new_pos.add((x - 1, y))
                        if not cells["{}, {}".format(x, y)].status and not cells["{}, {}".format(x, y)].polarity_protein_A and not cells["{}, {}".format(x, y)].polarity_protein_B and not cells["{}, {}".format(x, y)].centrosome_pos and not cells["{}, {}".format(x, y)].centrosome_neg:
                            if (x, y) in positions:
                                positions.remove((x, y))
                if not grid.neg_ready_divide:
                    for nucleus in grid.neg_nuclei:
                        x, y = nucleus
                        positions.add((x + 1, y))
                        cells["{}, {}".format(x + 1, y)].nucleus = True
                        cells["{}, {}".format(x, y)].nucleus = False
                        new_neg.add((x + 1, y))
                        if not cells["{}, {}".format(x, y)].status and not cells["{}, {}".format(x, y)].polarity_protein_A and not cells["{}, {}".format(x, y)].polarity_protein_B and not cells["{}, {}".format(x, y)].centrosome_pos and not cells["{}, {}".format(x, y)].centrosome_neg:
                            if (x, y) in positions:
                                positions.remove((x, y))
            if grid.centrosome_pos_direction == "right":
                if not grid.pos_ready_divide:
                    for nucleus in grid.pos_nuclei:
                        x, y = nucleus
                        positions.add((x + 1, y))
                        cells["{}, {}".format(x + 1, y)].nucleus = True
                        cells["{}, {}".format(x, y)].nucleus = False
                        new_pos.add((x + 1, y))
                        if not cells["{}, {}".format(x, y)].status and not cells["{}, {}".format(x, y)].polarity_protein_A and not cells["{}, {}".format(x, y)].polarity_protein_B and not cells["{}, {}".format(x, y)].centrosome_pos and not cells["{}, {}".format(x, y)].centrosome_neg:
                            if (x, y) in positions:
                                positions.remove((x, y))
                if not grid.neg_ready_divide:
                    for nucleus in grid.neg_nuclei:
                        x, y = nucleus
                        positions.add((x - 1, y))
                        cells["{}, {}".format(x - 1, y)].nucleus = True
                        cells["{}, {}".format(x, y)].nucleus = False
                        new_neg.add((x - 1, y))
                        if not cells["{}, {}".format(x, y)].status and not cells["{}, {}".format(x, y)].polarity_protein_A and not cells["{}, {}".format(x, y)].polarity_protein_B and not cells["{}, {}".format(x, y)].centrosome_pos and not cells["{}, {}".format(x, y)].centrosome_neg:
                            if (x, y) in positions:
                                positions.remove((x, y))
            if grid.centrosome_pos_direction == "up":
                if not grid.pos_ready_divide:
                    for nucleus in grid.pos_nuclei:
                        x, y = nucleus
                        positions.add((x, y - 1))
                        cells["{}, {}".format(x, y - 1)].nucleus = True
                        cells["{}, {}".format(x, y)].nucleus = False
                        new_pos.add((x, y - 1))
                        if not cells["{}, {}".format(x, y)].status and not cells["{}, {}".format(x, y)].polarity_protein_A and not cells["{}, {}".format(x, y)].polarity_protein_B and not cells["{}, {}".format(x, y)].centrosome_pos and not cells["{}, {}".format(x, y)].centrosome_neg:
                            if (x, y) in positions:
                                positions.remove((x, y))
                if not grid.neg_ready_divide:
                    for nucleus in grid.neg_nuclei:
                        x, y = nucleus
                        positions.add((x, y + 1))
                        cells["{}, {}".format(x, y + 1)].nucleus = True
                        cells["{}, {}".format(x, y)].nucleus = False
                        new_neg.add((x, y + 1))
                        if not cells["{}, {}".format(x, y)].status and not cells["{}, {}".format(x, y)].polarity_protein_A and not cells["{}, {}".format(x, y)].polarity_protein_B and not cells["{}, {}".format(x, y)].centrosome_pos and not cells["{}, {}".format(x, y)].centrosome_neg:
                            if (x, y) in positions:
                                positions.remove((x, y))
            if grid.centrosome_pos_direction == "down":
                if not grid.pos_ready_divide:
                    for nucleus in grid.pos_nuclei:
                        x, y = nucleus
                        positions.add((x, y + 1))
                        cells["{}, {}".format(x, y + 1)].nucleus = True
                        cells["{}, {}".format(x, y)].nucleus = False
                        new_pos.add((x, y + 1))
                        if not cells["{}, {}".format(x, y)].status and not cells["{}, {}".format(x, y)].polarity_protein_A and not cells["{}, {}".format(x, y)].polarity_protein_B and not cells["{}, {}".format(x, y)].centrosome_pos and not cells["{}, {}".format(x, y)].centrosome_neg:
                            if (x, y) in positions:
                                positions.remove((x, y))
                if not grid.neg_ready_divide:
                    for nucleus in grid.neg_nuclei:
                        x, y = nucleus
                        positions.add((x, y - 1))
                        cells["{}, {}".format(x, y - 1)].nucleus = True
                        cells["{}, {}".format(x, y)].nucleus = False
                        new_neg.add((x, y - 1))
                        if not cells["{}, {}".format(x, y)].status and not cells["{}, {}".format(x, y)].polarity_protein_A and not cells["{}, {}".format(x, y)].polarity_protein_B and not cells["{}, {}".format(x, y)].centrosome_pos and not cells["{}, {}".format(x, y)].centrosome_neg:
                            if (x, y) in positions:
                                positions.remove((x, y))

            grid.pos_nuclei = new_pos
            grid.neg_nuclei = new_neg
    
    return positions, cells

def divide_cells(positions, cells, grids, split_cells, centrosome_threshold, centrosome_threshold_multiplier, cell_name_counter):
    for grid in grids:
        if grid.pos_ready_divide and grid.neg_ready_divide:
            if grid.centrosome_pos_direction == "left" or grid.centrosome_pos_direction == "right":
                division_line = abs(grid.centrosome_pos[0] + grid.centrosome_neg[0]) // 2
                grid_A = Grid(division_line, grid.Min_Width, grid.Max_Length, grid.Min_Length, cell_name_counter, grid.lineage + [str(cell_name_counter)])
                grid_B = Grid(grid.Max_Width, division_line + 1, grid.Max_Length, grid.Min_Length, cell_name_counter + 1, grid.lineage + [str(cell_name_counter + 1)])

                positions, cells = redistribute_pp(positions, cells, grid_A, division_line, grid.centrosome_pos_direction)
                positions, cells = redistribute_pp(positions, cells, grid_B, division_line + 1, grid.centrosome_pos_direction)

                grids.append(grid_A)
                grids.append(grid_B)

                split_cells.append((division_line + 1, division_line + 1, grid.Min_Length, grid.Max_Length + 1))
                grids.remove(grid)
            else:
                division_line = abs(grid.centrosome_pos[1] + grid.centrosome_neg[1]) // 2
                grid_A = Grid(grid.Max_Width, grid.Min_Width, grid.Max_Length, division_line + 1, cell_name_counter, grid.lineage + [str(cell_name_counter)])
                grid_B = Grid(grid.Max_Width, grid.Min_Width, division_line, grid.Min_Length, cell_name_counter + 1, grid.lineage + [str(cell_name_counter + 1)])

                positions, cells = redistribute_pp(positions, cells, grid_A, division_line + 1, grid.centrosome_pos_direction)
                positions, cells = redistribute_pp(positions, cells, grid_B, division_line, grid.centrosome_pos_direction)

                grids.append(grid_A)
                grids.append(grid_B)

                split_cells.append((grid.Min_Width, grid.Max_Width + 1, division_line + 1, division_line + 1))
                grids.remove(grid)

            centrosome_threshold *= centrosome_threshold_multiplier

            cell_name_counter += 2
    
    return positions, cells, grids, split_cells, centrosome_threshold, cell_name_counter

def redistribute_pp(positions, cells, grid, new_edge, side):
    proteins = set()
    on_membrane = set()
    new_additions = []

    for pos in grid.positions:
        col, row = pos
        if cells["{}, {}".format(col, row)].polarity_protein_A or cells["{}, {}".format(col, row)].polarity_protein_B:
            proteins.add(pos)

    for protein in proteins:
        col, row = protein
        if col == grid.Min_Width or col == grid.Max_Width or row == grid.Min_Length or row == grid.Max_Length:
            on_membrane.add(protein)
            
    top = []
    left = []
    bottom = []
    right = []

    for i in range(grid.Min_Width, grid.Max_Width + 1):
        top.append((i, grid.Min_Length))
    top.sort()
    top.reverse()

    for i in range(grid.Min_Length, grid.Max_Length + 1):
        left.append((grid.Min_Width, i))
    left.sort() 

    for i in range(grid.Min_Width, grid.Max_Width + 1):
        bottom.append((i, grid.Max_Length))
    bottom.sort()

    for i in range(grid.Min_Length, grid.Max_Length + 1):
        right.append((grid.Max_Width, i))
    right.sort()
    right.reverse()

    if new_edge == grid.Max_Width and (side == "left" or side == "right"):
        now = top + left + bottom
        now.remove((grid.Min_Width, grid.Min_Length))
        now.remove((grid.Min_Width, grid.Max_Length))

        half = len(right) // 2
        all = right[half:] + now + right[:half]
        all.remove((grid.Max_Width, grid.Min_Length))
        all.remove((grid.Max_Width, grid.Max_Length))

        max = 200
        min = -200

        for position in right:
            x, y = position
            if (cells["{}, {}".format(x, y)].polarity_protein_A or cells["{}, {}".format(x, y)].polarity_protein_B) and (y != grid.Min_Length and y != grid.Max_Length):
                if y <= right[half][1] and y > min:
                    min = y
                if y > right[half][1] and y < max:
                    max = y

        if min != -200:
            new = []
            for i in range(min, grid.Min_Length, -1):
                new.append((grid.Max_Width, i))
            now = new + now
        
        if max != 200:
            new = []
            for i in range(max, grid.Max_Length):
                new.append((grid.Max_Width, i))
            new.reverse()
            now = now + new

    elif new_edge == grid.Min_Length and (side == "up" or side == "down"):
        now = left + bottom + right
        now.remove((grid.Max_Width, grid.Max_Length))
        now.remove((grid.Min_Width, grid.Max_Length))

        half = len(top) // 2
        all = top[half:] + now + top[:half]
        all.remove((grid.Max_Width, grid.Min_Length))
        all.remove((grid.Min_Width, grid.Min_Length))

        min = -200
        max = 200

        for position in top:
            x, y = position
            if (cells["{}, {}".format(x, y)].polarity_protein_A or cells["{}, {}".format(x, y)].polarity_protein_B) and (x != grid.Min_Width and x != grid.Max_Width):
                if x <= top[half][1] and x > min:
                    min = x
                if x > top[half][1] and x < max:
                    max = x

        if min != -200:
            new = []
            for i in range(min, grid.Min_Width, -1):
                new.append((i, grid.Min_Length))
            now = new + now
        
        if max != 200:
            new = []
            for i in range(max, grid.Max_Width):
                new.append((i, grid.Min_Length))
            new.reverse()
            now = now + new

    elif new_edge == grid.Min_Width and (side == "left" or side == "right"):
        now = bottom + right + top
        now.remove((grid.Max_Width, grid.Max_Length))
        now.remove((grid.Max_Width, grid.Min_Length))

        half = len(left) // 2
        all = left[half:] + now + left[:half]
        all.remove((grid.Min_Width, grid.Min_Length))
        all.remove((grid.Min_Width, grid.Max_Length))

        max = 200
        min = -200

        for position in left:
            x, y = position
            if (cells["{}, {}".format(x, y)].polarity_protein_A or cells["{}, {}".format(x, y)].polarity_protein_B) and (y != grid.Min_Length and y != grid.Max_Length):
                if y < left[half][1] and y > min:
                    min = y
                if y >= left[half][1] and y < max:
                    max = y

        if min != -200:
            new = []
            for i in range(min, grid.Min_Length, -1):
                new.append((grid.Min_Width, i))
            new.reverse()
            now = now + new
        
        if max != 200:
            new = []
            for i in range(max, grid.Max_Length):
                new.append((grid.Min_Width, i))
            now = new + now

    elif new_edge == grid.Max_Length and (side == "up" or side == "down"):
        now = right + top + left
        now.remove((grid.Max_Width, grid.Min_Length))
        now.remove((grid.Min_Width, grid.Min_Length))

        half = len(bottom) // 2
        all = bottom[half:] + now + bottom[:half]
        all.remove((grid.Max_Width, grid.Max_Length))
        all.remove((grid.Min_Width, grid.Max_Length))

        max = 200
        min = -200

        for position in bottom:
            x, y = position
            if (cells["{}, {}".format(x, y)].polarity_protein_A or cells["{}, {}".format(x, y)].polarity_protein_B) and (x != grid.Min_Width and x != grid.Max_Width):
                if x < bottom[half][1] and x > min:
                    min = x
                if x >= bottom[half][1] and x < max:
                    max = x

        if min != -200:
            new = []
            for i in range(min, grid.Min_Width, -1):
                new.append((i, grid.Max_Length))
            new.reverse()
            now = now + new
        
        if max != 200:
            new = []
            for i in range(max, grid.Max_Width):
                new.append((i, grid.Max_Length))
            now = new + now

    for pp in on_membrane:
        x, y = pp
        me = cells["{}, {}".format(x, y)]

        place = now.index(pp)
        relative = place/len(now)
        new_place = all[int(relative * len(all)) - 1]

        adict = {"A": False,  "B": False}

        if me.polarity_protein_A:
            adict["A"] = True
        if me.polarity_protein_B:   
            adict["B"] = True

        me.polarity_protein_A = False
        me.polarity_protein_B = False
        if not me.status and not me.nucleus and not me.centrosome_pos and not me.centrosome_neg:
            positions.remove(pp)

        new_additions.append((new_place, adict))

    for details in new_additions:
        position, adict = details
        x, y = position

        positions.add(position)
        if adict["A"] == True:
            cells["{}, {}".format(x, y)].polarity_protein_A = True
        if adict["B"] == True:
            cells["{}, {}".format(x, y)].polarity_protein_B = True

    return positions, cells

def differentiate(grids, cells):
    for grid in grids:
        if grid.can_divide == False:
            blacks = 0
            greys = 0
            pp_A = 0
            pp_B = 0

            for position in grid.positions:
                x, y = position
                me = cells["{}, {}".format(x, y)]

                if me.status == 1:
                    blacks += 1
                elif me.status == 2:
                    greys += 1
                if me.polarity_protein_A:
                    pp_A += 1
                if me.polarity_protein_B:
                    pp_B += 1

            if greys >= 7:
                grid.differentiated_type = 1
            elif blacks >= 10:
                grid.differentiated_type = 2
            else:
                grid.differentiated_type = 3
