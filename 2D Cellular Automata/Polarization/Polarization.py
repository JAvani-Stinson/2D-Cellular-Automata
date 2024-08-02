import pygame
import random
import os
from datetime import datetime
from Classes_and_Grids import Grid, new_cells_obj
from Classes_and_Grids import HEIGHT, WIDTH, TILE_SIZE, GRID_HEIGHT, GRID_WIDTH, clock, FPS, screen, LBLUE, black_btn, grey_btn, nuc_btn, pp_btn
from Classes_and_Grids import gen, draw_grid
from Classes_and_Grids import I_to_I, II_to_II, I_to_II
from Cytoplasmic_Determinant_Movement import grouping, adjust_grid, get_total_energy
from Output import make_png, make_mp4, plot_it, make_tree, save_data
from Splitting_Process import move_pp_A, move_pp_B, double_nucleus, move_centrosomes, move_nuclei, divide_cells, differentiate
from Splitting_Process import p_to_c_differ_rate, p_to_c_match_rate


#initiate pygame
pygame.init()

def link_attributes(positions, cells, grids):
    for grid in grids:
        grid.nucleus = set()
        grid.pp = set()
        grid.centrosome_pos = ()
        grid.centrosome_neg = ()

    for position in positions:
        x, y = position
        me = cells["{}, {}".format(x, y)]
        grid = me.grid

        if me.nucleus:
            grid.nucleus.add((x, y))
        if me.polarity_protein_A or me.polarity_protein_B:
            grid.pp.add((x, y))
        if me.centrosome_pos:
            grid.centrosome_pos = (x, y)
        if me.centrosome_neg:
            grid.centrosome_neg = (x, y)

