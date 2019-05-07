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


#"fix" matplotlib font - it´s arial instead of helvetica but better than nothing
#rc('text', usetex=True)
#mpl.rcParams['usetex'] = "True"
mpl.rcParams['font.sans-serif'] = "Arial"
mpl.rcParams['font.family'] = "sans-serif"
mpl.rcParams['mathtext.default']='default'


def doAllFiles(direct=".\\Data"):
    respath = ".\\Results\\result.csv"
    res = open(respath,"w")
    apppath = ".\\Results\\appendix.tex"
    app = open(apppath,"w")
    app.write("\includepdf[pages=-]{appendix/lacing.pdf}")
    app.close()
#    res.write("name \t thickness \t energy level\t drop height\t theoretical velocity\t peak loadcell 1\t peak loadcell 2\t peak loadcell 3 \t peak sum loadcell \t peak acceleration \t broken/cracked \n")
#    res.write("\t mm \t kJ/m^2 \t mm \t m/s \t kN/m^2 \t kN/m^2 \t kN/m^2 \t kN/m^2 \t m/s^2 \t \n")
    res.write("Name;Energy level;Thickness;Drop height;Age;Velocity;Force;Acceleration;Broken/Cracked;Crack area;Opening angle\n")
    res.write(r"nan;[$kJ$];[$mm$];[$mm$];[$days$];[$\frac{m}{s}$];[$kN$];[$\frac{m}{s^2}$];nan;[$mm^2$];[\textdegree]" + "\n")
    res.close()
    for root, folders, files in os.walk(direct):
        for file in files:
            if file[-3:].lower() == "npy":
                path = root+"\\"+file
                if os.path.isfile(path):
                    print(path)
#                    if path[-7:] !="fix.npy":
#                        os.remove(path)
#                        print("REMOVED: " + path)
#                    else: print(path)
#                    draw(path)
#                    os.rename(path,path[:-8]+".npy")
#                    print(path,path[:-8]+".npy")
                    Everything(path)
#                    displacement(path)
#                    fix_accel(path)
#    allGraphics(respath)

def las_start(array):
    x = np.where(array[:,6]==1)
#    print(x[0][0])
    start = np.where(array[x[0][0]:,4] < -10)[0][0]
    return start    

def add_list(lst,thing,rnd=0,sep=";"):
    if isinstance(thing,str):
        lst.append(thing + sep)
    else:
        lst.append(str(np.round(thing,rnd))+sep)
#    .replace(".",",")
    
def throwaway(file = ".\\Data\\cracked\\2019-04-16_Rfrs_75_0,5.npy"):
#    start = 1000 * 2585
    array = read_array(file)
#    for i in range(start):
#        array[i,1:6] = [0,0,0,0,0]
#    for j in range(1000 * 2680,1000 * 2700):
#        array[j,1:6] = [0,0,0,0,0]
#    print(array.shape)
    array = fix_time(array)
    np.save(".\\Data\\cracked\\2019-04-16_Rfrs_75_0,5.npy",array)
#    Everything(file = ".\\Data\\2019-04-16_Rfrs_75_0,5.npy")

def maxAccel(file=r"C:\Users\kekaun\OneDrive - LKAB\roundSamples\Data\broken\2019-02-20_Rfrs_75_1,0.npy"):
    array = read_array(file)
    #### NORMAL FILES
    start = findStart(array,cushion=500)
    length = 3000
    end = start + length
    up = peak(array[start:end,5])
    down = peak(-array[start:end,5])

    #### EXTRA ACCEL
#    up = peak(array[:,1])
#    down = peak(-array[:,1])

    print(up,down)
    
#alternate Everything for .npy files    
def Everything(file=".\\Data\\cracked\\2019-05-06_Rfrs_75_0,8.npy"):
#    file = ".\\Data\\cracked\\2019-02-20-Rfs-100-0,5.asc"  
#    array = readData(maxLines=-1,filename=file)

#open array
    array = read_array(file)
    
#    print(array.shape)

##correct values
    startLoad = findStart(array,cushion=1000)
    startAccel = startLoad - 500
    lenAccel = 3000
    lenLoad = 3000
    

