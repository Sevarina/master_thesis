# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 13:44:53 2019

@author: kekaun
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

direct=".\\Results\\result.csv"

res = pd.read_csv(direct,sep=";")
#unit = res.query("""Broken/Cracked == ["cracked"]""") 
#unit = res.lookup("broken",["Broken/Cracked"])
#leg = res[res.Name != "NaN"]
#num = pd.Series(leg)
#print(unit)
#df = pd.DataFrame.from_records(np.array([data,status]).transpose(),
#                               columns = ['Data','Status'])
#index = pd.MultiIndex.from_list
#fancy = list(res.columns)

#boy = res.iloc[0,:]


#print(res.drop(res.index[0]))
#unit = res.iloc[0]
#unit = unit.drop(columns = ['Name','Broken/Cracked'])
#print(unit)
res = res.drop(res.index[0])
mask = res['Broken/Cracked'] == 'cracked'
res = res.drop(['Name','Broken/Cracked'],axis = 1)
res = res.astype(float)
crack = res[mask]
broke = res[~mask]
second = res.copy()
#second = res.drop("Name",axis = 1)
path = r"C:\Users\kekaun\OneDrive - LKAB\playData"
for i in res.columns[1:]:
    second = second.drop(i,axis = 1)
    for j in second.columns:
#        plt.figure()
        plt.plot(crack[i].astype(float),crack[j].astype(float),"b.",label="cracked")
        plt.plot(broke[i].astype(float),broke[j].astype(float),"r.",label="broken")
        plt.xlabel(i + unit[i])
        plt.ylabel(j + unit[j])
#        plt.xlabel(i + "\t[$"+ unit[i][3:-3] + "$]")
#        plt.ylabel(j + "\t[$"+ unit[j][3:-3] + "$]")
        dx = (plt.xlim()[1] - plt.xlim()[0]) * 0.01
        dy = (plt.ylim()[1] + plt.ylim()[0]) * 0.01
        plt.grid()
        for k in res.index:
            print(type(res.iloc[k-1][j]))
#            print(res.iloc(int(k)))
            plt.annotate(k-1,(res.iloc[k-1][j]+dy,res.iloc[k-1][i]+dx))
#            print(res.iloc[k-1][i])
#            plt.annotate(k, (res[i,k] + dx, res[j,k] + dy))
#        for k, txt in enumerate(crack):
#                    plt.annotate(txt, (xb[k]+dx, yb[k]+dy))
#        for k, txt in enumerate(lc):
#                    plt.annotate(txt, (xc[k]+dx, yc[k]+dy))
        filename = path + "\\" + j.replace(" ","-") + "_" + i.replace(" ","-") + ".png"
        plt.savefig(filename,format="png")

        plt.close()

    

#cracked = res[res['Broken/Cracked'] == 'cracked',:]
#cracked = res[res['Broken/Cracked'] == 'cracked']
#boy.drop(columns='Broken/Cracked')
#print(boy)
#cracked = cracked.append(boy)
#fancy = res.columns
#print(fancy)

#cracked.drop(columns='Broken/Cracked')
#cracked = res['Broken/Cracked'] == 'cracked'
#print('all:\n', res)
#print('\ncracked:\n',cracked)
#cracked.columns = [fancy,boy]
#nuage = cracked.drop(["Broken/Cracked","Drop height","Velocity"], axis=1)
#
#
#nuage.to_latex("flopsy.tex",escape=False,index=False)
#thisfile = open("./something.tex","w")
#res.set_index("Broken/Cracked",inplace=True)
#full = pd.MultiIndex.from_frame(res)
#print(unit)
#res.to_latex("yup.tex",na_rep="",escape=False,index=False)
#nope.to_latex("why.tex",na_rep="",escape=False,index=False)

#print(res)
#res.to_latex("flopsy.tex",columns=["Name"],escape=False,index_names=False)