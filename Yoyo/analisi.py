"""   ISTRUZIONI ALL'USO
#PER IL VOLANO LIBERO
1)Mettere in dati[0] il file del volano libero
#PER QUELLO OSCILLATORIO
1)prendere il file di acquisizione
2)tagliare l'ultima parte se è troppo brutta e metterlo
3)nel vettore dei dati dei dati.
4)mettere nel vettore delle masse il suo peso in kg nella medesima posizione
5)indicare la posizione in nummero
6)pregare
7)eseguire il programma
"""

import numpy as np
import matplotlib
import pylab
from scipy.optimize import curve_fit
from scipy import stats
dati=['dati/ruota_libera.txt','dati/150.txt','dati/300.txt','dati/400.txt']
massa_piattello=np.array([0.023011,0.000001])
masse=([0,0.15,0.3,0.5])
raggio_pesetto=np.array([0.02006,0.000005])
raggio_cerchio=np.array([0.16,0.0000075])
g=9.81
nummero=2
taglio=0
mInerzia=3.146*10**6

errore=0.05

#lettura[m][n][l] indica m=il file, se n=0 il tempo, ne n=1 omega, l indica l'essesimo elemento della lista
lettura=[]
for i in range (0,len(dati)):
	estrazione=np.loadtxt(dati[i],unpack='true')
	lettura.append(estrazione)


#faccio tutto quello che c'è da fare nel caso in cui la ruota è libera
def fRuotaLibera(tempo,omega0,tau):
	return omega0-(tempo*tau)/mInerzia

datiRuotaLibera,varRuotaLibera=curve_fit(fRuotaLibera,lettura[0][0],lettura[0][1])

chi2libero=(((lettura[0][1]-fRuotaLibera(lettura[0][0],*datiRuotaLibera))/errore)**2).sum()
print("\n\nil chi^2 della ruota libera è",chi2libero,"\ne il numero di misurazioni è",len(lettura[0][0]))
print("\nil pvalue è",stats.chi2.cdf(chi2libero,len(lettura[0][0])),"\n\n")

pylab.plot(lettura[0][0],lettura[0][1])
print(datiRuotaLibera,varRuotaLibera.diagonal())
x=np.linspace(0,100,200)
y=fRuotaLibera(x,*datiRuotaLibera)
pylab.plot(x,y)
pylab.title("Ruota libera")
pylab.ylabel("ω[rad/s]")
pylab.xlabel("t[s]")
pylab.show()

#adesso si fa le oscillazioni normali
#creo l'equazione che descrive il moto dell'oggetto quande sale e quando scende
def YoyoSu(tempo,omega0,tau):
	return tempo*((massa_piattello[0]+masse[nummero])*g*raggio_pesetto[0]-tau)/(mInerzia+masse[nummero]*raggio_pesetto[0]**2)+omega0

def YoyoGiu(tempo,omega0,tau):
	return -tempo*((massa_piattello[0]+masse[nummero])*g*raggio_pesetto[0]+tau)/(mInerzia+masse[nummero]*raggio_pesetto[0]**2)+omega0


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


#e ora faccio un mucchio di fit
def fit(lista):
	massimi,minimi=RicercaMaxMin(lista)
	pylab.plot(lista[0],lista[1],'-',color='grey',lw=2)
	a=0
	b=0
	chi2=0
	while a<len(massimi)-taglio and b<len(minimi)-taglio:
		if massimi[a]<minimi[b]:
			fit,varFit=curve_fit(YoyoGiu,lista[0][massimi[a]:minimi[b]+1],lista[1][massimi[a]:minimi[b]+1])
			achi2=(((lista[1][massimi[a]:minimi[b]+1]-YoyoGiu(lista[0][massimi[a]:minimi[b]+1],*fit))/errore)**2).sum()
			chi2=chi2+achi2
			x=np.linspace(lista[0][massimi[a]],lista[0][minimi[b]],100)
			y=YoyoGiu(x,*fit)
			a=a+1
		else:
			fit,varFit=curve_fit(YoyoSu,lista[0][minimi[b]:massimi[a]+1],lista[1][minimi[b]:massimi[a]+1])
			achi2=(((lista[1][massimi[a]:minimi[b]+1]-YoyoSu(lista[0][massimi[a]:minimi[b]+1],*fit))/errore)**2).sum()
			chi2=chi2+achi2
			x=np.linspace(lista[0][minimi[b]],lista[0][massimi[a]],100)
			y=YoyoSu(x,*fit)
			b=b+1
		pylab.plot(x,y,'--',color='black',lw=3)
		if a+b<3:
			print("\n\nomega0, tau",fit)
			print("\nerrori",varFit.diagonal(),"\n\n")
	print("\n\nil chi^2 è",chi2,"\ne il numero di misurazioni è",len(lista[1]))
	print("\nil pvalue è",stats.chi2.cdf(chi2,len(lista[1])))


fit(lettura[nummero])

pylab.title("Oscillazione volano")
pylab.ylabel("ω[rad/s]")
pylab.xlabel("t[s]")
pylab.show()