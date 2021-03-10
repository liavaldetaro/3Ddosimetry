import matplotlib.pyplot as plt
import scipy as sc
import os, os.path
from scipy.io import savemat
import numpy as np
import seaborn as sns


class Dos_class():
    dos_list = []

    def __init__(self, dos_number=None, OCT=None, irrad_days=None, readout_days=None, side=None):
        self.dos_list.append(self)
        self.OCT = OCT
        self.irrad_days = irrad_days
        self.readout_days = readout_days
        self.side = side
        self.dos_number = dos_number

    def __str__(self):
        return "Dosimeter number {}, readout day {}".format(self.dos_number, self.readout_days)


def import_data():
    # data import
    d = 'data/reconstructions'
    subfolders = [os.path.join(d, o) for o in os.listdir(d)
                  if os.path.isdir(os.path.join(d, o))]

    subfolders = [i for i in subfolders if i.endswith('_crop_aligned_aligned_crop')]

    for i in subfolders:
        for name in os.listdir(i):
            if name.endswith("mat"):

                mat = sc.io.loadmat(i + str('/') + name)
                OCT = np.array(mat['OCT'])

                if name[6] == 'b':
                    dos_side = 'bottom'
                elif name[6] == 't':
                    dos_side = 'top'

                dosimeter = Dos_class()
                dosimeter.dos_number = name[4]
                dosimeter.OCT = np.array(mat['OCT'])
                dosimeter.readout_days = name[-5]
                dosimeter.side = dos_side

    # checking that all the files were imported
    print([str(dosimeter) for dosimeter in Dos_class.dos_list])


