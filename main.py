import tkinter as tk
import math
import random

# ---------------------------------
# CONFIG
# ---------------------------------
WIDTH = 1000
HEIGHT = 700

NUM_CREATURES = 50#25
NUM_PLANTS = 24#12

CREATURE_SPEED = 2.5
TURN_SPEED = 0.08

CREATURE_RADIUS = 12
EAT_DISTANCE = 10

BACKGROUND = "#14141E"
PLANT_COLOR = "#33DD55"

UPDATE_DELAY = 16  # ~60 FPS


# ---------------------------------
# PLANT
# ---------------------------------
class Plant:

    def __init__(self, x, y):

        self.x = x
        self.y = y

        # random food quantity
        self.food = random.randint(50, 300)

    def draw(self, canvas):

        # size reflects remaining food
        r = max(4, self.food / 15)

        canvas.create_oval(
            self.x - r,
            self.y - r,
            self.x + r,
            self.y + r,
            fill=PLANT_COLOR,
            outline=""
        )


# ---------------------------------
# CREATURE
# ---------------------------------
class Creature:

    def __init__(self):

        self.x = random.uniform(0, WIDTH)
        self.y = random.uniform(0, HEIGHT)

        self.heading = random.uniform(0, math.pi * 2)

        # one neuron
        self.weight = 2.0
        self.bias = 0.0

    # -----------------------------
    # DISTANCE
    # -----------------------------
    def distance_to(self, obj):

        dx = obj.x - self.x
        dy = obj.y - self.y

        return math.sqrt(dx * dx + dy * dy)

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
            angle_error * self.weight + self.bias
        )

    # -----------------------------
    # SMELL BLOCKING
    # -----------------------------
    def smell_blocked(self, plant, creatures):

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

            # projection along line
            t = (
                dx * line_dx +
                dy * line_dy
            ) / (line_length * line_length)

            # only between self and plant
            if 0 < t < 1:

                closest_x = ax + t * line_dx
                closest_y = ay + t * line_dy

                dist_to_line = math.sqrt(
                    (bx - closest_x) ** 2 +
                    (by - closest_y) ** 2
                )

                # another body blocks smell
                if dist_to_line < CREATURE_RADIUS * 1.5:
                    return True

        return False

    # -----------------------------
    # FIND NEAREST SMELLABLE PLANT
    # -----------------------------
    def find_nearest_plant(self, plants, creatures):

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
    def update(self, plants, creatures):

        nearest = self.find_nearest_plant(
            plants,
            creatures
        )

        # no smell detected
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

        target_angle = math.atan2(dy, dx)

        angle_error = self.normalize_angle(
            target_angle - self.heading
        )

        # neuron steering
        turn = self.neuron(angle_error)

        distance = self.distance_to(nearest)

        # stronger turning near target
        turn_strength = TURN_SPEED * (
            1 + 1 / (distance + 1)
        )

        self.heading += turn * turn_strength

        # move toward food
        if distance > EAT_DISTANCE:

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
            # eat
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
    def draw(self, canvas):

        # body dimensions
        body_length = 24
        body_width = 24#16

        # direction vector
        dx = math.cos(self.heading)
        dy = math.sin(self.heading)

        # perpendicular vector
        px = -dy
        py = dx

        cx = self.x
        cy = self.y

        # body
        canvas.create_oval(
            cx - body_length / 2,
            cy - body_width / 2,
            cx + body_length / 2,
            cy + body_width / 2,
            fill="#DDEEFF",
            outline=""
        )

        # -------------------------
        # EYES
        # -------------------------
        eye_forward = 6
        eye_side = 4
        eye_radius = 2

        left_eye_x = (
            cx +
            dx * eye_forward +
            px * eye_side
        )

        left_eye_y = (
            cy +
            dy * eye_forward +
            py * eye_side
        )

        right_eye_x = (
            cx +
            dx * eye_forward -
            px * eye_side
        )

        right_eye_y = (
            cy +
            dy * eye_forward -
            py * eye_side
        )

        canvas.create_oval(
            left_eye_x - eye_radius,
            left_eye_y - eye_radius,
            left_eye_x + eye_radius,
            left_eye_y + eye_radius,
            fill="black"
        )

        canvas.create_oval(
            right_eye_x - eye_radius,
            right_eye_y - eye_radius,
            right_eye_x + eye_radius,
            right_eye_y + eye_radius,
            fill="black"
        )

        # -------------------------
        # ANTENNAE
        # -------------------------
        front_x = cx + dx * body_length / 2
        front_y = cy + dy * body_length / 2

        antenna_length = 10
        spread = 5

        # left antenna
        ax1 = front_x + px * spread
        ay1 = front_y + py * spread

        ax2 = (
            ax1 +
            dx * antenna_length +
            px * 4
        )

        ay2 = (
            ay1 +
            dy * antenna_length +
            py * 4
        )

        # right antenna
        bx1 = front_x - px * spread
        by1 = front_y - py * spread

        bx2 = (
            bx1 +
            dx * antenna_length -
            px * 4
        )

        by2 = (
            by1 +
            dy * antenna_length -
            py * 4
        )

        canvas.create_line(
            ax1, ay1,
            ax2, ay2,
            fill="white",
            width=2
        )

        canvas.create_line(
            bx1, by1,
            bx2, by2,
            fill="white",
            width=2
        )


# ---------------------------------
# COLLISION SYSTEM
# ---------------------------------
def resolve_collisions(creatures):

    for i in range(len(creatures)):
        for j in range(i + 1, len(creatures)):

            a = creatures[i]
            b = creatures[j]

            dx = b.x - a.x
            dy = b.y - a.y

            distance = math.sqrt(
                dx * dx + dy * dy
            )

            min_distance = CREATURE_RADIUS * 2

            if 0 < distance < min_distance:

                overlap = (
                    min_distance - distance
                )

                nx = dx / distance
                ny = dy / distance

                push_x = nx * overlap / 2
                push_y = ny * overlap / 2

                a.x -= push_x
                a.y -= push_y

                b.x += push_x
                b.y += push_y


# ---------------------------------
# CREATE WORLD
# ---------------------------------
plants = [
    Plant(
        random.randint(50, WIDTH - 50),
        random.randint(50, HEIGHT - 50)
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
root.title("Cute One-Neuron Creatures")

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

    # resolve body collisions
    resolve_collisions(creatures)

    # remove exhausted plants
    plants[:] = [
        p for p in plants
        if p.food > 0
    ]

    # spawn new plants
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


# start simulation
update()
root.mainloop()
