# Class to create and store data points


class Particle:
    current_colour = "#000000"  # Default black
    current_category = "None"

    def __init__(self, canvas, x, y):
        RADIUS_MODIFIER = 5

        # x and y should also be unique at this point
        self.x = x
        self.y = y
        self.category = self.current_category
        self.point = canvas.create_oval(
            x - RADIUS_MODIFIER,
            y - RADIUS_MODIFIER,
            x + RADIUS_MODIFIER,
            y + RADIUS_MODIFIER,
            width=0,
            fill=self.current_colour,
            tags="points",
        )