#play values ###############
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
    if os.path.isdir("./Results/" +  os.path.basename(file[:-4])) == False:
        os.mkdir("./Results/" +  os.path.basename(file[:-4]))
        
#open the results files
    if os.path.isdir("./Results/" +  os.path.basename(file[:-4])) == False:
        os.mkdir("./Results/" +  os.path.basename(file[:-4]))        
#    fpath =".\\Results\\" + os.path.basename(file)[:-4] + "\\" + os.path.basename(file)[:-3] + "txt"
##    if os.path.exists(fpath) != True:
##        os.makedirs(".\\Results\\" + os.path.basename(file)[:-4])
#    f = open(fpath,"w")
# 
#    result = open(respath,"r")
#    f.write(result.readline())
#    f.write(result.readline())
#    result.close()
    respath = ".\\Results\\result.csv"   
    result = open(respath,"a")
    
#make and appendix file
    apppath = ".\\Results\\appendix.tex"
    app = open(apppath,"a")
    app.write("\n\\chapter{" + os.path.basename(file)[:-4].replace("_","\_") + "}\n")      
#make a list to add each individual line
    text = []    
    #name
    add_list(text,os.path.basename(file)[:-4].replace("_","\_"))
    #energy level
    weig = ponder.loc["weight"]
    heig = int(dropheight(array))
    add_list(text,energy(heig,weig),2)
    
#    text.append(str(energy(heig,weig)) + ";")    

    #thickness
    add_list(text,ponder.loc["thickness"])
#    text.append(str(ponder.loc["thickness"]) + ";")    

    #drop height
    add_list(text,heig)
#    text.append(str(heig) + ";")

    #age
    add_list(text,ponder.loc["age"])
#    text.append(str(ponder.loc["age"]) + ";")     

    #velocity
    #theoretic, just needs drop height
    add_list(text,theoryVelo(heig),1)
#    text.append(str(theoryVelo(heig)) + ";")
    #calculated, needs array and some reworking /take just a tiny snip of the accel array
#    text.append(str(calcVelocity(array[startLoad:startLoad+200,7]) + "\t"))
#    velo, peakvelo =  calc_velo(array[startLoad-200:startLoad+200,7],array[startLoad-200:startLoad+200,0],200)
#    text.append(str(peakvelo) + "\t")

    # loadcell 1 to 3
#    for i in range(1,4):
#        text.append(str(peak(array[startLoad:startLoad+lenLoad,i])) + "\t")

    #load sum
    loadsum = array[startLoad:startLoad+lenLoad,1]+array[startLoad:startLoad+lenLoad,2]+array[startLoad:startLoad+lenLoad,3]
#    loadtime = array[startLoad:startLoad+lenLoad,0]
    add_list(text,peak(loadsum),2)
#    text.append(str(round(peak(loadsum),2)) + ";")

    #peak accel
    add_list(text,peak(array[startAccel:startAccel+lenAccel,5]),2)
#    text.append(str(round(peak(array[startAccel:startAccel+lenAccel,5]),2)) + ";")

    #peak deformation
    add_list(text,peak(sig.medfilt(-array[startLoad+800:startLoad+1200,4])),1)

#    #impulse
#    #text.append(str(impulse(loadsum, loadtime))+"\t")
    
#    broken or cracked?
    panda = panda_fun(filename=os.path.basename(file)[:-4])
    if panda.loc["cracked/broken"] == "broken":
        add_list(text,"broken",sep=";nan;\n")
    else:
        add_list(text,"cracked")
#        text.append("cracked;")
        add_list(text,panda.loc["crack area"])
#        text.append(str(panda.loc["crack area"])+";")
#        text.append(str(panda.loc["opening angle"])+"\n")
        add_list(text,panda.loc["opening angle"],1,sep="\n")
    for i in text:
#        f.write(i)
        result.write(i)
    #put everything into file    
    result.close()
