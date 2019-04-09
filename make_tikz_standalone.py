# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 08:00:20 2019

@author: kekaun
"""
#turn tikz into standalone files

import os

while True:
    print("Please enter directory!")
    i = input()
    if os.path.isdir(i) == True:
        break

for root, folders, files in os.walk(i):
#    for folder in folders:
#        if os.path.isdir(root + "\\" + folder + "\\tikz\\standalone"):
#            os.remove(root + "\\" + folder + "\\tikz\\standalone")
    if os.path.isdir(root[0] +"\\tikz\\standalone") == False:
        os.makedirs(root[0] +"\\tikz\\standalone")
        print(root[0] +"\\tikz\\standalone")
    for file in files:
#        if file[-15:] == "_standalone.tex":
#            os.remove(root + "\\" + file)
#        elif
        if file[:4] == "tikz" and file[-4:] ==".tex" and file[-15:] !="_standalone.tex":
            old = open(root +"\\" + file,"r")
            new = open(root +"\\standalone\\" + file[:-4] + "_standalone.tex","w")
            new.write(r"""\documentclass{standalone}
\usepackage{helvet}
\renewcommand\familydefault{\sfdefault}
\usepackage[T1]{fontenc}
\usepackage{textcomp}
\usepackage{comment} 
\usepackage{tikz} 
\usetikzlibrary{arrows.meta,calc,datavisualization,patterns,shapes.arrows} 
\begin{document}""" + "\n")
            for line in old.readlines():
                new.write(line)
            new.write("""\n\\end{document}""")
            new.close()
            old.close()
