import os
import PySimpleGUI as sg
import pandas as pd
import scipy as sp
import numpy as np
from adjustText import adjust_text
import GUI as gui
import matplotlib as mpl
import clean_array as clean
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

def convert_single_file(target_file = "the file you want to convert", target_folder = "where you want the converted data to be saved"):
    if target_file != "":
        file = gui.nav_file_check(target = target_file, extension = "asc")
        if file is None:
            return
    if target_folder != "":
        _, data = gui.nav_folder_check(target = target_folder)
    if data == "" or file == "":
        return
    #convert
    basic_array = core.find_folder(data, "basic_array")
    filename = convert_file(basic_array, [file])
    return filename, basic_array, data

def convert_file(basic_array, file_list):
    direct = "\\".join(basic_array.split("\\")[:-1])
    data = gui.UI_open_df(direct)
    if data is None:
        return
    res_list = []
    for i in file_list:
        print(data.index)
        filename = os.path.basename(i)[:-4]
        save_path = basic_array + "\\" + data.loc[filename,"Broken/cracked"] + "\\" + filename + ".npy"
        #if file is already converted skip it
        if os.path.isfile(save_path):
            continue
        clean.clean_array(initial_file= i, clean_file = save_path,  sample_type= data.loc[filename,"Sample type"].lower())
        res_list.append(save_path)
    return res_list

convert_single_file()   