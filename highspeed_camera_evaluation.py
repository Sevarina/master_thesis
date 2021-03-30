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


fps = 1.0 * 10 ** 3 # frames per second

def tsv_to_csv(direct = r"C:\Users\kunge\Downloads\KIRUNA\Tests\100sc+geobrugg\raw_data\Videos scale\fixed"):
    file_list = core.make_file_list(direct, "tsv")
    for i in file_list:
        table = read_tsv(i)
        table.to_csv(i[:-3] + "csv")

# read data
def read_tsv(filepath):
    table = pd.read_csv(filepath, sep = '\t', dtype= {'x': np.float64, 'y': np.float64, 't' : np.float64}, skiprows = 1)# index_col=0) 
    return table

# read data
def read_csv(filepath):
    table = pd.read_csv(filepath, sep = ',', dtype= {'x': np.float64, 'y': np.float64, 't' : np.float64}, index_col=0)#), skiprows = 1, )# ) 
    return table

def replace_time(table):
    """set start time to zero
    #substract start time from following time stamps
    #look at difference between time stamps 
    #compare difference with desired difference
    #get divisor
    #divide time steps by divisor
    """   
    table["t"] = table["t"] - table["t"].iloc[0] * 1.0
    time_step = table["t"].iloc[1] - table["t"].iloc[0]
    if time_step != 1/fps:  
        divisor = time_step / (1/fps)
        table["t"] = table["t"] / divisor
    return table

def fix_time(table):
    time = [0.0]
    for i in range(table.shape[0] - 1):
        time.append(round(time[-1] + 1 / fps, 5))
    table["t"] = time
    return table

# print(table)
def fix_x(table):
    table["x"] =  (table["x"] - table["x"].iloc[0])
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
    table = read_csv(filepath)
    # dummydata = [[1,2,2],[2,1,2], [3,2,4], [11,2,6]]
    # table = pd.DataFrame(data = dummydata, columns = ['t', 'x', 'y'])
    # table = fix_time(table)
    # table = fix_x(table)
    table = replace_time(table)
    plot(table, filepath)
    # if not os.path.isdir(os.path.dirname(filepath) + r"/fixed/"):
    #     os.mkdir(os.path.dirname(filepath) + r"/fixed/")
    # save_path = os.path.dirname(filepath) + r"/fixed/" + os.path.basename(filepath)[:-3] + "csv"
    # table.to_csv(save_path)
    

def fix_tracker_data(direct = r"C:\Users\kunge\Downloads\Files\schnippi-schnappi"):
    file_list = core.make_file_list(direct, "csv")
    for i in file_list:
        print(i)
        fix_data(i)

#TO DO
def piece_together(file_1 = r'C:\Users\kunge\Downloads\Files\schnippi-schnappi\WM single impact\fixed\15_a.csv', 
            file_2 = r'C:\Users\kunge\Downloads\Files\schnippi-schnappi\WM single impact\fixed\15_b.csv',#file_3 = False):#, 
            file_3 = r'C:\Users\kunge\Downloads\Files\schnippi-schnappi\WM single impact\fixed\15_c.csv'):
    """# open all parts
    # set start of each part to the value of the end of previous part (remember difference!)
    # substract difference between start and end from everything in the part
    # append part
    """
    part_1 = read_csv(file_1)
    part_2 = read_csv(file_2)
    # dummydata = [[1,2,2],[2,4,2], [3,6,4], [11,8,6]]
    # part_1 = pd.DataFrame(data = dummydata, columns = ['t', 'x', 'y'])
    # part_2 = pd.DataFrame(data = dummydata, columns = ['t', 'x', 'y'])
    t_diff = part_2["t"].iloc[0] - part_1["t"].iloc[-1]
    x_diff = part_2["x"].iloc[0] - part_1["x"].iloc[-1]
    y_diff = part_2["y"].iloc[0] - part_1["y"].iloc[-1]
    part_2["t"] = part_2["t"] - t_diff
    part_2["x"] = part_2["x"] - x_diff
    part_2["y"] = part_2["y"] - y_diff
    part_2.drop(index = 0, inplace=True)
    part_1 = part_1.append(part_2)
    save_path = file_1[:-4] + "+b.csv"
    if file_3:
        part_3 = read_csv(file_3)
        t_diff = part_3["t"].iloc[0] - part_1["t"].iloc[-1]
        x_diff = part_3["x"].iloc[0] - part_1["x"].iloc[-1]
        y_diff = part_3["y"].iloc[0] - part_1["y"].iloc[-1]
        part_3["t"] = part_3["t"] - t_diff
        part_3["x"] = part_3["x"] - x_diff
        part_3["y"] = part_3["y"] - y_diff
        part_3.drop(index = 0, inplace=True)
        part_1 = part_1.append(part_3)
        save_path = file_1[:-4] + "+b+c.csv"
    print(save_path)
    part_1.to_csv(save_path)

# piece_together()
fix_tracker_data(r"C:\Users\kunge\Downloads\KIRUNA\deformation\geobrugg\fixed")
#tsv_to_csv(r"C:\Users\kunge\Downloads\Files\schnippi-schnappi\geobrugg\fixed")
        
