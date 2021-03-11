import matplotlib.pyplot as plt
import scipy as sc
import os, os.path
from scipy.io import savemat
import numpy as np
import seaborn as sns
from lib.import_data import imp_data, Dos_class
from scipy import stats

def main():
    imp_data()
    dosimeter = Dos_class.dos_list
    marker_list = ['s', 'd', 'o', 'h', 'p', '^']
    n = 1
    plt.style.use('seaborn-dark-palette')
    plt.rcParams.update({'font.size': 12})
    c_string = sns.color_palette("dark", 7)
    fig, ax = plt.subplots(1, 1, sharex=True)

    #dosimeter = [i.score for i in names if i.gender == "Male"]

    alpha_list = []
    temp_list = []
    alpha_list2 = []
    temp_list2 = []
    alpha_list1 = []
    temp_list1 = []
    alpha_list3 = []
    temp_list3 = []
    for m in range(1, 7):
        '''
        dos_list = [i.dose_levels for i in Dos_class.dos_list
                    if int(i.dos_number) == m and int(i.CA) == 9 and i.side == 'bottom']
        hrs_list = [i.readout_hours for i in Dos_class.dos_list
                    if int(i.dos_number) == m and int(i.CA) == 9 and i.side == 'bottom']

        hrs_list, dos_list = zip(*sorted(zip(hrs_list, dos_list)))
        hrs_list = np.array(hrs_list).astype(np.float)
        dos_list = np.array(dos_list).astype(np.float)
        slope, intercept, r_value, p_value, std_err = stats.linregress(hrs_list, dos_list)

        ax[1].errorbar(hrs_list, dos_list,
                       markersize=5, marker='s', linestyle='None', capsize=3)
        hrs = np.linspace(np.amin(hrs_list), np.amax(hrs_list))

        ax[1].plot(hrs, slope * hrs + intercept, color='black')

        if m >= 4:
            alpha_list1.append(slope)
            temp_list1.append([i.temp for i in Dos_class.dos_list
                              if int(i.dos_number) == m and int(i.CA) == 9 and i.side == 'bottom'][0])
        else:
            alpha_list3.append(slope)
            temp_list3.append([i.temp for i in Dos_class.dos_list
                               if int(i.dos_number) == m and int(i.CA) == 9 and i.side == 'bottom'][0])
        '''
        dos_list = [i.dose_levels for i in Dos_class.dos_list
                    if int(i.dos_number) == m and int(i.CA) == 5 and i.side == 'bottom']
        hrs_list = [i.readout_hours for i in Dos_class.dos_list
                    if int(i.dos_number) == m and int(i.CA) == 5 and i.side == 'bottom']
        print(hrs_list)
        hrs_list, dos_list = zip(*sorted(zip(hrs_list, dos_list)))
        hrs_list = np.array(hrs_list).astype(np.float)
        dos_list = np.array(dos_list).astype(np.float)
        slope, intercept, r_value, p_value, std_err = stats.linregress(hrs_list, dos_list)

        ax.errorbar(hrs_list, dos_list,
                       markersize=5, marker='s', linestyle='None', capsize=3)
        hrs = np.linspace(np.amin(hrs_list), np.amax(hrs_list))

        if m >= 4:
            alpha_list.append(slope)
            temp_list.append([i.temp for i in Dos_class.dos_list
                              if int(i.dos_number) == m and int(i.CA) == 5 and i.side == 'bottom'][0])
        else:
            alpha_list2.append(slope)
            temp_list2.append([i.temp for i in Dos_class.dos_list
                              if int(i.dos_number) == m and int(i.CA) == 5 and i.side == 'bottom'][0])
        ax.plot(hrs, slope * hrs + intercept, color='black')
    plt.xlabel('Hours after production')
    plt.show()

    plt.style.use('seaborn-dark-palette')
    plt.rcParams.update({'font.size': 12})
    c_string = sns.color_palette("dark", 7)
    fig, ax = plt.subplots(1, 1)
    ax.plot(np.array(temp_list).astype(np.float) + 273, alpha_list, marker='*', linestyle='None')
    ax.plot(np.array(temp_list2).astype(np.float) + 273, alpha_list2, marker='x', linestyle='None')
    #ax.plot(np.array(temp_list1).astype(np.float) + 273, alpha_list1, marker='o', linestyle='None')
    #ax.plot(np.array(temp_list3).astype(np.float) + 273, alpha_list3, marker='d', linestyle='None')
    ax.set_ylabel('Auto oxidation rate [cm${}^{-1}$ hrs${}^{-1}$]')
    ax.set_xlabel('Temperature [K]')
    #ax.plot(np.array(temp_list1).astype(np.float), alpha_list1, marker='*', linestyle='None')
    plt.show()


    plt.style.use('seaborn-dark-palette')
    plt.rcParams.update({'font.size': 12})
    fig, ax = plt.subplots(1, 7)
    i = 0

    for dos in Dos_class.dos_list:
        if int(dos.CA) == 5 and dos.side == 'top':
            oct = dos.OCT
            tps = dos.tps_dose/np.amax(dos.tps_dose) * 6
            #vals = oct/tps
            n = int(oct.shape[1]/2)
            im = ax[i].imshow(oct[int(oct.shape[0]/2), :, :])
            ax[i].set_title(dos.readout_hours)
            #fig.colorbar(im, ax=ax[i])
            i = i + 1
            if i == 7:
                #ax.plot(np.mean(tps[n-2:n+2, int(oct.shape[2] / 2), 6:50], axis=0)/20)
                break

    plt.show()


if __name__ == "__main__":
    main()