#    f.close()
    
    # plot accel
    x = array[startAccel:startAccel+lenAccel,0]
    accel = sig.medfilt(array[startAccel:startAccel+lenAccel,5])
    plt.plot(x,accel)
    bottom,top = plt.ylim()
    if bottom < - 1000:
        plt.ylim(bottom=-1000)
    plt.ylabel(r"Acceleration $[\frac{m}{s^2}]$")
    plt.xlabel("Time [$s$]")
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
    plt.xlabel("Time [$s$]")
    plt.ylabel("Load [$kN$]")
    for i in range(1,4):
        plt.xlabel("Time [$s$]")
        plt.ylabel("Load [$kN$]")
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
    plt.xlabel("Time [$s$]")
    plt.ylabel("Load [$kN$]")
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
    y = sig.medfilt(array[startLoad+800:startLoad+2000,4])
    x = array[startLoad+800:startLoad+2000,0]
#    y = sig.medfilt(array[startLoad:startLoad+lenLoad,4])
#    x = array[startLoad:startLoad+lenLoad,0]
    plt.plot(x,y)
    bottom,top= plt.ylim()
    if bottom < -100 and top > -100:
        plt.ylim(bottom=-100)
#    plt.title("Laser Displacement")
    plt.xlabel("Time [$s$]")
    plt.ylabel("Displacement [$mm$]")
    plt.grid()
    plt.savefig(".\\Results\\" + os.path.basename(file)[:-4] + "/displacement.png")
    plt.close()
    write_appendix(app,os.path.basename(file)[:-4] + "/displacement.png","Displacement")
#    write_appendix(app,os.path.basename(file)[:-4] + "/displacement.png")
    

    
# add Picture into appendix
    if os.path.isfile(".\\Data\\pics\\" + os.path.basename(file)[:-4] + ".jpg"):
        write_appendix(app,os.path.basename(file)[:-4] + ".jpg","Picture of the sample after the test")      
    
#def nan_helper(y):
#    return np.isnan(y), lambda z: z.nonzero()[0]

def displacement(file=".\\Data\\cracked\\2019-02-20_Rfs_100_0,5.npy"):
    array = read_array(file)
    load =  sig.medfilt(array[:,1] + array[:,2] + array[:,3])
    star = findStart(array,cushion=20)
######### JUST FOR 50_0,3_2
#    silly = []
#    for i in range (star,star+400):
#        if array[i,4] < -40:
#            array[i,4] = np.NaN
#            silly.append(i)
#    for j in silly:
#        array[j,4] = np.interp(j,[silly[0]-5,silly[-1]+5],[array[silly[0]-5,4],array[silly[-1]+5,4]])      
#    nans, x= nan_helper(array[:,4])
#    array[nans,4]= np.interp(x(nans), x(~nans), array[~nans,4])
    c,d = 0,(0,0)
    length = np.argmin(array[star:star+400,4])
#    length = 200
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

    
def read_array(file=".\\Data\\cracked\\2018-12-04_Rfrs_50_0,3_2.npy"):
    array = np.load(file)
    return array

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


    #get Energy from filename
def Energy(filename="ENERGY.asc"):
    regex = re.compile(r"\d,\d")
    mo = regex.search(filename)
    try:
        x = mo.group()
        return (x[0]+"."+x[2])
    except:
        return "ENERGY"

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
def allGraphics(direct=".\\Results\\result.csv"):
    #where to save stuff
    path = os.path.dirname(direct) + "\\Diagram"
    if os.path.isdir(path) == False:
        os.makedirs(path)
    #open csv
    res = pd.read_csv(direct,sep=";")
    #write a legend    
    write_legend(direct,res.drop(res.index[0]))
    #make a latex table
    results(direct)
    #make a mask to filter out broken/cracked
    mask = res['Broken/Cracked'] == 'cracked'
    #throw useless info away
    res = res.drop(['Name','Broken/Cracked'],axis = 1)
    #keep the unit
    unit = res.iloc[0]
    res = res.drop(res.index[0])
    res = res.astype(float)
    
    #make two frames for broken/cracked - easier use later
    crack = res[mask]
    broke = res[~mask]
    second = res.copy()
    
    #draw all the silly graphics    
    for i in res.columns:
        second = second.drop(i,axis = 1)
        for j in second.columns:
