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


def draw_diagrams(metadata = r"C:\Users\kekaun\OneDrive - LKAB\roundSamples\Data", results = r"C:\Users\kekaun\OneDrive - LKAB\roundSamples\Results", df = ""):
    #if df is not open yet, open it
    if isinstance(df, str):
        df = core.open_df(metadata, "test_data")
    
    res_df = core.open_df(results, "result")
    
    #make dir to save stuff
    path = results + "\\diagram"
    if os.path.isdir(path) == False:
        os.makedirs(path)
            
    #throw useless info away
    res_df = res_df.drop(['Broken/Cracked',"Drop weight","Drop height","Velocity","Number"],axis = 1)
    
    #correlation dataframe
#    corr = pd.DataFrame(index = res_df.columns, columns = res_df.columns, dtype = float)
        
    mask = core.make_mask(metadata, results, index = df.index, res_df=res_df)

    hold_thickness(res_df, df, mask, results)
#    counter = 1    
    #draw all the silly graphics    
#    for j in res_df.columns:
#        for i in res_df.columns:
#            sg.OneLineProgressMeter('Progress', counter, len(res_df.columns)**2, 'key','Drawing diagrams')
#            counter += 1
#            core.plot_correlation(i, j, mask, res_df, corr, df, path)

def plot_correlation(i, j, mask, res, corr, df, path):
     #begin plot
    ax = plt.subplot(111)
    
    #make submask
    exclude, broken, cracked = core.make_submask(i, j, mask, index = res.index ,df = df)
    print(exclude)

    crack = res[cracked]
    broke = res[broken]
    print(i,j)
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
    ax.set_xlabel(i + " " + latex_unit[i], usetex = True, fontsize = 14)
    ax.set_ylabel(j + " " + latex_unit[j], usetex = True, fontsize = 14)
    
    #grid
    plt.grid()
    
    #linear interpolation (if there are values for it)
#    try:
    print(crack[i], crack[j].empty)
    if crack[i].empty or crack[j].empty:
        corr[i][j] = 0
        corr[j][i] = 0
        print("HELP!")
    else:
        slope, intercept, r_value, p_value, std_err = sp.stats.linregress(crack[i].astype(float),crack[j].astype(float))
        sortx = list(crack[i].astype(float).sort_values())
        sorty =[]
        for m in sortx:
            sorty.append(m * slope + intercept)
        ax.plot(sortx, sorty,"b--", label="$R^2$ = %0.02f \nx = %0.04f \ny = %0.04f" %(r_value**2,slope,intercept))
    #            ax.plot(sortx, sorty,"b--")
        #put R2 in the correct spot of the dataframe
        corr[i][j] = r_value**2
        corr[j][i] = r_value**2
#    except:
#        print("no crack data!")
        
    Number = df['Number']
    try:
        Number = Number.astype(int)
    except:
        Number = Number.astype(str)    
    #write numbers next to points             
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

def hold_thickness(res, df, mask, results):
    fifty_res = res[res.loc[:,'Thickness'] == 50]
    fifty_df = df[df.loc[:,'Thickness'] == 50]
    fifty_mask = mask[mask.loc[:,'Thickness'] == 50]
    
    seventy = res[res.loc[:,'Thickness'] == 75]
    hundred = res[res.loc[:,'Thickness'] == 100]
    
    fifty_corr = pd.DataFrame(index = fifty_res.columns, columns = fifty_res.columns, dtype = float)    
    
    fifty_path = results + "\\diagram50"
    if os.path.isdir(fifty_path) == False:
        os.makedirs(fifty_path)

    iterate_diagrams(fifty_res, fifty_mask, fifty_corr, fifty_df, fifty_path)

    print(fifty_mask,fifty_res)
def iterate_diagrams(res_df, mask, corr, df, path):
    counter = 1    
#   draw all the silly graphics    
    for j in res_df.columns:
        for i in res_df.columns:
            sg.OneLineProgressMeter('Progress', counter, len(res_df.columns)**2, 'key','Drawing diagrams')
            counter += 1
            plot_correlation(i, j, mask, res_df, corr, df, path)

draw_diagrams()