from __future__ import division
import numpy as np
import scipy.io as sio
import matplotlib.pyplot as plt
import cPickle as pickle
#import sys
#sys.path.append('/home/wesley/github/UTide/')
#from utide import ut_solv, ut_reconstr
from utide import ut_constants
from ut_solv import ut_solv
from ut_reconstr import ut_reconstr


def simple_test(debug=True):
    ts = 735604
    duration = 35

    time = np.linspace(ts, ts+duration, 841)
    time_origin = 6.939615e5

    mat_contents = sio.loadmat(ut_constants, struct_as_record=False, squeeze_me=True)

    #shallow = mat_contents['shallow']
    const = mat_contents['const']

    amp = 1.0
    phase = 53
    lat = 45.5
    period = 1 / const.freq * 3600

    jj=48-1

    time_series = amp * np.cos((((time-time_origin) * (2*np.pi/period[jj]) *
                                (24*3600)) - 2 * np.pi * phase / 360))

    speed_coef = ut_solv(time, time_series, time_series, lat, cnstit='auto',
                notrend=True, rmin=0.95, method='ols',
                nodiagn=True, linci=True, conf_int=True)

    elev_coef = ut_solv(time, time_series, [], lat, cnstit='auto', gwchnone=True,
                nodsatnone=True, notrend=True, rmin=0.95, method='ols',
                nodiagn=True, linci=True, conf_int=True)


    amp_err = amp - elev_coef['A'][0]

    phase_err = phase - elev_coef['g'][0]

    ts_recon, _ = ut_reconstr(time, elev_coef)

    u, v = ut_reconstr(time, speed_coef)

    err = np.sqrt(np.mean((time_series-ts_recon[0])**2))

    ts_fvcom=elev_coef['A'][0]*np.cos(2*np.pi*((time-np.mean(time))/(period[jj]/(24*3600))-elev_coef['g'][0]/360))

    if debug:
        plt.plot(time, ts_recon)
        plt.plot(time, ts_fvcom)
        plt.show()
