#!/usr/bin/python3
import coreprogram as core
import clean_file as clean
import PySimpleGUI as sg
import os
import pandas as pd

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
        [sg.Text('Please navigate to test data', size=(30, 1))],
        [sg.InputText("C:/", key = "data"), sg.FolderBrowse()],
        [sg.Submit(), sg.Cancel()]
        ]

def make_add_test_layout(sample):
    layout = [
        [sg.Text("Please enter data for sample " + sample)],
        [sg.Text("Sample type"), sg.Radio('Round', "RADIO1", default=True, key = "Round"),
    sg.Radio('Square', "RADIO1", key = "Square") ],
         [sg.InputText(), sg.CalendarButton("Casting date", key = "cast")],
         [sg.InputText(), sg.CalendarButton("Testting date", key = "test_date")],
         [sg.Text("Drop weight"), sg.Combo(['50 kg', '100 kg', "200 kg", "500 kg", "1000 kg"], key = "weight")],
         [sg.Text("Sample thickness [mm]"), sg.InputText(key = "thickness")]
#         [sg.Text("Broken or cracked", tooltip = "If the sample was destroyed/failed during testing please select ""Broken""" ), sg.Radio('Broken', "RADIO2", default=True, key = "Broken"),
#    sg.Radio('Cracked', "RADIO2", default = False, key = "Cracked") ]    
        ]
    for i in range(1,6):
        layout.append([sg.Text("Crack " + str(i)), sg.Text("Length [mm]"), sg.Input(key = "crack_" + str(i) + "_len")])#, sg.Text("Width [mm]"), sg.Input(key = "crack_" + str(i) + "_width"]))
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

def make_test_data(metadata, file_list):
    data = pd.DataFrame()
    num = 1
    for file in file_list:
        window_test_data = sg.Window("Drop test program").Layout(make_add_test_layout(os.path.basename(file[:-4])))
        event, values = window_test_data.Read()
        if event == None or event == "Cancel":
            break
        else:
            test_dict = {"Number": num, 
                         "Name" : os.path.basename(file)[:-4]}
            age = values["test_date"] - values["cast"]
            if values["Round"]:
                test_dict["Sample type"] = "Round"
            else:
                test_dict["Sample type"] = "Square"
            test_dict.update({"Casting date": values["cast"], 
                             "Testing date": values["test_date"],
                             "Age" : age,
                             "Drop weight": values["weight"],
                             "Thickness" : values[""]
                             })
            if values["Broken"]:
                test_dict["Broken/cracked"] = "broken"
            else:
                test_dict["Sample type"] = "cracked"
            for i in range(1,6):
                test_dict.update({
                        "Length " + i : values["crack_" + i + "_len"],
                        "Width " + i : values["crack_" + i + "_width"]
                        })
            data.append(test_dict)
            num + 1
    data.to_excel(metadata + "//test_data.xlsx")

def auto_process(direct):
    basic_array, metadata, results = make_test_dir(direct)
    
    #make test_data file
    file_list = []
    for root, folders, files in os.walk(direct):
        for root, folders, files in os.walk(direct):
            for file in files:
                if file[-3:].lower() == "asc":
                    path = root+"\\"+file
                    if os.path.isfile(path):
                        file_list.append(path)
    make_test_data(metadata, file_list)


while True:
    window_initial = sg.Window('Drop test program').Layout(layout_initial)
    event, values = window_initial.Read()
    if event == None or event == "Close":
        window_initial.Close()
        break
    elif event == "Automatically process data":
        window_auto = sg.Window("Drop test program").Layout(layout_auto)
        event, values = window_auto.Read()
        if event == None or event == "Cancel":
            window_auto.Close()
        else: 
            direct = values["data"]
            auto_process(direct)
#        sg.Popup("Not yet implemented!")
    else:
        manual()
       

    

    
