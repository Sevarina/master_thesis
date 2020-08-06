# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 17:41:20 2020

@author: kunge
"""

import random

color = ['gold', 'silber', 'white', 'iridescent', 'green', 'brown', 'black']
animal = ['unicorn', 'sea horse', 'fish', 'bird', 'sea gull']

#randomly generate a tavernname
def show_tavern(amount=1):
    for i in range(amount):
        print(gen_tavern())

def gen_tavern():
    #adjective + noun        
    print(random.choice(color), ' ', random.choice(animal))
    
