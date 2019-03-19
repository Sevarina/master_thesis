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

#"fix" matplotlib font - it´s arial instead of helvetica but better than nothing
matplotlib.rcParams['font.sans-serif'] = "Arial"
matplotlib.rcParams['font.family'] = "sans-serif"
matplotlib.rcParams['mathtext.default']='default'

def doAllFiles(direct=".\\Data"):
    respath = ".\\Results\\result.txt"
    res = open(respath,"w")
    apppath = ".\\Results\\appendix.tex"
    app = open(apppath,"w")
    app.close()
#    res.write("name \t thickness \t energy level\t drop height\t theoretical velocity\t peak loadcell 1\t peak loadcell 2\t peak loadcell 3 \t peak sum loadcell \t peak acceleration \t broken/cracked \n")
#    res.write("\t mm \t kJ/m^2 \t mm \t m/s \t kN/m^2 \t kN/m^2 \t kN/m^2 \t kN/m^2 \t m/s^2 \t \n")
    res.write("Name \t Thickness \t Energy level\t Drop height\t Velocity \t Force \t Acceleration \t broken/cracked \n")
    res.write("\t \(mm\) \t \(kJ\) \t \(mm\) \t \(m/s\) \t \(kN\) \t \(m/s^2\) \t \n")
    res.close()
    for root, folders, files in os.walk(direct):
        for file in files:
            if file[-3:].lower() == "npy":
                path = root+"\\"+file
                if os.path.isfile(path):
                    print(path)
#                    draw(path)
                    Everything(path)
#    allGraphics(respath)

def las_start(array):
    x = np.where(array[:,6]==1)
#    print(x[0][0])
    start = np.where(array[x[0][0]:,4] < -10)[0][0]
    return start    

    

#alternate Everything for .npy files    
def Everything(file=".\\Data\\cracked\\2018-12-04_Rfrs_50_0,3_2.npy"):
#    file = ".\\Data\\cracked\\2019-02-20-Rfs-100-0,5.asc"  
#    array = readData(maxLines=-1,filename=file)
    array = read_array(file)
    array = fix_time(array)
    startLoad = findStart(array,cushion=1000)
#    startAccel = startLoad - 5000
    startAccel = startLoad
#    lenAccel = 9000
#    lenLoad = 3000
    lenAccel = 6000
    lenLoad = 5000
#    lasStart = las_start(array)
    
#make a folder for each file
    if os.path.isdir("./Results/" +  os.path.basename(file[:-4])) == False:
        os.mkdir(file[:-4])
        
#open the results files 
    fpath =".\\Results\\" + os.path.basename(file)[:-4] + "\\" + os.path.basename(file)[:-3] + "txt"
    if os.path.exists(fpath) != True:
        os.makedirs(".\\Results\\" + os.path.basename(file)[:-4])
    f = open(fpath,"w")
    respath = ".\\Results\\result.txt"    
    result = open(respath,"r")
    f.write(result.readline())
    f.write(result.readline())
    result.close()
    result = open(respath,"a")
    
#make and appendix file
    apppath = ".\\Results\\appendix.tex"
    app = open(apppath,"a")
    app.write("\\chapter{" + os.path.basename(file)[:-4].replace("_","\_") + "}\n")
    
#make a list to add each individual line
    text = []    
    #name
    text.append(os.path.basename(file)[:-4] + "\t")
    #thickness
    text.append(str(int(thickness(file))) + "\t")    
    #energy level
    text.append(str(Energy(file)) + "\t")
    #drop height
    height = int(dropheight(array))
    text.append(str(height) + "\t")
    #velocity
    #theoretic, just needs drop height
    text.append(str(theoryVelo(height)) + "\t")
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
    text.append(str(round(peak(loadsum),2)) + "\t")
    #peak accel
    text.append(str(round(peak(array[startAccel:startAccel+lenAccel,5]),2)) + "\t")
    #impulse
    #text.append(str(impulse(loadsum, loadtime))+"\t")
    #broken or cracked?
    if broken(file) == 1:
        print("broken")
        text.append("broken\n")
    else:
        text.append("cracked\n")
        print("cracked")
    for i in text:
        f.write(i)
        result.write(i)
    #put everything into file    
    result.close()
    f.close()
    
    # plot accel
    x = array[startAccel:startAccel+lenAccel,0]
    accel = sig.medfilt(9.8 * array[startAccel:startAccel+lenAccel,5])
    plt.plot(x,accel)
    plt.ylabel(r"Acceleration \n $\frac{m}{s^2}$")
    plt.xlabel("Time [$s$]")
