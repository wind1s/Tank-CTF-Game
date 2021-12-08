import os
import pygame as pyg
from config import SOUNDS_PATH


class CTFSounds():
    victory = None
    shooting = None
    wood_breaking = None
    explosion = None
    background = None

    def __init__(self):
        pyg.mixer.init()

        CTFSounds.victory = self.load_sound("victory.wav")
        CTFSounds.shooting = self.load_sound("shoot.wav")
        CTFSounds.wood_breaking = self.load_sound("wood_breaking.wav")
        CTFSounds.explosion = self.load_sound("wood_breaking.wav")
        CTFSounds.background = self.load_sound("wood_breaking.wav")

    @staticmethod
    def load_sound(file):
        """ Load a sound file. """
        file = os.path.join(SOUNDS_PATH, file)
        try:
            sound = pyg.mixer.Sound(file)
        except pyg.error:
            raise SystemExit(
                f"Could not load image \"{file}\" {pyg.get_error()}")
        return sound
