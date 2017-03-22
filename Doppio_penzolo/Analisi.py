#MEMO
#le colonne pari sono quelle dei tempi, quelle dispare delle posizioni

import numpy as np
from scipy.optimize import curve_fit
from scipy import constants
from scipy import stats
import pylab
lpiscina=([0.248,0.001])
errore=lpiscina[0]/1023
media=([0,443.2760778859527,0,469.16133518776076])
#elenco tutti i file in delle liste
dati=[['dati/semplice1.txt','dati/2pendolosemplicesx.txt'],
      ['dati/3pendolosupersmorzato.txt','dati/4pendolosupersmorzato.txt'],
      ['dati/5doppiettodellefaville.txt','dati/6doppfav.txt'],
      ['dati/7doppfavcontro.txt','dati/8doppfavcontro.txt'],
      ['dati/9doppfavbattim.txt','dati/battimenti.txt','dati/battimenti_2.txt','dati/battimenti_copia.txt']]
#annuncio gli arrei da riempire
tempo=([])
periodi=([])
#periodo teorico
teorico=2*np.pi*np.sqrt(0.464/9.81)
#creo una funzione che legge una intera colonna e restituisce un array
def lettura(file,colonna):
	esito=([])
	for line in open (file):
		if not line.startswith('#'):
			row=[float(item) for item in line.split()]
			if colonna%2==0:
				esito=np.insert(esito,len(esito),row[colonna])
			else:
				esito=np.insert(esito,len(esito),(row[colonna]-media[colonna])*lpiscina[0]/1023)
	return(esito)

#definisco la funzione dell'oscillatore armonico smorzato
def fSmorzato(tempo,decadimento,A,B,omega):
	return np.exp(-tempo/decadimento)*(A*np.sin(omega*tempo)+B*np.cos(omega*tempo))

#definisco la funzione dei battimenti
def fAccoppiato(tempo,ampiezza,coseno1,coseno2,phi1,phi2,C,decadimento):
	#coseno1=tempo*(omega1+omega2)/2
	#coseno2=tempo*(omega1-omega2)/2
	return np.exp(-tempo/decadimento)*(2*ampiezza*np.cos(tempo*coseno1+phi1)*np.cos(tempo*coseno2+phi2))+C
#e la vettorizzo
vfAccoppiato=np.vectorize(fAccoppiato)
#creo una funzione che mi rileva i passaggi dall'asse delle x
def zeri(file,colonnaposizioni):
	a=lettura(file,colonnaposizioni)
	b=lettura(file,colonnaposizioni-1)
	intercette=([])
	for i in range(0,len(a)-1):
		if a[i]>0:
			if a[i+1]<0:
				intercette=np.insert(intercette,len(intercette),b[i])
		if a[i]<0:
			if a[i+1]>0:
				intercette=np.insert(intercette,len(intercette),b[i])
	return intercette

#definisco una funzione che mi trova i massimi
def massimi(file,colonnaposizioni,lista):
	a=lettura(file,colonnaposizioni)
	b=lettura(file,lista)
	massimi=([])
	for i in range(0,len(a)-2):
		if a[i]<a[i+1]:
			if a[i+2]<a[i+1]:
				massimi=np.insert(massimi,len(massimi),b[i+1])
	return massimi

#definisco una funzione che mi ritorna un vettore 2D con la media e la dev standard del periodo
def periodo(file,colonnatempi):
	intercette=([])
	periodo=([0,0])
	a=zeri(file,colonnatempi)
	for i in range(1,len(a)):
		intercette=np.insert(intercette,len(intercette),a[i]-a[i-1])
	periodo[0]=np.mean(intercette)*2
	periodo[1]=np.std(intercette)*2
	return periodo

p0=np.array([0.07,6.28/0.75,6.28/40,0,0,0,30])
parv1,parc1=curve_fit(fAccoppiato,lettura(dati[4][1],2),lettura(dati[4][1],3),p0,maxfev=50000)
parv,parc=curve_fit(fAccoppiato,lettura(dati[4][3],2),lettura(dati[4][3],3),parv1,maxfev=50000)
pylab.plot(lettura(dati[4][3],2),lettura(dati[4][3],3),'.')

suca=(((lettura(dati[4][3],2)-fAccoppiato(lettura(dati[4][3],3),parv[0],parv[1],parv[2],parv[3],parv[4],parv[5],parv[6])/errore)**2)).sum()
dof=len(lettura(dati[4][3],2)-len(parv))
pvalue=stats.chi2.pdf(suca,dof)

print('pvalue=%.7f chi2=%f ' %(pvalue,suca))
x=np.linspace(0,90,1000)
y=vfAccoppiato(x,parv[0],parv[1],parv[2],parv[3],parv[4],parv[5],parv[6])
pylab.xlabel("t[s]")
pylab.ylabel("d[m]")
pylab.plot(x,y)
pylab.show()
