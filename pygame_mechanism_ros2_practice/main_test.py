import pygame as py

from pygame_ros2_tools.Screen import Screen

def main(args=None):
    print("TESTING")

    screen = Screen(800, 16)

    run = True

    while run:
        screen.initialize()
        screen.draw()
        

py.quit()