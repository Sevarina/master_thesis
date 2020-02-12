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
mpl.rcParams['text.latex.preamble'] = [r'\usepackage{amsmath}' , r'\usepackage[T1]{fontenc}'] 

#"fix" matplotlib font - it´s arial instead of helvetica but better than nothing
#plt.rcParams['mathtext.fontset'] = 'custom'
#mpl.rcParams['font.sans-serif'] = "Computer Modern"
mpl.rcParams['font.family'] = "serif"
#mpl.rcParams['mathtext.default']='default'
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
        "Energy per area" : r"\(\big[\frac{\text{kJ}}{\text{m}^2}\big]\)",
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


zero = 1.2 #kJ
step = 1.4 #kJ
max_step = 10
area = 1.3 ** 2 #m2
impact_energy = [zero]
cum_energy = [zero]

impact_energy_area = [zero * area]
cum_energy_area = [zero * area]
impact_num = [1]

for i in range(1, max_step):
    impact_num.append(int(i+1))
    impact_energy.append(zero + i * step)
    impact_energy_area.append(impact_energy[i]*area)
    cum_energy.append(cum_energy[i-1] + impact_energy[i])
    cum_energy_area.append(cum_energy[i] * area)
   
arrays = [['Impact Energy','Impact Energy','Cumulative Energy','Cumulative Energy'],
          [latex_unit['Energy per area'],latex_unit['Energy level'],latex_unit['Energy per area'],latex_unit['Energy level']]]
tuples = list(zip(*arrays))
multi = pd.MultiIndex.from_tuples(tuples)
    
df = pd.DataFrame(data=[impact_energy, impact_energy_area, cum_energy, cum_energy_area], index = multi)

#df = pd.DataFrame(data=[impact_num, impact_energy, cum_energy], index = ['Number of Impacts', 'Impact Energy', 'Cumulative Energy'])
df = df.T
df.insert(0,'Number of Impact',impact_num)

#df.loc[-1] = [latex_unit['Number'],latex_unit['Energy per area'],latex_unit['Energy per area']]
#df = df.sort_index()
print(df.to_latex(index = False, escape = False, float_format="{:0.1f}".format, decimal=','))

plt.step(impact_num,cum_energy_area,where = "pre")
plt.xlabel("Number of impacts [$-$]")
plt.ylabel("Cumulative energy input [$kJ$]")
plt.ylim(bottom = 0, top = cum_energy_area[-1] + 10)
plt.xlim(left = 0)
plt.grid()
plt.show()
#plt.savefig(r"C:\Users\kekaun\OneDrive - LKAB\Square Samples\cum_energy.png")
#plt.close()
##
#plt.plot(impact_num,impact_energy_area,'b.')
#plt.xlabel("Number of impacts [$-$]")
#plt.ylabel("Energy input per impact [$kJ$]")
#plt.ylim(bottom = 0)
#plt.xlim(left = 0, right = impact_num[-1] + 1)
#plt.grid()
#
#plt.savefig(r"C:\Users\kekaun\OneDrive - LKAB\Square Samples\impact_energy.png")
#plt.close()

    

