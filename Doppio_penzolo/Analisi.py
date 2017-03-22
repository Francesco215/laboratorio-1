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
teorico=2*np.pi*np.sqrt(0.464/9.81) #periodo teorico
#elenco tutti i file in delle liste
dati=[['dati/semplice1.txt','dati/2pendolosemplicesx.txt'],
      ['dati/3pendolosupersmorzato.txt','dati/4pendolosupersmorzato.txt'],
      ['dati/5doppiettodellefaville.txt','dati/6doppfav.txt'],
      ['dati/7doppfavcontro.txt','dati/8doppfavcontro.txt'],
      ['dati/9doppfavbattim.txt','dati/battimenti.txt','dati/battimenti_2.txt','dati/battimenti_copia.txt']]

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
def fSmorzato(tempo,decadimento,ampiezza,phi,omega,C):
	return np.exp(-tempo/decadimento)*ampiezza*np.sin(omega*tempo+phi)+C

vSmorzato=np.vectorize(fSmorzato)
#definisco la funzione dei battimenti
def fAccoppiato(tempo,ampiezza,omega1,omega2,phi1,phi2,C,decadimento):
	#coseno1=tempo*(omega1+omega2)/2
	#coseno2=tempo*(omega1-omega2)/2
	return np.exp(-tempo/decadimento)*2*ampiezza*np.cos(tempo*omega1+phi1)*np.cos(tempo*omega2+phi2)+C
#e la vettorizzo
vfAccoppiato=np.vectorize(fAccoppiato)

#fit dei battimenti e chi^2 dei battimenti
battP0=np.array([0.07,6.28/0.75,6.28/40,0,0,0,30])
parv1,parc1=curve_fit(fAccoppiato,lettura(dati[4][1],2),lettura(dati[4][1],3),battP0,maxfev=50000)
datiBattimenti,varBattimenti=curve_fit(fAccoppiato,lettura(dati[4][3],2),lettura(dati[4][3],3),parv1,maxfev=50000)
#pylab.plot(lettura(dati[4][3],2),lettura(dati[4][3],3),'.')
battChi2=(((lettura(dati[4][3],2)-fAccoppiato(lettura(dati[4][3],3),datiBattimenti[0],datiBattimenti[1],datiBattimenti[2],datiBattimenti[3],datiBattimenti[4],datiBattimenti[5],datiBattimenti[6])/errore)**2)).sum()
battDof=len(lettura(dati[4][3],2)-len(datiBattimenti))
battPvalue=stats.chi2.pdf(battChi2,battDof)
#y=vfAccoppiato(x,*datiBattimenti)

print('questi sono i dati dei battimenti',datiBattimenti,varBattimenti)

#fit delle oscillazioni in fase
faseP0=np.array([30,0.015,3.15,6.28/0.75,0.03])
datiFase,varFase=curve_fit(fSmorzato,lettura(dati[2][1],2)-lettura(dati[2][1],2)[0],lettura(dati[2][1],3),faseP0,maxfev=10000)
#pylab.plot(lettura(dati[2][1],2)-lettura(dati[2][1],2)[0],lettura(dati[2][1],3),'.')
#x=np.linspace(0,30,1000)
#y=vSmorzato(x,*datiFase)
print('questi sono i dati dei pendoli in fase',datiFase,varFase)

#fit delle oscillazioni in controfase
tempi=lettura(dati[3][0],0)
posizioni=lettura(dati[3][0],1)
#fit delle oscillazioni in controfase
confaseP0=np.array([60,0.007,6,6.28/0.7,0.03])
datiConFase,varConFase=curve_fit(fSmorzato,tempi-tempi[0],posizioni,confaseP0,maxfev=10000)
pylab.plot(tempi-tempi[0],posizioni,'.')
x=np.linspace(0,21.5,1000)
y=vSmorzato(x,*datiConFase)
print('questi sono i dati dei pendoli in contro-fase',datiConFase,varConFase)

pylab.xlabel("t[s]")
pylab.ylabel("d[m]")
pylab.plot(x,y)
pylab.show()
