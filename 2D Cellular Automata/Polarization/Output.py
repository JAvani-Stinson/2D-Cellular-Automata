import pygame
import os
import matplotlib.pyplot as plt
import glob
import graphviz as gv

#saves the images for each grid update
def make_png(screen, path, num):
    image_path = path + "Images/"
    if not os.path.exists(image_path):
        os.makedirs(image_path)
    num += 1
    fullpath = image_path + "//" + "%08d.png"%num
    pygame.image.save(screen, fullpath)
    return num

#turns the saved images into a movie
def make_mp4(path):
    vid_output = path + "Video.mp4"
    os.system("ffmpeg -r 1 -i '{}Images/%08d.png' -vcodec mpeg4 -q:v 0 -y '{}'".format(path, vid_output))

    #empties images folder
    files = glob.glob('{}Images/*'.format(path))
    for f in files:
        os.remove(f)

def plot_it(path, x_coord, y_coord):
    plt.plot(x_coord, y_coord)
    plt.xlabel("Timesteps (matches with video increments in base 60)")
    plt.ylabel("Overall Grid Enerfy")
    plot_output = path + 'plot.png'
    plt.savefig(plot_output)
    plt.show()

def make_tree(grids, path):
    tree = gv.Digraph(comment='Lineage Tree', strict = True)
    for grid in grids:

        for node in grid.lineage:
            tree.node(node)

        for i in range(len(grid.lineage) - 1):
            tree.edge(grid.lineage[i], grid.lineage[i + 1])
        
        if grid.differentiated_type == 1:
            color = "#8faab3"
        elif grid.differentiated_type == 2:
            color = "#81b14f"
        else:
            color = "#c4bd8b"

        tree.node(grid.lineage[-1], color = color, style = "filled")

    tree.render("Lineage_Tree.png", path, True)

def save_data(grids):
    count = len(grids)
    type_1 = 0
    type_2 = 0
    type_3 = 0

    length = 0
    width = 0
    size = 0

    add = True

    for grid in grids:
        if grid.differentiated_type == 0:
            add = False
        if grid.differentiated_type == 1:
            type_1 += 1
        elif grid.differentiated_type == 2:
            type_2 += 1
        elif grid.differentiated_type == 3:
            type_3 += 1

        length += grid.Max_Length - grid.Min_Length + 1
        width += grid.Max_Width - grid.Min_Width + 1
        size += len(grid.positions)

    if add == True:
        fname = '/Users/jstinson/Desktop/2D Cellular Automata/Polarization/data2.csv'
        file = open(fname, "a")
        file.write("{}, {}, {}, {}, {}, {}, {} \n".format(count, type_1/count, type_2/count, type_3/count, length/count, width/count, size/count))
        file.close()
    return