#    plt.title("Acceleration")
    plt.grid()
    plt.savefig(".\\Results\\" + os.path.basename(file)[:-4] + "//Accel.png")
    plt.close()
    write_appendix(app,os.path.basename(file)[:-4] + "/Accel.png")
    
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
        write_appendix(app,os.path.basename(file)[:-4] + "/Loadcell" + str(i) + ".png")
        
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
    write_appendix(app,os.path.basename(file)[:-4] + "/Loadcellsum.png")
    
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
    bottom,_= plt.ylim()
    if bottom < -100:
        plt.ylim(bottom=-100)
#    plt.title("Laser Displacement")
    plt.xlabel("Time [$s$]")
    plt.ylabel("Displacement [$mm$]")
    plt.grid()
    plt.savefig(".\\Results\\" + os.path.basename(file)[:-4] + "//displacement.png")
    plt.close()
    write_appendix(app,os.path.basename(file)[:-4] + "/displacement.png")
    
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
    return np.round(up - down)

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
    return np.round(math.sqrt(2*height*9.8/1000),1)

def broken(path):
    if os.path.dirname(path)[-1] == "n":
        return 1
    else: 
        return 0

#create every graphic imaginable
#make a legend to compare names with numbers
def allGraphics(direct=".\\Results\\result.txt"):
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
                title = head[j].capitalize() + " over " + head[i].lower()
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
                ax.plot(xc, yr,"b--", label="R= %0.04f" %r_value)
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
    
#def results(direct=".\\Results\\result.txt"):
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

def results(direct=".\\Results\\result.txt"):
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

#make a LaTeX ready table out of the result data
def makeTable(path="./Results/result.txt"):
    unit, header, name, number = results(path)
    broken = []
    for i in number[:,-1]:
        if i == 1:
            broken.append("broken")
        else:
            broken.append("cracked")
    leg = open(path[:-3]+"tex","w")
    leg.write("""
              \\begin{landscape}
              \\begin{table}[p!]
              \\centering
              \\begin{tabular}{*{""" + str(len(header)) + """}{l}}
              \\toprule \n""")
    leg.write(listtolatex(header))
    leg.write(listtolatex(unit))
    leg.write("""\\midrule \n""")
    a = number.shape
    for j in range(a[0]):
        leg.write(str(name[j]).replace("_","\_") + "\t & \t" + listtolatex(number[:][j])[:-7] + broken[j] + "\\\\ \n")
    leg.write("""\\bottomrule
              \\end{tabular}
              \\caption{all data}
              \\label{tab:res}
              \\end{table}
              \\end{landscape}
              """)
    leg.close()
    
    #turns a list into a string to be used in a latex table
def listtolatex(list):
    l = ""
    for i in list[:-1]:
        l += str(i).replace("_","\_") + "\t&\t"
    l += str(list[-1]).replace("_","\_") + "\\\\ \n"
    return l

def write_appendix(appendix,filename):
    appendix.write("\\includegraphics[width=0.9\linewidth]{./appendix/" + filename + "}\n")        

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
    
def fix_50(file=".\\Data\\cracked\\2018-12-04_Rfrs_50_0,3.npy"):
    array = np.load(file)
    start = findStart(array,cushion=1000)-5000
    end = np.argmin(array[:,5])-2
    for i in range(end,array.shape[0]):
        array[i][5]=0
    plt.plot(array[start:,0],array[start:,5])
    np.save(".\\Data\\cracked\\2018-12-04_Rfrs_50_0,3_fix.npy",array)

def fix_time(array):
    array[0][0]=0
    for i in range(1,array.shape[0]):
        array[i][0] = array[i-1][0] + 0.0001
    return array

#    return array