#            fig = plt.figure()
            ax = plt.subplot(111)
            #plot
            plt.plot(crack[i].astype(float),crack[j].astype(float),"b.",label="cracked")
            plt.plot(broke[i].astype(float),broke[j].astype(float),"r.",label="broken")
            #labels
#            plt.xlabel(i + " [$" + unit[i][2:-2] + "$]")
#            plt.ylabel(j + " [$" + unit[j][2:-2] + "$]")
            #try label
            plt.xlabel(i + " " + unit[i])
            plt.ylabel(j + " " + unit[j])            
            #grid
#            plt.grid()

#            dx = (plt.xlim()[1] - plt.xlim()[0]) * 0.01
#            dy = (plt.ylim()[1] + plt.ylim()[0]) * 0.01
            

            #linear interpolation
            slope, intercept, r_value, p_value, std_err = sp.stats.linregress(crack[i].astype(float),crack[j].astype(float))
            sortx = list(crack[i].astype(float).sort_values())
            sorty =[]
            for m in sortx:
                sorty.append(m * slope + intercept)
            ax.plot(sortx, sorty,"b--", label="R = %0.04f \nx = %0.02f \ny = %0.02f" %(r_value,slope,intercept))

            #broken line
            slope1, intercept2, r_value3, p_value4, std_err5 = sp.stats.linregress(broke[i].astype(float),broke[j].astype(float))
            sortx1 = list(broke[i].astype(float).sort_values())
            sorty1 =[]
            for n in sortx1:
                sorty1.append(n * slope1 + intercept2)
            ax.plot(sortx1,sorty1,"r--")
            
            #text
            texts = [plt.text(res.iloc[k-1][i], res.iloc[k-1][j], k) for k in res.index]
            adjust_text(texts)

            plt.grid()
            #legend            
            chartBox = ax.get_position()            
            ax.set_position([chartBox.x0, chartBox.y0, chartBox.width*0.8, chartBox.height])
            ax.legend(loc='upper center', bbox_to_anchor=(1.2, 0.8), shadow=True, ncol=1)
            #save
            filename = path + "\\" + j.replace(" ","-") + "_" + i.replace(" ","-") + ".png"
            plt.savefig(filename,format="png")
            plt.close()

