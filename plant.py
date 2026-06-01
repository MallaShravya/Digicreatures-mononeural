import random

import pygame

from config import PLANT_COLOR


def _hex_rgb(hex_color):
    h = hex_color.lstrip("#")
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))


_PLANT_RGB = _hex_rgb(PLANT_COLOR)


class Plant:

    def __init__(self, x, y):

        self.x = x
        self.y = y

        # random food quantity
        self.food = random.randint(50, 300)

    # -----------------------------
    # PHYSICAL SIZE
    # -----------------------------
    def radius(self):

        return max(4, self.food / 15)

    # -----------------------------
    # DRAW
    # -----------------------------
    def draw(self, surface):

        r = int(self.radius())

        pygame.draw.circle(
            surface,
            _PLANT_RGB,
            (int(self.x), int(self.y)),
            r,
        )
