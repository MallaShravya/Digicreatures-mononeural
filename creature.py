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
    # SENSOR
    # -----------------------------
    def sense(self, plants):

        observations = []

        for plant in plants:

            observations.append(
                (
                    plant.x - self.x,
                    plant.y - self.y,
                    plant,
                )
            )

        return observations

    # -----------------------------
    # NEURON
    # -----------------------------
    def neuron(self, observations):

        if not observations:
            return None, 0.0, 0.0

        nearest_distance = float("inf")
        nearest_dx = 0.0
        nearest_dy = 0.0
        nearest_plant = None

        # EXACTLY the same target choice
        # as the original implementation:
        # choose nearest plant
        for dx, dy, plant in observations:

            distance = math.sqrt(
                dx * dx +
                dy * dy
            )

            if distance < nearest_distance:

                nearest_distance = distance
                nearest_dx = dx
                nearest_dy = dy
                nearest_plant = plant

        target_angle = math.atan2(
            nearest_dy,
            nearest_dx
        )

        angle_error = self.normalize_angle(
            target_angle - self.heading
        )

        turn = math.tanh(
            angle_error * self.weight +
            self.bias
        )

        return (
            nearest_plant,
            nearest_distance,
            turn,
        )

    # -----------------------------
    # UPDATE
    # -----------------------------
    def update(
        self,
        plants,
        creatures
    ):

        observations = self.sense(
            plants
        )

        (
            target,
            distance,
            turn,
        ) = self.neuron(
            observations
        )

        if target is None:

            self.x += (
                math.cos(self.heading)
                * CREATURE_SPEED
            )

            self.y += (
                math.sin(self.heading)
                * CREATURE_SPEED
            )

            self.wrap()
            return

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

        eat_distance = (
            target.radius() +
            CREATURE_RADIUS
        )

        if distance > eat_distance:

            speed = min(
                CREATURE_SPEED,
                distance * 0.1
            )

            self.x += (
                math.cos(self.heading)
                * speed
            )

            self.y += (
                math.sin(self.heading)
                * speed
            )

        else:

            target.food -= 1

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

        eye_forward = 6
        eye_side = 4
        eye_radius = 2

        left_eye = (
            int(
                cx +
                dx * eye_forward +
                px * eye_side
            ),
            int(
                cy +
                dy * eye_forward +
                py * eye_side
            ),
        )

        right_eye = (
            int(
                cx +
                dx * eye_forward -
                px * eye_side
            ),
            int(
                cy +
                dy * eye_forward -
                py * eye_side
            ),
        )

        pygame.draw.circle(
            surface,
            (0, 0, 0),
            left_eye,
            eye_radius,
        )

        pygame.draw.circle(
            surface,
            (0, 0, 0),
            right_eye,
            eye_radius,
        )

        front_x = (
            cx +
            dx * body_length / 2
        )

        front_y = (
            cy +
            dy * body_length / 2
        )

        antenna_length = 10
        spread = 5

        left_base = (
            front_x + px * spread,
            front_y + py * spread,
        )

        left_tip = (
            left_base[0]
            + dx * antenna_length
            + px * 4,
            left_base[1]
            + dy * antenna_length
            + py * 4,
        )

        right_base = (
            front_x - px * spread,
            front_y - py * spread,
        )

        right_tip = (
            right_base[0]
            + dx * antenna_length
            - px * 4,
            right_base[1]
            + dy * antenna_length
            - py * 4,
        )

        pygame.draw.line(
            surface,
            (255, 255, 255),
            left_base,
            left_tip,
            2,
        )

        pygame.draw.line(
            surface,
            (255, 255, 255),
            right_base,
            right_tip,
            2,
        )