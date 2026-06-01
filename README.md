The code creates a window in which you can see the movements of several creatures with one neuron each, as they try to find food.

The world:
The world is the window on which a fixed number of food sources appear randomly. The size of the plant represents the amount of food. These are point sources, which means that the creature has to touch the center to consume the food. When a source is depleted, it disappears, and a new one appears on the board randomly.

Creatures:
The have 'smell' sensors. The sensors get inputs(the x and y coordinates) from all plants on the window, excepts for the ones that have another creature blocking the path to them. It then chooses the nearest food source, and calculates the angle to that.
$$\theta_{\text{food}} = \operatorname{atan2}(y_{\text{food}} - y, x_{\text{food}} - x)$$
They then compare it to the current direction of movement and get the angle difference, and normalize angles.

They have a neuron that takes the input from the sensor and turns it into a 'turn left' or 'turn right' signal.
$output = \tanh(w \cdot \text{error} + b)$
There's no bias right now, as we don't want the creatures to drift away from the food. The weight determines how sharply the creature turns.
​
Physical constraints:
Creatures are not allowed to overlap. This constraint is enforced by the environment rather than the neuron. As a result, many observed behaviors emerge from physical interactions:
- Congestion around food sources
- Resource shielding
- Competition for access
- Formation of temporary groups


