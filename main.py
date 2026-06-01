import random

import pygame

from config import (
    WIDTH,
    HEIGHT,
    NUM_CREATURES,
    NUM_PLANTS,
    BACKGROUND,
    FPS,
)
from plant import Plant
from creature import Creature
from collision import resolve_collisions


def hex_rgb(hex_color):
    h = hex_color.lstrip("#")
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))


def spawn_plant():
    return Plant(
        random.randint(50, WIDTH - 50),
        random.randint(50, HEIGHT - 50),
    )


def main():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Cute One-Neuron Ecosystem")

    clock = pygame.time.Clock()
    bg = hex_rgb(BACKGROUND)

    plants = [spawn_plant() for _ in range(NUM_PLANTS)]
    creatures = [Creature() for _ in range(NUM_CREATURES)]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for creature in creatures:
            creature.update(plants, creatures)

        resolve_collisions(creatures)

        plants[:] = [p for p in plants if p.food > 0]

        while len(plants) < NUM_PLANTS:
            plants.append(spawn_plant())

        screen.fill(bg)

        for plant in plants:
            plant.draw(screen)

        for creature in creatures:
            creature.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
