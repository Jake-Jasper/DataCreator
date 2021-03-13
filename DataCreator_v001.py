'''
TODO ETC


The data portion:
General:
- Add the ability to load other datasets e.g. the wine dataset.

UI:
- Could make it non basic, but cba
- Hook up variables with entry boxes and add conditional etc. For example, you should only be able to add a second variable after
- Would be nice to have the axis variable names actually along the axis oriented as a normal graph would. NOt sure how hard/easy this would be to program.
- Add a box for instructions.
- Add option to enable/disable secondary variable. 

Bugs:
- Throws an error when I reset the canvas, as you can't take a mean of a slice, but it doesn't effect the functionality.
'''

import pandas as pd
import tkinter as tk
from tkinter import *
import tkinter.colorchooser
import numpy as np
import random, time
from itertools import count
import random
from scipy.stats import pearsonr

# GLOBAL VARS
'''
global root
global canvas
global clicks
global point_ids
global current_colour
global animation_status
global x_mean,x_mean_label, x_std, x_std_label, xe, e_cat
global y_mean, y_mean_label, y_std, y_std_label, ye
global n, n_label
global Pearsons_R, Pearsons_R_label
global text_box


clicks = []   # stores the clicks that the user makes on the canvas.
current_colour = '#000000' # Default black
'''

# Class to create and store data points
class Particle:
    # this is used two assign different ids each time a class is called. There is probably  better way of doing this but it works.
    p_id = count(0)

    def __init__(self, x, y, velocity):
        RADIUS_MODIFIER = 5
        self.p_id = next(self.p_id)
        # x and y should also be unique at this point
        self.x = x
        self.y = y
        self.category = current_colour
        # need to set this so it has a random direction to start somehow
        self.velocity = velocity#[1,1]
        self.point = canvas.create_oval(x-RADIUS_MODIFIER, y-RADIUS_MODIFIER, x+RADIUS_MODIFIER, y+RADIUS_MODIFIER, width = 0, fill = current_colour, tags = 'points')
        self.location = (0,0,0,0)


# Function clear all data 
def reset_points():
    #reset data
    canvas.delete('points')
    clicks.clear()
    point_ids.clear()
    global x_mean, x_mean_label, x_std, x_std_label
    global y_mean, y_mean_label, y_std, y_std_label
    global n, n_label
    global Pearson_R, Pearsons_R_label

    x_mean.set(getx_mean()) 
    x_mean_label.config(text = f'X mean: {x_mean.get()}')
    x_std.set(getx_std())
    x_std_label.config(text = f'X std: {x_std.get()}')
    y_mean.set(gety_mean())
    y_mean_label.config(text = f'Y mean: {y_mean.get()}')
    y_std.set(gety_std())
    y_std_label.config(text = f'Y std: {y_std.get()}')
    Pearsons_R.set(get_r())
    Pearsons_R_label.config(text = f'Pearson\'s R: {Pearsons_R.get()}')
    n.set(get_n())
    n_label.config(text = f'N: {n.get()}')




# Recors click events and updates the screen
def click(event):
# record clicks
    x, y = event.x, event.y
    clicks.append((x, canvas.winfo_height() - y)) # canvas.winfo_height() - y makes it so the resulting data matches the canvas
    # create a new particle
    point_ids.append(Particle(x = x, y = y, velocity = [random.uniform(-4,4),random.uniform(-4,4)])) #
    global x_mean, x_mean_label, x_std, x_std_label
    global y_mean, y_mean_label, y_std, y_std_label
    global Pearsons_R, Pearsons_R_label
    global n, n_label 
    x_mean.set(getx_mean()) 
    x_mean_label.config(text = f'X mean: {x_mean.get()}')
    x_std.set(getx_std())
    x_std_label.config(text = f'X std: {x_std.get()}')
    y_mean.set(gety_mean())
    y_mean_label.config(text = f'Y mean: {y_mean.get()}')
    y_std.set(gety_std())
    y_std_label.config(text = f'Y std: {y_std.get()}')
    Pearsons_R.set(get_r())
    Pearsons_R_label.config(text = f'Pearson\'s R: {Pearsons_R.get()}') 
    n.set(get_n())
    n_label.config(text = f'N: {n.get()}')


# Save the current data. This needs a complete rework to take into account the sub-variables.
def file_save():
    #save data to a csv file
    global xe, ye, e_cat
    data = pd.DataFrame()
    x = x_var_entry.get()
    y = y_var_entry.get()
    category = x2_var_entry.get()
    data[x] = np.asarray(clicks)[:,0] / canvas.winfo_width()
    data[y] = np.asarray(clicks)[:,1] / canvas.winfo_height()
    data[category] = [point.category for point in point_ids]
    data.to_csv('data.csv', index = False)
    window = tk.Toplevel(root)
    window.title('File saved')
    T = tk.Text(window, height=1, width=30)
    T.pack()
    T.insert(tk.END, 'File saved')
    window.after(1000, lambda: window.destroy())


# Change the color of the particles, and also will be used to identify the category a variable belongs to
def choose_color(): 
    # variable to store hexadecimal code of color, it also retruns rgb, so I need to strip the hex code. "{rgb} #hexode" 
    color_code = tkinter.colorchooser.askcolor(title ="Choose color") 
    global current_colour 
    current_colour= color_code[1] 
    # set the colour of the second variable
    global x2_var_entry
    x2_var_entry.config(fg = current_colour)
    return color_code

# get the mean in the x plane
def getx_mean():
    xmean = [point.x for point in point_ids]
    return round(np.mean(xmean) / canvas.winfo_width(), 2)

