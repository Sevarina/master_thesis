#!/usr/bin/python3
import PySimpleGUI as sg
import os
import pandas as pd
import datetime
import re
import numpy as np

import coreprogram as core
import clean_file as clean

layout_initial = [
        [sg.Text("What do you want to do?")],
        [sg.Button(button_text="Automatically process data", tooltip = "Datasets will be converted from .asc and analysed")],
        [sg.Button(button_text="Manually process data", tooltip = "The user can choose which datasets to analyse and what to do with them")],
        [sg.Button(button_text="Close program")]
        ]

layout_manual = [
        [sg.Text("What do you want to do?")],
        [sg.Button(button_text="Add a new data set")],
        [sg.Button(button_text="Plot all datasets")],
        [sg.Button(button_text="Plot linear regression of parameters")],
        [sg.Button(button_text="Close program")]
        ]
    
layout_new_dataset = [
        [sg.Text("Add new dataset")],
        [sg.InputText(), sg.FileBrowse()],
        [sg.Text("Sample type:")],
        [sg.Radio('Round', "RADIO1", default=True, key = "Round"),
    sg.Radio('Square', "RADIO1", key = "Square")],
        [sg.Submit(), sg.Cancel()]   
        ]

layout_plot_datasets = [ [sg.Text('Please navigate to test data', size=(30, 1))],
    [sg.Text('Basic data array', size=(15, 1), auto_size_text=False, justification='right'),      
     sg.InputText("C:/Users/kekaun/OneDrive - LKAB/roundSamples/Data/basic_array", key = "data"), sg.FolderBrowse()],
    [sg.Text('Result folder' , size=(15, 1), auto_size_text=False, justification='right'),      
     sg.InputText("C:/Users/kekaun/OneDrive - LKAB/roundSamples/Results", key = "result"), sg.FolderBrowse()],
    [sg.Submit(), sg.Cancel()]      
     ]

layout_auto = [
        [sg.Text('Please choose to test data folder', size=(30, 1))],
        [sg.InputText("C:/Users/kekaun/OneDrive - LKAB/Desktop/Try", key = "data"), sg.FolderBrowse()],
        [sg.Submit(), sg.Cancel()]
        ]

def make_add_test_layout(sample):
    layout = [
        [sg.Text("Please enter data for sample: " + sample)],
        [sg.Text("Sample type"), sg.Radio('Round', "RADIO1", default=True, key = "Round"),
    sg.Radio('Square', "RADIO1", key = "Square") ],
         [sg.CalendarButton("Casting date", target = "cast", key = "cast_date"), sg.InputText("", key = "cast", disabled = True)], 
         [sg.CalendarButton("Testing date", target = "test", key = "test_date"), sg.InputText("", key = "test", disabled = True)],
         [sg.Text("Drop weight"), sg.Combo(['50 kg', '100 kg', "200 kg", "500 kg", "1000 kg"], key = "weight")],
         [sg.Text("Sample thickness [mm]"), sg.InputText(key = "thickness", do_not_clear = True)],
         [sg.Text("Broken or cracked"), sg.Radio('Broken', "RADIO2", default=True, key = "Broken", enable_events = True), sg.Radio('Cracked', "RADIO2", default = False, key = "Cracked", enable_events = True) ]    
        ]
    for i in range(1,5):
        layout.append([
                sg.Text("Crack " + str(i), visible = False, key = "crack_" + str(i)), 
                sg.Text("Length [mm]", visible = False, key = "crack_" + str(i) + "_len_txt"), 
                sg.Input(key = "crack_" + str(i) + "_len", visible = False), 
                sg.Text("Width [mm]",key = "crack_" + str(i) + "_width_txt", visible = False), 
                sg.Input(key = "crack_" + str(i) + "_width", visible = False)])
    layout.append([sg.Submit(), sg.Cancel()])
    return layout

def new_Dataset():
    window_new_dataset = sg.Window('Drop test program', default_element_size=(40, 1)).Layout(layout_new_dataset)
    event, values = window_new_dataset.Read()
    if event == "Cancel" or event == None:
        window_new_dataset.Close()
    elif values["Browse"][-4:].lower() == ".asc" and os.path.isfile(values["Browse"]):
        window_new_dataset.Close()
        sg.Popup("This will take a minute, please wait", non_blocking=True, auto_close=True)
        if values["Round"]:
            clean.clean_array(file = values["Browse"], sample_type = "Round")
        else:
            clean.clean_array(file = values["Browse"], sample_type = "Square")
        sg.Popup("Conversion completed!")
    else: 
        sg.Popup("Please choose an existing .asc file!")

