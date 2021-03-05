#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 15:33:33 2019

@author: KEKAUN
"""

import numpy as np
import math
import statistics as stat

import matplotlib.style
import matplotlib as mpl
#make all plots look nice
mpl.style.use('classic')

import matplotlib.pyplot as plt

import scipy as sp
import scipy.signal as sig
import scipy.integrate as integrate

import seaborn as sns

import os
import re
import pandas as pd
from adjustText import adjust_text
import locale
locale.setlocale(locale.LC_ALL, 'deu_deu')

import clean_file as clean

mpl.rcParams['text.latex.preamble'] = [r'\usepackage{helvet}\renewcommand\familydefault{\sfdefault}', r'\usepackage{amsmath}' , r'\usepackage[T1]{fontenc}'] 

#"fix" matplotlib font - it´s arial instead of helvetica but better than nothing
#plt.rcParams['mathtext.fontset'] = 'custom'
mpl.rcParams['font.sans-serif'] = "Arial"
mpl.rcParams['font.family'] = "sans-serif"
mpl.rcParams['mathtext.default']='default'
mpl.rcParams['legend.numpoints'] = 1
###############################################################

    #keep the unit
latex_unit = {
        "Acceleration" : r"\(\Big[\frac{\text{m}}{\text{s}^\text{2}}\Big]\)",
        "Age" : r"\([\text{days}]\)",
        "Average crack width" : r"\([\text{mm}]\)",
        "Broken/Cracked" : "",
        "Crack area" : r"\([\text{mm}^\text{2}]\)",
        "Deformation" : r"\([\text{mm}]\)",
        "Drop height" :  r"\([\text{mm}]\)",
        "Drop weight" :  r"\([\text{kg}]\)",
        "Energy level" : r"\([\text{kJ}]\)",
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
        "Spring constant" : r"\(\Big[\frac{\text{kN}}{\text{mm}\Big]\)",
        "Thickness" : r"\([\text{mm}]\)",
        "Velocity" : r"\(\big[\frac{\text{m}}{\text{s}}\big]\)",
        "Width 1" : r"\([\text{mm}]\)",
        "Width 2" : r"\([\text{mm}]\)",
        "Width 3" : r"\([\text{mm}]\)",
        "Width 4" : r"\([\text{mm}]\)",
        "Width 5" : r"\([\text{mm}]\)",
        "Width 6" : r"\([\text{mm}]\)",
        }

short_unit = {       
        "Acceleration" : r"[m/s2]",
        "Age" : r"[days]",
        "Average crack width" : r"[mm]",
        "Broken/Cracked" : "",
        "Crack area" : r"[mm2]",
        "Deformation" : r"[mm]",
        "Drop height" :  r"[mm]",
        "Drop weight" :  r"[kg]",
        "Energy level" : r"[kJ]",
        "Force" : r"[kN]",
        "High speed camera" : r"[mm]",
        "Length 1" : r"[mm]",
        "Length 2" : r"[mm]",
        "Length 3" : r"[mm]",
        "Length 4" : r"[mm]",
        "Length 5" : r"[mm]",
        "Length 6" : r"[mm]",
        "Name" : "",
        "Number" : "",
        "Opening angle": r"[degrees]",
        "Spring constant" : r"[kN/mm2]",
        "Thickness" : r"[mm]",
        "Velocity" : r"[m/s]",
        "Width 1" : r"[mm]",
        "Width 2" : r"[mm]",
        "Width 3" : r"[mm]",
        "Width 4" : r"[mm]",
        "Width 5" : r"[mm]",
        "Width 6" : r"[mm]",
        }

#contains everything you need from a dataset
class Dataset:
    def __init__(self, filename, sample_type = "square"):
        self.name = os.path.basename(filename)[:-4]
        self.array = np.load(filename)
        self.type = sample_type.lower()
        
        # 3  load cells
        if self.type == "round":
            indizes = {
                    "time":0,
                    "load":(1,2,3),
                    "laser":4,
                    "accelerometer":5,
                    "magnetventil":6,
                    "telfer_reset":7,
                    "distance_up":8,
                    "distance_down":9}
        
        # 4 load cells
        elif self.type == "square":
            indizes = {
                    "time":0,
                    "load":(1,2,3,4),
                    "laser":5,
                    "accelerometer":6,
                    "magnetventil":7,
                    "telfer_reset":8,
                    "distance_up":9,
                    "distance_down":10}
        else:
            raise ValueError ("Sample type unknown") 
            
        self.indizes = indizes
        
        # #define datasets
        self.time = self.array[:,self.indizes["time"]]
        self.load = self.array[:,self.indizes["load"]]
        self.laser = self.array[:,self.indizes["laser"]]
        self.accel = self.array[:,self.indizes["accelerometer"]]

        # calculate loadcellsum from loadcells
        loadcells = self.load
        self.loadsum = np.sum(loadcells,axis=1)
        
        #set the lengths
        start_accel, end_accel, start_load, end_load, start_laser, end_laser = calc_scope(self.array, self.indizes["magnetventil"])
        # start_accel, end_accel, start_load, end_load, start_laser, end_laser = 0,-1,0,-1,0,-1
        
        #define datasets
        self.load = self.array[start_load:end_load,self.indizes["load"]]
        self.laser = self.array[start_laser:end_laser,self.indizes["laser"]]
        self.accel = self.array[start_accel:end_accel,self.indizes["accelerometer"]]
        #calculate loadcellsum from loadcells
        self.loadsum = np.sum(self.load,axis=1)
        
        #define corresponding time

        self.load_time = self.time[start_load:end_load]
        self.laser_time =  self.time[start_laser:end_laser]
        self.accel_time =  self.time[start_accel:end_accel]

        # self.load_time = self.array[start_load:end_load,self.indizes["time"]]
        # self.laser_time = self.array[start_laser:end_laser,self.indizes["time"]]
        # self.accel_time = self.array[start_accel:end_accel,self.indizes["time"]]
        

    def peak_loads(self):
        peak_list = []
        for i in self.load.shape[1]:
            peak_list.append(filtered_peak[self.load[:,i]])
        return peak_list
        
    def peak_deformation(self):
        return filtered_peak(self.laser)
    
    def peak_accel(self):
        return filtered_peak(self.accel)
        
    # def get_dropheight(self):
    #     #m has a sampling rate of 10kHz, but the telfer of just 1 Hz
    #     m = int(np.argmax(self.array[:,self.indizes["magnetventil"]])/10000)
    #     print(self.array.shape)
    #     u = np.nanargmax(self.array[m:,self.indizes["distance_up"]])
    #     up = self.array[u+m,self.indizes["distance_up"]]
    #     d = np.nanargmax(self.array[m:,self.indizes["distance_down"]])
    #     down = self.array[d+m,self.indizes["distance_down"]]
    #     return up - down           
        
    def make_graphs(self,res_path,app):
        # plot accel
        plot(res_path,x = self.accel_time, y = self.accel ,xlabel= r"Time \([\text{s}]\)",ylabel= r"Acceleration \Big[\(\frac{\text{m}}{\text{s}^2}\)\Big]",name="Acceleration", limit = (-1000,-1),appendix = app, dataset_name = self.name)
            
    ##   plot calc velocity
    #    velo_time = accel_time
    #    velo = integrate.cumtrapz(accel,velo_time,initial = 0)
    #    plot(res_path,x = velo_time, y = velo ,xlabel= r"Time \([\text{s}]\)",ylabel= r"Calculated Velocity \Big[\(\frac{\text{m}}{\text{s}}\)\Big]", name="Velocity")
    #
    ##   plot calc velocity
    #    disp = integrate.cumtrapz(velo,velo_time,initial = 0) * 100
    #    disp_time = accel_time
    #    plot(res_path,x = disp_time, y = disp ,xlabel= r"Time \([\text{s}]\)",ylabel=r"Calculated Displacement \([\text{mm}]\)", name="Calc_Displacement")
    
    #    plot individual load cells
        for i in range(1, self.load.shape[1] + 1):
            plot(res_path,x = self.load_time, y = self.load[:,i-1] ,xlabel= r"Time \([\text{s}]\)",ylabel=r"Load \([\text{kN}]\)", name="Loadcell_" + str(i),appendix = False, dataset_name = self.name)
        
    #    plot sum of all loadcells
        plot(res_path,x = self.load_time, y = self.loadsum ,xlabel= r"Time \([\text{s}]\)",ylabel=r"Load \([\text{kN}]\)", name="Loadcell_sum",appendix = False, dataset_name = self.name)
        
    # plot compilation of load
        load_name = []
        for i in range(1,5):
            load_name.append("load cell " + str(i))
        load_name.append("load cell sum")
        plot_load(res_path,x = self.load_time, load = self.load, loadsum= self.loadsum ,xlabel= r"Time \([\text{s}]\)",ylabel=r"Load \([\text{kN}]\)", name = load_name,appendix = app, dataset_name = self.name)
            
    # plot laser
        # plot(res_path,x = self.laser_time, y = self.laser ,xlabel= r"Time \([\text{s}]\)",ylabel=r"Displacement \([\text{mm}]\)", name="Laser_Displacement", limit=(-100,-1),appendix = app, dataset_name = self.name)

#run all the things we really want on all files
def calc(data=r"C:\Users\kunge\Downloads\KIRUNA\Tests\100sc+geobrugg", results="" , single_impact = False, latex = True):
    '''data is the location of the .npy files for analysis
    results marks the location of the results of the analysis
    single_impact is true if every sample was hit just once. It is false if one sample was hit several times by drop weights.
    latex is true if the programm should generate various latex files for later usage
    if latex is set to false no files will be generated
    '''
    if results == "":
        results = data + r"\results"
    
    if single_impact == True:
        calc_single_impact(data, results, latex, diagrams = False)
    else:
        print("multi!")
        calc_multiple_impact(data, results)
        
def calc_single_impact(data, results, latex, diagrams = True):
    #split path into single_impact and metadata
    print("Calculating single impact")
    single_impact = os.path.join(data,'single_impact')
    metadata = os.path.join(data,'metadata')
    
    #open a result file in the result folder
    make_result_file(results)
    
    #make an appendix file which is necessary for latex
    if latex:
        app_file = make_appendix_file(results)
    else:
        app_file = False
        
    #open the file with the test data
    df = open_df(metadata, 'test_data')
    
    #evaluate every impact and add the data to the results file
    iterate_single(single_impact, results, df, app_file)
    
    # #draw the diagrams
    if diagrams:   
        draw_diagrams(metadata, results, df)

def calc_multiple_impact(data, results):
    # run simple analysis
    calc_single_impact(data, results, latex = True, diagrams = True)
    path = os.path.join(results, "stacked")
    print("individual analysis complete \n commence multi analysis")
    #open result file
    res_df = open_df(results, "result")
    res_df = res_df.drop(res_df.index[0])
    
    #sort results by energy level
    res_df = res_df.sort_values(by = "Energy level", axis = 0)
    
    stack = pd.DataFrame(index = res_df.index)
    #stack the energy level, force, acceleration, Displacement, High speed camera

    for i in ["Energy level", "Force", "Acceleration",]:
        name = i 
        stack[name] = stack_pandas(res_df[i])
        
    stack["Deformation"] = res_df["Deformation"]
    
    #plot stacked value
    if os.path.isdir(path) == False:
        os.mkdir(path)
    for j in stack.columns:
        for k in stack.columns:
            plot_stack(stack,j,k,path)
            
    #calculate spring constant
    stack["Spring constant"] = [stack.at[i,"Force"]/stack.at[i,"Deformation"] for i in stack.index]
    make_latex_table(stack, path + r"/stack.tex")
    stack.to_excel(path + r"/stack.xlsx")
    
def plot_stack(df, i, j, path):
    #begin plot
    ax = plt.subplot(111)
    
    mpl.rcParams["figure.figsize"] = (10,7)
    ax.plot(df[i], df[j], "b.")
    
    #make limits nice
    xlim = ax.get_xlim()
    ax.set_xlim((xlim[0] - 0.05 * xlim[0],xlim[1]+ 0.05 * xlim[1]))
    ylim = ax.get_ylim()
    ax.set_ylim((ylim[0] - 0.05 * ylim[0], ylim[1] + 0.05 * ylim[1]))
                    
    #labels
    ax.set_xlabel(i + " " + latex_unit[i], usetex = True, fontsize = 14)
    ax.set_ylabel(j + " " + latex_unit[j], usetex = True, fontsize = 14)
    
    #grid
    plt.grid()
            
    #save
    filename = path + "\\" + j.replace(" ","-") + "_" + i.replace(" ","-") + ".png"
    plt.savefig(filename)
    plt.close()    

def stack_pandas(series):
    stack = 0
    output = []
    for i in series:
        print(i)
        # add new number to stack
        stack = i + stack
        # append stack to output list
        output.append(stack)
    return pd.Series(data = output, index = series.index)
        
def calc_single_file(filename = r"C:\Users\kekaun\OneDrive - LKAB\roundSamples\Data\basic_array\cracked\2018-11-29_Rfrs_75_1,0.npy",results="",df = "sanity_check", res_file ="", app_file = "", sample_type = "Square"):
    print(filename)
    dataset = Dataset(filename, sample_type)
    
    if results == "":
        help_list = filename.split("\\")
        res_path = "\\".join(help_list[:-4]) + "\\Results\\" + dataset.name
    else: res_path = results + "\\" + dataset.name
        
    #make a folder for each file
    if os.path.isdir(res_path) == False:
        os.mkdir(res_path)
    
    #write to appendix
    if app_file:
        new_chapter_appendix(dataset_name = dataset.name, df = df , app_file = app_file)
        
    res_file = write_result(dataset,df,res_file)
    save_df(os.path.dirname(res_path),"result",res_file)

    dataset.make_graphs(res_path, app_file)
                        
def make_result_file(results):
    index = ["Name", "Number", "Energy level", "Thickness", "Drop weight", "Drop height", "Age", "Velocity", "Force", "Acceleration", "Deformation", "Broken/Cracked"] #, "Crack area", "Opening angle"]    
    data =  [short_unit[i] for i in index]
    res = pd.DataFrame(index = index, data = data)
    res = res.transpose()
    res = res.set_index("Name")
    res_path = results + r"\result.xlsx"
    res.to_excel(res_path)
    
def make_appendix_file(results):
    #open appendix file
    app_path = results + r"\appendix.tex"
    app = open(app_path,"w")
    #write appendix
    #app.write("\includepdf[pages=-]{appendix/lacing.pdf}\n\n")
    # app.write("\chapter{TSL}\n\n\includepdf[pages=-]{appendix/TSL.pdf}\n\n")
    return app
    
def iterate_single(direct, results, df, app_file):  
    file_list = make_file_list(direct, "npy")
    for i in file_list:
        if os.path.basename(i)[:-4] in df.index: 
            res_file = open_df(results, "result")
            calc_single_file(i,results,df,res_file,app_file, sample_type = df.at[os.path.basename(i)[:-4],"Sample type"])
    if app_file:
        app_file.close()

def find_folder(path, folder_name):
    #crawl a folder and return the path of the folder you are looking for:
    for root, folders, files in os.walk(path):
        for folder in folders:
            if folder.lower() == folder_name.lower():
                return os.path.join(root,folder)
    raise NoFolderError(folder_name, path)

#try which format the cell has
def table_format(c):
    cell = str(c)
    if cell == "":
        return np.nan
    cell = cell.replace(",",".")
    try:
        return int(cell)
    except:
        if "." in cell:
            return float(cell)
    return cell
    
def make_file_list(direct, extension = ""):
    file_list = []
    for root, folders, files in os.walk(direct):
        for file in files:
            path = os.path.join(root, file)
            if os.path.isfile(path) and (extension == "" or file[-len(extension):].lower() == extension):
                file_list.append(path)
    return file_list

def open_df(data, filename = "test_data"):
    '''looks for the .xlsx AND .csv file with the name "filename" in the folder "data"
    always prioritises .xlsx files
    uses some dynamic recasting to confuse the reader, the paths are first set as booleans and if no file is found they stay booleans
    '''
    excel_path, csv_path = False, False
    
    xlsx_list = make_file_list(data, extension = "xlsx")
    for i in xlsx_list:
        if os.path.basename(i).lower() == filename + ".xlsx":
            excel_path = i
            break
        
    csv_list = make_file_list(data, extension = "csv")
    for j in csv_list:
        if os.path.basename(j).lower() == filename + ".csv":
            csv_path = j
            break
        
    if excel_path:
        help_table = pd.read_excel(excel_path, header = 0, index_col = "Name")
        table_dtype = {}
        for i in help_table.columns:
            table_dtype[i] = table_format
        table = pd.read_excel(excel_path, header = 0, index_col = "Name", converters = table_dtype)
    elif csv_path:
        help_table = pd.read_csv(csv_path, sep = ";", header = 0, index_col = "Name")
        table_dtype = {}
        for i in help_table.columns:
            table_dtype[i] = table_format
        table = pd.read_csv(csv_path, sep = ";", header = 0, index_col = "Name", converters = table_dtype)
    else:
        raise NameError("No " + filename + " file available!")
        
    for i in table.index:
        if i == np.NaN or i == "" or i == " " or i == 0 or i == "0":
            table = table.drop(i, axis = 0)
    return table

def save_df(data, filename, df):
    '''tries to save a df'''
    excel_path, csv_path = False, False
    xlsx_list = make_file_list(data, extension = "xlsx")
    for i in xlsx_list:
        if os.path.basename(i).lower() == filename + ".xlsx":
            excel_path = i
            break
    csv_list = make_file_list(data, extension = "csv")
    for j in csv_list:
        if os.path.basename(j).lower() == filename + ".csv":
            csv_path = j
            break
    if excel_path:
        df.to_excel(excel_path, index_label = "Name")
        # open and close the file again so it looks nice
        df_new = open_df(data, filename)
        df_new.to_excel(excel_path)
    elif csv_path:
        df.to_csv(csv_path, sep = ";")
    else:
        raise NameError("No " + filename + " file available!")
    return

def make_meta_path(data):
    path = os.path.split(data)
    meta_path = os.path.join(path,'metadata')
    return meta_path
    
    
#write everything important to the result file        
def write_result(dataset,df,res_file):
#make a list to add each individual line
    text = []  

    #legend
    add_list(text,df.loc[dataset.name,"Number"])
        
    #energy leve
    weig = df.loc[dataset.name,"Drop weight"]
    heig = df.loc[dataset.name, "Drop height"]
    add_list(text,energy(heig,weig),2) 

    #thickness
    add_list(text,df.loc[dataset.name,"Thickness"])
    
    #drop weight
    add_list(text,weig,0)

    #drop height
    add_list(text,heig,1)

    #age
    add_list(text,df.loc[dataset.name,"Age"])  

    #velocity
    #theoretic, just needs drop height
    add_list(text,theoryVelo(heig),1)

    #TO DO calculated velocity
    #needs array and some reworking /take just a tiny snip of the accel array

    #load sum
    add_list(text,filtered_peak(dataset.loadsum),2)

    #peak accel
    add_list(text,filtered_peak(dataset.accel),2)

    # #peak deformation
    # deform = filtered_peak(-dataset.laser)
    # add_list(text,deform,1)
    
    #highspeed camera
    text.append(df.loc[dataset.name, "Deformation"])
    
#    broken or cracked?s
    if df.loc[dataset.name,"Broken/cracked"].lower() == "broken":
        add_list(text,"broken")
    else:
        add_list(text,"cracked")
        
    # irrelevant for square samples
    #     #if broken just add nan

    #     text.append("")
    #     text.append("")
    # else:
    #     #if cracked add damage mapping
    #     add_list(text,"cracked")
    #     add_list(text,df.loc[dataset.name,"Crack area"])
    #     add_list(text,df.loc[dataset.name,"Opening angle"],1)
    series =pd.Series(data = text, name = dataset.name, index = res_file.columns)
    res_file = res_file.append(series)
    return res_file
    
def new_chapter_appendix(app_file,df,dataset_name):
    app_file.write("\\chapter{" + dataset_name.replace("_","\_") + "}\n\n")
    # add Picture into appendix
    pic_path =".\\appendix\\" + dataset_name + ".jpg"
    #if df.loc[dataset_name,"Broken/cracked"] == "cracked":
     #   write_appendix(app_file,pic_path,"Picture of the sample after the test")

    #calculate exra accelerometer    
def calc_extra_accel():
    return "zero"
  
    #help function, makes it easier to add to a list
def add_list(lst,thing,rnd=0):
    if isinstance(thing,float):
        lst.append(str(np.round(thing,rnd)))        
    else:
        lst.append(str(thing))
        
def set_limit(limit):
    bottom,top = plt.ylim()
    if bottom < limit[0] and limit[0] != -1:
        plt.ylim(bottom = limit[0])
    if top > limit[1]  and limit[1] != -1:
        plt.ylim(top = limit[1])

# plot(res_path,x = self.load_time, y = self.load[:,i-1] ,xlabel= r"Time \([\text{s}]\)",ylabel=r"Load \([\text{kN}]\)", name="Loadcell_" + str(i),appendix = app, dataset_name = self.name)
        
    #    plot sum of all loadcells
        # plot(res_path,x = self.load_time, y = self.loadsum ,xlabel= r"Time \([\text{s}]\)",ylabel=r"Load \([\text{kN}]\)", name="Loadcell_sum",appendix = app, dataset_name = self.name)
    

def plot_load(direct,x,load, loadsum, limit=(-1,-1),xlabel="",ylabel="",name="", appendix = False, dataset_name = ""):
    for i in range(4):
        plt.plot(x,sig.medfilt(load[:,i]), label = name[i])
    plt.plot(x, sig.medfilt(loadsum), label = "load cell sum")
    set_limit(limit)
    plt.grid()
    plt.ylabel(ylabel, usetex= True)
    plt.xlabel(xlabel, usetex= True)
    plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.75), ncol=1)
    fig_path = direct + "\\load.png"
    plt.savefig(fig_path, bbox_inches='tight')
    plt.close()
    if appendix != False:
        write_appendix(appendix, ".\\appendix\\" + dataset_name + "\\" + "load.png", "load")
        
def plot(direct,x,y,limit=(-1,-1),xlabel="",ylabel="",name="", appendix = False, dataset_name = ""):
    plt.plot(x,sig.medfilt(y))
    set_limit(limit)
    plt.grid()
    plt.ylabel(ylabel, usetex= True)
    plt.xlabel(xlabel, usetex= True)
    fig_path = direct + "\\" + name + ".png"
    plt.savefig(fig_path)
    plt.close()
    if appendix != False:
        write_appendix(appendix, ".\\appendix\\" + dataset_name + "\\" + name + ".png", name)


def find_start(array, index = 6, cushion=500):
    # dx = 0.1
    # derivate = np.diff(array[:,index])/dx
    # peaks = sp.signal.find_peaks(derivate)
    
    # new solution
    # make a derivate
    # look at the peaks of the derivate
    # where most peaks are, is our start
    
    ### old solution
    # after the magnetventil opens look for peaks
    x = np.where(array[:,index]==1)
    dx = 0.1
    derivate = np.diff(array)/dx
    a = np.argmin(derivate[x[0][0]:],axis=0)
    # a = np.argmax(array[x[0][0]:],axis=0)
    c=[]
    for i in range(1,4):
# # just the load cells        
        c.append(a[i])
    return(int(math.floor(stat.median(c)) - cushion + x[0][0]))

def calc_scope(array,index):
    start_load = find_start(array, index, cushion=3000)
    
    # #if the program cannot find a start, just start from the beginning and end at the end
    # if start_load is None:    
    #     start_load = 0
    #     start_accel = 0
    #     start_laser = 0
    #     end_accel = array.shape[1]
    #     end_load = array.shape[1]
    #     end_laser = array.shape[1]
    #     return start_accel, end_accel, start_load, end_load, start_laser, end_laser
    
    start_accel = start_load
    start_laser = start_load
    #
    len_accel = 10000
    len_load = 10000
    len_laser = 2000
    
    end_accel = start_accel + len_accel
    end_load = start_load + len_load
    end_laser = start_laser + len_laser
    
    return start_accel, end_accel, start_load, end_load, start_laser, end_laser
        
def load_displacement_curve(file="C:\\Users\\kekaun\\OneDrive - LKAB\\roundSamples\\Data\\cracked\\2018-12-04_Rfrs_50_0,3_2.npy"):
    pot=0.74
    array = np.load(file)
    load =  sig.medfilt(array[:,1] + array[:,2] + array[:,3])
    star = find_start(array,cushion=20)
    c,d = 0,(0,0)
    length = np.argmin(array[star:star+400,4])
    
    for b in range(0,100):
        for a in range(0,100):
            startload = star + a
            startdisp = star + b
            endload = startload + length
            enddisp = startdisp + length
            disp = - sig.medfilt(array[startdisp:enddisp,4])
            loa = load[startload:endload]            
            energy = sp.integrate.trapz(loa,disp) / 1000
            if c < energy:
                c = energy
                d = (a,b)
    print(c)
    print(d)
    startload = star + d[0] + 1
    startdisp = star + d[1] + 4
    endload = startload + length
    enddisp = startdisp + length
    disp = - sig.medfilt(array[startdisp:enddisp,4])
    loa = load[startload:endload]

    plt.plot(disp, label="Displacement")
    plt.xlabel("Time [$ms$]")
    plt.plot(loa, label="Load")
    plt.title("Load and displacement CLIPPED")
    plt.ylabel("Force [$kN$] / Displacement [$mm$]")
    plt.grid()
    plt.legend()
    plt.show()
    plt.savefig("C:\\Users\\kekaun\\OneDrive - LKAB\\roundSamples\\Results\\" + os.path.basename(file)[:-4] + "_load_displacement.png")
    plt.close()
    plt.grid()

    plt.plot(disp,loa, label=("absorbed energy = %0.03f \n potential energy = %0.03f")%(c,pot))
    plt.legend()
    plt.ylim(bottom = 0)
    plt.xlim(left = 0)
#    plt.title("Energy CLIPPED")
    plt.ylabel("Force [$kN$]")
    plt.xlabel("Displacement [$mm$]")

    plt.savefig("C:\\Users\\kekaun\\OneDrive - LKAB\\roundSamples\\Results\\" + os.path.basename(file)[:-4] + "_energy.png")
    plt.close()
  
#get peak of anything, input: sliced array, uses a medium filter
    
def filtered_peak(array):
    index = np.argmax(sig.medfilt(array))
    return (array[index])

#get peak of anything, unfiltered
def true_peak(array):
    index = np.argmax(array)
    return (array[index])

# impact energy from dropheight and drop weight
def energy(height,weight):
    g = 9.8
    return float(height) * int(weight) * g / 10**3
    
# get thickness
def thickness(filename):
    regex = re.compile(r"\_\d*\_")
    mo = regex.search(filename)
    try:
        x = mo.group()
        return x.strip("\_")
    except:
        return "thickness"

#calc velo from height
def theoryVelo(height):
    height = math.sqrt(height ** 2)
    return math.sqrt(2*height*9.8/1000)

def broken(path):
    if os.path.dirname(path)[-1] == "n":
        return 1
    else: 
        return 0

def list_ex_include(length):
    return [ex_in_clude] * length

def ex_in_clude(boolean):
    if boolean == True:
        return ""
    else:
        return "faulty"


def draw_diagrams(metadata = r"C:\Users\kekaun\OneDrive - LKAB\Desktop\Fake", results = r"C:\Users\kekaun\OneDrive - LKAB\Desktop\Fake", df = ""):
    #if df is not open yet, open it
    if isinstance(df, str):
        df = open_df(metadata, "test_data")
    
    res_df = open_df(results, "result")
    res_df = res_df.drop(res_df.index[0])

    #make latex tables
    make_tables(res_df, results)
    
    #make dir to save stuff
    path = results + "\\diagram"
    if os.path.isdir(path) == False:
        os.makedirs(path)
            
    #throw useless info away
    res_df = res_df.drop(['Broken/Cracked',"Drop weight","Drop height","Velocity","Number"],axis = 1)

    
    #correlation dataframe
    corr = pd.DataFrame(index = res_df.columns, columns = res_df.columns, dtype = float)
    
    mask = make_mask(metadata, results, res_df.index, res_df)
    
    #compare impact force to force at the load cells
    compare_force(metadata, results, df, res_df, mask)
      
    #draw all the silly graphics    
    for j in res_df.columns:
        for i in res_df.columns:
            plot_correlation(i, j, mask, res_df, corr, df, path)
    
    #throw away empty columns
    corr = corr[(corr != 0).any()]
    corr = corr.loc[:, (corr != 0).any(axis=0)]

    #draw a heatmap
    heatmap(corr, results)
    
def compare_force(metadata = r"C:\Users\kunge\Downloads\KIRUNA\Tests\welded\single\metadata", results = r"C:\Users\kunge\Downloads\KIRUNA\Tests\welded\single\results", df = None, res_df = None, mask = None):
    i = 'Acceleration'
    j = 'Force'
    if df is None:
        df = open_df(metadata, "test_data")
    if res_df is None:
        res_df = open_df(results, "result")
        res_df = res_df.drop(res_df.index[0])
    if mask is None:
        mask = make_mask(direct = metadata, results = results, index = df.index, res_df = res_df)

    ax = plt.subplot(111)
    impact = res_df[i] * df['Drop weight'] *0.001
    loadcell = res_df[j]
    ##make submask
    exclude, broken, cracked = make_submask(i, j, mask, index = df.index ,df = df)
    print(["loadcell\n",loadcell])
    print(["impact\n",impact])
    ax.plot(impact, loadcell, "b.", label = "Measured \nvalues")
    cr_impact = impact
    cr_loadcell = loadcell
    # ax.plot(ex_impact, ex_loadcell,"xk", label = "excluded")  
    
    # # ex_impact = impact[exclude]
    # cr_impact = impact[cracked]
    # br_impact = impact[broken] 
    
    # # ex_loadcell = loadcell[exclude]
    # cr_loadcell = loadcell[cracked]
    # br_loadcell = loadcell[broken]
    
    # mpl.rcParams["figure.figsize"] = (10,7)

    # ax.plot(cr_impact, cr_loadcell, "b.",label="cracked")
    # ax.plot(br_impact, br_loadcell, "r.", label = "broken")
    # ax.plot(ex_impact, ex_loadcell,"xk", label = "excluded")       
    #
    # make limits nice
    # xlim = ax.get_xlim()
    # ax.set_xlim((xlim[0] - 0.05 * xlim[0],xlim[1]+ 0.05 * xlim[1]))
    # ylim = ax.get_ylim()
    # ax.set_ylim((ylim[0] - 0.05 * ylim[0], ylim[1] + 0.05 * ylim[1]))
    #            
    #labels
    ax.set_xlabel(r"Impact force \([\text{kN}]\)", usetex = True, fontsize = 14)
    ax.set_ylabel(r"Loadcell force \([\text{kN}]\)", usetex = True, fontsize = 14)
    #
    #grid
    plt.grid()
    #
    ##linear interpolation
    # if not cr_impact.empty or not cr_loadcell.empty:
        # slope, intercept, r_value, p_value, std_err = sp.stats.linregress(cr_impact.astype(float),cr_loadcell.astype(float))
        # sortx = list(cr_impact.astype(float).sort_values())
        # sorty =[]
        # for m in sortx:
        #     sorty.append(m * slope + intercept)
        # ax.plot(sortx, sorty, 'b--', label="Linear \ncorrelation \n$R^2$ = %0.04f \n x = %0.04f \n y = %0.04f" %(r_value**2,slope,intercept))
    
    ##draw the idealized line
    max_value1 = impact.max()
    max_value2 = loadcell.max()
    if max_value1 > max_value2:
        max_value = max_value1
    else:
        max_value = max_value2
        
    linear = [0,max_value]
    ax.plot(linear, linear,  linestyle = ":", color = "b", linewidth = "0.5" ,label = 'Theoretical \ncorrelation')
    
    Number = df['Number']
    try:
        Number = Number.astype(int)
    except:
        Number = Number.astype(str)    
    
    #write numbers next to points             
    texts = [plt.text(impact.loc[k],loadcell.loc[k],Number.loc[k]) for k in res_df.index]  
    adjust_text(texts)
    
    #
    #legend            
    chartBox = ax.get_position()            
    ax.set_position([chartBox.x0, chartBox.y0, chartBox.width*0.8, chartBox.height])
    ax.legend(loc='center left', bbox_to_anchor=(1.0, 0.75), ncol=1,fontsize = 14)
    #
    ##save
    filename = results + r"\compare_impact_loadcell_force.png"
    plt.savefig(filename)
    plt.close()
    
def remove_slash(df):
    new_index = [i.replace('\\', '') for i in df.index]
    df.index = new_index
    return df

def add_slash(df):
    #check if there is \_ and leave those alone
    #check if there is _ and change to \_
    new_index = []
    for i in df.index:
        if type(i) is str:
            if '\\_' in i:
                new_index.append(i)
            elif '_' in i:
                i.replace('_', '\\_')
                new_index.append(i)
        else:
            new_index.append(i)
    df.index = new_index
    return df

def plot_correlation(i, j, mask, res, corr, df, path):
     #begin plot
    ax = plt.subplot(111)
    
    #make submask
    exclude, broken, cracked = make_submask(i, j, mask, index = df.index ,df = df)
    exclude = res[exclude]
    crack = res[cracked]
    broke = res[broken]

    mpl.rcParams["figure.figsize"] = (10,7)
    ax.plot(crack[i], crack[j], "b.",label="cracked")
    ax.plot(broke[i], broke[j], "r.", label = "broken")  
    
    #make limits nice
    xlim = ax.get_xlim()
    ax.set_xlim((xlim[0] - 0.05 * xlim[0],xlim[1]+ 0.05 * xlim[1]))
    ylim = ax.get_ylim()
    ax.set_ylim((ylim[0] - 0.05 * ylim[0], ylim[1] + 0.05 * ylim[1]))
    
    #plot excluded data later to keep outliers out of the graphs
    ax.plot(exclude[i],exclude[j],"xk", label = "excluded")     
                
    #labels
    ax.set_xlabel(i + " " + latex_unit[i], usetex = True, fontsize = 14)
    ax.set_ylabel(j + " " + latex_unit[j], usetex = True, fontsize = 14)
    
    #grid
    plt.grid()
    
    #linear interpolation (if there are values for it)
    if crack[i].empty or crack[j].empty:
        corr[i][j] = 0
        corr[j][i] = 0
        print("HELP! NO VALUES!")
    else:
        slope, intercept, r_value, p_value, std_err = sp.stats.linregress(crack[i].astype(float),crack[j].astype(float))
        sortx = list(crack[i].astype(float).sort_values())
        sorty =[]
        for m in sortx:
            sorty.append(m * slope + intercept)
        ax.plot(sortx, sorty,"b--", label="$R^2$ = %0.02f \nx = %0.04f \ny = %0.04f" %(r_value**2,slope,intercept))
        corr[i][j] = r_value**2
        corr[j][i] = r_value**2
        
    Number = df['Number']
    try:
        Number = Number.astype(int)
    except:
        Number = Number.astype(str) 
        
#    #write numbers next to points             
    texts = [plt.text(res.at[k,i],res.at[k,j],Number.loc[k]) for k in res.index]  
    adjust_text(texts)

    #legend            
    chartBox = ax.get_position()            
    ax.set_position([chartBox.x0, chartBox.y0, chartBox.width*0.8, chartBox.height])
    ax.legend(loc='center left', bbox_to_anchor=(1.0, 0.75), ncol=1,fontsize = 14)

    #save
    filename = path + "\\" + j.replace(" ","-") + "_" + i.replace(" ","-") + ".png"
    plt.savefig(filename)
    plt.close()
    
def make_latex_table(df, path):
    index = ["Name"] + df.columns.tolist()
    data =  [latex_unit[i] for i in index]
    res = pd.DataFrame(index = index, data = data)
    res = res.transpose()
    res = res.set_index("Name")
    res = res.append(df)
    ## format latex table
    form = column_format(len(df.columns) + 1)
    ## format numbers with thousand separator . and decimal separator ,
    decimal = [number_format] * len(df.columns)
#    df  = add_slash(df)
    res.to_latex(path, na_rep="", formatters = decimal, column_format = form, escape=False)
    
#make a latex table out of the .csv       
def make_tables(df,res_path):
        #make dir to save stuff
    path = os.path.join(res_path, "tables")
    if os.path.isdir(path) == False:
        os.makedirs(path)    
    #result file
    res = df.sort_values(by = 'Number', axis = 'index')    
    make_latex_table(res, path + "\\result.tex")
    
    #test_values
    test_values = res[["Number","Energy level", "Thickness", "Drop weight", "Drop height", "Age"]]
    make_latex_table(test_values, path + "\\test_values.tex")
    
    #short_result
    short_result = res[["Number", "Force", "Acceleration", "Deformation"]]
    make_latex_table(short_result, path + "\\short_result.tex")
    
    #just cracks
    crack = res[res["Broken/Cracked"] == "cracked"]
    crack =  crack.drop(["Broken/Cracked"], axis=1)
    make_latex_table(crack, path + "\\crack.tex")
    
    #legend
    write_legend(res_path,df.iloc[1:]["Number"])
    
def make_mask(direct, results, index, res_df):
   #make a mask to filter out everything that is useless
   #if there is no exclude file just make a mask that is all True
    try:
        mask = open_df(direct,"exclude")
    except:
        print("Cannot find the exclude database!")
        shape = (len(index),5)
        dummy_data = np.zeros(shape = shape)
        columns = ["Loadcells","Accelerometer","Laser sensor",	"Cracks",	"High speed camera"]#, "Additional accelerometer vertical","Additional accelerometer horizontal"]
        mask = pd.DataFrame(data = dummy_data, index = index, columns = columns)
    mask = mask.astype(bool)

#    mask to latex
    path = os.path.join(results, 'tables')
    print(path)
    if os.path.isdir(path) == False:
        os.makedirs(path)  

    ##use if there is extra accel data
#    excl_accl = mask[["Additional accelerometer vertical","Additional accelerometer horizontal"]]    
#    excl_accl_format = [ex_in_clude] * len(excl_accl.columns)
#    excl_accl.to_latex(os.path.join(path, "exclude.tex"),formatters = excl_accl_format, escape = False,na_rep=" ")
    # exclude_table = mask.drop(["Additional accelerometer vertical","Additional accelerometer horizontal"], axis = 1)
    # excl_format = [ex_in_clude] * len(exclude_table.columns)
    # exclude_table.to_latex(os.path.join(path, "exclude.tex"),formatters = excl_format, escape = False,na_rep="")

#make a pretty mask#
    #rename columns
    new_columns={
    'Loadcells' : 'Force',
     'Accelerometer' : 'Acceleration',
     'Laser sensor' : 'Deformation',
     }
    mask = mask.rename(columns = new_columns)
    new_data = [True] * len(index)
      
    res_df = res_df.drop(res_df.index[0])
    
    #add the remaining columns as true                    
    for j in res_df.columns:
        if j not in mask.columns:
            mask.insert(loc = 0, column = j, value = new_data)

    check = res_df.isna()
    mask[check] = False
    return mask    
    
def make_submask(i, j, mask,index, df):
    if i not in mask.columns and j not in mask.columns:
        #if the data is not in the exlusion table just make a totally true mask
        #otherwise check if only one value is in there
        #lastly if both values are on the list, make a mixed list
        data = [True] * len(index)
        submask = pd.Series(data, index = index, dtype = bool, name = 'Name')
    elif i in mask.columns and j not in mask.columns:
        submask = mask[i]
    elif i not in mask.columns and j in mask.columns:
        submask = mask[j]
    else:
        submask = mask[i] & mask[j]
    exclude = ~submask
    broken_data = []
    for i in index:
        if df.loc[i,"Broken/cracked"] == "broken":
            broken_data.append(True)
        else:
            broken_data.append(False)
    broken = pd.Series(broken_data, index = index, dtype = bool, name = 'Name')
    cracked = ~broken
    broken = broken & submask
    cracked = cracked & submask
    print(broken)
    return exclude, broken, cracked
    
#make a string to format latex
def column_format(number):
    help_list = ["l"] * number
    return " ".join(help_list)
    
# format numbers with thousand separator . and decimal separator ,
def number_format(number):
    if number == 0:
        return ""
    if type(number) == str:
        return number
    else:
        return "{:n}".format(number)
        
#write something in the appendix
def write_appendix(appendix,pic_path,caption):
    appendix.write("""\\begin{figure}
    \\centering
    \\includegraphics[width=0.9\\linewidth]{""" + pic_path.replace(os.sep, '/') + """}
    \\caption{""" + caption.capitalize().replace("_"," ") + """}
    \\label{fig:""" + os.path.dirname(pic_path).split("\\")[-1] + "_" + caption +  """}
    \\end{figure}\n\n""")     

def fix_time(array):
    array[0][0]=0
    for i in range(1,array.shape[0]):
        array[i][0] = array[i-1][0] + 0.0001
    return array

def xls_to_df(excel=r'C:\Users\kekaun\OneDrive - LKAB\roundSamples\test_data.xlsx',filename="2019-02-20_Rfs_100_0,5"):
    data = pd.ExcelFile(excel)
    array = data.parse(index_col ="Name")
    first = array.loc[filename]
    return(first)
    
#writes a legend
def write_legend(direct,df):
    df = add_slash(df)
    leg = open(direct + "\\tables\\legend.tex","w")
    leg.write("""\\begin{table}
    \\centering
    \\begin{tabular}{ll}""" + 
    df.to_latex(escape = False, float_format = str) +
"""\\caption{Legend for the symbols assigned to tests}
\\label{tab:leg}
\\end{table}
              """)
    leg.close()
# some online code
def make_zero(start,end):
    length = end - start
    helper = np.empty(length)
    helper[:] = np.nan
    return helper
    
def nan_helper(y):
  return np.isnan(y), lambda z: z.nonzero()[0]

def fix_disp(file=r"C:\Users\kekaun\OneDrive - LKAB\roundSamples\Data\cracked\2018-12-10_Rfrs_100_1,5.npy"):
#open array
    array = np.load(file)

    start = find_start(array,cushion=500)
    end = start + 2500
    y = array[:,4]
#
#
##    # fix the first part
    start1 = start + 1670
    end1 = end - 375
    y[start1:end1] = make_zero(start1,end1)

##    
#    start2 = start + 1250
#    end2 = end - 190
#    y[start2:end2] = make_zero(start2,end2)
#    
#    start3 = start + 1075
#    end3 = end - 345
#    y[start3:end3] = make_zero(start3,end3)
#    
#    start4 = start + 1440
#    end4 = end - 30
#    y[start4:end4] = make_zero(start4,end4)
##    len2 = end2 - start2
##    helper2 = np.empty(len2)
##    helper2[:] = np.nan
##    y[1030:1030+len2] = helper2
#
##    start1 = start + 800
##    end1 = end - 50
##    
#    for i in range(1500):
#        if y[i] < - 14.3:
#            y[i] = np.nan
#    
##    start1 = start + 800
    nans, x= nan_helper(y)
    y[nans] = np.interp(x(nans), x(~nans), y[~nans])
    array[start:end,4] = y[start:end]
    
    y = sig.medfilt(array[start:end,4])
    x = array[start:end,0]
    
    y1 = sig.medfilt(array[start1:end1,4])
    x1 = array[start1:end1,0]
    
    plt.grid()
    plt.plot(x,y)
    plt.plot(x1,y1)
    np.save(file[:-4] + "_fix.npy",array)
    
def heatmap(df,direct):
    #colormap
    blackoutside = {
            'blue':  ((0.0, 0.0, 0.0),
                    (0.3, 0.0, 0.0),
                     (0.5, 1.0, 1.0),
                     (0.7, 1.0, 1.0),
                     (1.0, 0.0, 0.0)),
                     
            'green': ((0.0, 0.0, 0.0),
                      (0.3, 0.0, 0.0),
                      (0.5, 1.0, 1.0),
                      (0.7, 0.0, 0.0),
                      (1.0, 0.0, 0.0)),
    
            'red': ((0.0, 0.0, 0.0),
                     (0.3, 1.0, 1.0),
                     (0.5, 1.0, 1.0),
                     (0.7, 0.0, 0.0),
                     (1.0, 0.0, 0.0))}
            
    plt.register_cmap(name='LKAB', data=blackoutside)
    #sort index and colums
    df = df.sort_index(axis = 0)
    df = df.sort_index(axis = 1)
    
    sns_plot = sns.heatmap(df,  center = 0, annot=True, fmt='.2f',cmap = "LKAB", vmin = 0.0, vmax = 1.00,)
    plt.tight_layout()
    fig = sns_plot.get_figure()
    fig.savefig(direct + r"\heatmap.png")
    plt.close()
    
def helpline(start,end,offset,array):
    hline = np.ones((end-start,))
    for i in range(end-start):
        hline[i] = offset * i / (end - start)
    for j in range(start,end):
        array[j] = array[j] + hline[j - start]
    return array


def extra_accel(file="C:\\Users\\kekaun\\OneDrive - LKAB\\roundSamples\\extraAccel\\2019-02-20_Rfrs_100_0,5_vertical.npy"):
    mpl.rcParams["figure.figsize"] = (8,5)
    array = np.load(file)
    peak = np.argmax(array[:,1])
    
    ##off set coordinates
    #for 2019-04-16_Rfrs_75_0,5_horizontal and vertical
    #start = peak - 10
    #end = peak + 150
    #hstart = peak - 5 - start
    #hend = peak + 80 - start
    
    #for 2019-02-20_Rfrs_100_1,0_vertical
    #start = peak - 25
    #end = peak + 500
    #hstart = peak - 20 - start
    #hend = peak + 185 - start
    
    #for 2019-02-20_Rfrs_100_0,5_vertical
    start = peak - 25
    end = peak + 200
    hstart = peak - 20 - start
    hend = peak + 170 - start
    
    time = array[start:end,0]
    accel = array[start:end,1]
    
    velo = integrate.cumtrapz(accel,x = time,initial = 0)
    hine = helpline(hstart,hend,-0.15,velo)
    hine[hend:] = sig.detrend(hine[hend:])
    
    disp = integrate.cumtrapz(hine,initial = 0)
    #disp = integrate.cumtrapz(velo,initial = 0)
    
    
    
    # ACCEL
    plt.plot(time,accel)
    plt.xlabel("Time [s]")
    plt.ylabel(r"Acceleration \Big[\(\frac{\text{m}}{\text{s}^2}\)\Big]", usetex=True)
    plt.grid()
    plt.savefig(file[:-4] + "_acceleration.png")
    plt.close()
    
    # VELOCITY
    
    plt.plot(time,velo)
    #plt.plot(time,hine)
    plt.grid()
    plt.xlabel("Time [s]")
    plt.ylabel(r"Velocity \big[\(\frac{\text{m}}{\text{s}}\)\big]", usetex=True)
    plt.savefig(file[:-4] + "_velocity.png")
    plt.close()
    #
    ### DISPLACEMENT
    plt.plot(time,disp)
    plt.xlabel("Time [s]")
    plt.ylabel(r"Displacement [mm]")
    plt.grid()
    plt.savefig(file[:-4] + "_displacement.png")
    plt.close()
    
def replace_(string):
    if type(string) == str:
        string = string.replace("_","\_")
    return string

def compare_vel_disp():
    result = pd.read_csv(r"C:\Users\kekaun\OneDrive - LKAB\roundSamples\Results\result.csv",sep=";",index_col = 0)
    base = np.zeros((len(result.index),4))
    vel_disp_compare = pd.DataFrame(data = base, index = result.index, columns = ["Calculated velocity", "Measured velocity", "Laser displacement", "Accelerometer displacement"])
    for i in result.index:
        path = "C:\\Users\\kekaun\\OneDrive - LKAB\\roundSamples\\Data\cracked\\" + i.replace(r"\_","_") + ".npy"
    if os.path.isfile(path):        
        array = np.load(path)
        
        start = find_start(array,cushion=500)
        
        lenAccel = 1500
        
        accel = sig.medfilt(array[start:start+lenAccel,5])
        x = array[start:start+lenAccel,0]
        
        velo = integrate.cumtrapz(accel,x,initial = 0)
        mes_vel = filtered_peak(velo)        
        
        disp = integrate.cumtrapz(velo,x,initial = 0)
        mes_disp = filtered_peak(disp)
        
        vel_disp_compare["Measured velocity"].loc[i] = np.round(mes_vel,1)
        vel_disp_compare["Calculated velocity"].loc[i] = result["Velocity"].loc[i]
        vel_disp_compare["Laser displacement"].loc[i] = result["Displacement"].loc[i]
        vel_disp_compare["Accelerometer displacement"].loc[i] = np.round(mes_disp*100,2)        
        
    else: vel_disp_compare.drop(index = i,inplace = True)

    vel_disp_compare.to_latex("C:\\Users\\kekaun\\OneDrive - LKAB\\roundSamples\\Results\\compare.tex", escape = False)
    
def clean_dir(in_dir = r'C:\Users\kunge\Downloads\KIRUNA\Tests\welded\single\rawdata', out_dir=r'C:\Users\kunge\Downloads\KIRUNA\Tests\welded\single\single_impact', sample_type = "square"):
    """cleans a bunch of files in in_dir at once and saves them in at out_dir as .npy"""    
    file_list = make_file_list(in_dir, "asc")
    for i in file_list:
        out_file = os.path.join(out_dir, os.path.basename(i)[:-4] + '.npy')
        print(out_file)
        clean.clean_array(i, out_file, sample_type)
    
class NoFolderError(Exception):
    '''raise an error when a folder cannot be found'''
    def __init__(self, folder, directory):

        # Call the base class constructor with the parameters it needs
        super(NoFolderError, self).__init__('The folder {} could not be found in {}'.format(folder, directory))
        
def make_latex_input(dir = r"C:\Users\kunge\ownCloud\Work\documents\old", subdir = r"./documents/old/"):
    # takes all the files in a folder and creates input statements for latex
    # dir is the folder of the documents
    # subdir is the relative path from the main file to the subfile
    for root, folders, files in os.walk(dir):
            for file in files:
                print(r"\input{" + subdir + file[:-4] + "}" + "\n\n")
                
def make_test_data(test_file_directory=r'C:\Users\kunge\Downloads', output_directory=r'C:\Users\kunge\Downloads'):
    '''make an appropriate excel file for data analysis'''
    file_path = os.path.join(output_directory, 'test_data.xlsx')
    if os.path.isfile(file_path):
        print("File already exists!")
    else:
        column_list = ["Number", "Sample type", "Casting date", "Test date", "Age", "Drop weight", "Drop height", "Thickness", r"Broken/cracked", "Deformation"]
        file_list =  make_file_list(test_file_directory, 'npy')
        index = []
        for i in file_list:
            index.append(os.path.basename(i)[:-4])
        df = pd.DataFrame(columns=column_list, index = index)
        df.to_excel(file_path, index_label = 'Name')

def make_exclude(test_file_directory=r'C:\Users\kunge\Downloads\KIRUNA\Tests\SINGLE', output_directory=r'C:\Users\kunge\Downloads\KIRUNA\Tests\SINGLE\metadata'):
    file_path = os.path.join(output_directory, 'exclude.xlsx')
    if os.path.isfile(file_path):
        print("File already exists!")
    else:
        column_list = ["Acceleration", "Velocity", "Deformation"]
        file_list =  make_file_list(test_file_directory, 'npy')
        index = []
        for i in file_list:
            index.append(os.path.basename(i)[:-4])
        df = pd.DataFrame(columns=column_list, index = index, dtype = bool)
        df.to_excel(file_path, index_label = 'Name')
