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
import plotly.graph_objects as go


def plot(direct,x,y,limit=(-1,-1),xlabel="",ylabel="",name="", dataset_name = ""):
    plt.plot(x,sig.medfilt(y))
    core.set_limit(limit)
    plt.grid()
    plt.ylabel(ylabel, usetex= True)
    plt.xlabel(xlabel, usetex= True)
    plt.show()
#    fig_path = direct + "\\" + name + ".png"
#    plt.savefig(fig_path)
#    plt.close()


#dataset = core.Dataset(r"C:\Users\kekaun\OneDrive - LKAB\roundSamples\Data\basic_array\cracked\2019-09-02_75_Rfrs_0,5m1,5.npy")
#x = dataset.array[:,dataset.indizes["time"]]
#y = dataset.array[:,dataset.indizes["load"][2]]
#
#plot(r"C:\Users\kekaun\OneDrive - LKAB\roundSamples\Results",x,y)

# some online code
def make_zero(start,end):
    length = end - start
    helper = np.empty(length)
    helper[:] = np.nan
    return helper
    
def nan_helper(y):
  return np.isnan(y), lambda z: z.nonzero()[0]

def fix_disp(file=r"C:\Users\kekaun\OneDrive - LKAB\roundSamples\Data\basic_array\cracked\2019-09-02_75_Rfrs_0,5m1,5.npy"):
#open array
    array = np.load(file)

    start = core.find_start(array,cushion=500)
    end = start + 2000

    
##    # fix the first part
#    start1 = start + 1670
#    end1 = end - 375
#    y[start1:end1] = make_zero(start1,end1)

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
#    nans, x= nan_helper(y)
#    y[nans] = np.interp(x(nans), x(~nans), y[~nans])
#    array[start:end,4] = y[start:end]
    
    y = array[:,2]
    x = array[:,0]
    
    y_fix = np.where(y > -20, y, 0)
    
    array[:,3] = y_fix
    
    plt.grid()
    plt.plot(x[start:end],y_fix[start:end])

    np.save(file[:-4] + "_fix.npy",array)