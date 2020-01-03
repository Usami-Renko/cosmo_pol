# -*- coding: utf-8 -*-

'''
@Description: 
@Author: Hejun Xie
@Date: 2020-01-02 19:42:04
@LastEditors  : Hejun Xie
@LastEditTime : 2020-01-03 21:17:37
'''

import cosmo_pol
import pickle

LOAD_MODEL = True
LOAD_RADAR = True

if __name__ == '__main__':
    FILENAME = '../pathos/WRF/wsm6/wrfout_d03_2013-10-06_00_00_00'
    a = cosmo_pol.RadarOperator(options_file='./option_files/test.yml')
    a.load_model_file_WRF(FILENAME, itime=10, load_pickle=LOAD_MODEL, pickle_file='tempa.pkl')

    if not LOAD_RADAR:
        r = a.get_PPI(elevations = 1)
        with open("./tempr1.pkl", "wb") as f:
			pickle.dump(r, f)
    else:
        with open("./tempr1.pkl", "rb") as f:
			r = pickle.load(f)

    from cosmo_pol.radar.pyart_wrapper import RadarDisplay
    display = RadarDisplay(r, shift=(0.0, 0.0))
    import matplotlib.pyplot as plt
    plt.figure()
    display.plot('RVEL',0,vmin=-8.3,vmax=8.3,
                 title='aliased RVEL',
                 cmap = plt.cm.RdBu_r,
                 shading = 'flat',
                 max_range = 150000)

    plt.savefig('rvel_aliased.png',dpi=300,bbox_inches='tight')

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
            
    from cosmo_pol.radar.pyart_wrapper import RadarDisplay
    display = RadarDisplay(r, shift=(0.0, 0.0))
    import matplotlib.pyplot as plt
    plt.figure()
    display.plot('RVEL',0,vmin=-50,vmax=50,
                 title='real RVEL',
                 cmap = plt.cm.RdBu_r,
                 shading = 'flat',
                 max_range = 150000)

    plt.savefig('rvel_unaliased.png',dpi=300,bbox_inches='tight')
    
    plt.figure()
    display.plot('ZH',0,vmin=0,vmax=70,
                 title='reflectivity ZH [dBZ]',
                 cmap = plt.cm.viridis,
                 shading = 'flat',
                 max_range = 150000)

    plt.savefig('ZH.png',dpi=300, bbox_inches='tight')

    plt.figure()
    display.plot('ZDR',0,vmin=0,vmax=4,
                 title='differential reflectivity ZH [dBZ]',
                 cmap = plt.cm.viridis,
                 shading = 'flat',
                 max_range = 150000)

    plt.savefig('ZDR.png',dpi=300, bbox_inches='tight')

    plt.figure()
    display.plot('KDP',0,vmin=0,vmax=3,
                 title='specific differential phase Kdp [deg*km-1]',
                 cmap = plt.cm.viridis,
                 shading = 'flat',
                 max_range = 150000)

    plt.savefig('KDP.png',dpi=300, bbox_inches='tight')
