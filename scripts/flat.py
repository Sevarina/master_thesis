# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 11:12:42 2019

@author: kekaun
"""

#flatten a latex file and replace all \input{tikz} with include{tikz.pdf} 

import os
import re
import codecs

while True:
    print("Please enter file!")
    i = input()
    if os.path.isfile(i) == True and i[-4:] == ".tex":
        break
    else:
        print(i + " is not a file")
        continue

os.chdir(os.path.dirname(i))

##################### flatten the file
old = codecs.open(i,"r", "utf-8")
new = codecs.open(i[:-4] + "_flat.tex","w", "utf-8")

findtikz = re.compile(r"(tikz/tikz)(\d+)(.tex)")

findinput = re.compile(r"(%?\\input{)(.+)(})")
counter = 0
for line in old.readlines():
    mo = findinput.search(line)
    if mo != None and mo[1][0] !="%":
        
        #see if the input is a tikz
        start = line.find(r"\\input")
        if mo[2].find("tikz") != -1:
            tikz = findtikz.search(mo[1])
            if tikz != None:
                line = line[:start] + r"\include{" + tikz[2] + "standalone/tikz" + tikz[2] + "_standalone.png}\n"
            continue
        else:
            #otherwise look at the file, open it and write everything directly into the flat file
            inputfile = open(mo[2]+".tex",encoding="utf8")
            for row in inputfile.readlines():
                findtikzmatch = re.compile(r"(\\input{tikz/)(.*)(.tex})")
                match = findtikzmatch.search(row)
                if match != None:
#                    start = line.find(r"\\input")
                    row = r"\includegraphics{tikz/standalone/" + match[2] + "_standalone.png}\n"
                new.write(row.replace("\u200e",""))
            inputfile.close()
    else:
        new.write(line)
new.close()
old.close()

