import math

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