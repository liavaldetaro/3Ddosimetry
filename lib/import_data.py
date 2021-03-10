import scipy as sc
import os, os.path
from scipy.io import savemat
import numpy as np
import pydicom as dicom
import matplotlib.pyplot as plt
import scipy.ndimage

class Dos_class():
    dos_list = []

    def __init__(self, dos_number=None, OCT=None, irrad_days=None, readout_hours=None,
                 side=None, CA=None, temp=None, tps_dose=None, dose_levels=None):
        self.dos_list.append(self)
        self.OCT = OCT
        self.irrad_days = irrad_days
        self.readout_hours = readout_hours
        self.side = side
        self.dos_number = dos_number
        self.CA = CA
        self.temp = temp
        self.tps_dose = tps_dose
        self.dose_levels = dose_levels

    def __str__(self):
        return "Dosimeter number {}, readout hours {}, CA {}".format(self.dos_number, self.readout_hours, self.CA)


def determine_temp(dosimeter):
    if int(dosimeter.dos_number) == 1 or int(dosimeter.dos_number) == 4:
        if int(dosimeter.CA) == 9:
            dosimeter.temp = -5
        else:
            dosimeter.temp = 5
    if int(dosimeter.dos_number) == 2 or int(dosimeter.dos_number) == 5:
        dosimeter.temp = 15
    if int(dosimeter.dos_number) == 3 or int(dosimeter.dos_number) == 6:
        dosimeter.temp = 20

    return dosimeter.temp

def pol2cart(rho, phi):
    y = rho * np.cos(phi)
    z = rho * np.sin(phi)
    return y, z

def determine_dose_lvls(dosimeter):
    x = int(dosimeter.OCT.shape[0] / 2)
    y = int(dosimeter.OCT.shape[1] / 2)
    z = int(dosimeter.OCT.shape[2] / 2)

    n = 2
    m = 5

    dosimeter.dose_levels = np.mean(np.mean(dosimeter.OCT[x-m:x+m, y - n:y + n, 20:25], axis=0))

    return dosimeter.dose_levels

def imp_data():

    # tps import
    tps_dir = 'data/TPS/Dose_cropped.mat'

    # data import
    d = 'data/reconstructions/'
    subfolders = [os.path.join(d, o) for o in os.listdir(d)
                  if os.path.isdir(os.path.join(d, o))]

    subfolders1 = [i for i in subfolders if i.endswith('5_ca_regs')]
    for i in subfolders1:
        for name in os.listdir(i):
            if name.endswith("mat"):
                dosimeter = Dos_class()
                dosimeter.tps_dose = sc.io.loadmat(tps_dir)['TPS']#[0:30, 10:50, 10:50]
                mat = sc.io.loadmat(i + str('/') + name)
                OCT = np.array(mat['OCT'])

                if name[6] == 'b':
                    dos_side = 'bottom'
                elif name[6] == 't':
                    dos_side = 'top'

                dosimeter.dos_number = name[4]
                dosimeter.OCT = OCT #[0:30, 10:50, 10:50]
                dosimeter.readout_hours = name[-11:-8]
                dosimeter.side = dos_side
                dosimeter.CA = 5
                dosimeter.temp = determine_temp(dosimeter)
                dosimeter.dose_levels = determine_dose_lvls(dosimeter)

    subfolders2 = [i for i in subfolders if i.endswith('9_ca_regs')]
    for i in subfolders2:
        for name in os.listdir(i):
            if name.endswith("mat"):
                dosimeter = Dos_class()
                dosimeter.tps_dose = sc.io.loadmat(tps_dir)['TPS']
                mat = sc.io.loadmat(i + str('/') + name)
                OCT = np.array(mat['OCT'])

                if name[6] == 'b':
                    dos_side = 'bottom'
                elif name[6] == 't':
                    dos_side = 'top'

                dosimeter.dos_number = name[4]
                dosimeter.OCT = np.array(mat['OCT'])#[0:30, 10:50, 10:50]
                dosimeter.readout_hours = name[-11:-8]
                dosimeter.side = dos_side
                dosimeter.CA = 9
                dosimeter.temp = determine_temp(dosimeter)
                dosimeter.dose_levels = determine_dose_lvls(dosimeter)


    # checking that all the files were imported
    print([str(dosimeter) for dosimeter in Dos_class.dos_list])

if __name__ == "__main__":
    imp_data()