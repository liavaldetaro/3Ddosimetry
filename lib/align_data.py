#####################################################
# Written by Lia Valdetaro, 12/2020
# Contact info: liavaldetaro@gmail.com
#####################################################


import pyelastix
import numpy as np
import matplotlib.pyplot as plt
import scipy as sc
import tkinter as tk
from tkinter import *
from tkinter import filedialog
import os, os.path
from scipy.io import savemat
import scipy.ndimage

# -------------------------------------------------------------------------------------------------
# The program first prompts the user to align one dose map to the desired position, and then
# uses image registration to align all the other maps in teh folder to the same position.
#
#
# Uses pyelastix : https://pypi.org/project/pyelastix/
# -------------------------------------------------------------------------------------------------


def image_registration(oct, oct_target):
    params = pyelastix.get_default_params(type='RIGID')
    params.MaximumNumberOfIterations = 400
    params.FinalGridSpacingInVoxels = 10

    # Apply the registration (im1 and im2 can be 2D or 3D)
    oct_deformed, field = pyelastix.register(oct, oct_target, params)

    return oct_deformed


def main():

    print('Select the OCT file')
    root = tk.Tk()
    root.withdraw()
    filename = filedialog.askopenfilename()
    path = os.path.dirname(filename)

    if filename.endswith("mat"):
        mat = sc.io.loadmat(filename)
        oct = np.array(mat['OCT'])
    else:
        print('could not find .mat files')

    terminate = False
    while not terminate:

        ang = np.float(input('Input rotation angle (degrees):   '))
        rot_axis = input('Input the rotation axis (x/y/z):  ')
        if rot_axis == 'x':
            oct_rot = sc.ndimage.interpolation.rotate(oct, axes=(1, 0), angle=ang, reshape=True)
        if rot_axis == 'y':
            oct_rot = sc.ndimage.interpolation.rotate(oct, axes=(1, 2), angle=ang, reshape=True)
        if rot_axis == 'z':
            oct_rot = sc.ndimage.interpolation.rotate(oct, axes=(2, 0), angle=ang, reshape=True)

        plt.rcParams.update({'font.size': 12})
        fig, ax = plt.subplots(1, 3)
        ax[0].imshow(oct_rot[int(oct.shape[0] / 2), :, :], cmap='jet')
        ax[1].imshow(oct_rot[:, int(oct.shape[2] / 2), :], cmap='jet')
        ax[2].imshow(oct_rot[:, :, int(oct.shape[2] / 2)], cmap='jet')
        plt.show()

        ans = input('terminate? (y/n):  ')
        if ans == 'yes' or ans == 'y':
            if not os.path.isdir(path + "_aligned"):
                os.mkdir(path + "_aligned")
            mdic = {"OCT": oct_rot, "label": "experiment"}
            savemat(path + "_aligned" + "/" + os.path.split(filename)[1], mdic)
            terminate = True

    ans = input('Align the other files in the folder to the selected OCT? (y/n):    ')

    oct_rot = np.ascontiguousarray(oct_rot)

    if ans == 'y' or ans == 'Y':
        for name in os.listdir(path):
            if not name.endswith('.mat'):
                continue
            print(name)
            if name.endswith("mat"):
                # importing and cropping the data
                mat = sc.io.loadmat(path + str('/') + name)
                oct_new = np.array(mat['OCT'])

            oct_new = np.ascontiguousarray(oct_new)

            params = pyelastix.get_default_params(type='RIGID')
            #params.MaximumNumberOfIterations = 1000
            #params.NumberOfResolutions = 7
            #params.FinalGridSpacingInVoxels = 10

            oct_regs, field = pyelastix.register(oct_new, oct_rot, params)

            mdic = {"OCT": oct_regs, "label": "experiment"}
            savemat(path + "_aligned" + "/" + os.path.split(name)[1], mdic)



if __name__ == "__main__":
    main()