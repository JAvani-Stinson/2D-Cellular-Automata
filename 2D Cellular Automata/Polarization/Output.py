import pygame
import os
from datetime import datetime
import matplotlib.pyplot as plt
import glob

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