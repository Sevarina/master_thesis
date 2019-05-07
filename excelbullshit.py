# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 13:44:53 2019

@author: kekaun
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from adjustText import adjust_text
import scipy as sp
import scipy.stats
import matplotlib
import os.path

direct=".\\Results\\result.csv"
#
res = pd.read_csv(direct,sep=";")
##unit = res.query("""Broken/Cracked == ["cracked"]""") 
##unit = res.lookup("broken",["Broken/Cracked"])
##leg = res[res.Name != "NaN"]
##num = pd.Series(leg)
##print(unit)
##df = pd.DataFrame.from_records(np.array([data,status]).transpose(),
##                               columns = ['Data','Status'])
##index = pd.MultiIndex.from_list
##fancy = list(res.columns)
#
##boy = res.iloc[0,:]
#
#
#def write_legend(direct,df):
#    print(df)
#    leg = open(os.path.dirname(direct) + "\\legend.tex","w")
#    leg.write("""\\begin{table}
#    \\centering
#    \\begin{tabular}{ll}
#    \\toprule
#    Name & Symbol \\\\
#    \\midrule \n""")
#    for l, m in enumerate(df["Name"]):
#        leg.write(str(m) + "\t&\t" + str(l + 1)+"\t\\\\\n")
#    leg.write("""\\bottomrule
#\\end{tabular}
#\\caption{Legend for the symbols assigned to tests}
#\\label{tab:leg}
#\\end{table}
#              """)
#    leg.close()
#    
#write_legend(direct,res.drop(res.index[0]))
##print(res.drop(res.index[0]))
mask = res['Broken/Cracked'] == 'cracked'
res = res.drop(['Name','Broken/Cracked'],axis = 1)
unit = res.iloc[0]
#
res = res.drop(res.index[0])
#
res = res.astype(float)
crack = res[mask]
mask1 = res['Thickness'] == 75
crack.drop("Thickness",axis = 1)
crack = crack[mask1]

print(crack)
#broke = res[~mask]
#second = res.copy()
second = crack.copy()
#
path = r"C:\Users\kekaun\OneDrive - LKAB\roundSamples"
#
#for i in res.columns:
for i in crack.columns:
    second = second.drop(i,axis = 1)
    for j in second.columns:
        fig = plt.figure()
        ax = plt.subplot(111)

        plt.plot(crack[i].astype(float),crack[j].astype(float),"b.", markersize=12,label="cracked")
#        plt.plot(broke[i].astype(float),broke[j].astype(float),"r.",label="broken")

        plt.xlabel(i + " [$" + unit[i][2:-2] + "$]")
        plt.ylabel(j + " [$" + unit[j][2:-2] + "$]")

        plt.grid()
#        texts = [plt.text(res.iloc[k-1][i], res.iloc[k-1][j], k, ha='right', va='center') for k in res.index]
#        adjust_text(texts)
#        slope, intercept, r_value, p_value, std_err = sp.stats.linregress(crack[i].astype(float),crack[j].astype(float))
#        sortx = list(crack[i].astype(float).sort_values())
#        sorty =[]
#        for m in sortx:
#            sorty.append(m * slope + intercept)
#        ax.plot(sortx, sorty,"b--", label="R = %0.04f \nk = %0.02f \nd = %0.02f" %(r_value,slope,intercept))
#        chartBox = ax.get_position()
#        ax.set_position([chartBox.x0, chartBox.y0, chartBox.width*0.8, chartBox.height])
#        ax.legend(loc='upper center', bbox_to_anchor=(1.2, 0.8), shadow=True, ncol=1)

        filename = path + "\\try\\" + j.replace(" ","-") + "_" + i.replace(" ","-") + ".png"
        plt.savefig(filename,format="png")
        plt.close()