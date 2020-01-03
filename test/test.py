# -*- coding: utf-8 -*-

'''
@Description: 
@Author: Hejun Xie
@Date: 2020-01-02 19:42:04
@LastEditors  : Hejun Xie
@LastEditTime : 2020-01-03 23:26:01
'''

import cosmo_pol
import pickle
import pyart
import numpy as np

LOAD_MODEL = True
LOAD_RADAR = True

if __name__ == '__main__':
    FILENAME = '../pathos/WRF/wsm6/wrfout_d03_2013-10-06_00_00_00'
    a = cosmo_pol.RadarOperator(options_file='./option_files/test.yml')
    a.load_model_file_WRF(FILENAME, itime=10, load_pickle=LOAD_MODEL, pickle_file='tempa.pkl')

    # if not LOAD_RADAR:
    #     r = a.get_PPI(elevations = 1)
    #     with open("./tempr1.pkl", "wb") as f:
	# 		pickle.dump(r, f)
    # else:
    #     with open("./tempr1.pkl", "rb") as f:
	# 		r = pickle.load(f)

    # from cosmo_pol.radar.pyart_wrapper import RadarDisplay
    # display = RadarDisplay(r, shift=(0.0, 0.0))
    # import matplotlib.pyplot as plt
    # plt.figure()
    # display.plot('RVEL',0,vmin=-8.3,vmax=8.3,
    #              title='aliased RVEL',
    #              shading = 'flat',
    #              max_range = 150000)

    # plt.savefig('rvel_aliased.png',dpi=300,bbox_inches='tight')

    cc = a.config
    cc['radar']['nyquist_velocity']=None
    a.config = cc

    if not LOAD_RADAR:
        r = a.get_PPI(elevations = 1)
        with open("./tempr2.pkl", "wb") as f:
			pickle.dump(r, f)
    else:
        with open("./tempr2.pkl", "rb") as f:
			r = pickle.load(f)
            
    # from cosmo_pol.radar.pyart_wrapper import RadarDisplay
    # display = RadarDisplay(r, shift=(0.0, 0.0))
    # import matplotlib.pyplot as plt
    # plt.figure()
    # display.plot('RVEL',0,vmin=-50,vmax=50,
    #              title='real RVEL',
    #              shading = 'flat',
    #              max_range = 150000)

    # plt.savefig('rvel_unaliased.png',dpi=300,bbox_inches='tight')

    from pyart.graph import RadarMapDisplayBasemap
    display = pyart.graph.RadarMapDisplayBasemap(r)
    import matplotlib.pyplot as plt
    plt.figure()

    display.plot_ppi_map('ZH', 0, vmin=-5, vmax=60,
                     min_lon=119, max_lon=122.5, min_lat=26.3, max_lat=29.5,
                     lon_lines=np.arange(119, 122.7, 1), projection='lcc',
                     lat_lines=np.arange(26.3, 29.5, 1), resolution='h',
                     lat_0=r.latitude['data'],
                     lon_0=r.longitude['data'],
                     cmap='pyart_Carbone11',
                     title='Horizontal reflectivity ZH [dBZ]')
    
    # plot range rings at 10, 20, 30 and 40km
    display.plot_range_ring(50., line_style='k-', lw=1.0)
    display.plot_range_ring(100., line_style='k--', lw=1.0)
    display.plot_range_ring(150., line_style='k-', lw=1.0)

    # plots cross hairs
    display.plot_line_xy(np.array([-200000.0, 200000.0]), np.array([0.0, 0.0]),
                        line_style='k-', lw=1.2)
    display.plot_line_xy(np.array([0.0, 0.0]), np.array([-200000.0, 200000.0]),
                        line_style='k-', lw=1.2)

    display.plot_point(r.longitude['data'], r.latitude['data'])
    
    plt.savefig('ZH.png',dpi=300, bbox_inches='tight')

    # plt.figure()
    # display.plot('ZDR',0,vmin=0,vmax=4,
    #              title='differential reflectivity ZH [dBZ]',
    #              shading = 'flat',
    #              max_range = 150000)

    # plt.savefig('ZDR.png',dpi=300, bbox_inches='tight')

    # plt.figure()
    # display.plot('KDP',0,vmin=0,vmax=3,
    #              title='specific differential phase Kdp [deg*km-1]',
    #              shading = 'flat',
    #              max_range = 150000)

    # plt.savefig('KDP.png',dpi=300, bbox_inches='tight')
