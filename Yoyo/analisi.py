import numpy as np
import matplotlib
import pylab
from scipy.optimize import curve_fit
dati=['dati/ruota_libera.txt']
accelerazione=([])
massa_piattello=np.array([0.023011,0.000001])
raggio_pesetto=np.array([0.02006,0.000005])
raggio_cerchio=np.array([0.16],0.0000075)
tempi,velocità=np.loadtxt(dati[0],unpack='true')

for i in range (0,len(tempi)-2):
	accelerazione=np.insert(accelerazione,len(accelerazione),(velocità[i+1]-velocità[i])/(tempi[i+1]-tempi[i]))

pylab.plot(tempi,velocità)
pylab.plot(tempi[:-2],accelerazione)
pylab.show()