#def allGraphics_txt(direct=".\\Results\\result.txt"):
#    unit, head, name, num = results(direct)
#    _ = head.pop(0)
#    _ = unit.pop(0)
#    path = os.path.dirname(direct) + "\\Diagram"
#    if os.path.isdir(path) == False:
#        os.makedirs(path)
#        
## make legend        
#    leg = open(os.path.dirname(direct) + "\\legend.tex","w")
#    leg.write("""\\begin{table}
#    \\centering
#    \\begin{tabular}{ll}
#    \\toprule
#    Name & Symbol \\\\
#    \\midrule \n""")
#    regex = re.compile("_")
#    namex = name.copy()
#    symbol = 1
#    lb, lc = [], []
#    print(name)
#    for m in range(len(name)):
#        if num[m][-1] == 1:
#            namex[m] = regex.sub("\\_",name[m])            
#            leg.write(namex[m]+"&"+str(symbol)+"\\\\ \n")
#            lb.append(symbol)
#            symbol +=1
#        else:
#            namex[m] = regex.sub("\\_",name[m])            
#            leg.write(namex[m]+"&"+str(symbol)+"\\\\ \n")
#            lc.append(symbol)
#            symbol +=1
#    leg.write("""\\bottomrule
#              \\end{tabular}
#              \\caption{Legend for the symbols assigned to tests}
#              \\label{tab:leg}
#              \\end{table}
#              """)
#    leg.close()
#
## make diagrams
#    inc = open(os.path.dirname(direct) + "\\include.tex","w")    
#    for i in range(len(head)-1):
#        for j in range(i,len(head)-1):
#            if i != j:
#                fig = plt.figure()
#                ax = plt.subplot(111)
#                xb, yb, xc, yc = [], [], [], []
#                plt.xlabel(head[i].capitalize() +"\t[$"+ unit[i][3:-3] + "$]")
#                plt.ylabel(head[j].capitalize() +"\t[$"+ unit[j][3:-3] + "$]")
##                title = head[j].capitalize() + " over " + head[i].lower()
##                plt.title(title.capitalize())
#                plt.grid()
#
#                for k in range(num.shape[0]):
#                    if num[k][-1] == 1:
#                        xb.append(num[k][i])
#                        yb.append(num[k][j])
#                    else: 
#                        xc.append(num[k][i])
#                        yc.append(num[k][j])
#
#                ax.plot(xb,yb,"r.",label="broken")
#                ax.plot(xc,yc,"b.",label ="cracked")
#                dx = (plt.xlim()[1] - plt.xlim()[0]) * 0.01
#                dy = (plt.ylim()[1] + plt.ylim()[0]) * 0.01
#                for k, txt in enumerate(lb):
#                    plt.annotate(txt, (xb[k]+dx, yb[k]+dy))
#                for k, txt in enumerate(lc):
#                    plt.annotate(txt, (xc[k]+dx, yc[k]+dy))
#                slope, intercept, r_value, p_value, std_err = sp.stats.linregress(xc,yc)
#                yr = []
#                xc.sort()
#                for m in xc:
#                    yr.append(m * slope + intercept) 
##                ax.plot(xc, yr,"--", label="R=" + str(np.round(r_value,4)))
##                ax.plot(xc, yr,"b--", label="R= %0.04f" %r_value)
#                ax.plot(xc, yr,"b--", label="R = %0.04f \n k = %0.02f \n d = %0.02f" %(r_value,slope,intercept))
#                chartBox = ax.get_position()
#                ax.set_position([chartBox.x0, chartBox.y0, chartBox.width*0.8, chartBox.height])
#                ax.legend(loc='upper center', bbox_to_anchor=(1.2, 0.8), shadow=True, ncol=1)
#                filename = path + "\\" + head[j].replace(" ","-") +"_" + head[i].replace(" ","-") + ".png"
#                fig.savefig(filename,format="png")
#                plt.close(fig)
#                inc.write(
#                """\\begin{figure}
#                \\centering
#                \\includegraphics[width=0.95 \\linewidth]{./diagram/""" + os.path.basename(filename)[:-4] + """}
#                \\caption{""" + title + """}
#                \\label{fig:""""" + os.path.basename(filename)[:-4] + """}
#                \\end{figure}
#                \n""")
#    inc.close()
    
#def results(direct=".\\Results\\result.csv"):
#    f= open(direct)
#    header = f.readline().split("\t")[1:]
#    header[-1] = header[-1][:-1]
#    for i in range(len(header)):
#        header[i] = header[i].strip()
#    unit = f.readline().split("\t")[1:-1]
#    l1 = []
#    name = []
#    for line in f.readlines():
#        line = line.split("\t")
#        for l in line:
#            if l == "broken\n":
#               l1.append(1.0)
#               continue
#            elif l == "cracked\n":
#                l1.append(0.0)
#                continue
#            else:
#                try:
#                    l1.append(np.double(l))
#                except:
#                    name.append(str(l))
#    f.close()
#    
#    number = np.asarray(l1,dtype=np.float64)
#    number = number.reshape(len(name),-1)
#    return unit, header, name, number

def results_txt(direct=".\\Results\\result.txt"):
    f= open(direct)
    header = f.readline().split("\t")
    header[-1] = header[-1][:-1]
    for i in range(len(header)):
        header[i] = header[i].strip()
    unit = f.readline().split("\t")[:-1]
    unit.append("")
    l1 = []
    name = []
    for line in f.readlines():
        line = line.split("\t")
        for l in line:
            if l == "broken\n":
               l1.append(1.0)
               continue
            elif l == "cracked\n":
                l1.append(0.0)
                continue
            else:
                try:
                    l1.append(np.double(l))
                except:
                    name.append(str(l))
    f.close()
    
    number = np.asarray(l1,dtype=np.float64)
    number = number.reshape(len(name),-1)
    return unit, header, name, number        

def results(direct=".\\Results\\result.csv"):
    res = pd.read_csv(direct,sep=";",header=[0,1])
    res.to_latex(".\\Results\\result.tex",na_rep="", decimal =",", escape=False,index=False)
