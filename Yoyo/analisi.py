import numpy as np
import matplotlib
import pylab
from scipy.optimize import curve_fit
dati=['dati/ruota_libera.txt','dati/150.txt','dati/300.txt']
massa_piattello=np.array([0.023011,0.000001])
masse=([0,0.15,0.3])
raggio_pesetto=np.array([0.02006,0.000005])
raggio_cerchio=np.array([0.16,0.0000075])
g=9.81


#lettura[m][n][l] indica m=il file, se n=0 il tempo, ne n=1 omega, l indica l'essesimo elemento della lista
lettura=[np.loadtxt(dati[0],unpack='true'),np.loadtxt(dati[1],unpack='true'),np.loadtxt(dati[2],unpack='true')]

#faccio tutto quello che c'è da fare nel caso in cui la ruota è libera
def fRuotaLibera(tempo,omega0,tau,mInerzia):
	return omega0-(tempo*tau)/mInerzia
"""
datiRuotaLibera,varRuotaLibera=curve_fit(fRuotaLibera,lettura[0][0],lettura[0][1])

pylab.plot(lettura[0][0],lettura[0][1])
print(datiRuotaLibera)
x=np.linspace(0,100,200)
y=fRuotaLibera(x,*datiRuotaLibera)
pylab.plot(x,y)
pylab.title("Ruota libera")
"""

#adesso si fa le oscillazioni normali
#creo l'equazione che descrive il moto dell'oggetto quande sale e quando scende
def YoyoSu(tempo,omega0,tau,mInerzia):
	return tempo*((massa_piattello[0]+masse[1])*g*raggio_pesetto[0]-tau)/(mInerzia+masse[1]*raggio_pesetto[0]**2)+omega0

def YoyoGiu(tempo,omega0,tau,mInerzia):
	return -tempo*((massa_piattello[0]+masse[1])*g*raggio_pesetto[0]+tau)/(mInerzia+masse[1]*raggio_pesetto[0]**2)+omega0


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


#mi creo una funzione che mi trova l'accelerazione
#prende in input la stessa cose della RicercaMaxMin
'''
def accelerazione(lista):
	accelerazione=([])
	for i in range (1,len(lista[0])):
		a=(lista[1][i-1]-lista[1][i])/(lista[0][i-1]-lista[0][i])
		accelerazione=np.insert(accelerazione,len(accelerazione),a)
	return accelerazione

  plot temporaneo dell'accelerazione
pylab.title("accelerazione")
pylab.plot(lettura[1][0][1:],accelerazione(lettura[1]))
pylab.ylabel("accelerazione angolare [rad/s^2]")
'''

#e ora faccio un mucchio di fit
def fit(lista):
	massimi,minimi=RicercaMaxMin(lista)
	pylab.plot(lista[0],lista[1])
	a=0
	b=0
	oscillazioni=([])
	while a<len(massimi) and b<len(minimi):
		if massimi[a]<minimi[b]:
			fit,varFit=curve_fit(YoyoGiu,lista[0][massimi[a]:minimi[b]+1],lista[1][massimi[a]:minimi[b]+1])
			x=np.linspace(lista[0][massimi[a]],lista[0][minimi[b]],100)
			y=YoyoGiu(x,*fit)
			b=b+1
		else:
			fit,varFit=curve_fit(YoyoSu,lista[0][minimi[b]:massimi[a]+1],lista[1][minimi[b]:massimi[a]+1])
			x=np.linspace(lista[0][minimi[b]],lista[0][massimi[a]],100)
			y=YoyoSu(x,*fit)
			a=a+1
		pylab.plot(x,y)

fit(lettura[1])



pylab.ylabel("ω[rad/s]")
pylab.xlabel("t[s]")
pylab.show()