#!/usr/bin/env python3

import tkinter as tk
from tkinter import Canvas, Menu, Frame, DoubleVar, StringVar, IntVar, Label, Entry, Scale, Button

import numpy as np


# Class to create and store data points
class Particle:
    current_colour = '#000000' # Default black
    current_category = 'None'

    def __init__(self, canvas, x, y):
        RADIUS_MODIFIER = 5

        # x and y should also be unique at this point
        self.x = x
        self.y = y
        self.category = self.current_category
        self.point = canvas.create_oval(
            x-RADIUS_MODIFIER, y-RADIUS_MODIFIER, x+RADIUS_MODIFIER, y+RADIUS_MODIFIER,
            width = 0, fill = self.current_colour, tags = 'points')

class Drawing(tk.Canvas):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.point_ids = []

        # Create the canvas and make it visible with pack()
        self.config(highlightthickness =2, highlightbackground = 'black')
        self.config(background = 'white', width = 800, height = 700)

        # record clicks on canvas only.
        self.bind('<Button-1>', self.click)

        self.create_grid()

    def create_grid(self):
        """This makes the gridlines on the canvas.
        Extend well beyond any normal monitor to pixel 3000, to avoid
        the drama of redrawing as window sizes change"""
        w = h = 3000
        # Creates all vertical lines at intevals of 100
        for i in range(0, h, 100):
            self.create_line([(i, 0), (i, h)], tag='grid_line')

        # Creates all horizontal lines at intevals of 100
        for i in range(0, w, 100):
            self.create_line([(0, i), (w, i)], tag='grid_line')

    # Function clear all data
    def reset_points(self):
        #reset data
        self.delete('points')
        self.point_ids.clear()
        #update gui
        self.master.update_gui_text(self.point_ids)

    def undo(self):
        if len(self.point_ids) > 0:
            # delete the point_id
            del self.point_ids[-1] 
            # delete the last element from the canvas
            self.delete(list(self.find_withtag('points'))[-1])
            # update the gui text
            self.master.update_gui_text(self.point_ids)
            
    # Records click events and updates the screen
    def click(self, event):
        # record clicks
        # create a new particle
        self.point_ids.append(Particle(self, event.x, event.y))
        # update the gui
        self.master.update_gui_text(self.point_ids)

