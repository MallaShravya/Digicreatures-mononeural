import random

from config import PLANT_COLOR


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
    def draw(self, canvas):

        r = self.radius()

        canvas.create_oval(
            self.x - r,
            self.y - r,
            self.x + r,
            self.y + r,
            fill=PLANT_COLOR,
            outline=""
        )
