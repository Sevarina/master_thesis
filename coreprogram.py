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
from matplotlib import rc
import matplotlib.pyplot as plt
import scipy as sp
import scipy.signal as sig
from scipy.optimize import curve_fit
import math
import os
import re
import pandas as pd
from adjustText import adjust_text
import locale
locale.setlocale(locale.LC_ALL, 'deu_deu')



#rc('text', usetex=True)

#rc('text.latex', preamble=r'\usepackage{helvet}\renewcommand\familydefault{\sfdefault}')
mpl.rcParams['text.latex.preamble'] = [r'\usepackage{helvet}\renewcommand\familydefault{\sfdefault}', r'\usepackage{amsmath}' , r'\usepackage[T1]{fontenc}'] 

#"fix" matplotlib font - it´s arial instead of helvetica but better than nothing
#plt.rcParams['mathtext.fontset'] = 'custom'
mpl.rcParams['font.sans-serif'] = "Arial"
mpl.rcParams['font.family'] = "sans-serif"
mpl.rcParams['mathtext.default']='default'


#run all the things we really want on all files
def doAllFiles(direct=r"C:\Users\kekaun\OneDrive - LKAB\roundSamples\Data"):
    
    #go to the right directory - save time        
    os.chdir(direct)        
    os.chdir("..")
    
    #open results file
    respath = r".\Results\result.csv"
    res = open(respath,"w")
    
    #open appendix file
    apppath = r".\Results\appendix.tex"
    app = open(apppath,"w")
    app.write("\includepdf[pages=-]{appendix/lacing.pdf}")
    app.close()
    
    #write the seed for the appendix
    res.write("Name;Energy level;Thickness;Drop height;Age;Velocity;Force;Acceleration;Displacement;Broken/Cracked;Crack area;Opening angle\n")
    res.write(r"nan;\([\text{kJ}]\);\([\text{mm}]\);\([\text{mm}]\);\([\text{days}]\);\(\big[\frac{\text{m}}{\text{s}}\big]\);\([\text{kN}]\);\(\Big[\frac{\text{m}}{\text{s}^\text{2}}\Big]\);\([\text{mm}]\);nan;\([\text{mm}^\text{2}]\);\([\text{\textdegree}]\)"+ "\n")
    res.close()
    for root, folders, files in os.walk(direct):
        for file in files:
            if file[-3:].lower() == "npy":
                path = root+"\\"+file
                if os.path.isfile(path):
                    print(file)
                    Everything(path,direct)
    
    #draw all the Graphs
    allGraphics(respath)

    #help function, makes it easier to add to a list
def add_list(lst,thing,rnd=0,sep=";"):
    if isinstance(thing,str):
        lst.append(thing + sep)
    else:
        lst.append(str(np.round(thing,rnd))+sep)
#    .replace(".",",")
       
#alternate Everything for .npy files    
def Everything(file=r"C:\Users\kekaun\OneDrive - LKAB\roundSamples\Data\cracked\2018-11-29_Rfrs_75_1,0.npy",direct=""):
#change directory
    if direct == "":    
        os.chdir(os.path.dirname(file))        
        os.chdir("..")
        os.chdir("..")

#open array
    array = np.load(file)

##correct values
    startLoad = findStart(array,cushion=500)
    startAccel = startLoad
    lenAccel = 1500
    lenLoad = 1500
    
#####play values ###############
#    startLoad, startAccel = 0,0 
##    startLoad, startAccel = 1000 * 2585, 1000 * 2585
##    lenAccel = 4000 
##    lenLoad = 4000
#    lenAccel = array.shape[0] - startLoad
#    lenLoad = array.shape[0] - startLoad
###    lasStart = las_start(array)
###########################
    
#open meta data
    ponder = panda_fun(filename=os.path.basename(file)[:-4])

