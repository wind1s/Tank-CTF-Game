import os
import pygame as pyg
from config import (
    IMAGES_PATH, TILE_SIZE, EXPLOSION_IMG_FILE, BASES_IMG_FILES,
    TANKS_IMG_FILES, BULLET_IMG_FILE, GRASS_IMG_FILE, ROCK_IMG_FILE,
    METAL_IMG_FILE, FLAG_IMG_FILE, WOOD_IMG_FILE)
from utility import list_comp


class CTFImages():
    explosion = None
    grass = None
    rockbox = None
    metalbox = None
    woodbox = None
    flag = None
    bullet = None

    tank_images = None
    base_images = None

    def __init__(self, n_players):
        default_scale = CTFImages.scale_by_tile(1)
        CTFImages.explosion = self.load_image(
            EXPLOSION_IMG_FILE, CTFImages.scale_by_tile(1.5))
        CTFImages.grass = self.load_image(
            GRASS_IMG_FILE, default_scale)
        CTFImages.rockbox = self.load_image(
            ROCK_IMG_FILE, default_scale)
        CTFImages.woodbox = self.load_image(
            WOOD_IMG_FILE, default_scale)
        CTFImages.metalbox = self.load_image(
            METAL_IMG_FILE, CTFImages.scale_by_tile(0.7))
        CTFImages.flag = self.load_image(
            FLAG_IMG_FILE, default_scale)

        CTFImages.bullet = self.load_image(
            BULLET_IMG_FILE, CTFImages.scale_by_tile(0.25))
        CTFImages.bullet = pyg.transform.rotate(CTFImages.bullet, -90)

        half_scale = CTFImages.scale_by_tile(0.5)

        def load_img_func(img):
            return self.load_image(img, half_scale)

        # List of image of tanks of different colors
        CTFImages.tank_images = list_comp(
            TANKS_IMG_FILES[:n_players],
            func=load_img_func)

        # List of image of bases corresponding to the color of each tank
        CTFImages.base_images = list_comp(
            BASES_IMG_FILES[:n_players],
            func=load_img_func)

    @ staticmethod
    def scale_by_tile(percent):
        return (TILE_SIZE*percent, TILE_SIZE*percent)

    @ staticmethod
    def load_image(file, scale=None):
        """ Load an image. """
        file = os.path.join(IMAGES_PATH, file)

        try:
            surface = pyg.image.load(file)

        except pyg.error:
            raise SystemExit(
                f"Could not load image \"{file}\" {pyg.get_error()}")

        surface = surface.convert_alpha()

        if scale is not None:
            return pyg.transform.scale(surface, scale)

        return surface
