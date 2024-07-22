import random
from Classes_and_Grids import new_cells_obj

#get energy of the grid
def get_total_energy(cells, positions, distance_scaler):
    energy = 0
    for position in positions:
        i, j = position
        energy += cells["{}, {}".format(i, j)].get_energy(positions, cells, distance_scaler)
    return energy

def check_energies(position, orig_status, positions, new_positions, directions, cells, distance_scaler):
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
            directions[i] = (cells["{}, {}".format(x, y)].get_energy(positions, cells, distance_scaler), directions[i][1])
            cells["{}, {}".format(x, y)].status = 0
            cells["{}, {}".format(col, row)].status = orig_status

        
    directions.sort()

    return directions

#rule_set
def adjust_grid(positions, cells, grids, distance_scaler):
    new_positions = set()
    new_cells = new_cells_obj(grids)
            
    for position in positions:
        col, row = position
        orig_status = cells["{}, {}".format(col, row)].status
        pos_grid = cells["{}, {}".format(col, row)].grid

        if cells["{}, {}".format(col, row)].nucleus:
            new_positions.add(position)
            new_cells["{}, {}".format(col, row)].nucleus = True
        if cells["{}, {}".format(col, row)].polarity_protein_A:
            new_positions.add(position)
            new_cells["{}, {}".format(col, row)].polarity_protein_A = True
        if cells["{}, {}".format(col, row)].polarity_protein_B:
            new_positions.add(position)
            new_cells["{}, {}".format(col, row)].polarity_protein_B = True
        if cells["{}, {}".format(col, row)].centrosome_neg:
            new_positions.add(position)
            new_cells["{}, {}".format(col, row)].centrosome_neg = True
        if cells["{}, {}".format(col, row)].centrosome_pos:
            new_positions.add(position)
            new_cells["{}, {}".format(col, row)].centrosome_pos = True

        if not ((cells["{}, {}".format(col, row)].nucleus or cells["{}, {}".format(col, row)].polarity_protein_A or cells["{}, {}".format(col, row)].polarity_protein_B) and cells["{}, {}".format(col, row)].status == 0):
        
            #initializes some high energies 
            directions = [(float('inf'), "left"), (float('inf'), "right"), (float('inf'), "up"), (float('inf'), "down"), (float('inf'), "leftup"), (float('inf'), "leftdown"), (float('inf'), "rightup"), (float('inf'), "rightdown"), (cells["{}, {}".format(col, row)].get_energy(positions, cells, distance_scaler), "stay")]

            if col == pos_grid.Min_Width:
                directions.remove((float('inf'), "left"))
                directions.remove((float('inf'), "leftup"))
                directions.remove((float('inf'), "leftdown"))

            if col == pos_grid.Max_Width:
                directions.remove((float('inf'), "right"))
                directions.remove((float('inf'), "rightup"))
                directions.remove((float('inf'), "rightdown"))

            if row == pos_grid.Min_Length:
                directions.remove((float('inf'), "up"))
                if col != pos_grid.Min_Width:
                    directions.remove((float('inf'), "leftup"))
                if col != pos_grid.Max_Width:
                    directions.remove((float('inf'), "rightup"))

            if row == pos_grid.Max_Length:
                directions.remove((float('inf'), "down"))
                if col != pos_grid.Min_Width:
                    directions.remove((float('inf'), "leftdown"))
                if col != pos_grid.Max_Width:
                    directions.remove((float('inf'), "rightdown"))

            #iterates over all possible directions to move to.
            directions = check_energies(position, orig_status, positions, new_positions, directions, cells, distance_scaler)
                    
            if directions[0][1] == "left" and new_cells["{}, {}".format((col - 1), row)].status == 0 and cells["{}, {}".format((col - 1), row)].status == 0:
                new_cells["{}, {}".format((col - 1), row)].status = orig_status
                new_positions.add(((col - 1), row))
            elif directions[0][1] == "right" and new_cells["{}, {}".format((col + 1), row)].status == 0 and cells["{}, {}".format((col + 1), row)].status == 0:
                new_cells["{}, {}".format((col + 1), row)].status = orig_status
                new_positions.add(((col + 1), row))
            elif directions[0][1] == "up" and new_cells["{}, {}".format(col, (row - 1))].status == 0 and cells["{}, {}".format(col, (row - 1))].status == 0:
                new_cells["{}, {}".format(col, (row - 1))].status = orig_status
                new_positions.add((col, (row - 1)))
            elif directions[0][1] == "down" and new_cells["{}, {}".format(col, (row + 1))].status == 0 and cells["{}, {}".format(col, (row + 1))].status == 0:
                new_cells["{}, {}".format(col, (row + 1))].status = orig_status
                new_positions.add((col, (row + 1)))
            elif directions[0][1] == "leftup" and new_cells["{}, {}".format((col - 1), (row - 1))].status == 0 and cells["{}, {}".format((col - 1), (row - 1))].status == 0:
                new_cells["{}, {}".format((col - 1), (row - 1))].status = orig_status
                new_positions.add(((col - 1), (row - 1)))
            elif directions[0][1] == "leftdown" and new_cells["{}, {}".format((col - 1), (row + 1))].status == 0 and cells["{}, {}".format((col - 1), (row + 1))].status == 0:
                new_cells["{}, {}".format((col - 1), (row + 1))].status = orig_status
                new_positions.add(((col - 1), (row + 1)))
            elif directions[0][1] == "rightup" and new_cells["{}, {}".format((col + 1), (row - 1))].status == 0 and cells["{}, {}".format((col + 1), (row - 1))].status == 0:
                new_cells["{}, {}".format((col + 1), (row - 1))].status = orig_status
                new_positions.add(((col + 1), (row - 1)))
            elif directions[0][1] == "rightdown" and new_cells["{}, {}".format((col + 1), (row + 1))].status == 0 and cells["{}, {}".format((col + 1), (row + 1))].status == 0:
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

        neighbors = get_neighbors(position, cells)
        errbody = [position]

        for neighbor in neighbors:
            x, y = neighbor
            if neighbor in positions and cells["{}, {}".format(x, y)].status != 0 and cells["{}, {}".format(x, y)].status == cells["{}, {}".format(col, row)].status and (x, y) in cells["{}, {}".format(col, row)].grid.positions:
                group_potential += 1
                errbody.append(neighbor)
        
        if group_potential >= 4:
            new_group = set()
            for pos in errbody:
                new_group.add(pos)
                neighbors1 = get_neighbors(pos, cells)
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