#make a folder for each file
    if os.path.isdir(".\Results\\" +  os.path.basename(file[:-4])) == False:
        os.mkdir(".\Results\\" +  os.path.basename(file[:-4]))
        
    respath = r"C:\Users\kekaun\OneDrive - LKAB\roundSamples\Results\result.csv"   
    result = open(respath,"a")
    
#make and appendix file
    apppath = r"C:\Users\kekaun\OneDrive - LKAB\roundSamples\Results\appendix.tex"
    app = open(apppath,"a")
    app.write("\n\\chapter{" + os.path.basename(file)[:-4].replace("_","\_") + "}\n")
      
#make a list to add each individual line
    text = []  
    
    #name
    add_list(text,os.path.basename(file)[:-4].replace("_","\_"))
    
    #energy level
    weig = ponder.loc["weight"]
    heig = dropheight(array)
    add_list(text,energy(heig,weig),2) 

    #thickness
    add_list(text,ponder.loc["thickness"])
#    text.append(str(ponder.loc["thickness"]) + ";")    

    #drop height
    add_list(text,heig,1)

    #age
    add_list(text,ponder.loc["age"])  

    #velocity
    #theoretic, just needs drop height
    add_list(text,theoryVelo(heig),1)

    #TO DO calculated velocity
    #needs array and some reworking /take just a tiny snip of the accel array

    #load sum
    loadsum = array[startLoad:startLoad+lenLoad,1]+array[startLoad:startLoad+lenLoad,2]+array[startLoad:startLoad+lenLoad,3]
    add_list(text,peak(loadsum),2)

    #peak accel
    add_list(text,peak(array[startAccel:startAccel+lenAccel,5]),2)

    #peak deformation
    add_list(text,peak(sig.medfilt(-array[startLoad+800:startLoad+1200,4])),1)

    #TO DO impulse

#    broken or cracked?
    panda = panda_fun(filename=os.path.basename(file)[:-4])
    if panda.loc["cracked/broken"] == "broken":
        #if broken just add nan
        add_list(text,"broken",sep=";nan;\n")
    else:
        #if cracked add damage mapping
        add_list(text,"cracked")
        add_list(text,panda.loc["crack area"])
        add_list(text,panda.loc["opening angle"],1,sep="\n")
    
    for i in text:
        #put everything into file    
        result.write(i)

    result.close()
    
    # plot accel
    x = array[startAccel:startAccel+lenAccel,0]
    accel = sig.medfilt(array[startAccel:startAccel+lenAccel,5])
    plt.plot(x,accel)
    bottom,top = plt.ylim()
    if bottom < - 1000:
        plt.ylim(bottom=-1000)
    plt.ylabel(r"Acceleration \Big[\(\frac{\text{m}}{\text{s}^2}\)\Big]", usetex=True)
    plt.xlabel(r"Time \([\text{s}]\)", usetex=True)
#    plt.title("Acceleration")
    plt.grid()
    plt.savefig(".\\Results\\" + os.path.basename(file)[:-4] + "//Acceleration.png")
    plt.close()
    write_appendix(app,os.path.basename(file)[:-4] + "/Acceleration.png","Acceleration")
    
##   plot calc velocity
#    x = range(0,200)
#    y = velo
#    plt.plot(x,y)
#    plt.ylabel(r"Calculated Velocity [$m/s$]")
#    plt.xlabel("Time [$s$]")
#    plt.title("Calculated Velocity")
#    plt.grid()
#    plt.savefig(".\\Results\\" + os.path.basename(file)[:-4] + "//Vel.png")
#    plt.close()
#   write_appendix(app,os.path.basename(file)[:-4] + "/Vel.png")
        
#    load cells
    x = array[startLoad:startLoad+lenLoad,0]
#    x = array[startLoad+950:startLoad+1020,0]
    for i in range(1,4):
        plt.xlabel(r"Time \([\text{s}]\)", usetex=True)
        plt.ylabel(r"Load \([\text{kN}]\)", usetex=True)
        y = sig.medfilt(array[startLoad:startLoad+lenLoad,i])
