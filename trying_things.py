import os
import PySimpleGUI as sg
import pandas as pd
import scipy as sp
import numpy as np
import scipy.signal as sig
from adjustText import adjust_text
#import drop_test_analysis as gui
import matplotlib as mpl
#import clean_array as clean
#make all plots look nice
mpl.style.use('classic')
mpl.rcParams['text.latex.preamble'] = [r'\usepackage{helvet}\renewcommand\familydefault{\sfdefault}', r'\usepackage{amsmath}' , r'\usepackage[T1]{fontenc}'] 

import random
#"fix" matplotlib font - it´s arial instead of helvetica but better than nothing
#plt.rcParams['mathtext.fontset'] = 'custom'
mpl.rcParams['font.sans-serif'] = "Arial"
mpl.rcParams['font.family'] = "sans-serif"
mpl.rcParams['mathtext.default']='default'
import matplotlib.pyplot as plt
import coreprogram as core
# 5import plotly.graph_objects as go

from scipy.ndimage.filters import uniform_filter1d

import math
latex_unit = {
        "Acceleration" : r"\(\Big[\frac{\text{m}}{\text{s}^\text{2}}\Big]\)",
        "Age" : r"\([\text{days}]\)",
        "Average crack width" : r"\([\text{mm}]\)",
        "Broken/Cracked" : "",
        "Crack area" : r"\([\text{mm}^\text{2}]\)",
        "Displacement" : r"\([\text{mm}]\)",
        "Drop height" :  r"\([\text{mm}]\)",
        "Drop weight" :  r"\([\text{kg}]\)",
        "Energy level" : r"\([\text{kJ}]\)",
        "Energy per area" : r"\(\big[\frac{\text{kJ}}{\text{m}^2}\big]\)",
        "Force" : r"\([\text{kN}]\)",
        "High speed camera" : r"\([\text{mm}]\)",
        "Length 1" : r"\([\text{mm}]\)",
        "Length 2" : r"\([\text{mm}]\)",
        "Length 3" : r"\([\text{mm}]\)",
        "Length 4" : r"\([\text{mm}]\)",
        "Length 5" : r"\([\text{mm}]\)",
        "Length 6" : r"\([\text{mm}]\)",
        "Name" : "",
        "Number" : "",
        "Opening angle": r"\([\text{\textdegree}]\)",
        "Thickness" : r"\([\text{mm}]\)",
        "Time" : r"\([\text{s}]\)",
        "Velocity" : r"\(\big[\frac{\text{m}}{\text{s}}\big]\)",
        "Width 1" : r"\([\text{mm}]\)",
        "Width 2" : r"\([\text{mm}]\)",
        "Width 3" : r"\([\text{mm}]\)",
        "Width 4" : r"\([\text{mm}]\)",
        "Width 5" : r"\([\text{mm}]\)",
        "Width 6" : r"\([\text{mm}]\)",
        }


fps = 1.0 #* 10 ** 3 # frames per second

# read data
def read_table(filepath):
    table = pd.read_csv(filepath, sep = '\t', dtype= {'x': np.float64, 'y': np.float64}, skiprows = 1, )# index_col=0) 
    return table

#built time

def replace_time(table):
    """set start time to zero
    #substract start time from following time stamps
    #look at difference between time stamps 
    #compare difference with desired difference
    #get divisor
    #divide time steps by divisor
    #
    
    """   
    table["t"] = table["t"] - table["t"].iloc[0]
    time_step = table["t"].iloc[1] - table["t"].iloc[0]
    if time_step != 1/fps:  
        divisor = time_step / (1/fps)
        table["t"] = table["t"] / divisor
    # nan_index = []
    # for j in range(table["t"].shape[0],1):
    #     step = (table['t'].iloc[j] - table['t'].iloc[j-1])
    #     if np.round(step / fps, 0) != 1:
    #         nan_index.append(j, np.round(step / fps, 0))
    length = int(np.round((table['t'].iloc[-1] - table['t'].iloc[0]) / (1/fps), 0))
    if length > table['t'].shape[0]:
        empty_array = np.empty((length + 1, 3))
        empty_array[:] = np.NaN
        new_table = pd.DataFrame(data = empty_array, columns = ['t', 'x', 'y'])
        time_array = []
        for i in range(length + 1):
            time_array.append(1/fps * i)
        new_table["t"] = time_array
        print(table)
        print(new_table)
        for j in new_table["t"]:
            if j in table['t']:
        #print(df[df[‘Name’]==’Donna’].index.values)
                print("index : ", table[table['t'] == j].index.values)
#                new_table[new_table['t'].get_loc(j)] = table[table["t"].get_loc(j)]
        print(new_table)

def fix_time(table):
    time = [0.0]
    for i in range(table.shape[0] - 1):
        time.append(round(time[-1] + 1 / fps, 5))
    table["t"] = time
    return table

# print(table)
def fix_x(table):
    table["x"] =  (table["x"] - table["x"].iloc[0]) * - 1.0
    return table

def plot(table, filepath):
    plt.plot(table["t"], table["x"])
    fig_path = filepath[:-4] +  ".pdf"
    plt.grid()
    plt.xlabel("Time "+ latex_unit["Time"], usetex= True)
    plt.ylabel("Displacement "+ latex_unit["Displacement"], usetex= True)
    plt.savefig(fig_path, format = "pdf")
    fig_path = filepath[:-4] + ".png"
    plt.savefig(fig_path, format = "png")
    plt.close()

def fix_data(filepath):
    #table = read_table(filepath)
    dummydata = [[1,2,2],[2,1,2], [10 , 2,4]]
    table = pd.DataFrame(data = dummydata, columns = ['t', 'x', 'y'])
    # table = fix_time(table)
    # table = fix_x(table)
    # plot(table, filepath)
    # save_path = os.path.dirname(filepath) + r"/fixed/" + os.path.basename(filepath)
    # table.to_csv(save_path)
    replace_time(table)

def fix_tracker_data(direct = r"C:\Users\kunge\Downloads\KIRUNA\Tests\100sc+geobrugg\raw_data\Videos scale\fixed"):
    file_list = core.make_file_list(direct, "tsv")
    for i in file_list:
        fix_data(i)

#TO DO
    # find data that is in several parts
    # open all parts
    # set start of each part to the value of the end of previous part (remember difference!)
    # substract difference between start and end from everything in the part
    # append part

fix_data(r"C:\Users\kunge\Downloads\KIRUNA\Tests\100sc+geobrugg\raw_data\Videos scale\2kJ.tsv")
#fix_tracker_data()
        
