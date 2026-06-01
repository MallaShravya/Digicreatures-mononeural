import math
import random

import pygame

from config import (
    WIDTH,
    HEIGHT,
    CREATURE_SPEED,
    TURN_SPEED,
    CREATURE_RADIUS,
)


class Creature:

    def __init__(self):

        self.x = random.uniform(0, WIDTH)
        self.y = random.uniform(0, HEIGHT)

        self.heading = random.uniform(
            0,
            math.pi * 2
        )

        # one neuron
        self.weight = 2.0
        self.bias = 0.0

    # -----------------------------
    # DISTANCE
    # -----------------------------
    def distance_to(self, obj):

        dx = obj.x - self.x
        dy = obj.y - self.y

        return math.sqrt(
            dx * dx +
            dy * dy
        )

    # -----------------------------
    # NORMALIZE ANGLES
    # -----------------------------
    def normalize_angle(self, angle):

        while angle > math.pi:
            angle -= 2 * math.pi

        while angle < -math.pi:
            angle += 2 * math.pi

        return angle

    # -----------------------------
    # SINGLE NEURON
    # -----------------------------
    def neuron(self, angle_error):

        return math.tanh(
            angle_error * self.weight +
            self.bias
        )

    # -----------------------------
    # SMELL BLOCKING
    # -----------------------------
    def smell_blocked(
        self,
        plant,
        creatures
    ):

        ax = self.x
        ay = self.y

        px = plant.x
        py = plant.y

        line_dx = px - ax
        line_dy = py - ay

        line_length = math.sqrt(
            line_dx * line_dx +
            line_dy * line_dy
        )

        if line_length == 0:
            return False

        for other in creatures:

            if other is self:
                continue

            bx = other.x
            by = other.y

            dx = bx - ax
            dy = by - ay

            t = (
                dx * line_dx +
                dy * line_dy
            ) / (
                line_length * line_length
            )

            # only between creature and plant
            if 0 < t < 1:

                closest_x = (
                    ax + t * line_dx
                )

                closest_y = (
                    ay + t * line_dy
                )

                dist_to_line = math.sqrt(
                    (bx - closest_x) ** 2 +
                    (by - closest_y) ** 2
                )

                if dist_to_line < (
                    CREATURE_RADIUS * 1.5
                ):
                    return True

        return False

    # -----------------------------
    # FIND NEAREST PLANT
    # -----------------------------
    def find_nearest_plant(
        self,
        plants,
        creatures
    ):

        visible = []

        for plant in plants:

            if not self.smell_blocked(
                plant,
                creatures
            ):
                visible.append(plant)

        if not visible:
            return None

        return min(
            visible,
            key=lambda p: self.distance_to(p)
        )

    # -----------------------------
    # UPDATE
    # -----------------------------
    def update(
        self,
        plants,
        creatures
    ):

        nearest = self.find_nearest_plant(
            plants,
            creatures
        )

        # no smell available
        if nearest is None:

            self.heading += random.uniform(
                -0.1,
                0.1
            )

            self.x += math.cos(
                self.heading
            ) * CREATURE_SPEED * 0.5

            self.y += math.sin(
                self.heading
            ) * CREATURE_SPEED * 0.5

            self.wrap()
            return

        dx = nearest.x - self.x
        dy = nearest.y - self.y

        target_angle = math.atan2(
            dy,
            dx
        )

        angle_error = (
            self.normalize_angle(
                target_angle -
                self.heading
            )
        )

        # neuron output
        turn = self.neuron(
            angle_error
        )

        distance = self.distance_to(
            nearest
        )

        # stronger turning near target
        turn_strength = (
            TURN_SPEED *
            (
                1 +
                1 / (distance + 1)
            )
        )

        self.heading += (
            turn * turn_strength
        )

        # ---------------------------------
        # TOUCHING FOOD BOUNDARY
        # ---------------------------------
        eat_distance = (
            nearest.radius() +
            CREATURE_RADIUS
        )

        if distance > eat_distance:

            speed = min(
                CREATURE_SPEED,
                distance * 0.1
            )

            self.x += math.cos(
                self.heading
            ) * speed

            self.y += math.sin(
                self.heading
            ) * speed

        else:
            # consume food
            nearest.food -= 1

        self.wrap()

    # -----------------------------
    # WORLD WRAP
    # -----------------------------
    def wrap(self):

        self.x %= WIDTH
        self.y %= HEIGHT

    # -----------------------------
    # DRAW
    # -----------------------------
    def draw(self, surface):

        body_length = 24
        body_width = 24

        dx = math.cos(self.heading)
        dy = math.sin(self.heading)

        px = -dy
        py = dx

        cx = int(self.x)
        cy = int(self.y)

        # body
        pygame.draw.ellipse(
            surface,
            (221, 238, 255),
            (
                cx - body_length / 2,
                cy - body_width / 2,
                body_length,
                body_width,
            ),
        )

        # eyes
        eye_forward = 6
        eye_side = 4
        eye_radius = 2

        left_eye = (
            int(cx + dx * eye_forward + px * eye_side),
            int(cy + dy * eye_forward + py * eye_side),
        )
        right_eye = (
            int(cx + dx * eye_forward - px * eye_side),
            int(cy + dy * eye_forward - py * eye_side),
        )

        pygame.draw.circle(surface, (0, 0, 0), left_eye, eye_radius)
        pygame.draw.circle(surface, (0, 0, 0), right_eye, eye_radius)

        # antennae
        front_x = cx + dx * body_length / 2
        front_y = cy + dy * body_length / 2

        antenna_length = 10
        spread = 5

        left_base = (front_x + px * spread, front_y + py * spread)
        left_tip = (
            left_base[0] + dx * antenna_length + px * 4,
            left_base[1] + dy * antenna_length + py * 4,
        )

        right_base = (front_x - px * spread, front_y - py * spread)
        right_tip = (
            right_base[0] + dx * antenna_length - px * 4,
            right_base[1] + dy * antenna_length - py * 4,
        )

        pygame.draw.line(surface, (255, 255, 255), left_base, left_tip, 2)
        pygame.draw.line(surface, (255, 255, 255), right_base, right_tip, 2)