#    crack = res.xs("Broken/Cracked", axis = 1)
    crack = res[res["Broken/Cracked","nan"] == "cracked"]
    cracks = crack.drop(["Broken/Cracked","nan"], axis=1,level = 0)
    cracks.to_latex(".\\Results\\crack.tex",na_rep="", decimal =",", escape=False,index=False)
#    crack = res[res['Broken/Cracked'] == 'cracked', axis = 0]
#    crack = res.loc["Broken/Cracked"]
    print()
    
#make a LaTeX ready table out of the result data
#def makeTable(path="./Results/result.csv"):
#    unit, header, name, number = results(path)
#    broken = []
#    for i in number[:,-1]:
#        if i == 1:
#            broken.append("broken")
#        else:
#            broken.append("cracked")
#    leg = open(path[:-3]+"tex","w")
#    leg.write("""
#              \\begin{landscape}
#              \\begin{table}[p!]
#              \\centering
#              \\begin{tabular}{*{""" + str(len(header)) + """}{l}}
#              \\toprule \n""")
#    leg.write(listtolatex(header))
#    leg.write(listtolatex(unit))
#    leg.write("""\\midrule \n""")
#    a = number.shape
#    for j in range(a[0]):
#        leg.write(str(name[j]).replace("_","\_") + "\t & \t" + listtolatex(number[:][j])[:-7] + broken[j] + "\\\\ \n")
#    leg.write("""\\bottomrule
#              \\end{tabular}
#              \\caption{all data}
#              \\label{tab:res}
#              \\end{table}
#              \\end{landscape}
#              """)
#    leg.close()
#    
#    #turns a list into a string to be used in a latex table
#def listtolatex(list):
#    l = ""
#    for i in list[:-1]:
#        l += str(i).replace("_","\_") + "\t&\t"
#    l += str(list[-1]).replace("_","\_") + "\\\\ \n"
#    return l
#
def write_appendix(appendix,filename,typ):
    appendix.write("""\\begin{figure}
    \\centering
    \\includegraphics[width=0.9\\linewidth]{./appendix/""" + filename + """}
    \\caption{""" + typ.capitalize() + "}\n\\end{figure}\n\n")     
        
    
def fix_50(file=".\\Data\\cracked\\2018-12-10_Rfrs_100_1,5_fix_fix.npy"):
    array = np.load(file)
    start = findStart(array,cushion=1000)-5000
    end = np.argmin(array[:,5])-1
    for i in range(end,array.shape[0]):
        array[i][5]=0
    plt.plot(array[start:start+10000,0],array[start:start+10000,5])
    np.save(file[:-4]+"_fix.npy",array)

def fix_time(array):
    array[0][0]=0
    for i in range(1,array.shape[0]):
        array[i][0] = array[i-1][0] + 0.0001
    return array

def fix_accel(file):
    array = np.load(file)
    for i in range(array.shape[0]):
        array[i][5] = array[i][5] * 9.8
    np.save(file[:-4]+"_fix.npy",array)

def plt_extraaccel(file=".\\extraAccel\\2019-04-16_Rfrs_75_0,5_horizontal.npy"):
###### .TXT
#    f = open(file,"r")
#    x,y = [],[]
#    i,up,down,start = 0,0,0,0
#    for line in f.readlines():
#        line = line.split(",")
#        x.append(float(line[0]))
#        y.append(float(line[1])*50*9.8) #50 because x 10 amplification an 0,5 mV/g
#        if float(line[1]) > up:
#            up = float(line[1])
#            start = i
#        elif float(line[1]) < down:
#            down = float(line[1])
#        i += 1   
#    f.close()
#    array = np.stack((x,y),axis=1)
#    np.save(file[:-3]+"npy",array)
#    print(up,down)
###### .NPY
    array = np.load(file)
    array = fix_time(array)
    start = np.argmax(array[:,1])
    down = np.argmin(array[:,1])
    plt.plot(array[start-50:start+300,0],array[start-50:start+300,1])
    
    plt.ylabel(r"Acceleration [$\frac{m}{s^2}$]")
    plt.xlabel("Time [$s$]")
