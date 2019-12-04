"""
HOW TO RUN:
graph.py outputData.txt

where 'outputData.txt' is a file created by tsp.py with the result coordinates

"""

import matplotlib.pyplot as plt
import matplotlib.path as mpath
import numpy as np
import random
# READING FILES ----------------------------------------------------------------
import sys
import entrada

with open("/Users/Rhaissa_2/Downloads/ProjCurso IA/ProjCurso IA/outputData.txt", "r") as f:
        f.readline()
        fileData=  ([p.split() for p in f.read().strip().splitlines()])


# AMOUNT OF CITIES TO USE ------------------------------------------------------
numberCities = 10

"""
you'll need to instal matplotlib before running this code
for this, run:
  python -m pip install -U pip
  python -m pip install -U matplotlib

and you'll need to install some dependecies:
for this, run:
  python -m pip install --user numpy scipy matplotlib ipython jupyter pandas sympy nose
"""

# CHARTS DESIGN ----------------------------------------------------------------
circle = mpath.Path.unit_circle()
markerSize = 8

# BUILD OUR CHART --------------------------------------------------------------
"""
PARAMETERS FORMAT:
  ----------
  ax : Axes
    The axes to draw to

  xData : array
    The x data

  yData : array
    The y data

  param_dict : dict
    Dictionary of kwargs to pass to ax.plot

  RETURNS ----------------------------------------------------------------------
    out : list
      list of artists added

  HOW TO -----------------------------------------------------------------------
  out = ax.plot(xData, yData, **param_dict)
"""

xData = [] 
yData = []

i = 0
while i < numberCities:
  xData.append(float(fileData[i][0]))
  yData.append(float(fileData[i][1]))
  i += 1

f.close()
plt.plot(xData, yData, '--r', marker=circle, markersize=markerSize)
plt.savefig("Plot1")
plt.show()


with open("/Users/Rhaissa_2/Downloads/ProjCurso IA/ProjCurso IA/outputDataM.txt", "r") as f:
    f.readline()
    fileData=  ([p.split() for p in f.read().strip().splitlines()])

i = 0
while i < numberCities:
  xData.append(float(fileData[i][0]))
  yData.append(float(fileData[i][1]))
  i += 1

plt.plot(xData, yData, '--r', marker=circle, markersize=markerSize)
plt.savefig("Plot2")


f.close()
