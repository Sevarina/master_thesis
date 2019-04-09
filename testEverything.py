# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 15:33:33 2019

@author: KEKAUN
"""

import numpy as np
import statistics as stat
import matplotlib
import matplotlib.pyplot as plt
import scipy as sp
import scipy.signal as sig
import math
import os
import re
import pandas as pd

#"fix" matplotlib font - it´s arial instead of helvetica but better than nothing
matplotlib.rcParams['font.sans-serif'] = "Arial"
matplotlib.rcParams['font.family'] = "sans-serif"
matplotlib.rcParams['mathtext.default']='default'

def doAllFiles(direct=".\\Data"):
    respath = ".\\Results\\result.csv"
    res = open(respath,"w")
    apppath = ".\\Results\\appendix.tex"
    app = open(apppath,"w")
    app.write("\includepdf[pages=-]{appendix/lacing.pdf})
    app.close()
#    res.write("name \t thickness \t energy level\t drop height\t theoretical velocity\t peak loadcell 1\t peak loadcell 2\t peak loadcell 3 \t peak sum loadcell \t peak acceleration \t broken/cracked \n")
#    res.write("\t mm \t kJ/m^2 \t mm \t m/s \t kN/m^2 \t kN/m^2 \t kN/m^2 \t kN/m^2 \t m/s^2 \t \n")
    res.write("Name;Energy level;Thickness;Drop height;Age;Velocity;Force;Acceleration;Broken/Cracked;Crack area;Opening angle\n")
    res.write("nan;\(kJ\);\(mm\);\(mm\);\(days\);\(m/s\);\(kN\);\(m/s^2\);nan;\(mm^2\);\\textdegree\n")
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
    

#alternate Everything for .npy files    
def Everything(file=".\\Data\\cracked\\2018-12-10_Rfrs_100_1,5.npy"):
#    file = ".\\Data\\cracked\\2019-02-20-Rfs-100-0,5.asc"  
#    array = readData(maxLines=-1,filename=file)

#open array
    array = read_array(file)
    startLoad = findStart(array,cushion=1000)
    startAccel = startLoad - 500
#    lenAccel = 7000
    lenAccel = 3000
    lenLoad = 3000
#    lenAccel = 6000
#    lenLoad = 5000
#    lasStart = las_start(array)
    
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
#
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
        add_list(text,panda.loc["opening angle"],sep="\n")
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
    plt.ylabel(r"Acceleration \n $\frac{m}{s^2}$")
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
    res = pd.read_csv(direct,sep=";")
#    res.reset_index(inplace=True)
#    res.to_latex(".\\Results\\leg.tex",columns=["Name"],escape=False)
    
    
    
def allGraphics_txt(direct=".\\Results\\result.txt"):
    unit, head, name, num = results(direct)
    _ = head.pop(0)
    _ = unit.pop(0)
    path = os.path.dirname(direct) + "\\Diagram"
    if os.path.isdir(path) == False:
        os.makedirs(path)
        
# make legend        
    leg = open(os.path.dirname(direct) + "\\legend.tex","w")
    leg.write("""\\begin{table}
    \\centering
    \\begin{tabular}{ll}
    \\toprule
    Name & Symbol \\\\
    \\midrule \n""")
    regex = re.compile("_")
    namex = name.copy()
    symbol = 1
    lb, lc = [], []
    print(name)
    for m in range(len(name)):
        if num[m][-1] == 1:
            namex[m] = regex.sub("\\_",name[m])            
            leg.write(namex[m]+"&"+str(symbol)+"\\\\ \n")
            lb.append(symbol)
            symbol +=1
        else:
            namex[m] = regex.sub("\\_",name[m])            
            leg.write(namex[m]+"&"+str(symbol)+"\\\\ \n")
            lc.append(symbol)
            symbol +=1
    leg.write("""\\bottomrule
              \\end{tabular}
              \\caption{Legend for the symbols assigned to tests}
              \\label{tab:leg}
              \\end{table}
              """)
    leg.close()

# make diagrams
    inc = open(os.path.dirname(direct) + "\\include.tex","w")    
    for i in range(len(head)-1):
        for j in range(i,len(head)-1):
            if i != j:
                fig = plt.figure()
                ax = plt.subplot(111)
                xb, yb, xc, yc = [], [], [], []
                plt.xlabel(head[i].capitalize() +"\t[$"+ unit[i][3:-3] + "$]")
                plt.ylabel(head[j].capitalize() +"\t[$"+ unit[j][3:-3] + "$]")
#                title = head[j].capitalize() + " over " + head[i].lower()
#                plt.title(title.capitalize())
                plt.grid()

                for k in range(num.shape[0]):
                    if num[k][-1] == 1:
                        xb.append(num[k][i])
                        yb.append(num[k][j])
                    else: 
                        xc.append(num[k][i])
                        yc.append(num[k][j])

                ax.plot(xb,yb,"r.",label="broken")
                ax.plot(xc,yc,"b.",label ="cracked")
                dx = (plt.xlim()[1] - plt.xlim()[0]) * 0.01
                dy = (plt.ylim()[1] + plt.ylim()[0]) * 0.01
                for k, txt in enumerate(lb):
                    plt.annotate(txt, (xb[k]+dx, yb[k]+dy))
                for k, txt in enumerate(lc):
                    plt.annotate(txt, (xc[k]+dx, yc[k]+dy))
                slope, intercept, r_value, p_value, std_err = sp.stats.linregress(xc,yc)
                yr = []
                xc.sort()
                for m in xc:
                    yr.append(m * slope + intercept) 
#                ax.plot(xc, yr,"--", label="R=" + str(np.round(r_value,4)))
#                ax.plot(xc, yr,"b--", label="R= %0.04f" %r_value)
                ax.plot(xc, yr,"b--", label="R = %0.04f \n k = %0.02f \n d = %0.02f" %(r_value,slope,intercept))
                chartBox = ax.get_position()
                ax.set_position([chartBox.x0, chartBox.y0, chartBox.width*0.8, chartBox.height])
                ax.legend(loc='upper center', bbox_to_anchor=(1.2, 0.8), shadow=True, ncol=1)
                filename = path + "\\" + head[j].replace(" ","-") +"_" + head[i].replace(" ","-") + ".png"
                fig.savefig(filename,format="png")
                plt.close(fig)
                inc.write(
                """\\begin{figure}
                \\centering
                \\includegraphics[width=0.95 \\linewidth]{./diagram/""" + os.path.basename(filename)[:-4] + """}
                \\caption{""" + title + """}
                \\label{fig:""""" + os.path.basename(filename)[:-4] + """}
                \\end{figure}
                \n""")
    inc.close()
    
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
    res.to_latex(".\\Results\\result.tex",na_rep="",escape=False,index=False)

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

#def draw(file=".\\Data\\cracked\\2018-12-04_Rfrs_50_0,3_2.npy"):
##    file = ".\\Data\\cracked\\2019-02-20-Rfs-100-0,5.asc"  
##    array = readData(maxLines=-1,filename=file)
#    array = read_array(file)
##    array = fix_time(array)
#    x= array[:,0]
#    for i in range(5,array.shape[1]):
#        y = array[:,i]
#        plt.plot(x,y)
#        plt.grid()
#        plt.show()
#        
    
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

def plt_extraaccel(file=".\\Data\\extraAccel\\2019-02-20_Rfrs_100_1,0_vertical.npy"):
#    f = open(file,"r")
#    x,y = [],[]
#    i,up,down,start = 0,0,0,0
#    for line in f.readlines():
#        line = line.split(",")
#        x.append(float(line[0]))
#        y.append(float(line[1])*9.8)
#        if float(line[1]) > up:
#            up = float(line[1])
#            start = i
#        elif float(line[1]) < down:
#            down = float(line[1])
#        i += 1   
#    f.close()
#    array = np.stack((x,y),axis=1)
#    np.save(file[:-3]+".npy",array)
    array = np.load(file)
    start = np.argmax(array[:,1])
    down = np.argmin(array[:,1])
    plt.plot(array[start-50:start+300,0],array[start-50:start+300,1])
    
    plt.ylabel(r"Acceleration [$m/s^2$]")
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
    
