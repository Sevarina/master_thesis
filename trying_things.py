import numpy as np
import statistics as stat
import matplotlib as mpl
#make all plots look nice
mpl.style.use('classic')
from matplotlib import rc
import matplotlib.pyplot as plt

import scipy as sp
import scipy.signal as sig
import scipy.integrate as integrate
from scipy.optimize import curve_fit
import seaborn as sns
import math

import os
import re
import pandas as pd
from adjustText import adjust_text
import locale
locale.setlocale(locale.LC_ALL, 'deu_deu')

import PySimpleGUI as sg

sg.PopupGetFile("let's do this")

