import pygame as pg

# Server
host = "192.168.0.103"
port = 5555
buffer_size = 38
number_of_players = 1

# Game
fullscreen = False
flags = pg.RESIZABLE | pg.DOUBLEBUF
caption = "Pixel Arrow"
window_size = (800, 450)  # When not fullscreen
screen_size = (1536, 864)  # Virtual Screen Size active in both fullscreen and windowed
framerate = 60
use_busy_loop = False  # More tick precise and more cpu usage
images_folder = "pixel_arrow/res/images"
game_font_folder = "pixel_arrow/res/fonts/monogram/ttf/monogram.ttf"
systems_module_prefix = "pixel_arrow.systems."  # Need for hot reloading
