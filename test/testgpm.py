# -*- coding: utf-8 -*-

'''
@Description: Test GPM swath simulation
@Author: Hejun Xie
@Date: 2020-01-12 16:42:47
@LastEditors  : Hejun Xie
@LastEditTime : 2020-01-13 16:17:00
'''

import cosmo_pol
import pickle
import pyart
import numpy as np

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d

LOAD_MODEL = True
LOAD_RADAR = True
DEG = r'$^\circ$'

cmap = {'ZH':'pyart_Carbone11', 'RVEL': 'pyart_BuOr8', 'ZDR': 'pyart_Carbone17',
'KDP': 'pyart_EWilson17', 'PHIDP': 'pyart_Carbone42', 'RHOHV': 'pyart_GrMg16'}
clevels = {'ZH':range(50), 'ZDR':np.linspace(0., 0.1, 50)}
units = {'ZH':'[dBZ]', 'ZDR':'[dBZ]'}

if __name__ == '__main__':
    FILENAME = '../pathos/WRF/wsm6/wrfout_d03_2013-10-06_00_00_00'
    GPM_FILE = '../pathos/GPM/GPMCOR_KAR_2001091652_1825_033323_1BS_DAB_05C.h5'
    a = cosmo_pol.RadarOperator(options_file='./option_files/testgpm.yml')
    a.load_model_file_WRF(FILENAME, itime=10, load_pickle=LOAD_MODEL, pickle_file='tempa.pkl')
    
    # a.get_GPM_swath_test(GPM_FILE, 5201, 0, band='Ka')

    slice = (slice(5208, 5279), slice(0, 12))
    # slice = (slice(5208, 5209), slice(0, 12))
    if not LOAD_RADAR:
        r = a.get_GPM_swath(GPM_FILE, slice, band='Ka')
        with open("./tempr3.pkl", "wb") as f:
			pickle.dump(r, f)
    else:
        with open("./tempr3.pkl", "rb") as f:
			r = pickle.load(f)
    
    # print(r.bin_surface[0,:])
    # print(r.lats[0,0,:])
    # print(r.lons[0,0,:])
    # print(r.heights[0,0,:])
    # print(r.data['ZH'][0,0,:])

    var = 'ZDR' 

    fig = plt.figure()
    ax = fig.gca(projection='3d')

    x = r.lons
    y = r.lats
    h = r.heights
    z = 10*np.log10(r.data[var])
    levels = clevels[var]
    
    zgrids = [5, 15, 25, 35]

    csets = []
    for zgrid in zgrids: 
        csets.append(ax.contourf(x[:,:,zgrid], y[:,:,zgrid], z[:,:,zgrid],
        levels, offset=h[0,0,zgrid]/1000., cmap = cmap[var]))
    
    cbar = fig.colorbar(csets[0])
    cbar.ax.set_ylabel(units[var])

    ax.set_xlim(121, 123)
    ax.set_ylim(27.5, 30.0)
    ax.set_zlim(0, 10)

    ax.set_xlabel('longitude')
    ax.set_ylabel('latitude')
    ax.set_zlabel('heights [km]')
    ax.set_title('GPM-DPR ' + var)

    plt.show()