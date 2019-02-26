#! python3
#playing with a smaller file
#round sample

import numpy as np
import statistics as stat
import matplotlib.pyplot as plt
import scipy as sp
import scipy.signal as sig
import math
import os
import re
import json
#from matplotlib.backends.backend_pdf import PdfPages
#import matplotlib.backends.backend_agg as agg

#import logging

#set up logging correctly
#logging.basicConfig(level=logging.DEBUG, format= '%(asctime)s - %(levelname)s - %(message)s')

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
def readData(maxLines=10000,filename=".\\Data\\cracked\\2018-12-04_Rfrs_50_0,3.asc",start=0): 
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
    return np.array(l1).reshape(-1,26)
    
#Find the beginning of the interesting area
def findStart(array,cushion=500): 
    x = np.where(array[:,9]==1)
    a = np.argmax(array[x[0][0]:],axis=0)
    c=[]
    for i in range(1,4):
# just the load cells        
        c.append(a[i])
#        c.append(b[i])
    return(int(math.floor(stat.median(c)) - cushion + x[0][0]))
                   
    #do Everything for every file
def doAllFiles(direct=".\\Data"):
    respath = ".\\Results\\result.txt"
    res = open(respath,"w")
    res.write("name \t energy level\t drop height\t theoretical velocity\t measured velocity\t peak loadcell 1\t peak loadcell 2\t peak loadcell 3 \t peak sum loadcell \t peak acceleration \t impulse \t broken/cracked \n")
    res.write("\tkJ/m^2\tmm\tm/s\tm/s\tkN/m^2\tkN/m^2\tkN/m^2\tkN/m^2\tm/s^2\tNs\t\n")
    res.close()
    for root, folders, files in os.walk(direct):
        for file in files:
            if file[-3:] == "ASC":
#                print(file)
                path = root+"\\"+file
                if os.path.isfile(path) and os.path.dirname(path)[-1] == "d":
#                    Everything(path)
                    print(path)                    
                    something(path)
    allGraphics(respath)
                    
#cut accel data out of a file
def accelData(file = ".\\Data\\cracked\\2018-12-04_Rfrs_50_0,3.asc",length=200):
    f = readData(-1,file,0)
    start = findStart(f,0)
    f = f[start:start+length]
    x = np.zeros((length,2))
    for i in range(length):
        x[i,0] = f[i,0]
        x[i,1] = f[i,7] * 9.8
    return x

def loadData(file = ".\\Data\\cracked\\2018-12-04_Rfrs_50_0,3_2.asc",length=500):
    f = readData(-1,file,0)
    start = findStart(f,50)
    f = f[start:start+length]
    x = np.zeros((length,2))
    for i in range(length):
        x[i,0] = f[i,0]
        x[i,1] = f[i,1] + f[i,2] + f[i,3]
    return x

#get values from result table 
def results(direct=".\\Results\\result.txt"):
    f= open(direct)
    header = f.readline().split("\t")[1:]
    header[-1] = header[-1][:-1]
    for i in range(len(header)):
        header[i] = header[i].strip()
    unit = f.readline().split("\t")[1:-1]
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
    
#TO DO fix impulse
#TO DO filx calc velo

#create every graphic imaginable
#make a legend to compare names with numbers
def allGraphics(direct=".\\Results\\result.txt"):
    unit, head, name, num = results(direct)
    path = os.path.dirname(direct) + "\\Diagram"
    if os.path.isdir(path) == False:
        os.makedirs(path)
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
    #TO DO, give broken and cracked different colours!
    #split number in cracked and broken
    for i in range(len(head)-1):
        for j in range(i,len(head)-1):
            if i != j:
                fig = plt.figure()
                ax = plt.subplot(111)
                xb, yb, xc, yc = [], [], [], []
                plt.xlabel(head[i] + " [$"+ unit[i] + "$]")
                plt.ylabel(head[j] + " [$"+ unit[j] + "$]")
                plt.title(head[j] + " over " + head[i])
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
                fig.savefig(path + "\\" + head[j] +"_" + head[i] +".jpg")
                plt.close()




    #get drop height            
