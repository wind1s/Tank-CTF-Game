from pygame import (image, error, get_error, transform)
from os import path

main_dir = path.split(path.abspath(__file__))[0]


def load_image(file):
    """ Load an image from the data directory. """
    file = path.join(main_dir, 'data', file)
    try:
        surface = image.load(file)
    except error:
        raise SystemExit('Could not load image "%s" %s' %
                         (file, get_error()))
    return surface.convert_alpha()


TILE_SIZE = 40  # Define the default size of tiles

explosion_img = load_image('explosion.png')  # Image of an explosion

grass_img = load_image('grass.png')  # Image of a grass tile

rockbox_img = load_image('rockbox.png')  # Image of a rock box (wall)

metalbox_img = load_image('metalbox.png')  # Image of a metal box

woodbox_img = load_image('woodbox.png')  # Image of a wood box

flag_img = load_image('flag.png')  # Image of flag

bullet_img = load_image('bullet.png')
bullet_img = transform.scale(bullet_img, (10, 10))
bullet_img = transform.rotate(bullet_img, -90)

# List of image of tanks of different colors
tank_images = [
    load_image('tank_orange.png'),
    load_image('tank_blue.png'),
    load_image('tank_white.png'),
    load_image('tank_yellow.png'),
    load_image('tank_red.png'),
    load_image('tank_gray.png')]

# List of image of bases corresponding to the color of each tank
base_images = [
    load_image('base_orange.png'),
    load_image('base_blue.png'),
    load_image('base_white.png'),
    load_image('base_yellow.png'),
    load_image('base_red.png'),
    load_image('base_gray.png')]
