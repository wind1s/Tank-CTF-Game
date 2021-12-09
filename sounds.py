import os
import pygame as pyg
from config import SOUNDS_PATH


class CTFSounds():
    score = None
    tank_shoot = None
    box_break = None
    tank_death = None
    music = None

    def __init__(self):
        CTFSounds.score = self.load_sound("score_goodjob.wav")
        CTFSounds.tank_shoot = self.load_sound("tank_shoot.wav")
        CTFSounds.box_break = self.load_sound("box_break.wav")
        CTFSounds.tank_death = self.load_sound("tank_death.wav")
        CTFSounds.music = self.load_sound("music.wav")

        CTFSounds.music.set_volume(0.6)

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
