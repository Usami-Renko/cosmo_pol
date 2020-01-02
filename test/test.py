# -*- coding: utf-8 -*-

'''
@Description: 
@Author: Hejun Xie
@Date: 2020-01-02 19:42:04
@LastEditors  : Hejun Xie
@LastEditTime : 2020-01-03 00:09:13
'''

import cosmo_pol

if __name__ == '__main__':
    FILENAME = '../pathos/WRF/wsm6/wrfout_d03_2013-10-06_00_00_00'
    a = cosmo_pol.RadarOperator(options_file='./option_files/test.yml')
    a.load_model_file_WRF(FILENAME, itime=0)
    
    r = a.get_PPI(elevations = 1)
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

    r = a.get_PPI(elevations = 1)
    from cosmo_pol.radar.pyart_wrapper import RadarDisplay
    display = RadarDisplay(r, shift=(0.0, 0.0))
    import matplotlib.pyplot as plt
    plt.figure()
    display.plot('RVEL',0,vmin=-30,vmax=30,
                 title='real RVEL',
                 cmap = plt.cm.RdBu_r,
                 shading = 'flat',
                 max_range = 150000)


    plt.savefig('rvel_unaliased.png',dpi=300,bbox_inches='tight')
