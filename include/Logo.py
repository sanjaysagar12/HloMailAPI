import svgwrite
import random
import os

# Define the root path
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def draw_symmetric_shape(dwg, center_x, center_y, num_sides, length, color):
    angle = 360 / num_sides
    points = []
    for i in range(num_sides):
        theta = (i * angle) * (3.14 / 180)  # Convert degrees to radians
        x = center_x + length * random.uniform(0.8, 1.2) * random.choice([-1, 1])
        y = center_y + length * random.uniform(0.8, 1.2) * random.choice([-1, 1])
        points.append((x, y))
    return points


def generate_logo(filename):
    size = 500  # Size of the canvas
    dwg = svgwrite.Drawing(f"images/logos/{filename}", size=(size, size))
    dwg.viewbox(0, 0, size, size)

    # Generate random symmetrical shapes
    for _ in range(random.randint(5, 10)):  # Random number of shapes
        x = random.randint(-200, 200)
        y = random.randint(-200, 200)
        num_sides = random.choice([3, 4, 5, 6, 8])
        length = random.randint(20, 100)
        # Generate darker colors
        color = svgwrite.rgb(
            random.randint(0, 100),  # Red component (0-100 for darker colors)
            random.randint(0, 100),  # Green component (0-100 for darker colors)
            random.randint(0, 100),  # Blue component (0-100 for darker colors)
            "%",
        )
        shape1 = draw_symmetric_shape(dwg, 250 + x, 250 + y, num_sides, length, color)
        shape2 = [(500 - x, y) for (x, y) in shape1]  # Mirror on x-axis
        shape3 = [(x, 500 - y) for (x, y) in shape1]  # Mirror on y-axis
        shape4 = [(500 - x, 500 - y) for (x, y) in shape1]  # Mirror on both axes

        dwg.add(dwg.polygon(shape1, fill=color, stroke=color))
        dwg.add(dwg.polygon(shape2, fill=color, stroke=color))
        dwg.add(dwg.polygon(shape3, fill=color, stroke=color))
        dwg.add(dwg.polygon(shape4, fill=color, stroke=color))

    dwg.save()
