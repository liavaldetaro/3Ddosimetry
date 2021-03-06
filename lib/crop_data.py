#####################################################
# Written by Lia Valdetaro, 12/2020
# Contact info: liavaldetaro@gmail.com
#####################################################

import numpy as np
import matplotlib.pyplot as plt
import scipy as sc
import tkinter as tk
from tkinter import filedialog
import os, os.path
from scipy.io import savemat

# -------------------------------------------------------------------------------------------------
# Selects the cropping boundaries of the 3D data by prompting the users to click on the data slices.
# The user can choose between cropping the data sets separately, or applying the same values to all
# the sets. That is advised only if all dosimeters have the same dimensions.
# -------------------------------------------------------------------------------------------------

# The selection by mouse clicks functions was inspired by the stack exchange discussion:
# https://stackoverflow.com/questions/25521120/store-mouse-click-event-coordinates-with-matplotlib

def onclick(event):
    global x, y
    y, x = event.xdata, event.ydata

    coords_x.append(x)
    coords_y.append(y)

    if len(coords_y) == 4:
        plt.close()     # closes after 4 clicks
    return


def onclick_z(event):
    global x, z
    z, x = event.xdata, event.ydata

    coords_z.append(z)  # only the z coordinates are saved

    if len(coords_z) == 2:
        plt.close()
    return

def cropping_func(oct, rotate):
    global coords_x, coords_y, coords_z
    coords_x = []
    coords_y = []
    coords_z = []

    if rotate == 'y':
        oct = sc.ndimage.interpolation.rotate(oct, axes=(2, 0), angle=90, reshape=True)
        oct = sc.ndimage.interpolation.rotate(oct, axes=(1, 2), angle=180, reshape=True)

    fig = plt.figure(1)
    ax = fig.add_subplot(111)
    ax.imshow(oct[:, :, int(oct.shape[2] / 2)], cmap='jet')

    # Call click func
    cid = fig.canvas.mpl_connect('button_press_event', onclick)
    plt.show()

    fig = plt.figure(1)
    ax = fig.add_subplot(111)
    ax.imshow(oct[int(oct.shape[0] / 2), :, :], cmap='jet')

    # Call click func
    cid = fig.canvas.mpl_connect('button_press_event', onclick_z)
    plt.show()

    x = (int(np.amin(coords_x)), int(np.amax(coords_x)))
    y = (int(np.amin(coords_y)), int(np.amax(coords_y)))
    z = (int(np.amin(coords_z)), int(np.amax(coords_z)))

    oct = np.array(oct[x[0]:x[1], y[0]:y[1], z[0]:z[1]])

    plt.rcParams.update({'font.size': 12})
    fig, ax = plt.subplots(1, 2)
    ax[0].imshow(oct[int(oct.shape[0] / 2), :, :], cmap='jet')
    ax[1].imshow(oct[:, :, int(oct.shape[2] / 2)], cmap='jet')
    plt.show()

    return oct, x, y, z


