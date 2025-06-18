import pygame as py

from Screen import Screen

def main(args=None):
    print("TESTING")

    window = py.display.set_mode((500, 500))

    run = True

    while run:
        window.fill((255, 255, 255))


        for event in py.event.get():
            if event.type == py.QUIT:
                run = False

        py.display.update()