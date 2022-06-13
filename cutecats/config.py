import pygame as pg

# Server
host = "192.168.0.103"
port = 5555
buffer_size = 38
number_of_players = 1

# Game
fullscreen = False
flags = pg.RESIZABLE
caption = "Pixel Arrow"
window_size = (256 * 5, 144 * 5)  # When not fullscreen
screen_size = (256, 144)  # Virtual Screen Size active in both fullscreen and windowed
framerate = 60
use_busy_loop = True  # More tick precise and more cpu usage
images_folder = "cutecats/res/images"
game_font_folder = "cutecats/res/fonts/monogram/ttf/monogram.ttf"
debug_font_size = 16

enable_hot_reload = False
systems_module_prefix = "cutecats.systems."  # Need for hot reloading
