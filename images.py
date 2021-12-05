import pygame as pyg
import os


class CTFImages():
    imgs_path = ""
    TILE_SIZE = 40  # Define the default size of tiles

    explosion = None
    grass = None
    rockbox = None
    metalbox = None
    woodbox = None
    flag = None
    bullet = None

    tank_images = []
    base_images = []

    def __init__(self, imgs_path=os.path.split(os.path.abspath(__file__))[0]):
        CTFImages.path = imgs_path

        CTFImages.explosion = self.load_image('explosion.png')
        CTFImages.grass = self.load_image('grass.png')
        CTFImages.rockbox = self.load_image('rockbox.png')
        CTFImages.metalbox = self.load_image('metalbox.png')
        CTFImages.woodbox = self.load_image('woodbox.png')
        CTFImages.flag = self.load_image('flag.png')  # Image of flag

        CTFImages.bullet = self.load_image('bullet.png')
        CTFImages.bullet = pyg.transform.scale(
            CTFImages.bullet, (10, 10))
        CTFImages.bullet = pyg.transform.rotate(CTFImages.bullet, -90)

        # List of image of tanks of different colors
        CTFImages.tank_images = [
            self.load_image('tank_orange.png'),
            self.load_image('tank_blue.png'),
            self.load_image('tank_white.png'),
            self.load_image('tank_yellow.png'),
            self.load_image('tank_red.png'),
            self.load_image('tank_gray.png')]

        # List of image of bases corresponding to the color of each tank
        CTFImages.base_images = [
            self.load_image('base_orange.png'),
            self.load_image('base_blue.png'),
            self.load_image('base_white.png'),
            self.load_image('base_yellow.png'),
            self.load_image('base_red.png'),
            self.load_image('base_gray.png')]

    def load_image(self, file):
        """ Load an image from the data directory. """
        file = os.path.join(self.imgs_path, 'image_files', file)
        try:
            surface = pyg.image.load(file)
        except pyg.error:
            raise SystemExit('Could not load image "%s" %s' %
                             (file, pyg.get_error()))
        return surface.convert_alpha()
