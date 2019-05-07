import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from adjustText import adjust_text
import scipy as sp
import scipy.stats

import os.path

direct=r"C:\Users\kekaun\OneDrive - LKAB\Square Samples\energy_schema.xlsx"
#
sheet = pd.read_excel(direct,sheet_name="0,5 kj steps",indec_col=0)

limit = 16

#plt.plot(sheet["Hit"][:limit],sheet["Energy [kJ]"][:limit],"b.")

plt.step(sheet["Hit"][1:limit+1],sheet["Total energy [kJ]"][:limit],where = "pre")
plt.xlabel("Number of impacts [$-$]")
#plt.xlabel("Impact number [$-$]")
plt.ylabel("Cumulative energy input [$kJ$]")
#plt.ylabel("Impact energy [$kJ$]")
plt.ylim(bottom = 0)
plt.xlim(left = 0, right = limit)

plt.xticks(np.arange(0, limit -1 , 2.0))
plt.grid()
plt.show()
         