def dropheight(array):
    #m has a sampling rate of 10kHz, but the telfer of just 1 Hz
    m = int(np.argmax(array[:,12])/10000)
    u = np.nanargmax(array[m:,23])
    up = array[u+m,23]
    d = np.nanargmax(array[m:,24])
    down = array[d+m,24]
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

#calc velo from height
def theoryVelo(height):
    return np.round(math.sqrt(2*height*9.8/1000),1)


#fix the zero drift!
#give accel data where nothing happens
#def calc_velo(acc,time,start):
#    corr = sp.integrate.cumtrapz(acc[:start],time[:start],initial = 0)
#    vel = sp.integrate.cumtrapz(acc[start:],time[start:],initial = 0)
#    slope, intercept, r_value, p_value, std_err = sp.stats.linregress(corr,time[:start])
#    truevelo = []    
#    for i, txt in enumerate(vel):
#        truevelo.append(txt - intercept - slope * i)
#    maxvelo = max(truevelo) - min(truevelo)
#    return truevelo, maxvelo


def impulse(array,time):
    a,_ = first_peak(array)
    b,_ = last_peak(array,a)
    return sp.integrate.trapz(array[a:b],time[a:b])*1000

def broken(path):
    print(os.path.dirname(path))
    if os.path.dirname(path)[-1] == "n":
        return 1
    else: 
        return 0

#TO DO, only plot velocity for cracked plots, plots need to be in the results folder, calculate drop time, velocity is max pos peak - max neg peak
#draws plots for each diagram and write important info into individual and shared files
def Everything(file=".\\Data\\cracked\\2018-12-04_Rfrs_50_0,3.asc"):
#get data
    array = readData(maxLines=-1,filename=file)
    startLoad = findStart(array,cushion=1000)
    startAccel = startLoad - 5000
    lenAccel = 9000
    lenLoad = 3000
    
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

#make a list to add each individual line
    text = []
    
#    name
    text.append(os.path.basename(file)[:-4] + "\t")
    #energy level
    text.append(str(Energy(file)) + "\t")
    #drop height
    height = dropheight(array)
    text.append(str(height) + "\t")
    #velocity
    #theoretic, just needs drop height
    text.append(str(theoryVelo(height)) + "\t")
    #calculated, needs array and some reworking /take just a tiny snip of the accel array
#    text.append(str(calcVelocity(array[startLoad:startLoad+200,7]) + "\t"))
    velo, peakvelo =  calc_velo(array[startLoad-200:startLoad+200,7],array[startLoad-200:startLoad+200,0],200)
    text.append(str(peakvelo) + "\t")
    # loadcell 1 to 3
    for i in range(1,4):
        text.append(str(peak(array[startLoad:startLoad+lenLoad,i])) + "\t")
    #load sum
    loadsum = array[startLoad:startLoad+lenLoad,1]+array[startLoad:startLoad+lenLoad,2]+array[startLoad:startLoad+lenLoad,3]
    loadtime = array[startLoad:startLoad+lenLoad,0]
    text.append(str(peak(loadsum)) + "\t")
    #peak accel
    text.append(str(peak(array[startAccel:startAccel+lenAccel,7])) + "\t")
    #impulse
    text.append(str(impulse(loadsum, loadtime))+"\t")
    #broken or cracked?
    if broken(file) == 1:
        text.append("broken\n")
    else: text.append("cracked\n")
    for i in text:
        f.write(i)
        result.write(i)
    #put everything into file    
    result.close()
    f.close()
    
    # plot accel
    x = array[startAccel:startAccel+lenAccel,0]
    accel = sig.medfilt(9.8 * array[startAccel:startAccel+lenAccel,7])
    plt.plot(x,accel)
    plt.ylabel(r"Acceleration [$m/s^2$]")
    plt.xlabel("Time [$s$]")
    plt.title("Acceleration")
    plt.grid()
    plt.savefig(".\\Results\\" + os.path.basename(file)[:-4] + "//Accel.png")
    plt.close()
    