#        y = f[:,i]
        plt.plot(x,y)
#        plt.title(os.path.basename(file)[:-4] + " Loadcell " + str(i))
        plt.grid()
        plt.savefig(".\\Results\\" + os.path.basename(file)[:-4] + "//Loadcell" + str(i) + ".png")
        plt.close()
        write_appendix(app,os.path.basename(file)[:-4] + "/Loadcell" + str(i) + ".png", "Loadcell " + str(i))
        
#    plot sum of all loadcells    
    y = sig.medfilt(loadsum)
#    a,b = first_peak(loadsum)
#    c,d = last_peak(loadsum,a)
    plt.plot(x,y)
#   TO DO, fix those fucks!
#    plt.plot(a,array[b+startLoad][0],"r.")
#    plt.plot(c,array[d+startLoad][0],"b.")
#    plt.title("Sum of all Loadcells")
    plt.xlabel(r"Time \([\text{s}]\)", usetex=True)
    plt.ylabel(r"Load \([\text{kN}]\)", usetex=True)
    plt.grid()
    plt.savefig(".\\Results\\" + os.path.basename(file)[:-4] + "//Loadcellsum.png")
    plt.close()
    write_appendix(app,os.path.basename(file)[:-4]+ "/Loadcellsum.png","Sum of all loadcells")
    
##   plot impulse 
#    print(loadsum.shape)
#    print(x.shape)
#    y = sp.integrate.cumtrapz(loadsum[a:c],x[a:c],initial = 0)*1000
#    plt.plot(x[a:c],y)
#    plt.ylabel(r"Impulse [$Ns$]")
#    plt.xlabel("Time [$s$]")
#    plt.title("Impulse")
#    plt.grid()
#    plt.savefig(".\\Results\\" + os.path.basename(file)[:-4] + "//imp.png")
#    plt.close()
#    write_appendix(app,os.path.basename(file)[:-4] + "/imp.png")
#     
# plot laser
    y = sig.medfilt(array[startLoad:startLoad+2000,4])
    x = array[startLoad:startLoad+2000,0]
    plt.plot(x,y)
    bottom,top= plt.ylim()
    if bottom < -100 and top > -100:
        plt.ylim(bottom=-100)
    plt.xlabel(r"Time \([\text{kN}]\)", usetex=True)
    plt.ylabel(r"Displacement \([\text{mm}]\)", usetex=True)
    plt.grid()
    plt.savefig(".\\Results\\" + os.path.basename(file)[:-4] + "/displacement.png")
    plt.close()
    write_appendix(app,os.path.basename(file)[:-4] + "/displacement.png","Displacement")
        
# add Picture into appendix
    if os.path.isfile(".\\Data\\pics\\" + os.path.basename(file)[:-4] + ".jpg"):
        write_appendix(app,os.path.basename(file)[:-4] + ".jpg","Picture of the sample after the test")      
    
def load_displacement_curve(file=".\\Data\\cracked\\2019-02-20_Rfs_100_0,5.npy"):
    array = np.load(file)
    load =  sig.medfilt(array[:,1] + array[:,2] + array[:,3])
    star = findStart(array,cushion=20)
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
    startload = star + d[0] -5
    startdisp = star + d[1] +2
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
    plt.savefig(".\\Results\\" + os.path.basename(file)[:-4] + "_load_displacement.png")
    plt.close()
    pot=0.490
    plt.plot(disp,loa, label=("absorbed energy = %0.03f \n potential energy = %0.03f")%(c,pot))
    plt.legend()
#    plt.title("Energy CLIPPED")
    plt.ylabel("Force [$kN$]")
    plt.xlabel("Displacement [$mm$]")

    plt.savefig(".\\Results\\" + os.path.basename(file)[:-4] + "_energy.png")
    plt.close()
#    

