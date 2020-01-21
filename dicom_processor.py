#!/usr/bin/env python
# coding: utf-8

# @author: Luigi Palladino

import pydicom
import os
import numpy
import scipy.misc
import time

import tkinter as tk
from tkinter import filedialog
from pathlib import Path

# USE ONLY IN PRODUCTION! (comment next 2 lines for debugging)
import warnings
warnings.filterwarnings("ignore")

# Populate a emphasis **lstFilesDcm** with te filenames of the DICOM files under a given **PathDicom** directory:

Path("./DATASET").mkdir(parents=True, exist_ok=True)

root = tk.Tk()
root.withdraw()
PathDicom = filedialog.askdirectory()

print("Processing...")

lstFilesDCM = [] # create an empty list

for dirName, subdirList, fileList in os.walk(PathDicom):
    for filename in fileList:
        if ".dcm" in filename.lower(): #check wheter the file's DICOM
            lstFilesDCM.append(os.path.join(dirName,filename))

if not lstFilesDCM:
    for dirName, subdirList, fileList in os.walk(PathDicom):
        for filename in fileList:
            lstFilesDCM.append(os.path.join(dirName,filename))
            #DO NOT check wheter the file's DICOM

# Loop through files, read metadata, allocate a numpy array and load data in that numpy array:

elements = []
# loop through all the DICOM files
for filenameDCM in lstFilesDCM:
    # read the file
    ds = pydicom.read_file(filenameDCM)
    # store the raw image data
    try:
        array = ds.pixel_array
        elements.append(array)
    except:
        continue
        # enable next line for debugging
        #print("Exception: "+filenameDCM)

for arr in elements:

    if len(numpy.shape(arr)) > 3:
        for i in arr:
            scipy.misc.imsave("./DATASET/"+str(time.time())+".png", i)
    else:
        scipy.misc.imsave("./DATASET/"+str(time.time())+".png", arr)


print("\nDone!\n");