def plot_all():
    window_plot = sg.Window('Drop test program', default_element_size=(40, 1)).Layout(layout_plot_datasets)
    event, values = window_plot.Read()
    if event == "Submit":
        core.calc(data = values["data"], results = values["result"])
        window_plot.Close()
    else: window_plot.Close()

def manual():
    window_manual = sg.Window('Drop test program', default_element_size=(40, 1)).Layout(layout_manual)
    event, values = window_manual.Read()
    print(event)
    if event == "Add a new data set":
        window_manual.Close()
        new_Dataset()
    if event == "Plot all datasets":
        window_manual.Close()
        plot_all()
    if event =="Plot linear regression of parameters":
        sg.Popup("Not yet implemented!")
    elif event == None or event == "Cancel":
        window_manual.Close()

def make_test_dir(direct):
    basic_array = (direct + "//test_analysis//Data//basic_array")
    if os.path.isdir(basic_array) == False:
        os.makedirs(basic_array)
    metadata = direct + "//test_analysis//Data//metadata"
    if os.path.isdir(metadata) == False:
        os.makedirs(metadata)
    results = direct + "//test_analysis//Results"
    if os.path.isdir(results) == False:
        os.makedirs(results)
    return basic_array, metadata, results

def check_crack(values):
    for i in range(1,5):
        if re.search("\D", values["crack_" + str(i) + "_len"]) != None or re.search("\D", values["crack_" + str(i) + "_width"]) != None:
            return (True, i)
        else: return (False, 0)

def calc_crack(values):
    area = 0
    num = 0
    sum_l = 0 
    sum_area = 0
    med_width = ""
    angle = ""
    for i in range(1,5):
         if values["crack_" + str(i) + "_len"] != "" and values["crack_" + str(i) + "_width"] != "":
            area = area + int(values["crack_" + str(i) + "_len"]) * int(values["crack_" + str(i) + "_width"])
            num += 1
            sum_l +=  int(values["crack_" + str(i) + "_len"])
            sum_area += int(values["crack_" + str(i) + "_len"]) * int(values["crack_" + str(i) + "_width"])
            med_width = np.round(sum_area/sum_l, 0)
            if values["thickness"] != "":
                angle = np.round(2 * np.arctan(med_width/2/int(values["thickness"])),1)
    return (area, num, med_width, angle)

