#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 15:33:33 2019

@author: KEKAUN
"""

import numpy as np
import statistics as stat
import matplotlib as mpl
#make all plots look nice
mpl.style.use('classic')

import matplotlib.pyplot as plt

import scipy as sp
import scipy.signal as sig
import scipy.integrate as integrate

import seaborn as sns
import math

import os
import re
import pandas as pd
from adjustText import adjust_text
import locale
locale.setlocale(locale.LC_ALL, 'deu_deu')
import PySimpleGUI as sg

import clean_file as clean
#rc('text', usetex=True)

#rc('text.latex', preamble=r'\usepackage{helvet}\renewcommand\familydefault{\sfdefault}')
mpl.rcParams['text.latex.preamble'] = [r'\usepackage{helvet}\renewcommand\familydefault{\sfdefault}', r'\usepackage{amsmath}' , r'\usepackage[T1]{fontenc}'] 

#"fix" matplotlib font - it´s arial instead of helvetica but better than nothing
#plt.rcParams['mathtext.fontset'] = 'custom'
mpl.rcParams['font.sans-serif'] = "Arial"
mpl.rcParams['font.family'] = "sans-serif"
mpl.rcParams['mathtext.default']='default'

###############################################################

#contains everything you need from a dataset
class Dataset:
    def __init__(self, filename, sample_type = "round"):
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
        if self.type == "square":
            indizes = {
                    "time":0,
                    "load":(1,2,3,4),
                    "laser":5,
                    "accelerometer":6,
                    "magnetventil":7,
                    "telfer_reset":8,
                    "distance_up":9,
                    "distance_down":10}
        
        if self.type != "square" and self.type != "round":
            raise ValueError ("Sample type unknown") 
            
        self.indizes = indizes
        
        start_accel, end_accel, start_load, end_load, start_laser, end_laser = calc_scope(self.array)
        
        #define datasets
        self.load = self.array[start_load:end_load,self.indizes["load"]]
        self.laser = self.array[start_laser:end_laser,self.indizes["laser"]]
        self.accel = self.array[start_accel:end_accel,self.indizes["accelerometer"]]
        #calculate loadcellsum from loadcells
        loadcells = self.load
        self.loadsum = np.sum(loadcells,axis=1)
        
        #define corresponding time
        self.load_time = self.array[start_load:end_load,self.indizes["time"]]
        self.laser_time = self.array[start_laser:end_laser,self.indizes["time"]]
        self.accel_time = self.array[start_accel:end_accel,self.indizes["time"]]
        

    def peak_loads(self):
        peak_list = []
        for i in self.load.shape[1]:
            peak_list.append(filtered_peak[self.load[:,i]])
        return peak_list
        
    def peak_deformation(self):
        return filtered_peak(self.laser)
    
    def peak_accel(self):
        return filtered_peak(self.accel)
        
    def get_dropheight(self):
        #m has a sampling rate of 10kHz, but the telfer of just 1 Hz
        m = int(np.argmax(self.array[:,self.indizes["magnetventil"]])/10000)
        u = np.nanargmax(self.array[m:,self.indizes["distance_up"]])
        up = self.array[u+m,self.indizes["distance_up"]]
        d = np.nanargmax(self.array[m:,self.indizes["distance_down"]])
        down = self.array[d+m,self.indizes["distance_down"]]
        return up - down           
        
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
            plot(res_path,x = self.load_time, y = self.load[:,i-1] ,xlabel= r"Time \([\text{s}]\)",ylabel=r"Load \([\text{kN}]\)", name="Loadcell_" + str(i),appendix = app, dataset_name = self.name)
        
    #    plot sum of all loadcells
        plot(res_path,x = self.load_time, y = self.loadsum ,xlabel= r"Time \([\text{s}]\)",ylabel=r"Load \([\text{kN}]\)", name="Loadcell_sum",appendix = app, dataset_name = self.name)
    
    # plot laser
        plot(res_path,x = self.laser_time, y = self.laser ,xlabel= r"Time \([\text{s}]\)",ylabel=r"Displacement \([\text{mm}]\)", name="Laser_Displacement", limit=(-100,-1),appendix = app, dataset_name = self.name)

#run all the things we really want on all files
def calc(data=r"C:\Users\kekaun\OneDrive - LKAB\roundSamples\Data\basic_array", results=r"C:\Users\kekaun\OneDrive - LKAB\roundSamples\Results" , extra_accel=False):
    #go to the right directory - save time
    os.chdir(data)
    
    #do you want to calculate with the normal sensor array or for the extra accelerometers
    if extra_accel == False:
        calc_basic_array(data, results)
    else:
        calc_extra_accel()

    #calculate basic array
def calc_basic_array(data,results):
    res_file = make_result_file(results)
    app_file = make_appendix_file(results)
    df = open_df(data)
    iterate_over(data,results,df,res_file,app_file)
    draw_diagrams(results,df,data)

def make_result_file(results):    
    #open results file
    res_path = results + r"\result.csv"
    res = open(res_path,"w")

    #write column titles
    res.write("Name;Number;Energy level;Thickness;Drop weight;Drop height;Age;Velocity;Force;Acceleration;Displacement;Broken/Cracked;Crack area;Opening angle\n")
    res.write(r" ; ;\([\text{kJ}]\);\([\text{mm}]\);\([\text{kg}]\);\([\text{mm}]\);\([\text{days}]\);\(\big[\frac{\text{m}}{\text{s}}\big]\);\([\text{kN}]\);\(\Big[\frac{\text{m}}{\text{s}^\text{2}}\Big]\);\([\text{mm}]\); ;\([\text{mm}^\text{2}]\);\([\text{\textdegree}]\)"+ "\n")
    return res
    
def make_appendix_file(results):
    #open appendix file
    app_path = results + r"\appendix.tex"
    app = open(app_path,"w")
    
    #write appendix
    app.write("\includepdf[pages=-]{appendix/lacing.pdf}\n\n")
    
    return app
    
def iterate_over(direct,results,df,res_file,app_file):    
    #iterate over file 
    file_list = []
    for root, folders, files in os.walk(direct):
        for file in files:
            if file[-3:].lower() == "npy":
                path = root+"\\"+file
                if os.path.isfile(path):
                    file_list.append(path)
    for i in file_list:
        sg.OneLineProgressMeter('Progress', file_list.index(i) + 1, len(file_list), 'key','Progress of calculation')
        calc_single_file(i,results,df,res_file,app_file, sample_type = df.at[os.path.basename(i)[:-4],"Sample type"])
    res_file.close()
    app_file.close()

#try which format the cell has
def table_format(c):
    cell = str(c)
    if cell == "":
        return np.nan
    if "," in cell:
        return float(cell.replace(",","."))
    if "." in cell:
        return float(cell)
    if cell.isdigit():
        return int(cell)
    return cell
    

def open_df(data):
    excel_path = make_meta_path(data) + r"\test_data.xlsx"
    csv_path = make_meta_path(data) + r"\test_data.csv"
    table_dtype = {"Age" : table_format, "Drop weight" : table_format, "Thickness": table_format, "Cracked/broken" : table_format, "Crack area" : table_format, "Opening angle" : table_format, "Number" : int}
    if os.path.isfile(excel_path):
        table = pd.read_excel(excel_path, header = 0, index_col = "Name", converters  = table_dtype)
    elif os.path.isfile(csv_path):
        table = pd.read_csv(csv_path, sep = ";", header = 0, index_col = "Name" , converters  = table_dtype)
    else:
        raise NameError("No test_data file available!")
    return table

def make_meta_path(data):
    path = os.path.split(data)
    print(path[0])
    meta_path = path[0] + "\\metadata"
    print(meta_path)
    return meta_path
    
def calc_single_file(filename = r"C:\Users\kekaun\OneDrive - LKAB\roundSamples\Data\basic_array\cracked\2018-11-29_Rfrs_75_1,0.npy",results="",df = "sanity_check", res_file ="", app_file = "", sample_type = "Round"):
    dataset = Dataset(filename, sample_type)
    
    if results == "":
        help_list = filename.split("\\")
        res_path = "\\".join(help_list[:-4]) + "\\Results\\" + dataset.name
    else: res_path = results + "\\" + dataset.name
        
    #make a folder for each file
    if os.path.isdir(res_path) == False:
        os.mkdir(res_path)
    
    # if there is no data frame and no results file, don't try to make entries into the appendix
    if type(df) != str and results != "": 
    #write everything to result files and appendix
        new_chapter_appendix(dataset_name = dataset.name, df = df , app_file = app_file)
        write_result(dataset,df,res_file,filename)
    dataset.make_graphs(res_path, app = app_file)    
    
#write everything important to the result file        
def write_result(dataset,df,res_file,filename):
    
#make a list to add each individual line
    text = []  
    
    #name
    add_list(text,dataset.name.replace("_","\_"))
    
    #legend
    add_list(text,df.loc[dataset.name,"Number"])
        
    #energy level

    weig = df.loc[dataset.name,"Drop weight"]

    heig = dataset.get_dropheight()

    add_list(text,energy(heig,weig),2) 

    #thickness
    add_list(text,df.loc[dataset.name,"Thickness"])
#    text.append(str(ponder.loc["thickness"]) + ";") 
    
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

    #peak deformation
    deform = filtered_peak(dataset.laser)
    add_list(text,deform,1)


#    broken or cracked?
    if df.loc[dataset.name,"Broken/cracked"] == "broken":
        #if broken just add nan
        add_list(text,"broken",sep=";;\n")
    else:
        #if cracked add damage mapping
        add_list(text,"cracked")
        add_list(text,df.loc[dataset.name,"Crack area"])
        add_list(text,df.loc[dataset.name,"Opening angle"],1,sep="\n")
    
    for i in text:   
        res_file.write(i)
    
def new_chapter_appendix(app_file,df,dataset_name):
    app_file.write("\\chapter{" + dataset_name.replace("_","\_") + "}\n\n")
    # add Picture into appendix
    pic_path =".\\appendix\\" + dataset_name + ".jpg"
    if df.loc[dataset_name,"Broken/cracked"] == "cracked":
        write_appendix(app_file,pic_path,"Picture of the sample after the test")

    #calculate exra accelerometer    
def calc_extra_accel():
    return "zero"

    #help function, makes it easier to add to a list
def add_list(lst,thing,rnd=0,sep=";"):
    if isinstance(thing,float):
        lst.append(str(np.round(thing,rnd))+sep)        
    else:
        lst.append(str(thing) + sep)
       
#calculate Everything for .npy files    
        
def set_limit(limit):
    bottom,top = plt.ylim()
    if bottom < limit[0] and limit[0] != -1:
        plt.ylim(bottom = limit[0])
    if top > limit[1]  and limit[1] != -1:
        plt.ylim(top = limit[1])
        
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

def calc_scope(array):
    start_load = find_start(array,cushion=500)
    start_accel = start_load
    start_laser = start_load
    
    len_accel = 1500
    len_load = 1500
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

def find_start(array,cushion=500): 
    x = np.where(array[:,6]==1)
    a = np.argmax(array[x[0][0]:],axis=0)
    c=[]
    for i in range(1,4):
# just the load cells        
        c.append(a[i])
#        c.append(b[i])
    return(int(math.floor(stat.median(c)) - cushion + x[0][0]))
    
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
    return float(height) * int(weight) * g / 10**6
    
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
    return math.sqrt(2*height*9.8/1000)

def broken(path):
    if os.path.dirname(path)[-1] == "n":
        return 1
    else: 
        return 0

def ex_in_clude(boolean):
    if boolean == True:
        return ""
    else:
        return "faulty"

def open_res_df(direct):
    res_path = direct + r"\result.csv"
    res = pd.read_csv(res_path, sep = ";", header = [0])
    res.set_index("Name", inplace = True)
    return res

def draw_diagrams(direct= "C:\\Users\\kekaun\\OneDrive - LKAB\\roundSamples\\Results", df = "place_holder", data = "C:\\Users\\kekaun\\OneDrive - LKAB\\roundSamples\\Data\\basic_array"):
    #if df is not open yet, open it
    if isinstance(df, str):
        df = open_df(data)
    
    res = open_res_df(direct)
    
    #make dir to save stuff
    path = direct + "\\diagram"
    if os.path.isdir(path) == False:
        os.makedirs(path)

    make_tables(res,direct)
        
    mask = make_mask(data, direct, index = df.index)
    
    #throw useless info away
    res = res.drop(['Broken/Cracked',"Drop weight","Drop height","Velocity","Number"],axis = 1)

    #keep the unit
    unit = res.iloc[0]
    
    #don't need the unit in the data anymore
    res = res.drop(res.index[0])
    
    #make data usable
    res = res.astype(float)
    
    #correlation dataframe
    corr = pd.DataFrame(index = res.columns, columns = res.columns, dtype = float)
    
    counter = 1
    #draw all the silly graphics    
    for j in res.columns:
        for i in res.columns:
            sg.OneLineProgressMeter('Progress', counter, len(res.columns)**2, 'key','Drawing diagrams')
            counter += 1
            plot_correlation(i, j, mask, res, unit, corr, df, path)
           
    #draw a heatmap
    heatmap(corr, direct)
    
    
def plot_correlation(i, j, mask, res, unit, corr, df, path):
     #begin plot
    ax = plt.subplot(111)
    
    #make submask
    submask = make_submask(i, j, mask, index = res.index)

    #exclude the data
    exclude = res[~submask]
    
    crack = res[submask][mask["Crack area"]]
    broke = res[submask][~mask["Crack area"]]
    
    mpl.rcParams["figure.figsize"] = (10,7)
    ax.plot(crack[i], crack[j], "b.",label="cracked")
    ax.plot(broke[i], broke[j], "r.", label = "broken")
    ax.plot(exclude[i],exclude[j],"xk", label = "excluded")       
    
    #make limits nice
    xlim = ax.get_xlim()
    ax.set_xlim((xlim[0] - 0.05 * xlim[0],xlim[1]+ 0.05 * xlim[1]))
    ylim = ax.get_ylim()
    ax.set_ylim((ylim[0] - 0.05 * ylim[0], ylim[1] + 0.05 * ylim[1]))
                
    #labels
    print(i, unit[i])
    ax.set_xlabel(i + " " + unit[i], usetex = True, fontsize = 14)
    ax.set_ylabel(j + " " + unit[j], usetex = True, fontsize = 14)
    
    #grid
    plt.grid()
    
    #linear interpolation
    slope, intercept, r_value, p_value, std_err = sp.stats.linregress(crack[i].astype(float),crack[j].astype(float))
    sortx = list(crack[i].astype(float).sort_values())
    sorty =[]
    for m in sortx:
        sorty.append(m * slope + intercept)

    ax.plot(sortx, sorty,"b--", label="$R^2$ = %0.04f \nx = %0.04f \ny = %0.04f" %(r_value**2,slope,intercept))
#            ax.plot(sortx, sorty,"b--")

    #put R2 in the correct spot of the dataframe
    corr[i][j] = r_value**2
    corr[j][i] = r_value**2
    
    #write numbers next to points            
    texts = [plt.text(res.at[k,i],res.at[k,j],df.at[k.replace("\\",""),"Number"]) for k in res.index]            
    adjust_text(texts)

    #legend            
    chartBox = ax.get_position()            
    ax.set_position([chartBox.x0, chartBox.y0, chartBox.width*0.8, chartBox.height])
    ax.legend(loc='center left', bbox_to_anchor=(1.0, 0.75), ncol=1,fontsize = 14)

    #save
    filename = path + "\\" + j.replace(" ","-") + "_" + i.replace(" ","-") + ".png"
    plt.savefig(filename)
    plt.close()
    
#make a latex table out of the .csv       
def make_tables(df,direct):
        #make dir to save stuff
    path = direct + "\\tables"
    if os.path.isdir(path) == False:
        os.makedirs(path)
    
    #result file
    res = df
    
    ## format latex table
    form = column_format(len(res.columns))
    ## format numbers with thousand separator . and decimal separator ,
    decimal = [number_format] * len(res.columns)
    res.fillna(0, inplace = True)
    res.to_latex(path + "\\result.tex",na_rep="", formatters = decimal, column_format = form, escape=False)
    
    #test_values
    test_values = res[["Number","Energy level", "Thickness", "Drop weight", "Drop height", "Age"]]
    test_values.to_latex(path + "\\test_values.tex",na_rep="", formatters = decimal, column_format = form, escape=False)
    
    #short_result
    short_result = res[["Number", "Force", "Acceleration", "Displacement", "Crack area", "Opening angle"]]
    short_result.to_latex(path + "\\short_result.tex",na_rep="", formatters = decimal, column_format = form, escape=False)
    
    #just cracks
    crack = res[res["Broken/Cracked"] == "cracked"]
    cracks = crack.drop(["Broken/Cracked"], axis=1)
    
    ## format numbers with thousand separator . and decimal separator ,
    form = column_format(len(crack.columns))
    decimal = [number_format] * len(crack.columns)    
    cracks.to_latex(path + "\\crack.tex",na_rep="", formatters = decimal, column_format = form, escape=False, index=False)
    
    write_legend(direct,df.iloc[1:]["Number"])
    
    with pd.ExcelWriter(path + '\\result.xlsx') as writer:
            res.to_excel(writer, sheet_name = "Results", na_rep="")
    
def make_mask(data, direct, index):
        #make a mask to filter out everything that is useless
    csv_path = make_meta_path(data) + "\exclude.csv"
    excel_path = make_meta_path(data) + "\exclude.xlsx"
    if os.path.isfile(excel_path):
        mask = pd.read_excel(excel_path, header = 0, index_col = 0)
    elif os.path.isfile(csv_path):
        mask = pd.read_csv(csv_path, sep = ";", header = 0, index_col = 0)
    else:
        shape = (len(index),8)
        dummy_data = np.ones(shape = shape)
        columns = ["Loadcells","Accelerometer","Laser sensor",	"Crack area",	 "Opening angle",	"High speed camera", "Additional accelerometer vertical","Additional accelerometer horizontal"]
        mask = pd.DataFrame(data = dummy_data, index = index, columns = columns)
        print("TO DO: write a data frame that is all true!")
    
    mask = mask.astype(bool)

    #mask to latex
    excl_accl = mask[["Additional accelerometer vertical","Additional accelerometer horizontal"]]
    excl = mask.drop(["Opening angle","Crack area","Additional accelerometer vertical","Additional accelerometer horizontal"], axis = 1)
    excl_format = [ex_in_clude] * len(excl.columns)
    excl_accl_format = [ex_in_clude] * len(excl_accl.columns)
    excl.to_latex(direct + "\\tables\\exclude.tex",formatters = excl_format, escape = False,na_rep=" ")
    excl_accl.to_latex(direct + "\\tables\\exclude_accel.tex",formatters = excl_accl_format, escape = False,na_rep=" ")
    
    return mask
    
def make_submask(i, j, mask, index):
    if i not in mask.columns and j not in mask.columns:
        #if the data is not in the exlusion table just make a totally true mask
        #otherwise check if only one value is in there
        #lastly if both values are on the list, make a mixed list
        data = [True] * len(index)
        submask = pd.Series(data, index = index, dtype = bool)
    elif i in mask.columns and j not in mask.columns:
        submask = mask[i]
    elif i not in mask.columns and j in mask.columns:
        submask = mask[j]
    else:
        submask = mask[i] & mask[j]
    return submask
    
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
    print(path)
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
    
        