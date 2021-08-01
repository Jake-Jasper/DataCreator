import tkinter as tk
from particle import Particle


class Drawing(tk.Canvas):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.point_ids = []

        # Create the canvas and make it visible with pack()
        self.config(highlightthickness=2, highlightbackground="black")
        self.config(background="white", width=800, height=700)

        # record clicks on canvas only.
        self.bind("<Button-1>", self.click)

        self.create_grid()

    def create_grid(self):
        """This makes the gridlines on the canvas.
        Extend well beyond any normal monitor to pixel 3000, to avoid
        the drama of redrawing as window sizes change"""
        w = h = 3000
        # Creates all vertical lines at intevals of 100
        for i in range(0, h, 100):
            self.create_line([(i, 0), (i, h)], tag="grid_line")

        # Creates all horizontal lines at intevals of 100
        for i in range(0, w, 100):
            self.create_line([(0, i), (w, i)], tag="grid_line")

    # Function clear all data
    def reset_points(self):
        # reset data
        self.delete("points")
        self.point_ids.clear()
        # update gui
        self.master.update_gui_text(self.point_ids)

    def undo(self):
        if len(self.point_ids) > 0:
            # delete the point_id
            del self.point_ids[-1]
            # delete the last element from the canvas
            self.delete(list(self.find_withtag("points"))[-1])
            # update the gui text
            self.master.update_gui_text(self.point_ids)

    # Records click events and updates the screen
    def click(self, event):
        # record clicks
        # create a new particle
        self.point_ids.append(Particle(self, event.x, event.y))
        # update the gui
        self.master.update_gui_text(self.point_ids)
