import numpy as np
from scipy.optimize import curve_fit
from scipy import stats
import pylab
g=9.807
#dati acquisito
masse=([])
lunghezza=([])
tempi=([[],[],[],[],[]])
#comincia l'elaborazione dati
periodi=([])
DevPeriodi=([])
for i in range (0,len(tempi)):
	media=np.mean(tempi[i])/10
	std=np.std(tempi[i])/10
	periodi=np.insert(periodi,len(periodi),media)
	DevPeriodi=np.insert(DevPeriodi,len(DevPeriodi),std)

def Periodo(lunghezza):
	return 4*np.pi*np.sqrt(lunghezza/g)

