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
        [sg.Button(button_text="Process data using GUI", tooltip = "Datasets will be converted from .asc and analysed")],
        [sg.Button(button_text="Manually process data", tooltip = "The user can choose which datasets to analyse and what to do with them")],
        [sg.Button(button_text="Close program")]
        ]

layout_GUI = [
        [sg.Text("What do you want to do?")],
        [sg.Button(button_text="Start new project", tooltip = "All datasets will be converted from .asc and analysed")],
        [sg.Button(button_text="Add sample to existing project", tooltip = "A single data set will be converted and added to an existing project")],
        [sg.Button(button_text="Close program")]       
        ]

layout_manual = [
        [sg.Text("What do you want to do?")],
        [sg.Button(button_text="Convert .asc data")],
        [sg.Button(button_text="Plot sensor data")],
        [sg.Button(button_text="Plot linear regression of results")],
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

layout_GUI = [
        [sg.Text("What do you want to do?")],
        [sg.Button(button_text="Start new project", tooltip = "All datasets will be converted from .asc and analysed")],
        [sg.Button(button_text="Add sample to existing project", tooltip = "A single data set will be converted and added to an existing project")],
        [sg.Button(button_text="Close program")],
        ]

def make_layout_nav_folder(target):
    layout = [
        [sg.Text('Please navigate to '+ target +"!")],
        [sg.InputText("", key = "data"), sg.FolderBrowse(target = "data")],
        [sg.Submit(), sg.Cancel()]
        ]
    return layout

def make_layout_nav_file(target):
    layout = [
        [sg.Text('Please navigate to '+ target +"!")],
        [sg.InputText("", key = "data"), sg.FileBrowse(target = "data")],
        [sg.Submit(), sg.Cancel()]
        ]
    return layout

def make_add_test_layout(sample):
    layout = [
        [sg.Text("Please enter data for sample: " + sample)],
        [sg.Text("Sample type"), sg.Radio('Round', "RADIO1", default=True, key = "Round"),
    sg.Radio('Square', "RADIO1", key = "Square") ],
         [sg.CalendarButton("Casting date", target = "cast", key = "cast_date"), sg.InputText("", key = "cast", disabled = True)], 
         [sg.CalendarButton("Test date", target = "test", key = "test_date"), sg.InputText("", key = "test", disabled = True)],
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
    layout.append([sg.Submit(), sg.Button("Skip sample"), sg.Button("Quit")])
    return layout

def make_choose_test_layout(file_list, verb):
    layout = [[sg.Text("Please tick which files you want to "+ verb +" !")]]
    for i in file_list:
        layout.append([sg.Checkbox(os.path.basename(i),default = True, key = i)])
    layout  = layout + [[sg.Submit(), sg.Cancel()]]
    return layout

def new_Dataset():
    window_new_dataset = sg.Window('Drop test program', default_element_size=(40, 1)).Layout(layout_nav_folder)
    event, values = window_new_dataset.Read()
    while True:
        if event == "Cancel" or event == None:
            window_new_dataset.Close()    
        elif os.path.isdir(values["data"]) == False:            
            sg.PopupError("Please enter a valid path!")
        elif core.make_file_list(values["data"]) == []:
            sg.PopupError("No .asc files in folder to process!")
        else:
            file_list = core.make_file_list(values["data"])
            sg.PopupError("NOT IMPLEMENTED YET!")
            window_new_dataset.Close()
            break
##################################
#def new_Dataset():
#    window_new_dataset = sg.Window('Drop test program', default_element_size=(40, 1)).Layout(layout_new_dataset)
#    event, values = window_new_dataset.Read()
#    if event == "Cancel" or event == None:
#        window_new_dataset.Close()
#    elif values["Browse"][-4:].lower() == ".asc" and os.path.isfile(values["Browse"]):
#        window_new_dataset.Close()
#        sg.Popup("This will take a minute, please wait", non_blocking=True, auto_close=True)
#        if values["Round"]:
#            clean.clean_array(file = values["Browse"], sample_type = "Round")
#        else:
#            clean.clean_array(file = values["Browse"], sample_type = "Square")
#        sg.Popup("Conversion completed!")
#    else: 
#        sg.Popup("Please choose an existing .asc file!")

def plot_all():
    window_plot = sg.Window('Drop test program', default_element_size=(40, 1)).Layout(layout_plot_datasets)
    event, values = window_plot.Read()
    if event == "Submit":
        core.calc(data = values["data"], results = values["result"])
        window_plot.Close()
    else: window_plot.Close()

########################### FIXME

layout_man = [
        [sg.Text("What do you want to do?")],
        [sg.Button("Convert a single data set", tooltip = "Convert one data set from .asc to .npy")],
        [sg.Button("Convert several data sets at once", tooltip = "Convert all data sets in a folder from .asc to .npy")],
        [sg.Button("Run analysis for all data sets in a folder", tooltip = "Analyse all .npy in the chosen folder")],
#        [sg.Button("Edit data set", tooltip = "Remove outliers from a data set")],
        [sg.Submit(), sg.Cancel()]   
        ]

def choose_file(file_list, verb):
    choose_window = sg.Window('Drop test program').Layout(make_choose_test_layout(file_list, verb))
    event, values = choose_window.Read()
    choose_window.Close()
    if event == None or event == "Cancel":
        return []
    chosen_list = [j for j in file_list if values[j]]
    return chosen_list

def manual():
    while True:
        window = sg.Window('Drop test program').Layout(layout_man)    
        event, values = window.Read()
        if event == None or event == "Cancel":
            window.Close()
        elif event == "Convert a single data set":
            window.Close()
            file = nav_file_check(target = "test data", extension = "asc")
            _, basic_array = nav_folder_check(target = "where you want the converted data to be saved")
            convert_single_file(basic_array, [file])
        elif event == "Convert several data sets at once":
            window.Close()
            file_list, direct = nav_folder_check(target = "test data", extension = "asc")
            _, basic_array = nav_folder_check(target = "where you want the converted data to be saved", extension = "")
            convert_list = choose_file(file_list, "convert")
            if convert_list != []:
                convert_file(basic_array, convert_list)
        else:
            window.Close()
            file_list, basic_array = nav_folder_check(target = "data you want to analyse", extension = "npy")
            _, result = nav_folder_check(target = "where you the results to be saved")
            core.calc(basic_array, result)
#        else:
#            file = nav_file_check(target = "test data", extension = "npy")
            

#    window_manual = sg.Window('Drop test program', default_element_size=(40, 1)).Layout(layout_manual)
#    event, values = window_manual.Read()
#    print(event)
#    if event == "Convert .asc data":
#        window_manual.Close()
#        new_Dataset()
#    if event == "Plot all datasets":
#        window_manual.Close()
#        plot_all()
#    if event =="Plot linear regression of parameters":
#        window_manual.Close()
#        sg.Popup("Not yet implemented!")

def convert_single_file(basic_array):
    file = nav_file_check(target = "new data set", extension = "asc")
    if file == None:
        return
    #convert
    filename = convert_file(basic_array, [file])
    return filename

def make_test_dir(direct):
    basic_array = (direct + "//test_analysis//Data//basic_array")
    if os.path.isdir(basic_array) == False:
        os.makedirs(basic_array)
    broken = direct + "//test_analysis//Data//basic_array//broken"
    if os.path.isdir(broken) == False:
        os.makedirs(broken)
    cracked = direct + "//test_analysis//Data//basic_array//cracked"
    if os.path.isdir(cracked) == False:
        os.makedirs(cracked)
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
    for file in file_list:
        window_test_data = sg.Window("Drop test program").Layout(make_add_test_layout(os.path.basename(file[:-4])))
        while True:
            event, values = window_test_data.Read()
            print(values)
            if event == None or event == "Quit":
                window_test_data.Close()
                break
            elif event == "Skip sample":
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
                    test_dict["Sample type"] = "round"
                else:
                    test_dict["Sample type"] = "square"
                if values["test"] != "" and values["cast"] != "":
                    print(values)
                    test = datetime.date(year = int(values["test"][:4]), month = int(values["test"][5:7]), day = int(values["test"][8:10]))
                    cast = datetime.date(year = int(values["cast"][:4]), month = int(values["cast"][5:7]), day = int(values["cast"][8:10]))
                    age = test - cast
                    test_dict.update({
                    "Casting date": cast, 
                     "Test date": test,
                     "Age" : age.days})
                else: 
                    test_dict.update({"Casting date": "", 
                     "Test date": "",
                     "Age" : "",})
                test_dict.update({
                    "Drop weight": values["weight"][:-3],
                    "Thickness" : values["thickness"]
                    })
                if values["Broken"]:
                    test_dict["Broken/cracked"] = "broken"
                    for i in range(1,5):
                        test_dict.update({
                            "Length " + str(i) : "",
                            "Width " + str(i) : "" 
                            })
                    test_dict.update({
                        "Crack area" : "",
                        "Amount of cracks" : "",
                        "Average crack width" : "",
                        "Opening angle" : ""
                                })
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
                        "Average crack width" : calc_crack(values)[2],
                        "Opening angle" : calc_crack(values)[3]
                                })
                    print(test_dict["Age"])
                data = data.append(test_dict, ignore_index=True)
                num = num + 1
                break
    if len(data.index) != 0:
        column_list = ["Number", "Name", "Sample type", "Casting date", "Test date", "Age", "Drop weight", "Thickness", "Broken/cracked"]
        for i in range(1,5):
            column_list.append("Length " + str(i))
            column_list.append("Width " + str(i))
        column_list = column_list + ["Crack area", "Amount of cracks", "Average crack width", "Opening angle"]
        data = data[column_list]
        data = data.set_index("Name")
        data.to_excel(metadata + "//test_data.xlsx")
        data.to_latex(metadata + "//test_data.tex")
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
    columns = ["Loadcells","Accelerometer","Laser sensor",	"Crack area",	 "Opening angle",	"High speed camera", "Additional accelerometer vertical","Additional accelerometer horizontal"]
    index = [os.path.basename(i)[:-4] for i in file_list]
    exclusion = pd.DataFrame(columns = columns, index = index)
    layout_exclusion = [
    [sg.Text("Please tick what you want to be excluded from analysis!")]
    ]
    layout_exclusion = layout_exclusion + make_index_list(index, columns)
    layout_exclusion.append([sg.Submit(), sg.Cancel()])
    exclusion_window = sg.Window('Drop test program').Layout(layout_exclusion)
    event, values = exclusion_window.Read()
    if event == "Cancel" or event == None:
        exclusion_window.Close()
    else:
        exclusion_window.Close()
        for i in index:
            for j in columns:
                exclusion.loc[i,j] = int(values[i + "_" + j])
        exclusion.to_excel(metadata + "//exclude.xlsx")
        
