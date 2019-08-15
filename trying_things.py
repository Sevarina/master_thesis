import os
import PySimpleGUI as sg
import pandas as pd
import scipy as sp
import numpy as np
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

def make_layout_nav_filelist(target= 'files you want to test'):
    layout = [
        [sg.Text('Please use CTRL and SHIFT to choose '+ target +"!")],
        [sg.InputText("", key = "data"), sg.FilesBrowse(target = "data")],
        [sg.Submit(), sg.Cancel()]
        ]
    return layout

window_initial = sg.Window('Drop test program').Layout(make_layout_nav_filelist())
event, values = window_initial.Read()
file_list = values['data'].split(';')
print(file_list)
