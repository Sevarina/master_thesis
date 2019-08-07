import os
import PySimpleGUI as sg
import pandas as pd
import GUI as gui

import coreprogram as core

index = ["Name", "Number", "Energy level", "Thickness", "Drop weight", "Drop height", "Age", "Velocity", "Force", "Acceleration", "Displacement", "Broken/Cracked", "Crack area", "Opening angle"]    
data =  ["", "",r"\([\text{kJ}]\)", r"\([\text{mm}]\)", r"\([\text{kg}]\)", r"\([\text{mm}]\)", r"\([\text{days}]\)", r"\(\big[\frac{\text{m}}{\text{s}}\big]\)", r"\([\text{kN}]\)", r"\(\Big[\frac{\text{m}}{\text{s}^\text{2}}\Big]\)", r"\([\text{mm}]\)", " ", r"\([\text{mm}^\text{2}]\)", r"\([\text{\textdegree}]\)"]
res = pd.DataFrame(index = index, data = data)
res = res.transpose()
res = res.set_index("Name")
res_path = r"C:\Users\kekaun\OneDrive - LKAB\Desktop\try\test_analysis\Results\result.xlsx"
res.to_excel(res_path)