def shifting(positions, groups, cells, grids):
    amalg = set()
    new_cells = new_cells_obj(grids)
    new_positions = set()

    for cell in cells:
        if cells[cell].nucleus:
            new_positions.add((cells[cell].i, cells[cell].j))
            new_cells["{}, {}".format(cells[cell].i, cells[cell].j)].nucleus = True
            amalg.add((cells[cell].i, cells[cell].j))
        if cells[cell].polarity_protein_A:
            new_positions.add((cells[cell].i, cells[cell].j))
            new_cells["{}, {}".format(cells[cell].i, cells[cell].j)].polarity_protein_A = True
            amalg.add((cells[cell].i, cells[cell].j))
        if cells[cell].polarity_protein_B:
            new_positions.add((cells[cell].i, cells[cell].j))
            new_cells["{}, {}".format(cells[cell].i, cells[cell].j)].polarity_protein_B = True
            amalg.add((cells[cell].i, cells[cell].j))
        if cells[cell].centrosome_pos:
            new_positions.add((cells[cell].i, cells[cell].j))
            new_cells["{}, {}".format(cells[cell].i, cells[cell].j)].centrosome_pos = True
            amalg.add((cells[cell].i, cells[cell].j))
        if cells[cell].centrosome_neg:
            new_positions.add((cells[cell].i, cells[cell].j))
            new_cells["{}, {}".format(cells[cell].i, cells[cell].j)].centrosome_neg = True
            amalg.add((cells[cell].i, cells[cell].j))

    for group in groups:
        amalg = amalg.union(group)

    for group in groups:

        can_move = True

        orig_point = next(iter(group))
        a, b = orig_point
        orig_status = cells["{}, {}".format(a, b)].status

        pos_grid = cells["{}, {}".format(a, b)].grid

        directions = ["left", "right", "up", "down", "leftup", "leftdown", "rightup", "rightdown", "stay"]

        for pos in group:
            x, y = pos
            pos_grid = cells["{}, {}".format(x, y)].grid
            if x == pos_grid.Min_Width:
                if "left" in directions:
                    directions.remove("left")
                if "leftup" in directions:
                    directions.remove("leftup")
                if "leftdown" in directions:
                    directions.remove("leftdown")

            if x == pos_grid.Max_Width:
                if "right" in directions:
                    directions.remove("right")
                if "rightup" in directions:
                    directions.remove("rightup")
                if "rightdown" in directions:
                    directions.remove("rightdown")

            if y == pos_grid.Min_Length:
                if "up" in directions:
                    directions.remove("up")
                if "leftup" in directions:
                    directions.remove("leftup")
                if "rightup" in directions:
                    directions.remove("rightup")

            if y == pos_grid.Max_Length:
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
                if new_cells["{}, {}".format((x - 1) , y)].status != 0 or ((x - 1), y) not in pos_grid.positions: 
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
                if new_cells["{}, {}".format((x + 1) , y)].status != 0 or ((x + 1), y) not in pos_grid.positions: 
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
                if new_cells["{}, {}".format(x, (y - 1) )].status != 0 or (x, (y - 1)) not in pos_grid.positions: 
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
                if new_cells["{}, {}".format(x, (y + 1) )].status != 0 or (x, (y + 1)) not in pos_grid.positions: 
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
                if new_cells["{}, {}".format((x - 1) , (y - 1))].status != 0 or ((x - 1), (y - 1)) not in pos_grid.positions: 
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
                if new_cells["{}, {}".format((x - 1) , (y + 1))].status != 0 or ((x - 1), (y + 1)) not in pos_grid.positions: 
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
                if new_cells["{}, {}".format((x + 1) , (y - 1))].status != 0 or ((x + 1), (y - 1)) not in pos_grid.positions: 
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
                if new_cells["{}, {}".format((x + 1) , (y + 1))].status != 0 or ((x + 1), (y + 1)) not in pos_grid.positions: 
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
            pos_grid = cells["{}, {}".format(x, y)].grid
            orig_status = cells["{}, {}".format(x, y)].status

            directions = ["left", "right", "up", "down", "leftup", "leftdown", "rightup", "rightdown", "stay"]

            if x == pos_grid.Min_Width:
                for dir in directions:
                    if dir == "left":
                        directions.remove("left")
                    if dir == "leftdown":
                        directions.remove("leftdown")
                    if dir == "left":
                        directions.remove("leftup")

            if x == pos_grid.Max_Width:
                for dir in directions:
                    if dir == "right":
                        directions.remove("right")
                    if dir == "rightdown":
                        directions.remove("rightdown")
                    if dir == "left":
                        directions.remove("rightup")
            if y == pos_grid.Min_Length:
                for dir in directions:
                    if dir == "up":
                        directions.remove("up")
                    if dir == "leftup":
                        directions.remove("leftup")
                    if dir == "rightup":
                        directions.remove("rightup")

            if y == pos_grid.Max_Length:
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
                        if new_cells["{}, {}".format((x - 1) , y)].status == 0 and ((x - 1), y) in pos_grid.positions:
                            unplaced = False
                            new_positions.add(((x - 1) , y))
                            new_cells["{}, {}".format((x - 1) , y)].status = orig_status

                    elif directions[i] == "right":
                        if new_cells["{}, {}".format((x + 1) , y)].status == 0 and ((x + 1), y) in pos_grid.positions:
                            unplaced = False
                            new_positions.add(((x + 1) , y))
                            new_cells["{}, {}".format((x + 1) , y)].status = orig_status

                    elif directions[i] == "up":
                        if new_cells["{}, {}".format(x, (y - 1) )].status == 0 and (x, (y - 1)) in pos_grid.positions:
                            unplaced = False
                            new_positions.add((x, (y - 1) ))
                            new_cells["{}, {}".format(x, (y - 1) )].status = orig_status
                    
                    elif directions[i] == "down":
                        if new_cells["{}, {}".format(x, (y + 1) )].status == 0 and (x, (y + 1)) in pos_grid.positions:
                            unplaced = False
                            new_positions.add((x, (y + 1) ))
                            new_cells["{}, {}".format(x, (y + 1) )].status = orig_status

                    elif directions[i] == "leftup":
                        if new_cells["{}, {}".format((x - 1) , (y - 1))].status == 0 and ((x - 1), (y - 1)) in pos_grid.positions:
                            unplaced = False
                            new_positions.add(((x - 1) , (y - 1) ))
                            new_cells["{}, {}".format((x - 1) , (y - 1) )].status = orig_status

                    elif directions[i] == "leftdown":
                        if new_cells["{}, {}".format((x - 1) , (y + 1))].status == 0 and ((x - 1), (y + 1)) in pos_grid.positions:
                            unplaced = False
                            new_positions.add(((x - 1) , (y + 1) ))
                            new_cells["{}, {}".format((x - 1) , (y + 1) )].status = orig_status
            
                    elif directions[i] == "rightup":
                        if new_cells["{}, {}".format((x + 1) , (y - 1))].status == 0 and ((x + 1), (y - 1)) in pos_grid.positions:
                            unplaced = False
                            new_positions.add(((x + 1) , (y - 1) ))
                            new_cells["{}, {}".format((x + 1) , (y - 1) )].status = orig_status

                    elif directions[i] == "rightdown":
                        if new_cells["{}, {}".format((x + 1) , (y + 1))].status == 0 and ((x + 1), (y + 1)) in pos_grid.positions:
                            unplaced = False
                            new_positions.add(((x + 1) , (y + 1) ))
                            new_cells["{}, {}".format((x + 1) , (y + 1) )].status = orig_status
                    else:
                        if new_cells["{}, {}".format(x, y)].status == 0:
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
def get_neighbors(pos, cells):
    x,y = pos
    pos_grid = cells["{}, {}".format(x, y)].grid
    neighbors = []
    potential_neighbors = [(-1, 0), (1, 0), (0, 1), (0, -1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

    if x == pos_grid.Min_Width:
        potential_neighbors.remove((-1, 0))
        potential_neighbors.remove((-1, 1))
        potential_neighbors.remove((-1, -1))
    if x == pos_grid.Max_Width:
        potential_neighbors.remove((1, 0))
        potential_neighbors.remove((1, 1))
        potential_neighbors.remove((1, -1))
    if y == pos_grid.Min_Length:
        potential_neighbors.remove((0, -1))
        if (1, -1) in potential_neighbors:
            potential_neighbors.remove((1, -1))
        if (-1, -1) in potential_neighbors:
            potential_neighbors.remove((-1, -1))
    if y == pos_grid.Max_Length:
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