def getx_std():
    xstd = [point.x for point in point_ids]
    return round(np.std(xstd) / canvas.winfo_width(), 2)

# get the mean in the y plane, need to take into account the fact that 0,0 is nw
def gety_mean():
    ymean = [canvas.winfo_height() - point.y for point in point_ids]
    return round(np.mean(ymean) / canvas.winfo_height(), 2)

def gety_std():
    ystd = [point.y for point in point_ids]  # don't need to normalise for canvas in this case
    return round(np.std(ystd) / canvas.winfo_height(), 2)

def get_r():
    xs, ys = [point.x for point in point_ids], [point.y for point in point_ids]
    r, p = pearsonr(xs, ys)
    return round(-r,2)

def get_n():
    return len(point_ids)

# This makes the gridlines on the canvas.
def create_grid(event=None):
    w = canvas.winfo_width() # Get current width of canvas
    h = canvas.winfo_height() # Get current height of canvas
    #canvas.delete('grid_line') # Will only remove the grid_line

    # Creates all vertical lines at intevals of 100
    for i in range(0, w, 100):
        canvas.create_line([(i, 0), (i, h)], tag='grid_line')

    # Creates all horizontal lines at intevals of 100
    for i in range(0, h, 100):
        canvas.create_line([(0, i), (w, i)], tag='grid_line')


def dataCreator():
    global root
    global canvas
    global clicks
    global point_ids
    global current_colour
    global animation_status
    global x_mean,x_mean_label, x_std, x_std_label, xe, e_cat
    global y_mean, y_mean_label, y_std, y_std_label, ye
    global n, n_label
    global Pearsons_R, Pearsons_R_label
    global text_box


    clicks = []   # stores the clicks that the user makes on the canvas.
    current_colour = '#000000' # Default black


    # Create the window and draw the canvas
    # create window
    root = tk.Tk()
    root.geometry("1300x710")
    root.title('Draw your data')

    # Create the canvas and make it visible with pack()
    canvas = tk.Canvas(root, highlightthickness =2, highlightbackground = 'black')
    canvas.grid(row=0, column =0)
    canvas.config(background = 'white', width = 800, height = 700)
    canvas.bind('<Configure>', create_grid) # This adds the grid line every 100 piexels
    canvas.update()

    frame = Frame(root)
    frame.grid(row=0,column=1, sticky="n")
    # store all the particle objects.
    point_ids = []



    # menu items
    menubar = tk.Menu(root)
    filemenu = tk.Menu(menubar, tearoff=0)
    filemenu.add_command(label="Reset", command=reset_points)
    filemenu.add_command(label="Exit", command=root.quit)
    filemenu.add_command(label="Save", command=file_save)
    menubar.add_cascade(label="Options", menu=filemenu)
    menubar.add_command(label="Change color", command=choose_color) #This changes the global color

    # record clicks on canvas only.
    canvas.bind('<Button-1>', click)

    # add menubar
    root.config(menu=menubar)

    # Add some boxes to show the stats.
    x_mean = DoubleVar() 
    xe = StringVar()
    x_mean_label = Label(frame, text = f'X mean: {x_mean.get()}')
    x_mean_label.grid(row=0,column=0, sticky="e") # starting label
    Label(frame, text = 'X name:').grid(row=0, column=1, padx = 10)
    x_var_entry = Entry(frame, textvariable=xe)
    x_var_entry.grid(row=0, column =2)
    x_var_entry.config(fg = current_colour) # This should always stay the base colour
    xe.set('X') # Default x label


    x_std = DoubleVar()
    x_std_label = Label(frame, text = f'X std: {x_std.get()}')
    x_std_label.grid(row=1,column=0, sticky="e")

    y_mean = DoubleVar()
    ye = StringVar()
    y_mean_label = Label(frame, text = f'Y mean: {y_mean.get()}')
    y_mean_label.grid(row=2,column=0, sticky="e")
    Label(frame, text = 'Y name:').grid(row=2, column =1, padx =20)
    y_var_entry = Entry(frame, textvariable = ye)
    y_var_entry.grid(row=2, column = 2)
    ye.set('Y')

    y_std = DoubleVar()
    y_std_label = Label(frame, text = f'Y std: {y_std.get()}')
    y_std_label.grid(row=3,column=0, sticky="e")

    Pearsons_R = DoubleVar()
    Pearsons_R_label = Label(frame, text = f'Pearson\'s R: {Pearsons_R.get()}')
    Pearsons_R_label.grid(row=4, column = 0, sticky = 'e')


    n = IntVar()
    n_label = Label(frame, text = f'N: {n.get()}')
    n_label.grid(row=5,column=0, sticky="e")

    ### Secondary X variable -- need a better name than x2 for this.
    global x2_var_entry
    e_cat = StringVar()
    Label(frame, text = '3rd Variable name:').grid(row=7, column=1, padx = 10)
    x2_var_entry = Entry(frame, textvariable=e_cat)
    x2_var_entry.grid(row=7, column =2)
    x2_var_entry.config(fg = current_colour) # This should change to the new colour
    # Forget why I called this e_cat, but once I think of that better name
    e_cat.set('3rd Variable')

    text_box = Label(frame, text = 'To create another variable, change the colour.  \n All points will be sub classified by colour')



    frame.grid_rowconfigure(8, weight=1, minsize=100)
    text_box.grid(row = 20, column = 0, columnspan = 2)



    # run mainloop
    root.mainloop()



dataCreator()