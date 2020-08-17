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

#"fix" matplotlib font - it´s arial instead of helvetica but better than nothing
#plt.rcParams['mathtext.fontset'] = 'custom'
mpl.rcParams['font.sans-serif'] = "Arial"
mpl.rcParams['font.family'] = "sans-serif"
mpl.rcParams['mathtext.default']='default'
import matplotlib.pyplot as plt
import coreprogram as core
# 5import plotly.graph_objects as go

from scipy.ndimage.filters import uniform_filter1d


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
        "Velocity" : r"\(\big[\frac{\text{m}}{\text{s}}\big]\)",
        "Width 1" : r"\([\text{mm}]\)",
        "Width 2" : r"\([\text{mm}]\)",
        "Width 3" : r"\([\text{mm}]\)",
        "Width 4" : r"\([\text{mm}]\)",
        "Width 5" : r"\([\text{mm}]\)",
        "Width 6" : r"\([\text{mm}]\)",
        }

def make_marker_list():
# build a marker array
    color = ["b", "g", "r", "c","m", "y", "k"]
    shape = [".", "v", "^", "1", "s", "*", "+", "x", "D"]
    marker_list = []
    for c in color:
        for s in shape:
            marker_list.append(s+c)
    return marker_list

def plot_dynamic(sheet = r"C:\Users\kunge\Downloads\KIRUNA\kiruna.xlsx"):
    table = pd.read_excel(sheet, sheet_name = "python_dynamic")
    table.set_index("element", inplace=True)
    a = ""
    short_index = []
    for i in table.index:
        if a is i:
            continue
        else:
            short_index.append(i)
            a = i
    
    Table = table.T
    marker_list = make_marker_list()
    for j in short_index:
        energy = Table[j].T["energy [kJ/m2]"]
        deformation = Table[j].T["deflection [m]"]
        plt.plot(deformation, energy, marker_list.pop(0), label = j)
    xlim = (0, 0.65)
    ylim = (0, 18)
    plt.plot(xlim, ylim, 'r-', alpha=0.0)      
    plt.xlabel("Deflection [m]")
    plt.ylabel(r"Energy $\Big[\frac{\text{kJ}}{\text{m}^\text{2}}\Big]$", usetex = True)
    plt.grid()
    plt.legend(bbox_to_anchor=(1.04,1), loc="upper left")
    plt.savefig(r"C:\Users\kunge\OneDrive\Desktop\dynamic.png", bbox_inches='tight')

def plot_static(sheet = r"C:\Users\kunge\Downloads\KIRUNA\kiruna.xlsx"):
    table = pd.read_excel(sheet, sheet_name = "python_static")
    table.set_index("element", inplace=True)
    
    a = ""
    short_index = []
    for i in table.index:
        if a is i:
            continue
        else:
            short_index.append(i)
            a = i
    
    Table = table.T
    marker_list = make_marker_list()
    for j in short_index:
        energy = Table[j].T["energy [kJ/m2]"]
        deformation = Table[j].T["deflection [m]"]
        plt.plot(deformation, energy, marker_list.pop(0), label = j)
 # plt.xlim is not working so I am adding and invisble line to make the plot fit the boundaries
    xlim = (0, 0.4)
    ylim = (0, 0.25)
    plt.plot(xlim, ylim, alpha=0.0)        
    plt.xlabel("Deflection [m]")
    plt.ylabel(r"Energy $\Big[\frac{\text{kJ}}{\text{m}^\text{2}}\Big]$", usetex = True)
    # plt.title("Results of Static Tests")
    plt.grid()
    plt.legend(bbox_to_anchor=(1.04,1), loc="upper left")
    plt.savefig(r"C:\Users\kunge\OneDrive\Desktop\static.png", bbox_inches='tight')



def common_member(a, b): 
    a_set = set(a) 
    b_set = set(b) 
  
    if (a_set & b_set): 
        return (a_set & b_set) 
    else: 
        return "No common elements" 


def update_limits(df, limit):
    if df.max() > limit:
        return df.max()
    else:
        return limit

def compare_static_dynamic(sheet = r"C:\Users\kunge\Downloads\KIRUNA\kiruna.xlsx"):
    dynamic= pd.read_excel(sheet, sheet_name = "python_dynamic")
    dynamic.set_index("element", inplace=True)
    
    a = ""
    dynamic_index = []
    for i in dynamic.index:
        if a is i:
            continue
        else:
            dynamic_index.append(i)
            a = i
            
    static = pd.read_excel(sheet, sheet_name = "python_static")
    static.set_index("element", inplace=True)
    a = ""
    static_index = []
    for i in static.index:
        if a is i:
            continue
        else:
            static_index.append(i)
            a = i
    combined_index = common_member(dynamic_index, static_index)
    if combined_index == "No common elements":
        return combined_index
    marker_list = make_marker_list()
    Dynamic = dynamic.T
    Static = static.T
    for i in combined_index:
        xlim = [0,0]
        ylim = [0,0]
        static_energy = Static[i].T["energy [kJ/m2]"]
        ylim[1] = update_limits(static_energy, ylim[1])
        static_deformation = Static[i].T["deflection [m]"]
        xlim[1] = update_limits(static_deformation, xlim[1])
        plt.plot(static_deformation, static_energy, marker_list.pop(0), label = "static")
        
        dynamic_energy = Dynamic[i].T["energy [kJ/m2]"]
        ylim[1] = update_limits(dynamic_energy, ylim[1])        
        dynamic_deformation = Dynamic[i].T["deflection [m]"]
        xlim[1] = update_limits(static_deformation, xlim[1])        
        plt.plot(dynamic_deformation, dynamic_energy, marker_list.pop(0), label = "dynamic")
        
        xlim[1] = xlim[1] * 1.2
        ylim[1] = ylim[1] * 1.2
        plt.plot(xlim, ylim, alpha=0.0)
        
        plt.xlabel("Deflection [m]")
        plt.ylabel(r"Energy $\Big[\frac{\text{kJ}}{\text{m}^\text{2}}\Big]$", usetex = True)
        plt.title(i)
        plt.grid()
        plt.legend(bbox_to_anchor=(1.04,1), loc="upper left")
        plt.savefig(r"C:\Users\kunge\OneDrive\Desktop" + "\\" + i + ".png", bbox_inches='tight')
        plt.close()


compare_static_dynamic()