#   plot calc velocity
    x = range(0,200)
    y = velo
    plt.plot(x,y)
    plt.ylabel(r"Calculated Velocity [$m/s$]")
    plt.xlabel("Time [$s$]")
    plt.title("Calculated Velocity")
    plt.grid()
    plt.savefig(".\\Results\\" + os.path.basename(file)[:-4] + "//Vel.png")
    plt.close()
    
    # load cells
    x = array[startLoad:startLoad+lenLoad,0]
    plt.xlabel("Time [$s$]")
    plt.ylabel("Load [$kN$]")
    for i in range(1,4):
        plt.xlabel("Time [$s$]")
        plt.ylabel("Load [$kN$]")
        y = sig.medfilt(array[startLoad:startLoad+lenLoad,i])
#        y = f[:,i]
        plt.plot(x,y)
        plt.title("Loadcell " + str(i))
        plt.grid()
        plt.savefig(".\\Results\\" + os.path.basename(file)[:-4] + "//Loadcell" + str(i) + ".png")
        plt.close()
        
#    plot sum of all loadcells    
    y = sig.medfilt(loadsum)
    a,b = first_peak(loadsum)
    c,d = last_peak(loadsum,a)
    plt.plot(x,y)
    plt.plot(a,array[b+startLoad][0],"r.")
    plt.plot(c,array[d+startLoad][0],"b.")
    plt.title("Sum of all Loadcells")
    plt.xlabel("Time [$s$]")
    plt.ylabel("Load [$kN$]")
    plt.grid()
    plt.savefig(".\\Results\\" + os.path.basename(file)[:-4] + "//Loadcellsum.png")
    plt.close()
    
#   plot impulse 
    y = sp.integrate.cumtrapz(loadsum[a:c],x[a:c],initial = 0)*1000
    plt.plot(x[a:c],y)
    plt.ylabel(r"Impulse [$Ns$]")
    plt.xlabel("Time [$s$]")
    plt.title("Impulse")
    plt.grid()
    plt.savefig(".\\Results\\" + os.path.basename(file)[:-4] + "//imp.png")
    plt.close()

#test of everything
def something(array):
#    array = readData(maxLines=-1,filename=file)
    file = ".\\Data\\cracked\\2018-12-04_Rfrs_50_0,3.asc"
    startLoad = findStart(array,1000)
#    startLoad= start
    startLongAccel = startLoad - 5000
    lenLongAccel = 9000
    startShortAccel,_ = first_peak(array[start:,7])
    lenShortAccel,_ = last_peak(array[start:,7],0)
    lenLoad = 3000
    
##make a folder for each file
#    if os.path.isdir("./Results/" +  os.path.basename(file[:-4])) == False:
#        os.mkdir("./Results/" +  os.path.basename(file[:-4]))
#        
##open the results files 
#    fpath =".\\Results\\" + os.path.basename(file)[:-4] + "\\" + os.path.basename(file)[:-3] + "txt"
#    if os.path.exists(fpath) != True:
#        os.makedirs(".\\Results\\" + os.path.basename(file)[:-4])
#    f = open(fpath,"w")
#    respath = ".\\Results\\result.txt"    
#    result = open(respath,"r")
#    f.write(result.readline())
#    f.write(result.readline())
#    result.close()
#    result = open(respath,"a")

#make a list to add each individual line
#    text = []
#    
##    name
#    text.append(os.path.basename(file)[:-4] + "\t")
##    energy level
#    text.append(str(Energy(file)) + "\t")
# #   drop height
#    height = dropheight(array)
#    text.append(str(height) + "\t")
# #   velocity
#  #  theoretic, just needs drop height
#    text.append(str(theoryVelo(height)) + "\t")
##    calculated, needs array and some reworking /take just a tiny snip of the accel array
##    text.append(str(calcVelocity(array[startLoad:startLoad+200,7]) + "\t"))
    velo, peakvelo =  calc_velo(array[startShortAccel-200:lenShortAccel,7],array[startShortAccel-200:lenShortAccel,0],200)
#    text.append(str(peakvelo) + "\t")
# #    loadcell 1 to 3
#    for i in range(1,4):
#        text.append(str(peak(array[startLoad:startLoad+lenLoad,i])) + "\t")
#  #  load sum
#    loadsum = array[startLoad:startLoad+lenLoad,1]+array[startLoad:startLoad+lenLoad,2]+array[startLoad:startLoad+lenLoad,3]
#    text.append(str(peak(loadsum)) + "\t")
#   # peak accel
#    text.append(str(peak(array[startAccel:startAccel+lenAccel,7])) + "\t")
#    #impulse
#    text.append(str(impulse(loadsum, array[startLoad:startLoad+lenLoad,1]))+"\t")
##    broken or cracked?
#    if broken(file) == 1:
#        text.append("broken\n")
#    else: text.append("cracked\n")
#    for i in text:
#        f.write(i)
#        result.write(i)
# #   put everything into file    
#    result.close()
#    f.close()
    
    # plot accel
