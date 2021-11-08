"""
"""
import pygame as pyg
import pymunk as pym

# Initialise the display
pyg.init()
pyg.display.set_mode()

# Initialise the clock
clock = pyg.time.Clock()

# Initialise the physics engine
space = pym.Space()
space.gravity = (0.0,  0.0)
space.damping = 0.1  # Adds friction to the ground for all objects

FRAMERATE = 50