def findStart(array,cushion=500): 
    x = np.where(array[:,6]==1)
    a = np.argmax(array[x[0][0]:],axis=0)
    c=[]
    for i in range(1,4):
# just the load cells        
        c.append(a[i])
#        c.append(b[i])
    return(int(math.floor(stat.median(c)) - cushion + x[0][0]))
    
    #get drop height            
def dropheight(array):
    #m has a sampling rate of 10kHz, but the telfer of just 1 Hz
    m = int(np.argmax(array[:,7])/10000)
    u = np.nanargmax(array[m:,8])
    up = array[u+m,8]
    d = np.nanargmax(array[m:,9])
    down = array[d+m,9]
    return up - down

#get peak of anything, input: sliced array
def peak(array):
    index = np.argmax(array)
    return (array[index])

# impact energy from dropheight and drop weight
def energy(height,weight):
    g = 9.8
    return height * weight * g / 10**6
    
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

#create every graphic imaginable
#make a legend to compare names with numbers
def allGraphics(direct=r"C:\Users\kekaun\OneDrive - LKAB\roundSamples\Results\result.csv"):
    #where to save stuff
    path = os.path.dirname(direct) + "\\Diagram"
    if os.path.isdir(path) == False:
        os.makedirs(path)
    #open csv
    res = pd.read_csv(direct,sep=";",index_col = 0)
    
    #write a legend    
    write_legend(direct,res.drop(res.index[0]))
    #make a latex table
    results(direct)
    #make a mask to filter out everything that is useless
    mask = pd.read_csv(r"C:\Users\kekaun\OneDrive - LKAB\roundSamples\exclude.csv", sep = ";", header = 0, index_col = 0)
    mask = mask.astype(bool)
    
#    #make a mask to filter out broken/cracked
#    mask = res['Broken/Cracked'] == 'cracked'
    
    #throw useless info away

    res = res.drop(['Broken/Cracked'],axis = 1)

    #keep the unit
    unit = res.iloc[0]
    
    #don't need the unit in the data anymore
    res = res.drop(res.index[0])
    
    #make data usable
    res = res.astype(float)
    
#    #make two frames for broken/cracked - easier use later
        #TO DO make the data sets
            #first separate into broken/cracked globally
            #second seperate into exclude/include globally (exclude gets a x, and include a . as marker)



    crack = res[mask["Crack area"]]
    broke = res[~mask["Crack area"]]
    second = res.copy()
    
    #draw all the silly graphics    
    for i in res.columns:
        second = second.drop(i,axis = 1)
        for j in second.columns:
#            fig = plt.figure()
            ax = plt.subplot(111)
            #TO DO make the data sets
                #first exclude 
            #plot
            plt.plot(crack[i].astype(float),crack[j].astype(float),"b.",label="cracked")
            plt.plot(broke[i].astype(float),broke[j].astype(float),"r.",label="broken")
            
            #labels
            plt.xlabel(i + " " + unit[i], usetex = True)
            plt.ylabel(j + " " + unit[j], usetex = True)
            
            #grid
            plt.grid()

            #linear interpolation
            slope, intercept, r_value, p_value, std_err = sp.stats.linregress(crack[i].astype(float),crack[j].astype(float))
            sortx = list(crack[i].astype(float).sort_values())
            sorty =[]
            for m in sortx:
                sorty.append(m * slope + intercept)
            ax.plot(sortx, sorty,"b--", label="R = %0.04f \nx = %0.02f \ny = %0.02f" %(r_value,slope,intercept))

#            #broken line
#            slope1, intercept2, r_value3, p_value4, std_err5 = sp.stats.linregress(broke[i].astype(float),broke[j].astype(float))
#            sortx1 = list(broke[i].astype(float).sort_values())
#            sorty1 =[]
#            for n in sortx1:
#                sorty1.append(n * slope1 + intercept2)
#            ax.plot(sortx1,sorty1,"r--")
            
            #text
