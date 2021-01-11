# -*- coding: utf-8 -*-
"""
Created on Sat Dec 12 11:05:04 2020

@author: kunge
"""
import os


def make_file_list(direct, extension = ""):
    file_list = []
    for root, folders, files in os.walk(direct):
        for file in files:
            path = os.path.join(root, file)
            if os.path.isfile(path) and (extension == "" or file[-len(extension):].lower() == extension):
                file_list.append(path)
    return file_list

def make_image_list(tex_path, pic_folder, pic_extension):
    pic_list = make_file_list(pic_folder, pic_extension)
    file = open(tex_path,"a")
    for i in pic_list:
        pic_name = os.path.basename(i).capitalize()
        file.write("""\\begin{figure}
        \\centering
        \\includegraphics[width=0.9\\linewidth]{""" + i.replace(os.sep, '/') + """}
        \\caption{""" + pic_name.replace("_"," ") + """}
        \\label{fig:""" + pic_name +  """}
        \\end{figure}\n\n""")
        
    