#    x = array[startAccel:startAccel+lenAccel,0]
#    y = sig.medfilt(9.8 * array[startAccel:startAccel+lenAccel,7])
#    plt.plot(x,y)
#    plt.ylabel(r"Acceleration [$m/s^2$]")
#    plt.xlabel("Time [$s$]")
#    plt.title("Acceleration")
#    plt.grid()
#    plt.savefig(".\\Results\\" + os.path.basename(file)[:-4] + "_Accel.png")
#    plt.close()
#    
##   plot calc velocity
#    x = range(0,200)
#    y = velo
#    plt.plot(x,y)
#    plt.ylabel(r"Calculated Velocity [$m/s$]")
#    plt.xlabel("Time [$s$]")
#    plt.title("Calculated Velocity")
#    plt.grid()
#    plt.savefig(".\\Results\\" + os.path.basename(file)[:-4] + "_Vel.png")
#    plt.close()
    
#    # load cells
#
#    x = array[startLoad:startLoad+lenLoad,0]
#    plt.xlabel("Time [$s$]")
#    plt.ylabel("Load [$kN$]")
#    for i in range(1,4):
#        plt.xlabel("Time [$s$]")
#        plt.ylabel("Load [$kN$]")
#        y = sig.medfilt(array[startLoad:startLoad+lenLoad,i])
##        y = f[:,i]
#        plt.plot(x,y)
#        plt.title("Loadcell " + str(i))
#        plt.grid()
#        plt.savefig(".\\Results\\" + os.path.basename(file)[:-4] + "//Loadcell" + str(i) + ".png")
#        plt.close()
#
#
#
##    plot sum of all loadcells    
#    y = sig.medfilt(loadsum)
#    a,b = first_peak(loadsum)
#    c,d = last_peak(loadsum,a)
#    plt.plot(x,y)
#    plt.plot(x[a],y[a],"r.")
#    plt.plot(x[c],y[c],"b.")
#    plt.title("Sum of all Loadcells")
#    plt.xlabel("Time [$s$]")
#    plt.ylabel("Load [$kN$]")
#    plt.grid()
#    plt.savefig(".\\Results\\" + os.path.basename(file)[:-4] + "_Loadcellsum.png")
#    plt.close()
#    
##   plot impulse 
#    y = sp.integrate.cumtrapz(y[a:c],x[a:c],initial = 0)*1000
#    plt.plot(x[a:c],y)
#    plt.ylabel(r"Impulse [$Ns$]")
#    plt.xlabel("Time [$s$]")
#    plt.title("Impulse")
#    plt.grid()
#    plt.savefig(".\\Results\\" + os.path.basename(file)[:-4] + "_imp.png")
#    plt.close()
    
def calc_velo(acc,time,start):
    print(acc.shape)
    print(time.shape)
    corr = sp.integrate.cumtrapz(acc[:start],time[:start],initial = 0)
    vel = sp.integrate.cumtrapz(acc[start:],time[start:],initial = 0)
    slope, intercept, r_value, p_value, std_err = sp.stats.linregress(corr,time[:start])
    truevelo = []    
    for i, txt in enumerate(vel):
        truevelo.append(txt - intercept - slope * i)
    maxvelo = max(truevelo) - min(truevelo)
    x,y = first_peak(acc)
    plt.plot(acc)
    plt.plot(x,y,".")
#    plt.plot(time[start:],vel)
#    plt.plot(time[:start],corr)
#    plt.plot(time[start:],truevelo)
    plt.show()
    return truevelo, maxvelo


