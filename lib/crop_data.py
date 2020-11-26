import numpy as np
import matplotlib.pyplot as plt
import scipy as sc

# -------------------------------------------------------------------------------------------------
# Selects the cropping boundaries of the 3D data by prompting the users to click on the data slices.
# The user can choose between cropping the data sets separately, or applying the same values to all
# the sets. That is advised only if all dosimeters have the same dimensions.
# -------------------------------------------------------------------------------------------------

# The selection by mouse clicks functions where inspired by the stack exchange discussion:
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

    coords_z.append(z) # only the z coordinates are saved

    if len(coords_z) == 2:
        plt.close()
    return


def cropping_dosimeters(oct):
    oct = cropping_func(oct, 'yes')

    terminate = False
    while not terminate:
        ans = input('Continue cropping? (y/n)')
        if ans == 'y' or ans == 'Y':
            oct = cropping_func(oct, 'no')
        elif ans == 'n' or ans == 'N':
            terminate = True

    return oct


def cropping_func(oct, rotate):
    global coords_x, coords_y, coords_z
    coords_x = []
    coords_y = []
    coords_z = []

    if rotate == 'yes':
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

    oct = oct[x[0]:x[1], y[0]:y[1], z[0]:z[1]]

    plt.rcParams.update({'font.size': 12})
    fig, ax = plt.subplots(1, 2)
    ax[0].imshow(oct[int(oct.shape[0] / 2), :, :], cmap='jet')
    ax[1].imshow(oct[:, :, int(oct.shape[2] / 2)], cmap='jet')
    plt.show()

    return oct
