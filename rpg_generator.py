# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 17:41:20 2020

@author: kunge
"""

import random

color = ['gold', 'silber', 'white', 'iridescent', 'green', 'brown', 'black']
animal = ['unicorn', 'sea horse', 'fish', 'bird', 'sea gull']

farb_eigenschaft = ["trüb", "tief", "hell", "dunkel", "gelblich", "grünlich", "rötlich", "bläulich", "ölig", "blass"]
farbe = ['gelb', 'rot', 'schwarz', 'grün', "violet", "braun"]
geschmack_eigenschaft = ["minzig", "rauchig", "zitronig", "süß", "herb", "sauer", "bitter", "ölig", "klebrig", "salzig", "ranzig", "fischig", "fruchtig"]
geschmack = ["gut", "einschläfernd", "beruhigend", "belebend", "eklig", "beunruhigend", "herzhaft", "anregend", "aufputschend", "eigenartig", "eigentümlich"]
riecht_nach=["Orangen", "Limette", "Eisen", "Veilchen", "Rosen", "Gewürzen", "Schnee", "Gewitter", "frisch geschnittenem Gras", "Rosmarin", "Zwiebel"]

def tee():
    help_int = random.randint(0,2)
    message =["Der Tee ist ", random.choice(farb_eigenschaft),"-", random.choice(farbe),". Er schmeckt ", random.choice(geschmack_eigenschaft), " und "]
    if help_int == 1:
        help_str = random.choice(geschmack) + "."
    else: help_str = "riecht nach " + random.choice(riecht_nach) + "."
    message.append(help_str)
    message_str = "".join([str(elem) for elem in message])
    print(message_str)
    
    
#randomly generate a tavernname
def show_tavern(amount=1):
    for i in range(amount):
        print(gen_tavern())

def gen_tavern():
    #adjective + noun        
    print(random.choice(color), ' ', random.choice(animal))
    