#get start peak reliably
#input: loadsum
#def first_peak(array):
#    diff = 0
#    for i, txt in enumerate(array[:-1]):
#        if txt < 0 and diff > txt - array[i+1]:
#            diff = txt - array[i+1]
#            x = i
#            y = txt
#    return x, int(y)
def first_peak(array):
    diff, x, y = 0,0,0
    for i, txt in enumerate(array[:-1]):
        if 10 < diff:
            diff = txt - array[i+1]
        else:
            x = i
            y = txt
    return x, int(y)
#get end of impulse reliably
#input: loadsum and position of first peak
#def last_peak(array,start):
#    x,y = 0,0
#    for i, txt in enumerate(array[start+10:]):
#        if txt < 0:
#            x = i + start + 10
#            y = txt
#            break
#    return x, int(y)
def last_peak(array,start):
    diff, x, y = 0,0,0
    for i, txt in enumerate(array[:-5]):
        if  - 10 > diff:
            diff = txt - array[i+5]
        else:
            x = i
            y = txt
    return x, int(y)

#find the beginning / end
def peaks(array):
    index = sig.find_peaks(-array,distance=10)
    print(len(index))
    plt.plot(array)
    height = []
    for i in index:
        height.append(array[i])
#    #TO DO find first lowest element, overwrite with something(?)
    firsty = min(height)
    firstx = height.index(firsty)
    lasty = height[0]
    lastx = 0
    for i, txt in enumerate(height):
        if lasty > txt:
            lasty = txt
            lastx = i
    if firstx > lastx:
        firstx,lastx=lastx,firstx
        firsty, lasty = lasty, firsty
        return firstx,firsty,lastx,lasty

    
#make a LaTeX ready table out of the result data
def makeTable(path="./Results/result.txt"):
    unit, header, name, number = results(path)
    leg = open(path[:-3]+"tex","w")
    leg.write("""
              \\begin{landscape}
              \\begin{table}[p!]
              \\centering
              \\begin{tabular}{*{""" + str(len(header)) + """"}{l}}
              \\toprule \n""")
    leg.write(listtolatex(header))
    leg.write("&" + listtolatex(unit))
    leg.write("""\\midrule \n""")
    a = number.shape
    for j in range(a[0]):
        leg.write(str(name[j]) + "\t & \t" + listtolatex(number[j][:]))
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
        l += str(i) + "\t & \t"
    l += str(list[-1]) + "\\\\ \n"
    return l
#TO DO turn this snippets into a one-click programm

#take Data at a certain path and clip it to size
def turn_json(array,file=".\\Data\\cracked\\2018-12-04_Rfrs_50_0,3.asc"):
    #make a json file in place of the normal file
    f = open(file[:-4]+".json","w")
    #put the max height in the json file
    json.dump({"maxheight":dropheight(array)},f,sort_keys=True)
    #find start (when is the magnetventil activated?)
    start = np.where(array[:,9]==1)
#    start = findStart(data,0)
    #find end (10 seconds later)
    end = start + 10^6
    #TO DO clip the data further down
    newarray = array[start:end]
    mask = np.ones(newarray.shape[1],bool)
    for i in [0,1,2,3,4,7]:
        mask[i]=0
# delete useless data
    newarray = np.delete(newarray,mask,axis=1)
    print(newarray.shape)

    

    f.close()

    
# values begin at a[38]
# len(a[38]) = 26 for round samples
# a[8] gives the headers
#    0 time 1 s (10.000 times per second)
#    1 last cell 1 kN
#    2 last cell 2 kN
#    3 lastcell 3 kN 
#    4 lasersensor mm
#    5 Telfer 1 V (?)
#    6 Telfer 2 V (?)
#    7 Accelerometer g
    
#    8 time 2 (once per second maybe? not sure)

#    9 Magnetventil (0/1)
#    10 Gate reset (0/1)
#    11 Gate status (0/1)
#    12 Telferreset (0/1)
#    13 Kompressor (0/1)
#    14 Belysning Kamera (camera lights) (0/1)
#    15 Varningsbelysning (warning lights) (0/1)
#    16 Klarsignal (0/1)
#    17 Deriv Telfer 1 ???
#    18 Deriv Telfer 2 ???
#    19 Pos_pulse ???
#    20 Neg_pulse ???
#    21 pos_counts ???
#    22 neg_counts ???
#    23 Dist_up mm
#    24 Dist_down mm 
#    25 load average kN

