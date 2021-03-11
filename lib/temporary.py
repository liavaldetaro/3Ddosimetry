
#import pyelastix
import numpy as np
import matplotlib.pyplot as plt
import scipy as sc
import tkinter as tk
from tkinter import *
from tkinter import filedialog
import os, os.path
from scipy.io import savemat
import scipy.ndimage
from pathlib import Path

def image_registration(OCT, OCT_original):
    params = pyelastix.get_default_params(type='RIGID')
    params.MaximumNumberOfIterations = 200
    params.FinalGridSpacingInVoxels = 10

    # Apply the registration (im1 and im2 can be 2D or 3D)
    oct_deformed, field = pyelastix.register(OCT_original, OCT, params)

    return oct_deformed


def main():
    '''
    path =  '/home/lia/Documents/Photon_project/3Ddosimetry/data/reconstructions/_mat_crop_aligned'

    filename = '/home/lia/Documents/Photon_project/3Ddosimetry/data/reconstructions/_mat_crop_aligned/dos_1_bottom_day_2.mat'

    if filename.endswith("mat"):
        mat = sc.io.loadmat(filename)
        oct = np.array(mat['OCT'])
    else:
        print('could not find .mat files')

    mat = sc.io.loadmat('/home/lia/Documents/Photon_project/3Ddosimetry/data/reconstructions/_mat_crop_aligned/dos_1_bottom_day_1.mat')
    oct_fixed = np.array(mat['OCT'])
    print(oct_fixed.shape)


    oct_fixed = np.ascontiguousarray(oct_fixed)
    oct = np.ascontiguousarray(oct)

    params = pyelastix.get_default_params(type='RIGID')
    params.MaximumNumberOfIterations = 200
    params.FinalGridSpacingInVoxels = 10

    oct_new, field = pyelastix.register(oct, oct_fixed, params)

    plt.style.use('seaborn-dark-palette')
    plt.rcParams.update({'font.size': 12})
    fig, ax = plt.subplots(1, 3)
    ax[0].imshow(oct_new[int(oct_new.shape[0] / 2), :, :], cmap='jet')
    ax[1].imshow(oct_new[:, int(oct_new.shape[2] / 2), :], cmap='jet')
    ax[2].imshow(oct_new[:, :, int(oct_new.shape[2] / 2)], cmap='jet')
    plt.show()

    if not os.path.isdir(path + "_aligned"):
        os.mkdir(path + "_aligned")
    mdic = {"OCT": oct_new, "label": "experiment"}
    savemat(path + "_aligned" + "/" + os.path.split(filename)[1], mdic)


    '''


    path =  '../data/reconstructions/5_ca_crop'

    for name in os.listdir(path):

        if name.endswith("mat"):
            mat = sc.io.loadmat(path + str('/') + name)
            oct = np.array(mat['OCT'])
        else:
            continue

        my_file = Path(path + "_aligned" + "/" + os.path.split(name)[1])
        if my_file.is_file():
            continue
        terminate = False
        while not terminate:

            ang = np.float(input('Input rotation angle (degrees):   '))
            rot_axis = input('Input the rotation axis (x/y/z):  ')


            if rot_axis == 'x':
                oct_rot = sc.ndimage.interpolation.rotate(oct, axes=(1, 0), angle=ang, reshape=False)
            if rot_axis == 'y':
                oct_rot = sc.ndimage.interpolation.rotate(oct, axes=(1, 2), angle=ang, reshape=False)
            if rot_axis == 'z':
                oct_rot = sc.ndimage.interpolation.rotate(oct, axes=(2, 0), angle=ang, reshape=False)


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
                savemat(path + "_aligned" + "/" + os.path.split(name)[1], mdic)
                terminate = True

    '''
    bol = 'y'
    while bol == 'y':
        for name in os.listdir(path):

            if name.endswith("mat"):
                # importing and cropping the data
                mat = sc.io.loadmat(path + str('/') + name)
                oct_new = np.array(mat['OCT'])

            oct_new = np.ascontiguousarray(oct_new)
            oct_new = image_registration(oct_new, oct_rot)

            plt.style.use('seaborn-dark-palette')
            plt.rcParams.update({'font.size': 12})
            fig, ax = plt.subplots(1, 3)
            ax[0].imshow(oct_new[int(oct_new.shape[0] / 2), :, :], cmap='jet')
            ax[1].imshow(oct_new[:, int(oct_new.shape[2] / 2), :], cmap='jet')
            ax[2].imshow(oct_new[:, :, int(oct_new.shape[2] / 2)], cmap='jet')
            plt.show()

            ans = input('acccept registration? (y/n)')
            if ans == 'y':
                mdic = {"OCT": oct_new, "label": "experiment"}
                savemat(path + "_aligned" + "/" + os.path.split(name)[1], mdic)

            bol = input('finish? ')
            
    '''
if __name__ == "__main__":
    main()