#this order must match the output of the logic code
STATS_CATS = ("X mean", "X std", "Y mean", "Y std", "Pearson's R", "N")
class StatsFrame(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.data = []
        for row_num, name in enumerate(STATS_CATS):
            desc = tk.Label(self, text=f"{name}: ")
            desc.grid(row=row_num, column=0, sticky='e')
            result = tk.Label(self, text="0.0")
            result.grid(row=row_num, column=1, sticky='w')
            self.data.append(result)

    def update_values(self, new_data):
        for result_lbl, value in zip(self.data, new_data):
            result_lbl.config(text=f"{value:.2f}")

'''
I need to modify the calss below so that I can have the X and Y variable label and Entry boxes below the and to the left of the canvas
'''

class VariableFrame(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        # Add some boxes to show the stats.
        self.xe = StringVar()
        Label(self, text = 'X name:').grid(row=0, column=0, padx = 10)
        self.x_var_entry = Entry(self, textvariable=self.xe)
        self.x_var_entry.grid(row=0, column =1)
        self.x_var_entry.config(fg = Particle.current_colour) # This should always stay the base colour
        self.xe.set('X') # Default x label

        self.ye = StringVar()
        Label(self, text = 'Y name:').grid(row=1, column =0, padx =20)
        self.y_var_entry = Entry(self, textvariable = self.ye)
        self.y_var_entry.grid(row=1, column = 1)
        self.ye.set('Y')

        # Add sub variables
        new_cat_button = Button(self, text = 'Add sub variable', command = color_picker().color_chooser)
        new_cat_button.grid(row=2, column=0, padx = 10)

# GUI etc
class DataCreator(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.draw_window = Drawing(self)
        self.draw_window.grid(row=0,column=0, rowspan=3)

        self.stats = StatsFrame(self)
        self.stats.grid(row=0,column=1, sticky="n")

        self.variables = VariableFrame(self, relief = 'raised')
        self.variables.grid(row=1,column=1, columnspan = 2, sticky="n")

        self.rowconfigure(2, weight=1)
        
        # menu items
        menubar = tk.Menu(self.master)
        filemenu = tk.Menu(menubar, tearoff=0)
        menubar.add_command(label="Reset", command=self.draw_window.reset_points)
        filemenu.add_command(label="Exit", command=self.quit)
        filemenu.add_command(label="Save", command=self.file_save)
        menubar.add_cascade(label="Options", menu=filemenu)
        menubar.add_command(label="Undo", command=self.draw_window.undo)

        # add menubar
        self.master.config(menu=menubar)


    # Save the current data. 
    def file_save(self):
        #save data to a csv file
        height = self.draw_window.winfo_height()
        width = self.draw_window.winfo_width()
        clicks = [(point.x, height-point.y) for point in self.draw_window.point_ids]

        x_name = self.variables.x_var_entry.get() # get the label for the x var
        y_name = self.variables.y_var_entry.get() # get the label for the y var
        category_name = 'sub variables' # find the more scientific naming schemes for this
        xs = np.asarray(clicks)[:,0] / width  # This changes the data so that (0,0) is SW, so it works correctly when plotting
        ys = np.asarray(clicks)[:,1] / height # This changes the data so that (0,0) is SW, so it works correctly when plotting
        cats = [point.category for point in self.draw_window.point_ids] # get all the values for the categorys, atm this is the hex code
        data = np.array((xs,ys,cats)).T # concatenate the arrays so that we can write them to file
        np.savetxt('data.csv', data, delimiter = ',', comments="", header = ','.join([x_name,y_name,category_name]), fmt="%s") # write to file

        # New window that confirms file has been saved
        window = tk.Toplevel()
        window.title('File saved')
        T = tk.Text(window, height=1, width=30)
        T.pack()
        T.insert(tk.END, 'File saved')
        window.after(1000, window.destroy)

    def update_gui_text(self, point_ids):
        #save data to a csv file
        height = self.draw_window.winfo_height()
        width = self.draw_window.winfo_width()
        xs, ys = [point.x for point in point_ids], [point.y for point in point_ids]

        # get the mean in the x plane
        xmean = np.mean(xs) / width
        xstd = np.std(xs) / width

        # get the mean in the y plane, need to take into account the fact that 0,0 is nw
        ymean = np.mean(ys) / height
        ystd = np.std(ys) / height

        r = 0 # default r^2
        n = len(point_ids)
        # only calculate r^2 if there is more than one point 
        if n > 1:
            r = np.corrcoef(xs, ys)[0, 1]**2

        self.stats.update_values([xmean, xstd, ymean, ystd, r, n])

# Class that replicates the tkinter.colorchooser dialog
class color_picker(DataCreator):
    def __init__(self):
        self.color = 'None'
        self.new_cat_name = StringVar()
    
    # return the variables
    def get_vars(self):
        return self.color, self.new_cat_name
    # get hex value
    def rgbtohex(self, r,g,b):
        return f'#{r:02x}{g:02x}{b:02x}'

    # Function to update the color of the canvas
    def update_col(self, val):
        self.display_box.configure(bg = self.rgbtohex(self.R_scale.get(),self.G_scale.get(),self.B_scale.get()))

    # Close the window and print chosen value
    def close_dialog(self):
        self.color = self.rgbtohex(self.R_scale.get(),self.G_scale.get(),self.B_scale.get())
        self.new_cat_name = self.new_cat_entry.get()
        Particle.current_colour, Particle.current_category = self.get_vars()

        self.window.destroy()
    
    # Gui for the color chooser
    def color_chooser(self):
        # Create window
        self.window = tk.Tk()
        self.window.title('Choose a color')
        self.window.geometry("356x200")

        # Slider widgets
        self.R_scale = Scale(master = self.window, length = 256, orient='horizontal', from_=0, to=255)
        self.R_scale.grid(row = 0, column = 0)
        self.G_scale = Scale(master = self.window, length = 256, orient='horizontal', from_=0, to=255)
        self.G_scale.grid(row = 1, column = 0)
        self.B_scale = Scale(master = self.window, length = 256, orient='horizontal', from_=0, to=255)
        self.B_scale.grid(row = 2, column = 0)

        # Bindings for mouse interactions
        self.R_scale.bind("<Motion>", self.update_col)
        self.G_scale.bind("<Motion>", self.update_col)
        self.B_scale.bind("<Motion>", self.update_col)

        # Canvas to display color
        self.display_box = Canvas(master = self.window, width =90, height = 125, bg = self.rgbtohex(self.R_scale.get(),self.G_scale.get(),self.B_scale.get()))
        self.display_box.grid(row = 0, rowspan =3, column = 1)

        # Label and entry for new variable name
        self.new_cat_label = Label(master = self.window, text = 'Enter variable name')
        self.new_cat_label.grid(row=3, column=0)
        self.new_cat_entry = Entry(master = self.window, textvariable=self.new_cat_name)
        self.new_cat_entry.grid(row=4, column=0)

        # Buttons to exit the dialog
        self.ok_button = Button(master = self.window, text = 'Okay', command = self.close_dialog)
        self.ok_button.grid(row = 5, column = 0)
        self.close_button = Button(master = self.window, text = 'Cancel', command = self.window.destroy)
        self.close_button.grid(row = 5, column = 1)

def main():
    # create window
    root = tk.Tk()
    root.geometry("1300x710") # arbitrary size
    root.title('DataCreator')
    win = DataCreator(root)
    win.pack()
    root.mainloop()

if __name__ == "__main__":
    main()