#            texts = [plt.text(res.iloc[k-1][i], res.iloc[k-1][j], k) for k in res.index]
#            adjust_text(texts)

            #legend            
            chartBox = ax.get_position()            
            ax.set_position([chartBox.x0, chartBox.y0, chartBox.width*0.8, chartBox.height])
            ax.legend(loc='upper center', bbox_to_anchor=(1.2, 0.8), shadow=True, ncol=1)

            #save
            filename = path + "\\" + j.replace(" ","-") + "_" + i.replace(" ","-") + ".png"
            plt.savefig(filename,format="png")
            plt.close()

#make a latex table out of the .csv       
def results(direct=r"C:\Users\kekaun\OneDrive - LKAB\roundSamples\Results\result.csv"):
    
    #result file
    res = pd.read_csv(direct,sep=";",header=[0,1])
    ## format latex table
    form = column_format(len(res.columns))
    ## format numbers with thousand separator . and decimal separator ,
    decimal = [number_format] * len(res.columns)
    res.fillna(0, inplace = True)
    
    res.to_latex(os.path.dirname(direct) + "\\result.tex",na_rep="", formatters = decimal, column_format = form, escape=False, index=False)

    #just cracks
    crack = res[res["Broken/Cracked","nan"] == "cracked"]
    cracks = crack.drop(["Broken/Cracked","nan"], axis=1,level = 0)
    ## format numbers with thousand separator . and decimal separator ,
    form = column_format(len(crack.columns))
    decimal = [number_format] * len(crack.columns)    
    cracks.to_latex(os.path.dirname(direct) + "\\crack.tex",na_rep="", formatters = decimal, column_format = form, escape=False, index=False)
    print()
    
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
def write_appendix(appendix,filename,typ):
    appendix.write("""\\begin{figure}
    \\centering
    \\includegraphics[width=0.9\\linewidth]{./appendix/""" + filename + """}
    \\caption{""" + typ.capitalize() + "}\n\\end{figure}\n\n")     

def fix_time(array):
    array[0][0]=0
    for i in range(1,array.shape[0]):
        array[i][0] = array[i-1][0] + 0.0001
    return array

def panda_fun(excel=r'C:\Users\kekaun\OneDrive - LKAB\roundSamples\panda.xlsx',filename="2019-02-20_Rfs_100_0,5"):
    data = pd.ExcelFile(excel)
    array = data.parse(skiprows=4, index_col ="Name")
    first = array.loc[filename]
    return(first)
    
#writes a legend
def write_legend(direct,df):
    leg = open(os.path.dirname(direct) + "\\legend.tex","w")
    leg.write("""\\begin{table}
    \\centering
    \\begin{tabular}{ll}
    \\toprule
    Name & Symbol \\\\
    \\midrule \n""")
    for l, m in enumerate(df.index):
        leg.write(str(m) + "\t&\t" + str(l + 1)+"\t\\\\\n")
    leg.write("""\\bottomrule
\\end{tabular}
\\caption{Legend for the symbols assigned to tests}
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

def fix_disp(file=r"C:\Users\kekaun\OneDrive - LKAB\roundSamples\Data\cracked\2019-02-20_Rfrs_75_0,5.npy"):
#open array
    array = np.load(file)

    start = findStart(array,cushion=500)
    end = start + 1500
    y = array[:,4]
#
#
##    # fix the first part
    start1 = start + 883
    end1 = end - 600
    y[start1:end1] = make_zero(start1,end1)

##    
    start2 = start + 1250
    end2 = end - 190
    y[start2:end2] = make_zero(start2,end2)
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
    
    y1 = sig.medfilt(array[start2:end2,4])
    x1 = array[start2:end2,0]
    
    plt.grid()
    plt.plot(x,y)
    plt.plot(x1,y1)
    np.save(file[:-4] + "_fix.npy",array)
    