def convert_file(basic_array, file_list):
    data = core.open_df(basic_array)
    res_list = []
    for i in file_list:
        filename = os.path.basename(i)[:-4]
        save_path = basic_array + "\\" + data.loc[filename,"Broken/cracked"] + "\\" + filename + ".npy"
        print(data.loc[filename,"Sample type"].lower())
        clean.clean_array(initial_file= i, clean_file = save_path,  sample_type= data.loc[filename,"Sample type"].lower())
        res_list.append(save_path)
    return res_list

#TODO add progress bar
def run_auto(file_list, direct):
    #make folders
    basic_array, metadata, results = make_test_dir(direct)
    make_test_data(metadata, file_list)
    make_exclusion_data(metadata, file_list)
    sg.Popup("The conversion process takes some time, please be patient!", non_blocking=True)
    convert_file(basic_array, file_list)
    core.calc(data = basic_array, results = results)

def nav_folder_check(target, extension = ""):
    while True:
        window = sg.Window("Drop test program").Layout(make_layout_nav_folder(target))
        event, values = window.Read()
        if event == None or event == "Cancel":
            window.Close()
            return None, None
        elif os.path.isdir(values["data"]) == False:
            window.Close()
            sg.PopupError("Please enter a valid path!")
        else:
            file_list = core.make_file_list(extension = extension, direct = values["data"])
            if file_list == [] and extension != "":
                sg.PopupError("No files in location!")
                window.Close()  
            else:
                window.Close()
                return file_list, values["data"]

