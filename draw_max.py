#!/usr/bin/python3

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from scipy.optimize import curve_fit
from scipy import interpolate
import matplotlib.ticker as mticker 

mpl.rcParams['font.serif'] = "Times New Roman"
mpl.rcParams['font.family'] = "serif"

array = pd.read_excel(r"C:\Users\kekaun\OneDrive - LKAB\Desktop\max_diagram.xlsx", index_col = "MRMR")
plt.figure(num = 1, figsize=(7,5))
plt.grid(color = (1,1,1), marker = "+")

plt.ylim(bottom = 0, top = 100)
plt.xlim(left = 0, right = 80)

##dots
#plt.plot(array["Stable"],array.index, "b.")
#plt.plot(array["Transitional"],array.index, "y.")
#plt.plot(array["Caving"], array.index, "r.")


from scipy.interpolate import UnivariateSpline

x= np.linspace(0,80, num = 1000)



stable_spline = UnivariateSpline(array.loc[14:,"Stable"], array.index[2:])
transit_spline = UnivariateSpline(array.loc[:88,"Transitional"], array.index[:-2])
cave_spline =  UnivariateSpline(array.loc[:82,"Caving"], array.index[:-3])
vertical = np.linspace(100,100, num = 1000)
horizontal = np.linspace(0, 0, num = 1000)


#fill
plt.fill_between(x, vertical, stable_spline(x), facecolor = (0.4588, 0.6980, 1))
plt.fill_between(x, stable_spline(x), transit_spline(x), facecolor = (0.3529, 0.7294, 0.6549))
plt.fill_between(x, transit_spline(x), horizontal, facecolor = (0.4784, 0.7137, 0.2824))

#plt.plot(x, stable_spline(x), color = "xkcd:azure")
plt.plot(x, transit_spline(x), label = "HR for \nrectangular \nore body", color = "#b7ff7bfd")
plt.plot(x, cave_spline(x), label = "HR for an \nequidimensional \nore body without \nhoop  stress \ncorrection", color = "#7bffe4fd")


plt.text(51.3,35.875, "Caving")
plt.text(27,66.25, "Transitional")
plt.text(12,85, "Stable")

plt.xlabel("Hydraulic radius = radius / perimeter")
plt.ylabel("MRMR")
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
plt.gca().xaxis.set_major_formatter(mticker.FormatStrFormatter('%d m'))

plt.tight_layout()

#stable_x= np.linspace(array.index[2], array.index[-1], num = 1000)
#stable_interpol = interpolate.interp1d(array.index[2:], array.loc[14:,"Stable"])
#
#print(array.index[:-3])
#print(array.loc[:88,"Transitional"])
#
#transit_x= np.linspace(array.index[0], array.index[-3], num = 1000)
#transit_interpol = interpolate.interp1d(array.index[:-2], array.loc[:88,"Transitional"])
#
#
#plt.plot(stable_interpol(stable_x), stable_x)
#plt.plot(transit_interpol(transit_x), transit_x)
#def func(x, a, b, c, d):
#    return a*x**3  + b*x**2 + c*x + d
#
#def exp(x, a, b, c):
#    return a * np.exp(-b * x) + c
#
#

#near = curve_fit(func, array.index[2:], array.loc[20:,"Stable"])
#far = curve_fit(func, array.index[:-2], array.loc[:80,"Transitional"])
#here = curve_fit(func, array.index[:-2], array.loc[:80,"Caving"])
#
#
#stable_pop,_ = curve_fit(func, array.loc[20:,"Stable"], array.index[2:])
#transit_pop,_ = curve_fit(func, array.loc[:80,"Transitional"], array.index[:9])
#cave_pop,_ = curve_fit(func, array.loc[:80,"Caving"], array.index[:9]
#)
#
#estimate_x = []
#estimate_stable = []
#estimate_transit = []
#estimate_cave = []
#for i in range(0,80):
#    estimate_x.append(i)
##    estimate_stable.append(near[0][0] * i**3 + near[0][1] * i**2 + near[0][2] * i + near[0][3]) 
##    estimate_x.append(i)
##    estimate_transit.append(far[0][0] * i**3 + far[0][1] * i**2 + far[0][2] * i + far[0][3])
##    estimate_cave.append(here[0][0] * i**3 + here[0][1] * i**2 + here[0][2] * i + here[0][3])
#
##    estimate_stable.append(near[0][0] * i**2 + near[0][1] * i + near[0][2]) 
##    estimate_transit.append(far[0][0] * i**2 + far[0][1] * i + far[0][2])
##    estimate_cave.append(here[0][0] * i**2 + here[0][1] * i + here[0][2])
#    
#    estimate_stable.append(stable_pop[0] * i**2 + stable_pop[1] * i + stable_pop[2]) 
#    estimate_transit.append(transit_pop[0] * i**2 + transit_pop[1] * i + transit_pop[2])
#    estimate_cave.append(cave_pop[0] * i**2 + cave_pop[1] * i + cave_pop[2])
#    
#    
#plt.plot(array.loc[:,"Stable"],  func(array.loc[:,"Stable"],*stable_pop))
#plt.plot(array.loc[:,"Transitional"],  func(array.loc[:,"Transitional"],*transit_pop))
#plt.plot(array.loc[:,"Caving"],  func(array.loc[:,"Caving"],*cave_pop), )        
##plt.plot(estimate_x,estimate_stable)
##plt.plot(estimate_x,estimate_transit)
##plt.plot(estimate_x,estimate_cave)
#
