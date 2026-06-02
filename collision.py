import math

from config import CREATURE_RADIUS


def resolve_collisions(creatures):

    for i in range(len(creatures)):

        for j in range(i + 1, len(creatures)):

            a = creatures[i]
            b = creatures[j]

            dx = b.x - a.x
            dy = b.y - a.y

            distance = math.sqrt(
                dx * dx +
                dy * dy
            )

            min_distance = (
                CREATURE_RADIUS * 2
            )

            if (
                0 <
                distance <
                min_distance
            ):

                overlap = (
                    min_distance -
                    distance
                )

                nx = dx / distance
                ny = dy / distance

                push_x = (
                    nx * overlap / 2
                )

                push_y = (
                    ny * overlap / 2
                )

                a.x -= push_x
                a.y -= push_y

                b.x += push_x
                b.y += push_y