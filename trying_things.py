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

#def plot(direct,x,y,limit=(-1,-1),xlabel="",ylabel="",name="", dataset_name = ""):
#    plt.plot(x,sig.medfilt(y))
#    core.set_limit(limit)
#    plt.grid()
#    plt.ylabel(ylabel, usetex= True)
#    plt.xlabel(xlabel, usetex= True)
#    plt.show()
##    fig_path = direct + "\\" + name + ".png"
##    plt.savefig(fig_path)
##    plt.close()
#
#
#dataset = core.Dataset(r"C:\Users\kekaun\OneDrive - LKAB\roundSamples\Data\basic_array\cracked\2019-05-06_Rfrs_75_0,8.npy")
#x = dataset.array[:,dataset.indizes["time"]]
#y = dataset.array[:,dataset.indizes["accelerometer"]]
#plot(r"C:\Users\kekaun\OneDrive - LKAB\roundSamples\Results",x,y)

def draw_diagrams(metadata = r"C:\Users\kekaun\OneDrive - LKAB\roundSamples\Data", results = r"C:\Users\kekaun\OneDrive - LKAB\roundSamples\Results", df = ""):
    #if df is not open yet, open it
    if isinstance(df, str):
        df = core.open_df(metadata, "test_data")
    
    res_df = core.open_df(results, "result")
            
    #throw useless info away
    res_df = res_df.drop(['Broken/Cracked',"Drop weight","Drop height","Velocity","Number"],axis = 1)
    
    #correlation dataframe
    corr = pd.DataFrame(index = res_df.columns, columns = res_df.columns, dtype = float)
    
    
    mask = core.make_mask(metadata, results, index = df.index, res_df=res_df)
    
    i,j = "Energy level", "Thickness"
    plot_correlation(i, j, mask, res_df, corr, df, path = "")
        

def plot_correlation(i, j, mask, res, corr, df, path):
     #begin plot
    ax = plt.subplot(111)
    
    #make submask
    exclude, broken, cracked = core.make_submask(i, j, mask, index = res.index ,df = df)
    exclude = res[exclude]
    crack = res[cracked]
    broke = res[broken]
    print(i,j)
    mpl.rcParams["figure.figsize"] = (10,7)    
    ax.plot(broke[i], broke[j], "r.", label = "broken")
    ax.plot(crack[i], crack[j], "b.",label="cracked")
    ax.plot(exclude[i],exclude[j],"xk", label = "excluded")       
    
    #make limits nice
    xlim = ax.get_xlim()
    ax.set_xlim((xlim[0] - 0.05 * xlim[0],xlim[1]+ 0.05 * xlim[1]))
    ylim = ax.get_ylim()
    ax.set_ylim((ylim[0] - 0.05 * ylim[0], ylim[1] + 0.05 * ylim[1]))
                
    #labels
    ax.set_xlabel(i + " " + core.latex_unit[i], usetex = True, fontsize = 14)
    ax.set_ylabel(j + " " + core.latex_unit[j], usetex = True, fontsize = 14)
    
    #grid
    plt.grid()
    
    #linear interpolation (if there are values for it)
#    try:
    if crack[i].empty or crack[j].empty:
        corr[i][j] = 0
        corr[j][i] = 0
    else:
        slope, intercept, r_value, p_value, std_err = sp.stats.linregress(crack[i].astype(float),crack[j].astype(float))
        sortx = list(crack[i].astype(float).sort_values())
        sorty =[]
        for m in sortx:
            sorty.append(m * slope + intercept)
        ax.plot(sortx, sorty,"b--", label="$R^2$ = %0.04f \nx = %0.04f \ny = %0.04f" %(r_value**2,slope,intercept))
        
    
    slopeb, interceptb, r_valueb, p_valueb, std_errb = sp.stats.linregress(broke[i].astype(float),broke[j].astype(float))
    sortxb = list(broke[i].astype(float).sort_values())
    sortyb =[]
    for m in sortxb:
        sortyb.append(m * slopeb + interceptb)
    ax.plot(sortxb, sortyb,"r--", label="$R^2$ = %0.04f \nx = %0.04f \ny = %0.04f" %(r_valueb**2,slopeb,interceptb))
    #            ax.plot(sortx, sorty,"b--")
        #put R2 in the correct spot of the dataframe
#        corr[i][j] = r_value**2
#        corr[j][i] = r_value**2
#    except:
#        print("no crack data!")
        
#    Number = df['Number']
#    try:
#        Number = Number.astype(int)
#    except:
#        Number = Number.astype(str)    
#    #write numbers next to points             
#    texts = [plt.text(res.at[k,i],res.at[k,j],Number.loc[k]) for k in res.index]  
#    adjust_text(texts)

    #legend            
    chartBox = ax.get_position()            
    ax.set_position([chartBox.x0, chartBox.y0, chartBox.width*0.8, chartBox.height])
    ax.legend(loc='center left', bbox_to_anchor=(1.0, 0.75), ncol=1,fontsize = 14)