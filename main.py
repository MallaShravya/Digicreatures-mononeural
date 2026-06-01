import tkinter as tk
import random

from config import (
    WIDTH,
    HEIGHT,
    NUM_CREATURES,
    NUM_PLANTS,
    BACKGROUND,
    UPDATE_DELAY,
)
from plant import Plant
from creature import Creature
from collision import resolve_collisions


# ---------------------------------
# CREATE WORLD
# ---------------------------------
plants = [

    Plant(
        random.randint(
            50,
            WIDTH - 50
        ),
        random.randint(
            50,
            HEIGHT - 50
        )
    )

    for _ in range(NUM_PLANTS)
]

creatures = [
    Creature()
    for _ in range(NUM_CREATURES)
]


# ---------------------------------
# TKINTER SETUP
# ---------------------------------
root = tk.Tk()

root.title(
    "Cute One-Neuron Ecosystem"
)

canvas = tk.Canvas(
    root,
    width=WIDTH,
    height=HEIGHT,
    bg=BACKGROUND,
    highlightthickness=0
)

canvas.pack()


# ---------------------------------
# MAIN LOOP
# ---------------------------------
def update():

    canvas.delete("all")

    # update creatures
    for creature in creatures:

        creature.update(
            plants,
            creatures
        )

    # body collisions
    resolve_collisions(
        creatures
    )

    # remove empty plants
    plants[:] = [
        p for p in plants
        if p.food > 0
    ]

    # respawn plants
    while len(plants) < NUM_PLANTS:

        plants.append(

            Plant(
                random.randint(
                    50,
                    WIDTH - 50
                ),
                random.randint(
                    50,
                    HEIGHT - 50
                )
            )
        )

    # draw plants
    for plant in plants:
        plant.draw(canvas)

    # draw creatures
    for creature in creatures:
        creature.draw(canvas)

    root.after(
        UPDATE_DELAY,
        update
    )


# ---------------------------------
# START
# ---------------------------------
update()
root.mainloop()
