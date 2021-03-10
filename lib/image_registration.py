import scipy as sc
import os, os.path
from scipy.io import savemat
import numpy as np
import pydicom as dicom
import matplotlib.pyplot as plt
import scipy.ndimage
import pyelastix

def image_registration(oct):
    tps_dir = '../data/TPS/Dose_cropped.mat'
    tps_dose = np.ascontiguousarray(sc.io.loadmat(tps_dir)['TPS'])

    params = pyelastix.get_default_params(type='RIGID')
    params.MaximumNumberOfIterations = 200
    params.FinalGridSpacingInVoxels = 10

    # Apply the registration (im1 and im2 can be 2D or 3D)
    oct_deformed, field = pyelastix.register(oct, tps_dose, params)

    return oct_deformed

def cropping_tps():
       # importing the TPS dose
       path = "../data/TPS"
       file_list = []
       for dirName, subdirList, fileList in os.walk(path):
           for filename in fileList:
               if ".dcm" in filename.lower():  # check whether the file's DICOM
                   file_list.append(os.path.join(dirName, filename))

       TPS_dose = dicom.read_file(file_list[0])


       bol = 'y'
       while bol == 'y':
           TPS_dose_cropped, x, y, z = cropping_func(TPS_dose.pixel_array, 'y')
           #TPS_dose_cropped = sc.ndimage.interpolation.rotate(TPS_dose_cropped,
           #                                                   axes=(1, 2), angle=-180, reshape=True)
           TPS_dose_cropped = sc.ndimage.interpolation.rotate(TPS_dose_cropped,
                                                              axes=(1, 2), angle=180, reshape=True)

           bol = input('continue?')

       mdic = {"TPS": TPS_dose_cropped, "label": "eclipse"}
       savemat(path + '/' + 'Dose_cropped.mat', mdic)

       plt.style.use('seaborn-dark-palette')
       plt.rcParams.update({'font.size': 12})
       fig, ax = plt.subplots(1, 3, sharex=True)
       ax[0].imshow(TPS_dose_cropped[:, :, 40], cmap='jet')
       ax[1].imshow(TPS_dose_cropped[:, 40, :], cmap='jet')
       ax[2].imshow(TPS_dose_cropped[40, :, :], cmap='jet')
       plt.show()

def onclick(event):
    global x, y
    y, x = event.xdata, event.ydata

    coords_x.append(x)
    coords_y.append(y)

    if len(coords_y) == 4:
        plt.close()  # closes after 4 clicks
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

if __name__ == "__main__":

    d = '../data/reconstructions'


    subfolders = [os.path.join(d, o) for o in os.listdir(d)
                  if os.path.isdir(os.path.join(d, o))]

    '''
    subfolders1 = [i for i in subfolders if i.endswith('5_ca')]
    for i in subfolders1:
        for name in os.listdir(i):
            if name.endswith("mat"):
                mat = sc.io.loadmat(i + str('/') + name)
                OCT = np.array(mat['OCT'])
                oct_regs = image_registration(np.ascontiguousarray(OCT))
                mdic = {"OCT": oct_regs, "label": "experiment"}
                savemat(i + '_regs' + '/' + name, mdic)
    '''
    subfolders2 = [i for i in subfolders if i.endswith('9_ca')]
    for i in subfolders2:
        for name in os.listdir(i):
            if name.endswith("mat"):
                mat = sc.io.loadmat(i + str('/') + name)
                OCT = np.array(mat['OCT'])
                try:
                    oct_regs = image_registration(np.ascontiguousarray(OCT))
                    mdic = {"OCT": oct_regs, "label": "experiment"}
                    savemat(i + '_regs' + '/' + name, mdic)
                except:
                    mdic = {"OCT": OCT, "label": "experiment"}
                    savemat(i + '_regs' + '/' + name, mdic)