#    plt.title("Acceleration measured directly on sample \n 2019-02-20-Rfs-100-0,5, vertical")
    plt.grid()
    plt.savefig(file[:-4] + ".png")
    plt.close()
    print(array[start][1])
    print(array[down][1])

def panda_fun(excel='panda.xlsx',filename="2019-02-20_Rfs_100_0,5"):
    data = pd.ExcelFile('panda.xlsx')
    array = data.parse(skiprows=4, index_col ="Name")
    first = array.loc[filename]
#    if first.loc["cracked/broken"] == "broken":
#        text.append("broken")
#    else:
#        text.append(first.loc["age"])
#        text.append(first.loc["crack area"])
#        text.append(first.loc["opening angle"])
    return(first)
    
#writes a legend
def write_legend(direct,df):
    print(df)
    leg = open(os.path.dirname(direct) + "\\legend.tex","w")
    leg.write("""\\begin{table}
    \\centering
    \\begin{tabular}{ll}
    \\toprule
    Name & Symbol \\\\
    \\midrule \n""")
    for l, m in enumerate(df["Name"]):
        leg.write(str(m) + "\t&\t" + str(l + 1)+"\t\\\\\n")
    leg.write("""\\bottomrule
\\end{tabular}
\\caption{Legend for the symbols assigned to tests}
\\label{tab:leg}
\\end{table}
              """)
    leg.close()

#integrate the PCB Data, not working too well yet, zero drift and zero offset
def integrate(file="C:\\Users\\kekaun\\OneDrive - LKAB\\roundSamples\\extraAccel\\2019-04-16_Rfrs_75_0,5_horizontal.npy"):
    array = np.load(file)
    peak = np.argmax(array[:,1])
    start = peak - 15
    end = peak + 500
    plt.ylabel(r"Acceleration [$\frac{m}{s^2}$]")
    plt.xlabel("Time [$s$]")
    plt.grid()
    time = array[start:end,0]/1000
    plt.plot(time,array[start:end,1])

#    dx=0.0001
#    x = time
    velo = sp.integrate.cumtrapz(array[start:end,1],dx=0.0001,initial = 0)
    disp = sp.integrate.cumtrapz(velo,initial = 0)
#    peak = np.argmax(array[:,1])
#    plt.plot(time,velo)
#    plt.plot(time,disp)
#    plt.savefig(file[:-4] + ".png")
    
#function
def help_func(x, a, b, c):
    return a + b*x + c*x*x

#minimum curves
def fitdata(file = "C:\\Users\\kekaun\\OneDrive - LKAB\\roundSamples\\Results\\result.csv"):

    #where to save stuff
    path = os.path.dirname(file) + "\\Diagram"
    if os.path.isdir(path) == False:
        os.makedirs(path)
    #open csv
    res = pd.read_csv(file,sep=";")

    #make a mask to filter out broken/cracked
    mask = res['Broken/Cracked'] == 'cracked'
    
    #throw useless info away
    res = res.drop(['Name','Broken/Cracked'],axis = 1)

    res = res.drop(res.index[0])
    res = res.astype(float)
    
    #make two frames for broken/cracked - easier use later
    crack = res[mask]
    broke = res[~mask]
    crack.sort_values("Energy level",inplace = True)
    broke.sort_values("Energy level",inplace = True)
    
    y = crack["Thickness"]
    x = crack["Energy level"]
    y1 = broke["Thickness"]
    x1 = broke["Energy level"]
    x2 = res["Thickness"]
    y2 = res["Energy level"]
    
    popt, pcov = curve_fit(help_func, x, y)
    popt1, pcov1 = curve_fit(help_func, x1, y1)
    plt.grid()
    plt.plot(x, y,"b.")
    plt.plot(x,help_func(x,*popt), 'r-', label='fit: a=%5.3f, b=%5.3f, c=%5.3f' % tuple(popt))
#    plt.plot(x1,help_func(x1,*popt1), 'b-', label='fit: a=%5.3f, b=%5.3f, c=%5.3f' % tuple(popt1))
    plt.ylabel('Thickness')
    plt.xlabel('Energy level')
    plt.legend()
    