def main():
    import_data()


    '''

    ### figure 1
    plt.style.use('seaborn-dark-palette')
    plt.rcParams.update({'font.size': 12})
    c_string = sns.color_palette("dark", 7)
    # plt.rcParams['figure.constrained_layout.use'] = True
    fig, ax = plt.subplots(3, 3)  # constrained_layout=True)

    fig.set_size_inches(9.5, 8.5)
    n = 5
    for dosimeter in Dos_class.dos_list:

        if int(dosimeter.dos_number) == 1:
            x = int(dosimeter.OCT.shape[0] / 2)
            y = int(dosimeter.OCT.shape[1] / 2)
            z = int(dosimeter.OCT.shape[2] / 2)

            dos_lat_1 = np.mean(dosimeter.OCT[x-n:x+n, y, :], axis=0)
            dos_lat_2 = np.mean(dosimeter.OCT[x-n:x+n, :, z], axis=0)
            dos_depth = np.mean(dosimeter.OCT[:, y-n:y+n, z], axis=1)

            x_top = np.linspace(0, len(dos_depth), len(dos_depth))
            x_bottom = np.linspace(10, len(dos_depth) + 10, len(dos_depth))

            if dosimeter.side == 'bottom':
                ax[0, 0].plot(np.flip(dos_lat_1), linestyle='-.',
                              color=c_string[int(dosimeter.readout_days)])
                ax[0, 1].plot(np.flip(dos_lat_2), linestyle='-.', color=c_string[int(dosimeter.readout_days)])
                ax[0, 2].plot(x_bottom, np.flip(dos_depth), linestyle='-.', color=c_string[int(dosimeter.readout_days)])

            else:
                ax[0, 0].plot(dos_lat_1, color=c_string[int(dosimeter.readout_days)])
                ax[0, 1].plot(dos_lat_2, color=c_string[int(dosimeter.readout_days)])
                ax[0, 2].plot(x_top, dos_depth, color=c_string[int(dosimeter.readout_days)])


            ax[0, 0].title.set_text('Lateral view 2')
            ax[0, 1].title.set_text('Lateral view 1')
            ax[0, 2].title.set_text('Bottom-to-top view')

            ax[0, 0].set_ylabel('$\Delta$OD [cm${}^{-1}]$')
            ax[0, 0].set_ylim(0, 0.40)
            ax[0, 1].set_ylim(0, 0.40)
            ax[0, 2].set_ylim(0, 0.40)



        if int(dosimeter.dos_number) == 2:
            x = int(dosimeter.OCT.shape[0] / 2)
            y = int(dosimeter.OCT.shape[1] / 2)
            z = int(dosimeter.OCT.shape[2] / 2)

            dos_lat_1 = np.mean(dosimeter.OCT[x, y - n:y + n, :], axis=0)
            dos_depth = np.mean(dosimeter.OCT[:, y - n:y + n, z], axis=1)
            dos_lat_2 = np.mean(dosimeter.OCT[x, :, z - n:z + n], axis=1)

            x_top = np.linspace(0, len(dos_depth), len(dos_depth))
            x_bottom = np.linspace(10, len(dos_depth) + 10, len(dos_depth))

            if dosimeter.side == 'bottom':
                ax[1, 0].plot(np.flip(dos_lat_1), label=dosimeter.readout_days, linestyle='-.',
                              color=c_string[int(dosimeter.readout_days)])
                ax[1, 1].plot(np.flip(dos_lat_2), label=dosimeter.readout_days, linestyle='-.',
                              color=c_string[int(dosimeter.readout_days)])
                ax[1, 2].plot(x_bottom, np.flip(dos_depth), linestyle='-.', color=c_string[int(dosimeter.readout_days)])
            else:
                ax[1, 0].plot(dos_lat_1, color=c_string[int(dosimeter.readout_days)])
                ax[1, 1].plot(dos_lat_2, color=c_string[int(dosimeter.readout_days)])
                ax[1, 2].plot(x_top, dos_depth, color=c_string[int(dosimeter.readout_days)])

            ax[1, 0].set_ylabel('$\Delta$OD [cm${}^{-1}]$')
            ax[1, 0].set_ylim(0, 0.40)
            ax[1, 1].set_ylim(0, 0.40)
            ax[1, 2].set_ylim(0, 0.40)


        if int(dosimeter.dos_number) == 3:
            x = int(dosimeter.OCT.shape[0] / 2)
            y = int(dosimeter.OCT.shape[1] / 2)
            z = int(dosimeter.OCT.shape[2] / 2)

            dos_lat_1 = np.mean(dosimeter.OCT[x, y - n:y + n, :], axis=0)
            dos_depth = np.mean(dosimeter.OCT[:, y - n:y + n, z], axis=1)
            dos_lat_2 = np.mean(dosimeter.OCT[x, :, z - n:z + n], axis=1)

            x_top = np.linspace(0, len(dos_depth), len(dos_depth))
            x_bottom = np.linspace(10, len(dos_depth) + 10, len(dos_depth))

            if dosimeter.side == 'bottom':
                ax[2, 0].plot(np.flip(dos_lat_1),  linestyle='-.',
                              color=c_string[int(dosimeter.readout_days)])
                ax[2, 1].plot(np.flip(dos_lat_2), linestyle='-.',
                              color=c_string[int(dosimeter.readout_days)])
                ax[2, 2].plot(x_bottom, np.flip(dos_depth), linestyle='-.', color=c_string[int(dosimeter.readout_days)])
            elif dosimeter.side == 'top' and int(dosimeter.readout_days) == 1:
                continue
            else:
                ax[2, 0].plot(dos_lat_1, color=c_string[int(dosimeter.readout_days)])
                ax[2, 1].plot(dos_lat_2, color=c_string[int(dosimeter.readout_days)])
                ax[2, 2].plot(x_top, dos_depth, color=c_string[int(dosimeter.readout_days)])

            ax[2, 0].set_ylabel('$\Delta$OD [cm${}^{-1}]$')
            ax[2, 0].set_xlabel('Depth [mm]')
            ax[2, 1].set_xlabel('Depth [mm]')
            ax[2, 2].set_xlabel('Depth [mm]')

            ax[2, 0].set_ylim(0, 0.40)
            ax[2, 1].set_ylim(0, 0.40)
            ax[2, 2].set_ylim(0, 0.40)

    from matplotlib.lines import Line2D

    colors = [c_string[1], c_string[2], c_string[4], c_string[5], c_string[6]]
    lines = [Line2D([0], [0], color=c, linestyle='-') for c in colors]
    labels = ['0', '1', '3', '4', '5']
    legend2 = plt.legend(lines, labels, title='Days after irradiation', ncol=6, bbox_to_anchor=(1.035, -0.47),
                         fancybox=True, framealpha=0.3)
    plt.gca().add_artist(legend2)

    styles = ['-', '--']
    lines = [Line2D([0], [0], color='black', linestyle=c) for c in styles]
    labels = ['Top', 'Bottom']
    legend1 = plt.legend(lines, labels, bbox_to_anchor=(-0.97, -0.47), fancybox=True, framealpha=0.3)
    plt.gca().add_artist(legend1)

    props = dict(boxstyle='round', facecolor='White', edgecolor='gray', alpha=0.4)
    ax[0, 0].text(0.05, 0.90, '5 $ ^{\circ}$C', transform=ax[0, 0].transAxes,
                  verticalalignment='top', bbox=props)
    ax[1, 0].text(0.05, 0.90, '15 $ ^{\circ}$C', transform=ax[1, 0].transAxes,
                  verticalalignment='top', bbox=props)

    ax[2, 0].text(0.05, 0.90, '20 $ ^{\circ}$C', transform=ax[2, 0].transAxes,
                  verticalalignment='top', bbox=props)

    plt.tight_layout()
    plt.savefig('plots/fields_cross_section_dos_1_2_3.png', bbox_inches='tight', dpi=600)
    plt.show()

    





    ### figure 2
    plt.style.use('seaborn-dark-palette')
    plt.rcParams.update({'font.size': 12})
    c_string = sns.color_palette("dark", 7)
    #plt.rcParams['figure.constrained_layout.use'] = True
    fig, ax = plt.subplots(3, 2)#constrained_layout=True)

    #fig.set_size_inches(9.5, 8.5)
    n = 5
    for dosimeter in Dos_class.dos_list:

        if int(dosimeter.dos_number) == 4:
            x = int(dosimeter.OCT.shape[0] / 2)
            y = int(dosimeter.OCT.shape[1] / 2)
            z = int(dosimeter.OCT.shape[2] / 2)

            dos_lat_1 = np.mean(dosimeter.OCT[x, y - n:y + n, :], axis=0)
            dos_depth = np.mean(dosimeter.OCT[:, y - n:y + n, z], axis=1)
            dos_lat_2 = np.mean(dosimeter.OCT[x, :, z - n:z + n], axis=0)

            x_top = np.linspace(0, len(dos_depth), len(dos_depth))
            x_bottom = np.linspace(10, len(dos_depth) + 10, len(dos_depth))

            if dosimeter.side == 'bottom':
                ax[0, 0].plot(np.flip(dos_lat_1), label=dosimeter.readout_days, linestyle='-.',
                              color=c_string[int(dosimeter.readout_days)])
                ax[0, 1].plot(x_bottom, np.flip(dos_depth), linestyle='-.', color=c_string[int(dosimeter.readout_days)])
            else:
                ax[0, 0].plot(dos_lat_1, color=c_string[int(dosimeter.readout_days)])
                ax[0, 1].plot(x_top, dos_depth, color=c_string[int(dosimeter.readout_days)])
            # ax[0].legend(bbox_to_anchor=(1.05, 1), loc='upper left')
            #ax[3, 0].title.set_text('Dosimeter 4')
            #ax[3, 1].title.set_text('Dosimeter 4')
            ax[0, 0].set_ylabel('$\Delta$OD [cm${}^{-1}]$')
            ax[0, 0].title.set_text('Lateral view')
            ax[0, 1].title.set_text('Bottom-to-top view')

            ax[0, 0].set_ylim(0, 0.35)
            ax[0, 1].set_ylim(0, 0.35)



        if int(dosimeter.dos_number) == 5:
            x = int(dosimeter.OCT.shape[0] / 2)
            y = int(dosimeter.OCT.shape[1] / 2)
            z = int(dosimeter.OCT.shape[2] / 2)

            dos_lat_1 = np.mean(dosimeter.OCT[x, y - n:y + n, :], axis=0)
            dos_depth = np.mean(dosimeter.OCT[:, y - n:y + n, z], axis=1)
            dos_lat_2 = np.mean(dosimeter.OCT[x, :, z - n:z + n], axis=0)

            x_top = np.linspace(0, len(dos_depth), len(dos_depth))
            x_bottom = np.linspace(10, len(dos_depth) + 10, len(dos_depth))

            if dosimeter.side == 'bottom':
                ax[1, 0].plot(np.flip(dos_lat_1), label=dosimeter.readout_days, linestyle='-.',
                              color=c_string[int(dosimeter.readout_days)])
                ax[1, 1].plot(x_bottom, np.flip(dos_depth), linestyle='-.', color=c_string[int(dosimeter.readout_days)])
            else:
                ax[1, 0].plot(dos_lat_1, color=c_string[int(dosimeter.readout_days)])
                ax[1, 1].plot(x_top, dos_depth, color=c_string[int(dosimeter.readout_days)])

            ax[1, 0].set_ylabel('$\Delta$OD [cm${}^{-1}]$')
            ax[1, 0].set_ylim(0, 0.35)
            ax[1, 1].set_ylim(0, 0.35)



        if int(dosimeter.dos_number) == 6:
            x = int(dosimeter.OCT.shape[0] / 2)
            y = int(dosimeter.OCT.shape[1] / 2)
            z = int(dosimeter.OCT.shape[2] / 2)

            dos_lat_1 = np.mean(dosimeter.OCT[x, y - n:y + n, :], axis=0)
            dos_depth = np.mean(dosimeter.OCT[:, y - n:y + n, z], axis=1)
            dos_lat_2 = np.mean(dosimeter.OCT[x, :, z - n:z + n], axis=0)

            x_top = np.linspace(0, len(dos_depth), len(dos_depth))
            x_bottom = np.linspace(10, len(dos_depth) + 10, len(dos_depth))

            if dosimeter.side == 'bottom':
                ax[2, 0].plot(np.flip(dos_lat_1), label=dosimeter.readout_days, linestyle='-.',
                              color=c_string[int(dosimeter.readout_days)])
                ax[2, 1].plot(x_bottom, np.flip(dos_depth), linestyle='-.', color=c_string[int(dosimeter.readout_days)])
            else:
                ax[2, 0].plot(dos_lat_1, color=c_string[int(dosimeter.readout_days)])
                ax[2, 1].plot(x_top, dos_depth, color=c_string[int(dosimeter.readout_days)])

            ax[2, 0].set_ylabel('$\Delta$OD [cm${}^{-1}]$')
            ax[2, 0].set_xlabel('Depth [mm]')
            ax[2, 1].set_xlabel('Depth [mm]')
            ax[2, 0].set_ylim(0, 0.35)
            ax[2, 1].set_ylim(0, 0.35)

    from matplotlib.lines import Line2D

    colors = [c_string[1], c_string[2], c_string[3], c_string[5], c_string[6]]
    lines = [Line2D([0], [0], color=c,  linestyle='-') for c in colors]
    labels = ['0', '1', '2', '4', '5']
    legend2 = plt.legend(lines, labels, title='Days after irradiation', ncol=6, bbox_to_anchor=(1.035, -0.47), fancybox=True, framealpha=0.3)
    plt.gca().add_artist(legend2)

    styles = ['-', '--']
    lines = [Line2D([0], [0], color='black', linestyle=c) for c in styles]
    labels = ['Top', 'Bottom']
    legend1 = plt.legend(lines, labels, bbox_to_anchor=(-0.97, -0.47), fancybox=True, framealpha=0.3)
    plt.gca().add_artist(legend1)

    props = dict(boxstyle='round', facecolor='White', edgecolor='gray', alpha=0.4)
    ax[0, 0].text(0.05, 0.90, '5 $ ^{\circ}$C', transform=ax[0, 0].transAxes,
                  verticalalignment='top', bbox=props)
    ax[1, 0].text(0.05, 0.90, '15 $ ^{\circ}$C', transform=ax[1, 0].transAxes,
                  verticalalignment='top', bbox=props)

    ax[2, 0].text(0.05, 0.90, '20 $ ^{\circ}$C', transform=ax[2, 0].transAxes,
                  verticalalignment='top', bbox=props)

    plt.tight_layout()
    plt.savefig('plots/fields_cross_section_dos_4_5_6.png',  bbox_inches='tight', dpi=600)
    plt.show()


    '''


    #### figure 2

    signal_list = np.zeros(shape=(6, 2, 6))  # dosimeter number, side, day
    signal_list_2 = np.zeros(shape=(6, 2, 6))  # dosimeter number, side, day

    background_list = np.zeros(shape=(6, 2, 6))
    signal_list_error = np.zeros(shape=(6, 2, 6))
    background_list_error = np.zeros(shape=(6, 2, 6))
    marker_list = ['s', 'd', 'o', 'h', 'p', '^']
    n = 1
    for dosimeter in Dos_class.dos_list:

        x = int(dosimeter.OCT.shape[0] / 2)
        y = int(dosimeter.OCT.shape[1] / 2)
        z = int(dosimeter.OCT.shape[2] / 2)

        dos_background = np.mean(np.mean(dosimeter.OCT[x, y - n:y + n, 7:10], axis=0))
        dos_signal = np.mean(np.mean(dosimeter.OCT[x, y - n:y + n, 21:25], axis=0))
        dos_signal_2 = np.mean(np.mean(dosimeter.OCT[x, 7:10, z-n:z+n], axis=0))

        dos_signal_error = np.std(np.std(dosimeter.OCT[x, y - n:y + n, 7:10], axis=0))
        dos_background_error = np.std(np.mean(dosimeter.OCT[x, y - n:y + n, 21:25], axis=0))

        if dosimeter.side == 'top':
            i = 0
        else:
            i = 1
        signal_list[int(dosimeter.dos_number) - 1,
                    i, int(dosimeter.readout_days) - 1] = dos_signal
        background_list[int(dosimeter.dos_number) - 1,
                        i, int(dosimeter.readout_days) - 1] = dos_background
        signal_list_error[int(dosimeter.dos_number) - 1,
                          i, int(dosimeter.readout_days) - 1] = dos_signal_error
        background_list_error[int(dosimeter.dos_number) - 1,
                              i, int(dosimeter.readout_days) - 1] = dos_background_error

        signal_list_2[int(dosimeter.dos_number) - 1, i, int(dosimeter.readout_days) - 1] = dos_signal_2

    plt.style.use('seaborn-dark-palette')
    plt.rcParams.update({'font.size': 12})
    c_string = sns.color_palette("dark", 7)
    fig, ax = plt.subplots(1, 1)
    for i in range(0, 6):
        dosimeter_signal = np.zeros(6)
        dosimeter_background = np.zeros(6)
        dosimeter_signal_error = np.zeros(6)
        dosimeter_background_error = np.zeros(6)
        days_list = np.zeros(6)

        dosimeter_signal_2 = np.zeros(6)

        m = 0
        for j in range(0, 6):

            if signal_list[i, 0, j] == 0 and signal_list[i, 1, j] == 0:
                continue
            elif signal_list[i, 0, j] == 0:
                signal = signal_list[i, 1, j]
                background = background_list[i, 1, j]
                signal_error = signal_list_error[i, 1, j]
                background_error = background_list_error[i, 1, j]

                signal_2 = signal_list_2[i, 1, j]

                day = j + 1
            elif signal_list[i, 1, j] == 0:
                signal = signal_list[i, 0, j]
                background = background_list[i, 0, j]
                signal_error = signal_list_error[i, 0, j]
                background_error = background_list_error[i, 0, j]

                signal_2 = signal_list_2[i, 0, j]

                day = j + 1

            elif i == 2 and j == 0:
                signal = signal_list[i, 1, j]
                background = background_list[i, 1, j]
                signal_error = signal_list_error[i, 1, j]
                background_error = background_list_error[i, 1, j]

                signal_2 = signal_list[i, 1, j]

                day = j + 1
            else:
                signal = (signal_list[i, 0, j] + signal_list[i, 1, j]) / 2
                background = (background_list[i, 0, j] + background_list[i, 1, j]) / 2
                signal_error = (signal_list_error[i, 0, j] + signal_list_error[i, 1, j])/2
                background_error = (background_list_error[i, 0, j] + background_list_error[i, 1, j])/2

                signal_2 = (signal_list_2[i, 0, j] + signal_list_2[i, 1, j]) / 2

                day = j + 1

            if i > 2:
                day = day + 3

            days_list[j] = day
            dosimeter_signal[j] = signal
            dosimeter_background[j] = background
            dosimeter_signal_error[j] = signal_error
            dosimeter_background_error[j] = background_error

            dosimeter_signal_2[j] = signal_2


        if i < 3:
            dosimeter_signal = np.delete(dosimeter_signal, 2)
            dosimeter_background = np.delete(dosimeter_background, 2)
            dosimeter_signal_error = np.delete(dosimeter_signal_error, 2)
            dosimeter_background_error = np.delete(dosimeter_background_error, 2)

            days_list = np.delete(days_list, 2)

            dosimeter_signal_2 = np.delete(dosimeter_signal_2, 2)

        else:
            dosimeter_signal = np.delete(dosimeter_signal, 3)
            dosimeter_background = np.delete(dosimeter_background, 3)
            dosimeter_signal_error = np.delete(dosimeter_signal_error, 3)
            dosimeter_background_error = np.delete(dosimeter_background_error, 3)

            dosimeter_signal_2 = np.delete(dosimeter_signal_2, 3)

            days_list = np.delete(days_list, 3)

        days_list = days_list + 3
        if i == 0 or i == 3:
            temp = 0
        elif i == 1 or i == 4:
            temp = 2
        else:
            temp = 3


        #plt.errorbar(days_list, dosimeter_signal, color=c_string[temp], marker='*', markersize=8, linestyle='-', label=i+1)
        plt.errorbar(days_list, dosimeter_background, yerr=dosimeter_background_error,
                     color=c_string[temp],  markersize=5, marker='*', linestyle='--', capsize=3)
        plt.errorbar(days_list, dosimeter_signal_2, yerr=dosimeter_signal_error,
                     color=c_string[temp], markersize=5, marker='*', linestyle='-', capsize=3)



    plt.axvline(x=4, color='gray', alpha=0.6, linestyle='--')
    plt.axvline(x=7, color='gray', alpha=0.6, linestyle='--')
    plt.text(4, 0.42, 'Irradiation (group 1)', rotation=0)
    plt.text(7, 0.42, 'Irradiation (group 2)', rotation=0)

    plt.xlabel('Days after casting')
    plt.ylabel('$\Delta$OD')

    from matplotlib.lines import Line2D
    styles = ['-',  '--']
    lines = [Line2D([0], [0], color='black',  linestyle=c) for c in styles]
    labels = ['Signal', 'Background']
    legend1 = plt.legend(lines, labels, loc='lower right', fancybox=True, framealpha=0.3)
    plt.gca().add_artist(legend1)

    colors = [c_string[0], c_string[2], c_string[3]]
    lines = [Line2D([0], [0], color=c,  linestyle='-', marker='*', markersize=5) for c in colors]
    labels = ['5', '15', '20']
    legend2 = plt.legend(lines, labels, title='Storage [$^{\circ}$C]', loc='upper right', fancybox=True, framealpha=0.3)
    plt.gca().add_artist(legend2)

    #plt.legend(bbox_to_anchor=(1.0, 1), loc='upper left', title='Dosimeter')

    plt.tight_layout()
    plt.savefig('plots/bg_signal_ratio.png', dpi=600)
    plt.show()



    plt.style.use('seaborn-dark-palette')
    plt.rcParams.update({'font.size': 15})
    c_string = sns.color_palette("dark", 7)
    # plt.rcParams['figure.constrained_layout.use'] = True
    fig, ax = plt.subplots(3, 5, sharex=True, sharey=True)  # constrained_layout=True)
    fig.set_size_inches(12, 5.5)

    dos_lat_2_base = [0, 0, 0, 0, 0, 0]
    print(dos_lat_2_base)
    for dosimeter in Dos_class.dos_list:
        if int(dosimeter.readout_days) == 1:
            if int(dosimeter.dos_number) == 1 or int(dosimeter.dos_number) == 2 or int(dosimeter.dos_number) == 3:
                if dosimeter.side == 'top':
                    x = int(dosimeter.OCT.shape[0] / 2)
                    y = int(dosimeter.OCT.shape[1] / 2)
                    z = int(dosimeter.OCT.shape[2] / 2)

                    dos_lat_2_base[int(dosimeter.dos_number) - 1] = dosimeter.OCT[:, y, :]
                    if int(dosimeter.dos_number) == 3:
                        dos_lat_2_base[2] = dos_lat_2_base[0]

    n = 5
    for dosimeter in Dos_class.dos_list:
        if int(dosimeter.dos_number) == 1 or int(dosimeter.dos_number) == 2 or int(dosimeter.dos_number) == 3:

            if dosimeter.side == 'bottom':
                continue

            dos_lat_2 = dosimeter.OCT[:, y, :] - dos_lat_2_base[int(dosimeter.dos_number) - 1]

            if int(dosimeter.readout_days) == 1:
                dos_lat_2 = dos_lat_2_base[int(dosimeter.dos_number) - 1]

            i = int(dosimeter.readout_days) - 1

            if i >= 2:
                i = i - 1

            im = ax[int(dosimeter.dos_number) - 1 - 3, i].imshow(dos_lat_2, vmin=0, vmax=0.35, cmap='jet')


            #ax[int(dosimeter.dos_number) - 1, i].set_xticklabels([])
            #ax[int(dosimeter.dos_number) - 1, i].set_yticklabels([])


    fig.colorbar(im, ax=ax.ravel().tolist(), label='$\Delta \mathrm{OD} -\Delta \mathrm{OD}_{\mathrm{day\, 0}}$ ')

    ax[0, 0].set_ylabel('5${}^\circ$C\n Depth [mm]')
    ax[1, 0].set_ylabel('15${}^\circ$C\n Depth [mm]')
    ax[2, 0].set_ylabel('20${}^\circ$C\n Depth [mm]')
    ax[2, 0].set_xlabel('Width [mm]')
    ax[2, 1].set_xlabel('Width [mm]')
    ax[2, 2].set_xlabel('Width [mm]')
    ax[2, 3].set_xlabel('Width [mm]')
    ax[2, 4].set_xlabel('Width [mm]')

    ax[0, 0].set_title('Day 0')
    ax[0, 1].set_title('Day 1')
    ax[0, 2].set_title('Day 3')
    ax[0, 3].set_title('Day 4')
    ax[0, 4].set_title('Day 5')

    plt.savefig('plots/diff_dos_1_2_3.svg', dpi=600)

    plt.show()



if __name__ == "__main__":
    main()
