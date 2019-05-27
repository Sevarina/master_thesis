# -*- coding: utf-8 -*-
"""
Created on Tue May 21 14:12:35 2019

@author: kekaun
"""
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate
import scipy.signal as sig

def helpline(start,end,offset,array):
    hline = np.ones((end-start,))
    for i in range(end-start):
        hline[i] = offset * i / (end - start)
    for j in range(start,end):
        array[j] = array[j] + hline[j - start]
    return array

file="C:\\Users\\kekaun\\OneDrive - LKAB\\roundSamples\\extraAccel\\2019-04-16_Rfrs_75_0,5_vertical.npy"
array = np.load(file)
peak = np.argmax(array[:,1])

#2019-04-16_Rfrs_75_0,5_horizontal
##total coordinates 
start = peak - 10
end = peak + 500

##off set coordinates
hstart = peak - 5 - start
hend = peak + 80 - start




plt.ylabel(r"Acceleration [$\frac{m}{s^2}$]")
plt.xlabel("Time [$s$]")
plt.grid()
time = array[start:end,0]/1000
#plt.plot(time,array[start:end,1])



#    dx=0.0001
#    x = time

velo = integrate.cumtrapz(array[start:end,1],x = time,initial = 0)

hine = helpline(hstart,hend,0.02,velo)
hine[hend:] = sig.detrend(hine[hend:])

disp = integrate.cumtrapz(hine,x = time,initial = 0)
#nuvelo = velo + hine
#nudisp =  sig.detrend(disp)
#    peak = np.argmax(array[:,1])
#nuvelo = sig.detrend(velo,type="linear")
#plt.plot(hine)
#plt.plot(time,velo)
#plt.plot(time,hine)
plt.plot(time,disp)
#plt.plot(time,nudisp)
plt.show()
#    plt.savefig(file[:-4] + ".png")


    