def make_test_data(metadata, file_list):
    data = pd.DataFrame()
    num = 1
    
    print(file_list)
    for file in file_list:
        window_test_data = sg.Window("Drop test program").Layout(make_add_test_layout(os.path.basename(file[:-4])))
        while True:
            event, values = window_test_data.Read()
            print(values)
            if event == None or event == "Cancel":
                window_test_data.Close()
                break
            elif event == "Cracked":
                for i in range(1,5):
                    window_test_data.Element("crack_" + str(i)).Update(visible = True)
                    window_test_data.Element("crack_" + str(i) + "_len_txt").Update(visible = True)
                    window_test_data.Element("crack_" + str(i) + "_len").Update(visible = True)
                    window_test_data.Element("crack_" + str(i) + "_width_txt").Update(visible = True)
                    window_test_data.Element("crack_" + str(i) + "_width").Update(visible = True)
            elif event == "Broken":
                for i in range(1,5):
                    window_test_data.Element("crack_" + str(i)).Update(visible = False)
                    window_test_data.Element("crack_" + str(i) + "_len_txt").Update(visible = False)
                    window_test_data.Element("crack_" + str(i) + "_len").Update(visible = False)
                    window_test_data.Element("crack_" + str(i) + "_width_txt").Update(visible = False)
                    window_test_data.Element("crack_" + str(i) + "_width").Update(visible = False)
            elif re.search("\D", values["thickness"]) != None:
                sg.PopupError("Please enter a valid thickness!")
            elif check_crack(values)[0]:
                sg.PopupError("Please check crack " + str(check_crack(values)[1]))
            else:
                window_test_data.Close()
                test_dict = {"Number": num, 
                             "Name" : os.path.basename(file)[:-4]}
                if values["Round"]:
                    test_dict["Sample type"] = "Round"
                else:
                    test_dict["Sample type"] = "Square"
                if "test_date" in values.keys() and "cast" in values.keys():
                    test = datetime.date(year = int(values["test_date"][:4]), month = int(values["test_date"][5:7]), day = int(values["test_date"][8:10]))
                    cast = datetime.date(year = int(values["cast"][:4]), month = int(values["cast"][5:7]), day = int(values["cast"][8:10]))
                    age = test - cast
                    test_dict.update({
                    "Casting date": values["cast"], 
                     "Testing date": values["test_date"],
                     "Age" : age})
                else: 
                    test_dict.update({"Casting date": "", 
                     "Testing date": "",
                     "Age" : "",})
                test_dict.update({
                    "Drop weight": values["weight"][:-4],
                    "Thickness" : values["thickness"]
                    })
                if values["Broken"]:
                    test_dict["Broken/cracked"] = "broken"
                else:
                    test_dict["Broken/cracked"] = "cracked"
                    for i in range(1,5):
                        test_dict.update({
                            "Length " + str(i) : values["crack_" + str(i) + "_len"],
                            "Width " + str(i) : values["crack_" + str(i) + "_width"]
                            })
                    test_dict.update({
                        "Crack area" : calc_crack(values)[0],
                        "Amount of cracks" : calc_crack(values)[1],
                        "Median crack width" : calc_crack(values)[2],
                        "Opening angle" : calc_crack(values)[3]
                                })
                data = data.append(test_dict, ignore_index=True)
                num = num + 1
                break
    column_list = ["Number", "Name", "Sample type", "Casting date", "Testing date", "Age", "Drop weight", "Thickness", "Broken/cracked"]
    for i in range(1,6):
        column_list.append("Length " + str(i), "Width " + str(i))
    column_list.append("Crack area", "Amount of cracks", "Median crack width", "Opening angle")
    data = data[column_list]
    data = data.set_index("Name")
    data.to_excel(metadata + "//test_data.xlsx")
    sg.Popup("Data successfully entered!")



def make_columns_list(list):
    return [sg.Text(i) for i in list]

def make_index_list(index, columns):
    big_list = []
    for i in index:
       help_list = [sg.Text(i)]
       for j in columns:
           help_list.append(sg.Checkbox(j, key = i +"_" + j))
       big_list.append(help_list)
    return(big_list)

def make_exclusion_data(metadata, file_list):
    print("yay!")
    columns = ["Force",	"Acceleration",	"Displacement",	"Crack area",	 "Opening angle",	"High speed camera",	"Vertical acceleration of sample",	"Horizontal acceleration of sample"]
    index = [os.path.basename(i) for i in file_list]
    exclusion = pd.DataFrame(columns = columns, index = index)
    layout_exclusion = [
    [sg.Text("Please tick what you want to be excluded from calculation!")]
    ]
    layout_exclusion = layout_exclusion + make_index_list(index, columns)
    exclusion_window = sg.Window('Drop test program').Layout(layout_exclusion)
    event, values = exclusion_window.Read()

def auto_process(direct):
    basic_array, metadata, results = make_test_dir(direct)
    
    #make test_data file
    file_list = []
    for root, folders, files in os.walk(direct):
        for file in files:
            if file[-3:].lower() == "asc":
                path = root+"\\"+file
                if os.path.isfile(path):
                    file_list.append(path)
    make_test_data(metadata, file_list)
    make_exclusion_data(metadata, file_list)


while True:
    window_initial = sg.Window('Drop test program').Layout(layout_initial)
    event, values = window_initial.Read()
    if event == None or event == "Close program":
        window_initial.Close()
        break
    elif event == "Automatically process data":
        window_initial.Close()
        while True:
            window_auto = sg.Window("Drop test program").Layout(layout_auto)
            event, values = window_auto.Read()
            if event == None or event == "Cancel":
                window_auto.Close()
                break
            elif os.path.isdir(values["data"]):
                window_auto.Close()
                direct = values["data"]
                auto_process(direct)
                break
            else: 
                window_auto.Close()
                sg.PopupError("Please enter a valid path!")
    else:
        window_initial.Close()
        manual()