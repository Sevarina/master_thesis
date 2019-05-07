import os
import numpy as np

def plt_extraaccel(file=".\\extraAccel\\2019-04-16_Rfrs_75_0,5_horizontal.npy"):
###### .TXT
    f = open(file,"r")
    x,y = [],[]
    i,up,down,start = 0,0,0,0
    for line in f.readlines():
        line = line.split(",")
        x.append(float(line[0]))
        y.append(float(line[1])*50*9.8) #50 because x 10 amplification an 0,5 mV/g
        if float(line[1]) > up:
            up = float(line[1])
            start = i
        elif float(line[1]) < down:
            down = float(line[1])
        i += 1   
    f.close()
    array = np.stack((x,y),axis=1)
    np.save(file[:-3]+"npy",array)
    print("highest value: ",up,"\nlowest value: ",down)
###### .NPY
#    array = np.load(file)
#    array = fix_time(array)
#    start = np.argmax(array[:,1])
#    down = np.argmin(array[:,1])
#    plt.plot(array[start-50:start+300,0],array[start-50:start+300,1])
#    
#    plt.ylabel(r"Acceleration [$\frac{m}{s^2}$]")
#    plt.xlabel("Time [$s$]")
##    plt.title("Acceleration measured directly on sample \n 2019-02-20-Rfs-100-0,5, vertical")
#    plt.grid()
#    plt.savefig(file[:-4] + ".png")
#    plt.close()
#    print(array[start][1])
#    print(array[down][1])

#ask for filename
print("Please enter path to new txt file!")
name = input()

#check if file exists
while os.path.isfile(name) != True and name[:-3]=="txt":
    print("This file does not exist or is not an .asc file")
    print("Please enter path to new file!")
    name = input()    
    
print("File looks good, processing it might take a few minutes")

plt_extraaccel(name)