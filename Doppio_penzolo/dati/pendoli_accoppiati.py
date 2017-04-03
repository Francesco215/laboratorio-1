import numpy as np
from scipy.optimize import curve_fit
from scipy import constans 
from scipy import stats
import pylab as pl

def battimenti (time, tau, ampiezza, omega_c, omega_f, phi_1, phi_2, c)
    return np.exp(-time/tau)*ampiezza*[np.cos(omega_f*time + phi_1) + cos (omega_c*time + phi_2)]
time, position = pl.loadtxt('dati/7doppfavcontro.txt', unpack = True)
#popt_battimenti, pcov_battimenti = curve_fit(battimenti, time, position, [)
pl.plot(time, position)
