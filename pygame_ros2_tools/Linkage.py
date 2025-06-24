import pygame as py
import math as m


# All Linkage parameters input in iches, then converted in __init__ to pixels
class Linkage:
    def __init__(self, screen, length, x1, y1, theta, color, xy=True):
        self.screen = screen
        self.x1 = self.screen.inches_to_pixels(x1)
        self.y1 = self.screen.inches_to_pixels(y1)
        self.length = self.screen.inches_to_pixels(length)
        self.theta = theta
        self.x2 = self.x1 + self.length * m.cos((self.theta))
        self.y2 = self.y1 + self.length * m.sin((self.theta))
        self.color = color
        self.xyPlane = True
        self.xy = xy
        self.screen.linkages.append(self)

    def render(self):
        if self.xy == self.screen.xy:
            py.draw.line(self.screen.window, self.color, (self.x1, self.y1),
                         (self.x2, self.y2), 12)