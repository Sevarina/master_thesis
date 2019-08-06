import os
import PySimpleGUI as sg
import pandas as pd
import GUI as gui

import coreprogram as core

file = r"C:\Users\kekaun\OneDrive - LKAB\Desktop\try\new_data.ASC"
project = r"C:\Users\kekaun\OneDrive - LKAB\Desktop\try\test_analysis"

##test data
#### append new test to old test_data
df = gui.UI_open_df(data = project, filename = "test_data")
if os.path.basename(file)[:-4] in df.index:
    sg.PopupError("File with this name already exists in test_data")
num = df.loc[:,"Number"].iloc[-1,] + 1
test_df = pd.Series(gui.input_test_data(file, num))
test_df = test_df.rename(test_df.loc["Name"])
test_df = test_df.drop("Name")
df = df.append(test_df)
core.save_df(data = project, filename = "test_data", df = df)