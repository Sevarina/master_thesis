# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 15:35:49 2019

@author: KEKAUN
"""
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import random

#make some test data
x = [random.randint(0,10) for i in range(20)]
y = [random.randint(0,10) for i in range(20)]
z = [random.randint(0,10) for i in range(20)]

#make a figure
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

#plot
ax.scatter(x,y,z)

#animate
##turn horizontally
def turn_horizontally(figure = ax):
    '''turn the figure horizontally'''
    for angle in range(0, 90):
        figure.view_init(30, angle)
        plt.draw()
        plt.pause(.001)
    plt.close() 

##turn vertically
def turn_vertically(figure = ax):
    '''turn the figure vertically'''
    for angle in range(0, 90):
        figure.view_init(angle,45)
        plt.draw()
        plt.pause(.001)
    plt.close()
    
##turn arbitrary
def turn_arbitrary(figure = ax,start=(-90,0),end=(0,180), resolution = 200):
    '''turn the figure in an arbitrary fashion
    start is a tuple that denotes the start angles of the animation [horizontal,vertical]
    end is a tuple that denotes the ending angles of the animation [horizontal,vertical]
    resolution is the amount of steps taken in the animation, each step takes .001 seconds'''
    #build path
    path =  build_path(start, end, resolution)
    print(path)
    for k in path:
        figure.view_init(k[0],k[1])
        plt.draw()
        plt.pause(.001)
    plt.close()   

def build_path(start=(0,0),end=(0,0),resolution=100):
    """build the path the camera travels on"""
    step_up = (end[0] - start [0]) / resolution
    step_side = (end[1] - start [1]) / resolution
    up = [start[0] + i * step_up for i in range(resolution)]
    sideways= [start[1] + i * step_side for i in range(resolution)]
    path = []
    for k in range(resolution):
        path.append((up[k],sideways[k]))    
    return path
         
#turn_horizontally()
#turn_vertically()
turn_arbitrary()
