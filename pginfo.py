import ctypes

ctypes.windll.user32.SetProcessDPIAware()

import pygame as pg

pg.init()

print("DRIVER: ", pg.display.get_driver())
print("WM INFO: ", pg.display.get_wm_info())
print("DESKTOP SIZES", pg.display.get_desktop_sizes())
print("LIST MODES", pg.display.list_modes())
print("BEST COLOR DEPTH", pg.display.mode_ok((1920, 1080), depth=24))

# display = pg.display.set_mode((800, 600), 0, 0, 0, 0)
# print(display)
