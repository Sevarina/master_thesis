# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 14:17:25 2019

@author: kekaun
"""

from pydoc import help  # can type in the python console `help(name of function)` to get the documentation
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import scale
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from scipy import stats
from IPython.display import display, HTML

import matplotlib
matplotlib.axes.Axes.pcolormesh
matplotlib.figure.Figure.colorbar
matplotlib.colors
matplotlib.colors.LinearSegmentedColormap
matplotlib.colors.ListedColormap
matplotlib.cm
matplotlib.cm.get_cmap

blackoutside = {
        'blue':  ((0.0, 0.0, 0.0),
                (0.3, 0.0, 0.0),
                 (0.5, 1.0, 1.0),
                 (0.7, 1.0, 1.0),
                 (1.0, 0.0, 0.0)),
                 
        'green': ((0.0, 0.0, 0.0),
                  (0.3, 0.0, 0.0),
                  (0.5, 1.0, 1.0),
                  (0.7, 0.0, 0.0),
                  (1.0, 0.0, 0.0)),

        'red': ((0.0, 0.0, 0.0),
                 (0.3, 1.0, 1.0),
                 (0.5, 1.0, 1.0),
                 (0.7, 0.0, 0.0),
                 (1.0, 0.0, 0.0))}

whiteoutside = {
        'blue':  ((0.0, 1.0, 1.0),
                (0.3, 0.0, 0.0),
                 (0.5, 0.0, 0.0),
                 (0.7, 1.0, 1.0),
                 (1.0, 1.0, 1.0)),
                 
        'green': ((0.0, 1.0, 1.0),
                  (0.3, 0.0, 0.0),
                  (0.7, 0.0, 0.0),
                  (1.0, 1.0, 1.0)),

        'red': ((0.0, 1.0, 1.0),
                 (0.3, 1.0, 1.0),
                 (0.5, 0.0, 0.0),
                 (0.7, 0.0, 0.0),
                 (1.0, 1.0, 1.0))}

# figures inline in notebook
#matplotlib inline
        
plt.register_cmap(name='LKAB', data=blackoutside)

np.set_printoptions(suppress=True)

DISPLAY_MAX_ROWS = 20  # number of max rows to print for a DataFrame
pd.set_option('display.max_rows', DISPLAY_MAX_ROWS)

data = pd.read_csv(".\\Results\\result.csv",sep=";")

data = data.drop(data.index[0])
mask = data['Broken/Cracked'] == 'cracked'
data = data[mask]
data = data.drop(["Broken/Cracked","Drop height","Velocity"],axis = 1)
data.Name = data.Name.astype(str)
X = data.loc[:,"Energy level":].astype(float)
Y = data.Name


#pd.tools.plotting.scatter_matrix(X, diagonal="kde")
#plt.tight_layout()
#plt.show()

corr = X.corr()

corr = corr.round(4)

sns_plot = sns.heatmap(corr,  center = 0, annot=True, fmt='.2f',cmap = "LKAB", vmin = -1.0, vmax = 1.00,)
plt.tight_layout()
fig = sns_plot.get_figure()
fig.savefig("heatmap.png")

corr.to_latex(".\\Results\\correlation.tex",na_rep="",escape=False,decimal=",")
columns = np.full((corr.shape[0],), True, dtype=bool)
for i in range(corr.shape[0]):
    for j in range(i+1, corr.shape[0]):
        if corr.iloc[i,j] >= 0.9  :
            if columns[j]:
                columns[j] = False
#data = data.drop("Name",axis = 1)


selected_columns = corr.columns[columns]
print(corr.columns)
print(selected_columns)
#corr = corr[selected_columns]
##corr = corr[selected_columns]
#print(corr.shape)
#sns.heatmap(corr)
