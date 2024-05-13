import matplotlib.pyplot as plt
from gofish import imagecube
import numpy as np
import os
from scipy import integrate


def plot_image(inclination,PA,FOV):
    '''
    Plot image and grid to see if there is consistency
    in the chosen inclination, PA, and centering.
    '''
    cube = imagecube(os.path.join(path,file), FOV) # This defines the imagecube object from GoFish
    rvals, tvals, _ = cube.disk_coords(x0=0.0, y0=0.0, inc=inclination, PA=PA)

    ## define the plot parameters
    fig, ax = plt.subplots()
    cube.plot_surface(x0=-0.006, y0=-0.013,inc=inclination, PA=PA,
                            r_max=1.0, fill='rvals * np.cos(tvals)', return_fig=True,ax=ax)
    im = ax.imshow(cube.data, origin='lower', extent=cube.extent)

    ax.set_xlim(-1,1)
    ax.set_ylim(-1,1)
    ax.set_xlabel('Offset (arcsec)')
    ax.set_ylabel('Offset (arcsec)')
    plt.show()

def radial_cut(inclination,PA,FOV,plot=False):
    '''
    Obtain and plot radial profiles
    '''
    cube = imagecube(os.path.join(path,file), FOV) # This defines the imagecube object from GoFish
    x, y, dy = cube.radial_profile(x0=-0.006,y0=-0.013,inc=inclination, PA=PA,  dist=132, unit='Jy/beam')
    '''
    integration
    '''
    # total_integral = integrate.simpson(y, x)
    # print(total_integral)

    # integration_array=[]
    # for ii in range(len(x)-2):
    #     current_integral = integrate.simpson(y[0:ii+2], x[0:ii+2])
    #     integration_array.append(current_integral)
    #     # print(current_integral/total_integral*100,x[ii+2])
    #     if 67<current_integral/total_integral*100<68:
    #         print(str(round(x[ii+2],3))+' is the radius at '+str(round(current_integral/total_integral*100,3))
    #               +'% of total flux')

    """
    plot
    """
    if plot:
        fig, ax = plt.subplots()
        ax.errorbar(x, y, dy, fmt=' ', capsize=1.25, capthick=1.25, color='k', lw=1.0)
        ax.step(x, y, where='mid', color='k', lw=1.0)
        ax.set_xlim(x.min(), x.max())
        ax.set_xlabel('Radius (arcsec)')
        ax.set_ylabel('Peak Intensity (Jy/beam)')
        plt.show()

    return x,y,dy

def plot_flux_distribution(inclination,PA,FOV):
    '''
    CDF of the flux
    '''
    cube = imagecube(os.path.join(path,file), FOV) # This defines the imagecube object from GoFish
    fig, ax = plt.subplots()
    x, y, dy = cube.radial_profile(inc=inclination, PA=PA, mstar=0.5, dist=132, unit='Jy/beam')

    # plot the cumulative histogram
    n_bins=500
    n, bins, patches = ax.hist(y, n_bins, density=True, histtype='bar',
                               cumulative=True, label='Empirical')

    ax.grid(True)
    ax.legend(loc='right')
    ax.set_title('Cumulative step histograms')
    ax.set_xlabel('Flux (Jy/beam)')
    ax.set_ylabel('cummulative distribution')

    plt.show()

if __name__ == "__main__":
    path ='.' ### give full path to fits file. '.' means this directory.
    file='OphIRS63_SBLB_continuum_robust_0.0.pbcor.tt0.fits'

    inclination=47
    PA=149
    FOV=5.0

    plot_image(inclination,PA,FOV)
    radial_cut(inclination, PA,FOV, plot=True)
    plot_flux_distribution(inclination, PA,FOV)
