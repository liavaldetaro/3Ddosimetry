# Written by Simon Jensen July 2020
# Modified by Lia Valdetaro on Februay 2021
import tkinter as tk
from tkinter import filedialog
import numpy as np
from scipy.io import savemat
import os, os.path


def vff(file_path):
    # Get the matrix dimension n x n x n
    with open(file_path) as data:
        for i, line in enumerate(data):
            if i == 6:
                n = int(line.split(' ')[1])
            elif i > 6:
                break

    # Open file and read uint8 format and then after subtracting an offset
    # from the header format it to float32 i.e. double in python, if the offset
    # isn't subtracted the wrong uint8 numbers will be combined.
    # Byte swqpping from little endian (least significant byte first) system
    # to big endian system (most significant byte first) i.e. when
    # combining multiple int8 to int32 it is: little endian (1)*1 + (2)*256 + (3)*65536 + etc.
    #data_array = data_array.byteswap(True)
    with open(file_path, 'rb') as fid:
        data_array = np.fromfile(fid, np.uint8)
    data_array = data_array[(len(data_array)-4*n**3):]
    data_array = data_array.view(np.float32).byteswap(True)

    # To save space, save as .mat, if saving as txt it saves as unicode 24 bit
    # i.e. taking three times the space per character
    OCT = np.zeros((n, n, n))

    m = 0
    for i in np.arange(0, n):
        for j in np.arange(0, n):
            for k in np.arange(0,n):
                OCT[i, j, k] = str(data_array[m])
                m += 1
    mdic = {"OCT": OCT, "label": "experiment"}
    f = file_path[:-4] + str('.mat')
    print(f)
    savemat(f, mdic)

def main():

    d = '../data/reconstructions/5_ca/'
    print(d)
    for name in os.listdir(d):

        if name.endswith("vff"):
            vff(d + str('/') + name)


if __name__ == "__main__":
    main()