def cropping_dosimeters():

    ## Cropping the raw OCT files (not necessary in every run)
    # files are saved in a new "_crop" folder under the same name .............

    print('Select the OCT file')
    root = tk.Tk()
    root.withdraw()
    filename = filedialog.askopenfilename()

    if filename.endswith("mat"):
        mat = sc.io.loadmat(filename)
        oct = np.array(mat['OCT'])
    else:
        print('could not find .mat files')

    ans_rot = input('Rotate the data to match TOPAS? (y/n)')
    oct, x, y, z = cropping_func(oct, ans_rot)

    terminate = False
    while not terminate:
        ans = input('Continue cropping? (y/n)')
        if ans == 'y' or ans == 'Y':
            oct, x, y, z = cropping_func(oct, 'n')
        elif ans == 'n' or ans == 'N':
            terminate = True

    # saving the cropped data into a new folder
    file_dir = os.path.split(filename)[0]
    if not os.path.isdir(file_dir + "_crop"):
        os.mkdir(file_dir + "_crop")
    mdic = {"OCT": oct, "label": "experiment"}
    savemat(file_dir + "_crop" + "/" + os.path.split(filename)[1], mdic)


    # cropping all the other files in the folder in the same dimensions
    ans = input('Crop all the data set in the folder? (y/n)')

    if ans == 'y' or ans == 'Y':
        path = os.path.dirname(filename)
        for name in os.listdir(path):
            print(name)
            if name.endswith("mat"):
                # importing and cropping the data
                mat = sc.io.loadmat(path + str('/') + name)
                oct = np.array(mat['OCT'])
                oct = np.array(oct[x[0]:x[1], y[0]:y[1], z[0]:z[1]])
                # saving the data to the _crop folder
                if not os.path.isdir(file_dir + "_crop"):
                    os.mkdir(file_dir + "_crop")
                mdic = {"OCT": oct, "label": "experiment"}
                savemat(file_dir + "_crop" + "/" + os.path.split(name)[1], mdic)

    ans = input('Crop data sets from the folders as well? (y/n)')
    while ans == 'y' or ans == 'Y':
        path = filedialog.askdirectory()
        for name in os.listdir(path):
            print(name)
            if name.endswith("mat"):
                # importing and cropping the data
                mat = sc.io.loadmat(path + str('/') + name)
                oct = np.array(mat['OCT'])
                oct = np.array(oct[x[0]:x[1], y[0]:y[1], z[0]:z[1]])
                # saving the data to the _crop folder
                if not os.path.isdir(path + "_crop"):
                    os.mkdir(path + "_crop")
                mdic = {"OCT": oct, "label": "experiment"}
                savemat(path + "_crop" + "/" + os.path.split(name)[1], mdic)

        ans = input('Crop data sets from other folders as well? (y/n)')

    return


def cropping_TPS():
    ## Cropping the raw OCT files (not necessary in every run)
    # files are saved in a new "_crop" folder under the same name .............

    print('Select the OCT file')
    root = tk.Tk()
    root.withdraw()
    filename = filedialog.askopenfilename()

    if filename.endswith("mat"):
        mat = sc.io.loadmat(filename)
        oct = np.array(mat['OCT'])
    else:
        print('could not find .mat files')

    ans_rot = input('Rotate the data to match TOPAS? (y/n)')
    oct, x, y, z = cropping_func(oct, ans_rot)

    terminate = False
    while not terminate:
        ans = input('Continue cropping? (y/n)')
        if ans == 'y' or ans == 'Y':
            oct, x, y, z = cropping_func(oct, 'n')
        elif ans == 'n' or ans == 'N':
            terminate = True

    # saving the cropped data into a new folder
    file_dir = os.path.split(filename)[0]
    if not os.path.isdir(file_dir + "_crop"):
        os.mkdir(file_dir + "_crop")
    mdic = {"OCT": oct, "label": "experiment"}
    savemat(file_dir + "_crop" + "/" + os.path.split(filename)[1], mdic)

    # cropping all the other files in the folder in the same dimensions
    ans = input('Crop all the data set in the folder? (y/n)')

    if ans == 'y' or ans == 'Y':
        path = os.path.dirname(filename)
        for name in os.listdir(path):
            print(name)
            if name.endswith("mat"):
                # importing and cropping the data
                mat = sc.io.loadmat(path + str('/') + name)
                oct = np.array(mat['OCT'])
                oct = np.array(oct[x[0]:x[1], y[0]:y[1], z[0]:z[1]])
                # saving the data to the _crop folder
                if not os.path.isdir(file_dir + "_crop"):
                    os.mkdir(file_dir + "_crop")
                mdic = {"OCT": oct, "label": "experiment"}
                savemat(file_dir + "_crop" + "/" + os.path.split(name)[1], mdic)

    return


if __name__ == "__main__":
    cropping_dosimeters()