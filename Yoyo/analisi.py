import numpy as np
import matplotlib
import pylab
from scipy.optimize import curve_fit
dati=['dati/ruota_libera.txt','dati/150.txt','dati/300.txt']
accelerazione=([])
massa_piattello=np.array([0.023011,0.000001])
raggio_pesetto=np.array([0.02006,0.000005])
raggio_cerchio=np.array([0.16,0.0000075])
lettura=[np.loadtxt(dati[0],unpack='true'),np.loadtxt(dati[1],unpack='true'),np.loadtxt(dati[2],unpack='true')]

#faccio tutto quello che c'è da fare nel caso in cui la ruota è libera
def fRuotaLibera(tempo,omega0,tau,mInerzia):
	return omega0-(tempo*tau)/mInerzia
datiRuotaLibera,varRuotaLibera=curve_fit(fRuotaLibera,lettura[0][0],lettura[0][1])

#pylab.plot(lettura[0][0],lettura[0][1])
#print(datiRuotaLibera)
#x=np.linspace(0,100,200)
#y=fRuotaLibera(x,*datiRuotaLibera)
#pylab.plot(x,y)
#pylab.title("Ruota libera")

#adesso si fa le oscillazioni normali

#creo una funzione che trova i massimi e i minimi
#la funzione riceve un imput del tipo lettura[n] dove n indica il file da analizzare
def RicercaMaxMin(lista):
	massimi=([])
	minimi=([])
	for i in range(2,len(lista[0])):
		if lista[1][i-2]<lista[1][i-1] and lista[1][i]<lista[1][i-1]:
			massimi=np.insert(massimi,len(massimi),i-1)
		if lista[1][i-2]>lista[1][i-1] and lista[1][i]>lista[1][i-1]:
			minimi=np.insert(minimi,len(minimi),i-1)
	return massimi,minimi

pylab.plot(lettura[2][0],lettura[2][1])
a=RicercaMaxMin(lettura[2])
print(a)
print(lettura[2][0][a[0]])

pylab.xlabel("ω[rad/s]")
pylab.ylabel("t[s]")
pylab.show()