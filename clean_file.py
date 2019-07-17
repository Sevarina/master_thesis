#!/usr/bin/python3
#put some values into an array
import numpy as np


#the important code
def clean_array(initial_file=".\\Data\\cracked\\2019-05-06_Rfrs_75_0,8.asc", clean_file = ".\\Data\\cracked\\2019-05-06_Rfrs_75_0,8.npy",  sample_type= "Round"):
    array = readData(filename = initial_file)
    #throw away all the rows you don´t need
    if sample_type == "Round":
        newarray = np.delete(array,[5,6,8,10,11,13,14,15,16,17,18,19,20,21,22],1)
    else: newarray = np.delete(array,[6,8,10,11,13,14,15,16,17,18,19,20,21,22],1)
    newarray = fix_time(newarray)
    for i in range(newarray.shape[0]):
        newarray[i][5] = newarray[i][5] * 9.8

    np.save(clean_file,newarray)

def fix_time(array):
    array[0][0]=0
    for i in range(1,array.shape[0]):
        array[i][0] = array[i-1][0] + 0.0001
    return array

def readData(maxLines=-1,filename=".\\Data\\cracked\\2019-02-20-Rfs-100-0,5.asc",start=0, progress = 0):
    f= open(filename)
    if start == 0:
        clearData(f)
    else: 
        for i in range(start):
            f.readline()
    l1 = []
    for line in f.readlines()[:maxLines]:
        line = line.replace(",",".").split("\t")[:-1]
        for l in line:
            try:
                d = np.double(l)
            except:
                d = np.nan
            l1.append(d)   
    f.close()

    try:
        return np.array(l1).reshape(-1,26)
    except:
        return np.array(l1).reshape(-1,29)
    
def clearData(file):
# Read and ignore header lines
    i = 0
    while i < 8:
        file.readline()
        i += 1
# I checked the file, this is where the real headings are hidden
    global header # it´s dangerous to go alone, take this!
    header = file.readline().split("\t")
# ignore the useless stuff
    while i < 38:
        file.readline()
        i += 1