#            fig = plt.figure()
#    ax = plt.subplot(111)
            #plot
#    plt.plot(crack[i].astype(float),crack[j].astype(float),"b.",label="cracked")
#    plt.plot(broke[i].astype(float),broke[j].astype(float),"r.",label="broken")
            #labels
#            plt.xlabel(i + " [$" + unit[i][2:-2] + "$]")
#            plt.ylabel(j + " [$" + unit[j][2:-2] + "$]")
            #grid
#            plt.grid()

#            dx = (plt.xlim()[1] - plt.xlim()[0]) * 0.01
#            dy = (plt.ylim()[1] + plt.ylim()[0]) * 0.01
            

#            #linear interpolation
#            slope, intercept, r_value, p_value, std_err = sp.stats.linregress(crack[i].astype(float),crack[j].astype(float))
#            sortx = list(crack[i].astype(float).sort_values())
#            sorty =[]
#            for m in sortx:
#                sorty.append(m * slope + intercept)
#            #broken line
##            slope1, intercept2, r_value3, p_value4, std_err5 = sp.stats.linregress(broke[i].astype(float),broke[j].astype(float))
##            sortx1 = list(broke[i].astype(float).sort_values())
##            sorty1 =[]
##            for n in sortx1:
##                sorty1.append(n * slope1 + intercept2)
##            ax.plot(sortx1,sorty1,"r--")
#            ax.plot(sortx, sorty,"b--", label="R = %0.04f \nx = %0.02f \ny = %0.02f" %(r_value,slope,intercept))
#            
#            #text
#            texts = [plt.text(res.iloc[k-1][i], res.iloc[k-1][j], k) for k in res.index]
#            adjust_text(texts)
#
#            plt.grid()
#            #legend            
#            chartBox = ax.get_position()            
#            ax.set_position([chartBox.x0, chartBox.y0, chartBox.width*0.8, chartBox.height])
#            ax.legend(loc='upper center', bbox_to_anchor=(1.2, 0.8), shadow=True, ncol=1)
#            #save
#            filename = path + "\\" + j.replace(" ","-") + "_" + i.replace(" ","-") + ".png"
#            plt.savefig(filename,format="png")
#            plt.close()
            
def clean_array(file=".\\Data\\cracked\\2019-05-06_Rfrs_75_0,8.asc"):
    array = readData(filename = file)
    #where telfer is reset, should be the start
    #throw away all the rows you don´t need
#    delete = [5,6,8,10,11,13,14,15,16,17,18,19,20,21,22]
    newarray = np.delete(array,[5,6,8,10,11,13,14,15,16,17,18,19,20,21,22],1)
    newarray = fix_time(newarray)
    for i in range(newarray.shape[0]):
        newarray[i][5] = newarray[i][5] * 9.8
#    newarray = fix_accel(newarray)
#    print(newarray.shape)
    np.save(file[:-4]+".npy",newarray)
#    array = readData(filename=file)   
#    for i in range(array.shape[0]):
#        print(str(array[i][0]))
#        r.write(str(array[i][0]))
#        for j in range(1,array.shape[1]):
#            r.write("\t" + str(array[i][j]))
#        r.write("\n")

def clearData(file):
# Read and ignore header lines
    i = 0
    while i < 8:
        file.readline()
        i += 1
# I checked the file, this is where the real headings are hidden
    global header # it´s dangerous to go alone, take this!
    header = file.readline().split("\t")
# ignore the useless stuff
    while i < 38:
        file.readline()
        i += 1
        
#put some values into an array
def readData(maxLines=-1,filename=".\\Data\\cracked\\2019-02-20-Rfs-100-0,5.asc",start=0): 
    f= open(filename)
    if start == 0:
        clearData(f)
    else: 
        for i in range(start):
            f.readline()
    l1 = []
    for line in f.readlines()[:maxLines]:
        line = line.replace(",",".").split("\t")[:-1]
        for l in line:
            try:
                d = np.double(l)
            except:
                d = np.nan
            l1.append(d)   
    f.close()
    try:
        return np.array(l1).reshape(-1,26)
    except:
        return np.array(l1).reshape(-1,29)