#starts the game
def main():

    #sStarts the game (as Conway) in a paused state and gives the "speed" of play
    running = True
    playing = False

    count = 0
    update_freq = 30

    num = 0
    time = 0
    x_coord = []
    y_coord = []

    cell_name_counter = 1

    #Some flags/toggles
    sanity_checks = False
    color_groups = False
    color_grids = False

    #initializes a grouping mechanism as a list of sets
    groups = []

    #creates a list of grids and the initial grid
    grids = []
    grids.append(Grid(GRID_WIDTH - 1, 0, GRID_HEIGHT - 1, 0, 0, [str(0)]))

    #creates the cell objects for the grid
    cells = new_cells_obj(grids)

    #initializes positions
    positions = set()

    #initializes a color to add
    add_color = "nuc"

    #parameters
    distance_scaler = 30
    pp_attraction_factor = -30
    pp_repulsion_factor = 150
    centrosome_threshold = -1000
    centrosome_threshold_multiplier = 1.2

    #initializes a path for the all information to go to
    path_time = str(datetime.now())
    path = '/Users/jstinson/Desktop/2D Cellular Automata/Polarization/Runs/Polarization CA: ' + path_time + "/"
    os.makedirs(path)

    fname = path + 'parameters'
    file = open(fname, "w")
    file.write("Distance scaler = {}\n".format(distance_scaler))
    file.write("Polarity protein attraction factor = {}\n".format(pp_attraction_factor))
    file.write("Polarity protein repulsion factor = {}\n".format(pp_repulsion_factor))
    file.write("Centrosome I to I rate = {}\n".format(I_to_I))
    file.write("Centrosome II to II rate = {}\n".format(II_to_II))
    file.write("Centrosome I to II rate = {}\n".format(I_to_II))
    file.write("Centrosome threshold and multiplier = {} : {}\n".format(centrosome_threshold, centrosome_threshold_multiplier))
    file.write("Like Centrosome - Polarity Protein rate = {}\n".format(p_to_c_match_rate))
    file.write("Different Centrosome - Polarity Protein rate = {}\n".format(p_to_c_differ_rate))
    file.close

    '''
    initializes a list that will draw the lines of how cells are divided. List of tuples of size 4 in the 
    format (horizontal_start, horizontal_stop, vertical_start, vertical_stop)
    '''
    split_cells = []

    #the actual game code
    while running:

        #internal clock
        clock.tick(FPS)

        #checks if the game is no longer paused
        if playing:
            count += 1
            for grid in grids:
                grid.time += 1

        #updates the game according to "speed" set priorly
        if count >= update_freq:
            count = 0
                
            y_coord.append(get_total_energy(cells, positions, distance_scaler))
            x_coord.append(time)
            time += 1

            #takes picture
            num = make_png(screen, path, num)
        
            #determines the rule_set
            positions, cells = adjust_grid(positions, cells, grids, distance_scaler)
            groups, cells = grouping(positions, cells)
            positions, cells = move_pp_A(positions, cells, distance_scaler, pp_attraction_factor, pp_repulsion_factor)
            positions, cells = move_pp_B(positions, cells, distance_scaler, pp_attraction_factor, pp_repulsion_factor)

            link_attributes(positions, cells, grids)

            positions, cells = move_centrosomes(positions, cells, grids, centrosome_threshold)

            link_attributes(positions, cells, grids)

            positions, cells = move_nuclei(positions, cells, grids)

            link_attributes(positions, cells, grids)

            differentiate(grids, cells)

            if sanity_checks:
                blackies = 0 
                grey = 0
                pink = 0
                A = 0
                B = 0

                for cell in cells:
                    if cells[cell].status == 1:
                        blackies += 1
                    elif cells[cell].status == 2:
                        grey += 1
                    if cells[cell].nucleus:
                        pink += 1
                    if cells[cell].polarity_protein_A:
                        A += 1
                    if cells[cell].polarity_protein_B:
                        B += 1

                print("{}: blacks - {}, grey - {}, pink - {}, A - {}, B - {}".format(time, blackies, grey, pink, A, B))

        positions, cells = double_nucleus(positions, cells, grids)

        positions, cells, grids, split_cells, centrosome_threshold, cell_name_counter = divide_cells(positions, cells, grids, split_cells, centrosome_threshold, centrosome_threshold_multiplier, cell_name_counter)

        #initializes a way to see if the game is progressing
        if playing:
            status = "Playing"
        else:
            status = "Paused"

        #shows player what the rules are and if the game is proceeding
        pygame.display.set_caption("{}: Add color {}, Number of cells = {}, Color Groups = {}".format(status, add_color, len(grids), color_groups))

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

                if pp_btn.collidepoint(event.pos):
                    add_color = "pp"

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
                        if add_color == "nuc":
                            cells["{}, {}".format(col, row)].nucleus = not cells["{}, {}".format(col, row)].nucleus
                            if cells["{}, {}".format(col, row)].status == 0 and not cells["{}, {}".format(col, row)].polarity_protein_A and not cells["{}, {}".format(col, row)].polarity_protein_B and not cells["{}, {}".format(col, row)].centrosome_pos and not cells["{}, {}".format(col, row)].centrosome_neg:
                                positions.remove(pos)
                        elif add_color == "pp":  
                            cells["{}, {}".format(col, row)].polarity_protein_A = False
                            cells["{}, {}".format(col, row)].polarity_protein_B = False
                            if cells["{}, {}".format(col, row)].status == 0 and not cells["{}, {}".format(col, row)].nucleus and not cells["{}, {}".format(col, row)].polarity_protein_A and not cells["{}, {}".format(col, row)].polarity_protein_B and not cells["{}, {}".format(col, row)].centrosome_pos and not cells["{}, {}".format(col, row)].centrosome_neg:
                                positions.remove(pos)
                        else:
                            if cells["{}, {}".format(col, row)].nucleus or cells["{}, {}".format(col, row)].centrosome_pos or cells["{}, {}".format(col, row)].centrosome_neg or cells["{}, {}".format(col, row)].polarity_protein_A or cells["{}, {}".format(col, row)].polarity_protein_B:
                                cells["{}, {}".format(col, row)].status = 0
                            else:
                                positions.remove(pos)
                                cells["{}, {}".format(col, row)].status = 0

                    #adds cell
                    else:
                        positions.add(pos)
                        if add_color == "black":
                            cells["{}, {}".format(col, row)].status = 1
                        elif add_color == "grey":
                            cells["{}, {}".format(col, row)].status = 2 
                        elif add_color == "pp":
                            target = random.choice(["A", "B"])
                            if target == "A":
                                cells["{}, {}".format(col, row)].polarity_protein_A = True
                            else:
                                cells["{}, {}".format(col, row)].polarity_protein_B = True
                        elif add_color == "nuc":
                            positions.add((col + 1, row))
                            cells["{}, {}".format(col, row)].nucleus = True
                            cells["{}, {}".format(col + 1, row)].nucleus = True
                            cells["{}, {}".format(col, row)].centrosome_pos = True

            #checks for button presses
            if event.type == pygame.KEYDOWN:

                #allows to pause and play the game
                if event.key == pygame.K_SPACE:
                    playing = not playing

                #clears the board by emptying positions and reseting cells
                if event.key == pygame.K_c:
                    positions = set()
                    cells = new_cells_obj(grids)
                    grids = []
                    grids.append(Grid(GRID_WIDTH - 1, 0, GRID_HEIGHT - 1, 0, 0, [0]))
                    split_cells = []
                    playing = False
                    count = 0

                #generates a random set of positions
                if event.key == pygame.K_g:
                    (positions, cells) = gen(4 * GRID_WIDTH, grids)
                    print("new generation")

                #toggles grouping
                if event.key == pygame.K_k:
                    color_groups = not color_groups

                #toggles coloring grids
                if event.key == pygame.K_l:
                    color_grids = not color_grids

                #toggles all sanity checks
                if event.key == pygame.K_q:
                    sanity_checks = not sanity_checks


        #displays everything
        screen.fill(LBLUE)
        draw_grid(positions, cells, sanity_checks, color_groups, color_grids, split_cells, grids)
        pygame.display.update()

    #creates movie when the game is exited
    make_mp4(path)

    #makes and saves the chart
    plot_it(path, x_coord, y_coord)

    #makes the lineage tree
    make_tree(grids, path)

    #saves the data
    #save_data(grids)

    pygame.quit()

if __name__ == "__main__":
    main()
