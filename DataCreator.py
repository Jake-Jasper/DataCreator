#!/usr/bin/env python3

import tkinter as tk
from particle import Particle
from drawing import Drawing
import statistics, math, csv


# this order must match the output of the logic code
STATS_CATS = ("X mean", "X std", "Y mean", "Y std", "Pearson's R", "N")


class StatsFrame(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.data = []
        for row_num, name in enumerate(STATS_CATS):
            desc = tk.Label(self, text=f"{name}: ")
            desc.grid(row=row_num, column=0, sticky="e")
            result = tk.Label(self, text="0.0")
            result.grid(row=row_num, column=1, sticky="w")
            self.data.append(result)

    # update the values when they change
    def update_values(self, new_data):
        for result_lbl, value in zip(self.data, new_data):
            result_lbl.config(text=f"{value:.2f}")


# Class for storing and displaying the variables in the gui
class VariableFrame(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        # Add some boxes to show the stats.
        self.xe = tk.StringVar()
        tk.Label(self, text="X name:").grid(row=1, column=0, padx=10)
        self.x_var_entry = tk.Entry(self, width=20, textvariable=self.xe)
        self.x_var_entry.grid(row=1, column=1)
        self.xe.set("X")  # Default x label

        # xmin max entry
        tk.Label(self, text="min").grid(row=0, column=2, padx=10)
        tk.Label(self, text="max").grid(row=0, column=3, padx=10)
        self.xe_min = tk.StringVar()  # xe_min x entry min
        self.xe_max = tk.StringVar()  # xe_min x entry min
        self.x_var_entry_min = tk.Entry(self, textvariable=self.xe_min, width=5)
        self.x_var_entry_min.grid(row=1, column=2)
        self.xe_min.set("0.0")  # default min
        self.x_var_entry_max = tk.Entry(self, textvariable=self.xe_max, width=5)
        self.x_var_entry_max.grid(row=1, column=3)
        self.xe_max.set("1.0")  # default max

        # Y  var
        self.ye = tk.StringVar()
        tk.Label(self, text="Y name:").grid(row=2, column=0, padx=20)
        self.y_var_entry = tk.Entry(self, width=20, textvariable=self.ye)
        self.y_var_entry.grid(row=2, column=1)
        self.ye.set("Y")

        # y min max
        self.ye_min = tk.StringVar()  # xe_min x entry min
        self.ye_max = tk.StringVar()  # xe_min x entry min
        self.y_var_entry_min = tk.Entry(self, textvariable=self.ye_min, width=5)
        self.y_var_entry_min.grid(row=2, column=2)
        self.ye_min.set("0.0")  # default min
        self.y_var_entry_max = tk.Entry(self, textvariable=self.ye_max, width=5)
        self.y_var_entry_max.grid(row=2, column=3)
        self.ye_max.set("1.0")  # default max

        # Add sub variables button
        new_cat_button = tk.Button(
            self, text="Add sub variable", command=color_picker().color_chooser
        )
        new_cat_button.grid(row=3, column=0, padx=10)


# GUI etc
class DataCreator(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.draw_window = Drawing(self)
        self.draw_window.grid(row=0, column=0, rowspan=3)

        self.stats = StatsFrame(self)
        self.stats.grid(row=0, column=1, sticky="n")

        self.variables = VariableFrame(self, relief="raised")
        self.variables.grid(row=1, column=1, columnspan=2, sticky="n")

        self.rowconfigure(2, weight=1)

        # menu items
        menubar = tk.Menu(self.master)
        filemenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Options", menu=filemenu)
        menubar.add_command(label="Reset", command=self.draw_window.reset_points)
        filemenu.add_command(label="Exit", command=self.quit)
        filemenu.add_command(label="Save", command=self.file_save)
        menubar.add_command(label="Undo", command=self.draw_window.undo)

        # add menubar
        self.master.config(menu=menubar)

    # Function to scale the points to the desired range
    def scale_points(self, arr, low, high):
        """
        :param arr:
        :param low:
        :param high:
        :return: a list of the scaled data for arr between low and high values:
        """
        return [
            ((i - min(arr)) / (max(arr) - min(arr))) * (high - low) + low for i in arr
        ]

    # Save the current data.
    def file_save(self):
        # save data to a csv file
        height = self.draw_window.winfo_height()
        clicks = [(point.x, height - point.y) for point in self.draw_window.point_ids]

        x_name = self.variables.x_var_entry.get()  # get the label for the x var
        y_name = self.variables.y_var_entry.get()  # get the label for the y var
        category_name = (
            "sub variables"  # find the more scientific naming schemes for this
        )

        xs = [i[0] for i in clicks]
        ys = [i[1] for i in clicks]

        xs = self.scale_points(
            xs, float(self.variables.xe_min.get()), float(self.variables.xe_max.get())
        )  # scale x
        ys = self.scale_points(
            ys, float(self.variables.ye_min.get()), float(self.variables.ye_max.get())
        )  # scale y

        cats = [
            point.category for point in self.draw_window.point_ids
        ]  # get all the values for the categorys, atm this is the hex code

        if len(set(cats)) == 1:
            data = [[x_name, y_name]]  # headers
            data.extend([[x, y] for x, y in zip(xs, ys)])
        else:
            data = [[x_name, y_name, category_name]]  # headers
            data.extend([[x, y, c] for x, y, c in zip(xs, ys, cats)])

        with open("data.csv", "w+", newline="") as file:
            write = csv.writer(file)
            write.writerows(data)

        # New window that confirms file has been saved
        window = tk.Toplevel()
        window.title("File saved")
        T = tk.Text(window, height=1, width=30)
        T.pack()
        T.insert(tk.END, "File saved")
        window.after(1000, window.destroy)

    # Calculate r-squared
    def get_rsquared(self, xs, ys):
        xmean, ymean = statistics.mean(xs), statistics.mean(ys)
        r = sum([(x - xmean) * (y - ymean) for x, y in zip(xs, ys)]) / math.sqrt(
            sum([(x - xmean) ** 2 for x in xs]) * sum([(y - ymean) ** 2 for y in ys])
        )
        return r ** 2

    def update_gui_text(self, point_ids):
        # save data to a csv file
        height = self.draw_window.winfo_height()
        width = self.draw_window.winfo_width()
        xs, ys = [point.x for point in point_ids], [point.y for point in point_ids]
        n = len(point_ids)

        # get the mean in the x and y plane
        xmean = statistics.mean(xs) / width
        ymean = statistics.mean(ys) / height
        if n > 1:
            xstd = statistics.stdev(xs) / width
            ystd = statistics.stdev(ys) / height
        else:
            xstd = 0
            ystd = 0

        r = 0  # default r^2
        # only calculate r^2 if there is more than one point
        if n > 1:
            r = self.get_rsquared(xs, ys)

        self.stats.update_values([xmean, xstd, ymean, ystd, r, n])


# Class that replicates the tkinter.colorchooser dialog
class color_picker(DataCreator):
    def __init__(self):
        self.color = "None"
        self.new_cat_name = tk.StringVar()

    # return the variables
    def get_vars(self):
        return self.color, self.new_cat_name

    # get hex value
    def rgbtohex(self, r, g, b):
        return f"#{r:02x}{g:02x}{b:02x}"

    # Function to update the color of the canvas
    def update_col(self, val):
        self.display_box.configure(
            bg=self.rgbtohex(self.R_scale.get(), self.G_scale.get(), self.B_scale.get())
        )

    # Close the window and print chosen value
    def close_dialog(self):
        self.color = self.rgbtohex(
            self.R_scale.get(), self.G_scale.get(), self.B_scale.get()
        )
        self.new_cat_name = self.new_cat_entry.get()
        Particle.current_colour, Particle.current_category = self.get_vars()

        self.window.destroy()

    # Gui for the color chooser
    def color_chooser(self):
        # Create window
        self.window = tk.Tk()
        self.window.title("Choose a color")
        self.window.geometry("356x200")

        # Slider widgets
        self.R_scale = tk.Scale(
            master=self.window, length=256, orient="horizontal", from_=0, to=255
        )
        self.R_scale.grid(row=0, column=0)
        self.G_scale = tk.Scale(
            master=self.window, length=256, orient="horizontal", from_=0, to=255
        )
        self.G_scale.grid(row=1, column=0)
        self.B_scale = tk.Scale(
            master=self.window, length=256, orient="horizontal", from_=0, to=255
        )
        self.B_scale.grid(row=2, column=0)

        # Bindings for mouse interactions
        self.R_scale.bind("<Motion>", self.update_col)
        self.G_scale.bind("<Motion>", self.update_col)
        self.B_scale.bind("<Motion>", self.update_col)

        # Canvas to display color
        self.display_box = tk.Canvas(
            master=self.window,
            width=90,
            height=125,
            bg=self.rgbtohex(
                self.R_scale.get(), self.G_scale.get(), self.B_scale.get()
            ),
        )
        self.display_box.grid(row=0, rowspan=3, column=1)

        # tk.Label and entry for new variable name
        self.new_cat_label = tk.Label(master=self.window, text="Enter variable name")
        self.new_cat_label.grid(row=3, column=0)
        self.new_cat_entry = tk.Entry(
            master=self.window, textvariable=self.new_cat_name
        )
        self.new_cat_entry.grid(row=4, column=0)

        # Buttons to exit the dialog
        self.ok_button = tk.Button(
            master=self.window, text="Okay", command=self.close_dialog
        )
        self.ok_button.grid(row=5, column=0)
        self.close_button = tk.Button(
            master=self.window, text="Cancel", command=self.window.destroy
        )
        self.close_button.grid(row=5, column=1)


# main loop to run the program
def main():
    # create window
    root = tk.Tk()
    root.geometry("1300x710")  # arbitrary size
    root.title("DataCreator")
    win = DataCreator(root)
    win.pack()
    root.mainloop()


if __name__ == "__main__":
    main()