def nav_file_check(target, extension):
    while True:
        window = sg.Window("Drop test program").Layout(make_layout_nav_file(target))
        event, values = window.Read()
        if event == None or event == "Cancel":
            window.Close()
            return None
        elif os.path.isfile(values["data"]) == False or values["data"][-len(extension):].lower() != extension:
            window.Close()
            sg.PopupError("Please check the file path!")
        else:
            return values["data"]

def use_GUI():
    window = sg.Window("Drop test program").Layout(layout_GUI)
    while True:
        event, values = window.Read()
        if event == None or event == "Close program":
            window.Close()
            break 
        elif event == "Start new project":
            window.Close()
            file_list, direct = nav_folder_check(target = "test data", extension = "asc")
            if file_list == None:
                continue
            run_auto(file_list, direct)
        else:
            window.Close()
            file = nav_file_check(target = "test data", extension = "asc")
            basic_array, metadata, results = make_test_dir(os.path.basename(file))
            sg.Popup("The conversion process takes some time, please be patient!", non_blocking=True)
            filename = convert_single_file(basic_array)
            #open everything you need to calc
            res_file = pd.read_excel(results + r"\result.xlsx", header = 0, index_col = 0)
            app_path = results + r"\appendix.tex"
            app_file = open(app_path,"a")
            df = core.open_df(basic_array)
            #calc
            core.calc_single_file(filename = filename, results = results, res_file = res_file, app_file = app_file, df = df)

window_initial = sg.Window('Drop test program').Layout(layout_initial)                                
while True:    
    event, values = window_initial.Read()
    if event == None or event == "Close program":
        window_initial.Close()
        break
    elif event == "Process data using GUI":
        window_initial.Close()
        use_GUI()
    else:
        window_initial.Close()
        manual()