import pygame as pyg
import os


class CTFSounds():
    path = ""

    victory = None
    shooting = None
    wood_breaking = None
    explosion = None
    background = None

    def __init__(
            self, sounds_path=os.path.split(os.path.abspath(__file__))[0]):
        CTFSounds.path = sounds_path

        pyg.mixer.init()

        CTFSounds.victory = self.load_sound("wood_breaking.wav")
        CTFSounds.shooting = self.load_sound("wood_breaking.wav")
        CTFSounds.wood_breaking = self.load_sound("wood_breaking.wav")
        CTFSounds.explosion = self.load_sound("wood_breaking.wav")
        CTFSounds.background = self.load_sound("wood_breaking.wav")

    def load_sound(self, file):
        """ Load an image from the data directory. """
        file = os.path.join(CTFSounds.path, 'sound_files', file)
        try:
            sound = pyg.mixer.Sound(file)
        except pyg.error:
            raise SystemExit('Could not load image "%s" %s' %
                             (file, pyg.get_error()))
        return sound
