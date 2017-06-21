import numpy as np
import matplotlib
import pylab
from scipy.optimize import curve_fit
dati=['dati/ruota_libera.txt']
accelerazione=([])
massa_piattello=np.array([0.023011,0.000001])
raggio_pesetto=np.array([0.02006,0.000005])
raggio_cerchio=np.array([0.16,0.0000075])
tempiRuotaLibera,velocitàRuotaLibera=np.loadtxt(dati[0],unpack='true')

#mi calcolo l'accelerazione, non si può sapere mai...
for i in range (0,len(tempiRuotaLibera)-2):
	accelerazioneRuotaLibera=np.insert(accelerazione,len(accelerazione),(velocitàRuotaLibera[i+1]-velocitàRuotaLibera[i])/(tempiRuotaLibera[i+1]-tempiRuotaLibera[i]))

#faccio tutto quello che c'è da fare nel caso in cui la ruota è libera
def fRuotaLibera(tempo,omega0,tau,mInerzia):
	return omega0-(tempo*tau)/mInerzia
datiRuotaLibera,varRuotaLibera=curve_fit(fRuotaLibera,tempiRuotaLibera,velocitàRuotaLibera)


pylab.plot(tempiRuotaLibera,velocitàRuotaLibera)
print(datiRuotaLibera)
x=np.linspace(0,100,200)
y=fRuotaLibera(x,*datiRuotaLibera)
pylab.plot(x,y)
pylab.xlabel("ω[rad/s]")
pylab.ylabel("t[s]")
pylab.title("Ruota libera")
#pylab.plot(tempiRuotaLibera[:-2],accelerazioneRuotaLibera)
pylab.show()