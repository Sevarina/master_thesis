import numpy as np
import statistics as stat
import matplotlib as mpl
#make all plots look nice
mpl.style.use('classic')
from matplotlib import rc
import matplotlib.pyplot as plt

import scipy as sp
import scipy.signal as sig
import scipy.integrate as integrate
from scipy.optimize import curve_fit
import seaborn as sns
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



file=r"C:\Users\kekaun\OneDrive - LKAB\roundSamples\Data\cracked\2018-11-29_Rfrs_75_1,0.npy"

#open array
array = np.load(file)


# plot accel
#    x = array[startAccel:startAccel+lenAccel,0]
#    accel = sig.medfilt(array[startAccel:startAccel+lenAccel,5])
x = array[:,0]
print(array.shape)
#accel = array[5815216:5915216,5]
#plt.plot(accel)
plt.plot(array[:,5])
bottom,top = plt.ylim()
if bottom < - 1000:
    plt.ylim(bottom=-1000)
plt.ylabel(r"Acceleration \Big[\(\frac{\text{m}}{\text{s}^2}\)\Big]", usetex=True)
plt.xlabel(r"Time \([\text{s}]\)", usetex=True)
#    plt.title("Acceleration")
plt.grid()


    
###   plot calc velocity
##    x = range(0,200)
##    y = velo
##    plt.plot(x,y)
##    plt.ylabel(r"Calculated Velocity [$m/s$]")
##    plt.xlabel("Time [$s$]")
##    plt.title("Calculated Velocity")
##    plt.grid()
##    plt.savefig(".\\Results\\" + os.path.basename(file)[:-4] + "//Vel.png")
##    plt.close()
##   write_appendix(app,os.path.basename(file)[:-4] + "/Vel.png")
#        
##    load cells
#    x = array[startLoad:startLoad+lenLoad,0]
##    x = array[startLoad+950:startLoad+1020,0]
#    for i in range(1,4):
#        plt.xlabel(r"Time \([\text{s}]\)", usetex=True)
#        plt.ylabel(r"Load \([\text{kN}]\)", usetex=True)
#        y = sig.medfilt(array[startLoad:startLoad+lenLoad,i])
##        y = f[:,i]
#        plt.plot(x,y)
##        plt.title(os.path.basename(file)[:-4] + " Loadcell " + str(i))
#        plt.grid()
#        plt.savefig(".\\Results\\" + os.path.basename(file)[:-4] + "//Loadcell" + str(i) + ".png")
#        plt.close()
#        write_appendix(app,os.path.basename(file)[:-4] + "/Loadcell" + str(i) + ".png", "Loadcell " + str(i))
#        
##    plot sum of all loadcells    
#    y = sig.medfilt(loadsum)
##    a,b = first_peak(loadsum)
##    c,d = last_peak(loadsum,a)
#    plt.plot(x,y)
##   TO DO, fix those fucks!
##    plt.plot(a,array[b+startLoad][0],"r.")
##    plt.plot(c,array[d+startLoad][0],"b.")
##    plt.title("Sum of all Loadcells")
#    plt.xlabel(r"Time \([\text{s}]\)", usetex=True)
#    plt.ylabel(r"Load \([\text{kN}]\)", usetex=True)
#    plt.grid()
#    plt.savefig(".\\Results\\" + os.path.basename(file)[:-4] + "//Loadcellsum.png")
#    plt.close()
#    write_appendix(app,os.path.basename(file)[:-4]+ "/Loadcellsum.png","Sum of all loadcells")
#    
###   plot impulse 
##    print(loadsum.shape)
##    print(x.shape)
##    y = sp.integrate.cumtrapz(loadsum[a:c],x[a:c],initial = 0)*1000
##    plt.plot(x[a:c],y)
##    plt.ylabel(r"Impulse [$Ns$]")
##    plt.xlabel("Time [$s$]")
##    plt.title("Impulse")
##    plt.grid()
##    plt.savefig(".\\Results\\" + os.path.basename(file)[:-4] + "//imp.png")
##    plt.close()
##    write_appendix(app,os.path.basename(file)[:-4] + "/imp.png")
##     
## plot laser
#    y = sig.medfilt(array[startLoad:startLoad+2000,4])
#    x = array[startLoad:startLoad+2000,0]
#    plt.plot(x,y)
#    bottom,top= plt.ylim()
#    if bottom < -100 and top > -100:
#        plt.ylim(bottom=-100)
#    plt.xlabel(r"Time \([\text{kN}]\)", usetex=True)
#    plt.ylabel(r"Displacement \([\text{mm}]\)", usetex=True)
#    plt.grid()
#    plt.savefig(".\\Results\\" + os.path.basename(file)[:-4] + "/displacement.png")
#    plt.close()
#    write_appendix(app,os.path.basename(file)[:-4] + "/displacement.png","Displacement")    

