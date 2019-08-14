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
    
    #make data usable
#    res_df = res_df.astype(float)
    
    #correlation dataframe
    corr = pd.DataFrame(index = res_df.columns, columns = res_df.columns, dtype = float)
    
    mask = make_mask(metadata, results, index = df.index, res_df=res_df)
    
    counter = 1    
    #draw all the silly graphics    
#    for j in res_df.columns[2]:
#        for i in res_df.columns[4]:
    i = res_df.columns[2]
    j = res_df.columns[4]
#    sg.OneLineProgressMeter('Progress', counter, len(res_df.columns)**2, 'key','Drawing diagrams')
#    counter += 1
    plot_correlation(i, j, mask, res_df, corr, df, path)

def plot_correlation(i, j, mask, res, corr, df, path):
     #begin plot
    ax = plt.subplot(111)
    
    #make submask
    exclude, broken, cracked = make_submask(i, j, mask, index = res.index ,df = df)
    exclude = core.remove_slash(exclude)
    print('exclude')
    exclude = res[exclude]
    print('crack')
    crack = res[cracked]
    print('broken')
    broke = res[broken]

    mpl.rcParams["figure.figsize"] = (10,7)
    ax.plot(crack[i], crack[j], "bx",label="cracked")
    ax.plot(broke[i], broke[j], "rx", label = "broken")
#    ax.plot(exclude[i],exclude[j],"xk", label = "excluded")       
    
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
    #            ax.plot(sortx, sorty,"b--")
        #put R2 in the correct spot of the dataframe
        corr[i][j] = r_value**2
        corr[j][i] = r_value**2
#    except:
#        print("no crack data!")
    
    #write numbers next to points            
    texts = [plt.text(res.at[k,i],res.at[k,j],df.at[k.replace("\\",""),"Number"]) for k in res.index]            
    adjust_text(texts)

    #legend            
    chartBox = ax.get_position()            
    ax.set_position([chartBox.x0, chartBox.y0, chartBox.width*0.8, chartBox.height])
    ax.legend(loc='center left', bbox_to_anchor=(1.0, 0.75), ncol=1,fontsize = 14)

    #save
    filename = path + "\\" + j.replace(" ","-") + "_" + i.replace(" ","-") + ".png"
    plt.show()
#    plt.savefig(filename)
#    plt.close()
    
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
    return exclude, broken, cracked

def make_mask(direct, results, index, res_df):
   #make a mask to filter out everything that is useless
   #if there is no exclude file just make a mask that is all True
    try:
        mask = core.open_df(direct,"exclude")
    except:
        print("help!")
        columns = ["Loadcells","Accelerometer","Laser sensor",	"Cracks",	"High speed camera"]#, "Additional accelerometer vertical","Additional accelerometer horizontal"]
        shape = (len(index), len(columns))
        dummy_data = np.ones(shape = shape)
        mask = pd.DataFrame(data = dummy_data, index = index, columns = columns)
    mask = mask.astype(bool)
    
#    mask to latex
    path = core.find_folder(results, "tables")

    ##use if there is extra accel data
#    excl_accl = mask[["Additional accelerometer vertical","Additional accelerometer horizontal"]]    
#    excl_accl_format = [ex_in_clude] * len(excl_accl.columns)
#    excl_accl.to_latex(os.path.join(path, "exclude.tex"),formatters = excl_accl_format, escape = False,na_rep=" ")

    excl_format = [core.ex_in_clude] * len(mask.columns)
    mask.to_latex(os.path.join(path, "exclude.tex"),formatters = excl_format, escape = False,na_rep="")

#make a pretty mask#
    #rename columns
    new_columns={
    'Loadcells' : 'Force',
     'Accelerometer' : 'Acceleration',
     'Laser sensor' : 'Displacement',
     'Cracks' : 'Crack area',
     }
    mask = mask.rename(columns = new_columns)
    new_data = [True] * len(index)
    
    #turn cracks into two columns and exclude broken&cracked samples
    mask.insert(loc = 0, column = 'Opening angle', value = mask.loc[:,'Crack area']) 
    
    #add the remaining columns as true
    for j in res_df.columns:
        if j not in mask.columns:
            mask.insert(loc = 0, column = j, value = new_data)
    print(mask)
    return mask    

draw_diagrams()