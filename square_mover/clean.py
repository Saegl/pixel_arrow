import sys
import pygame as pg


# Windows Specific Optimizations
import ctypes
ctypes.windll.user32.SetProcessDPIAware()
import win32api
import win32process
import win32con

pid = win32api.GetCurrentProcessId()
handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, True, pid)
win32process.SetPriorityClass(handle, win32process.REALTIME_PRIORITY_CLASS)

# flags = pg.DOUBLEBUF
flags = 0

pg.init()

clock = pg.time.Clock()
display = pg.display.set_mode((1200, 800), flags=flags, vsync=True)

player_pos = pg.math.Vector2()

SPEED = 10.0
SQUARE_SIZE = 50.0

fps = -1
minfps = 100
maxfps = 0
frames = 1

dfont: pg.font.Font = pg.font.SysFont(pg.font.get_default_font(), 16)

while True:
    ## EVENT HANDLING
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                pg.quit()
                sys.exit()

    ## UPDATE
    dy = dx = 0.0
    pressed = pg.key.get_pressed()

    if pressed[pg.K_UP]:
        # print('UP')
        dy -= SPEED
    if pressed[pg.K_DOWN]:
        # print('Down')
        dy += SPEED
    if pressed[pg.K_LEFT]:
        # print('Left')
        dx -= SPEED
    if pressed[pg.K_RIGHT]:
        # print("right")
        dx += SPEED

    player_pos.x += dx
    player_pos.y += dy

    ## DRAW
    display.fill("black")
    pg.draw.rect(
        display,
        (0, 100, 0),
        pg.Rect(player_pos.x, player_pos.y, SQUARE_SIZE, SQUARE_SIZE),
    )

    if frames % 100 == 0:
        fps = int(clock.get_fps())
        minfps = min(minfps, fps)
        maxfps = max(maxfps, fps)
    
    text = dfont.render(f'fps: {fps}, minfps: {minfps}, maxfps: {maxfps}', True, 'white')
    display.blit(text, (10, 10))
    
    pg.display.flip()
    # pg.display.update([(player_pos.x - 100, player_pos.x - 100, 200, 200)])
    clock.tick(60)
    frames += 1
