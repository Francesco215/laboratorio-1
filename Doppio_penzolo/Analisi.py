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

#definisco la funzione dei battimenti
def fAccoppiato(tempo,ampiezza,omega1,omega2,phi1,phi2,C,decadimento):
	#coseno1=tempo*(omega1+omega2)/2
	#coseno2=tempo*(omega1-omega2)/2
	return np.exp(-tempo/decadimento)*2*ampiezza*np.cos(tempo*omega1+phi1)*np.cos(tempo*omega2+phi2)+C

#e li vettorizzo
vfAccoppiato=np.vectorize(fAccoppiato)
vSmorzato=np.vectorize(fSmorzato)

#fit coso smorzato
smoP0=np.array([30,0.015,3.15,6.28/0.75,0.03])
datismo,varismo=curve_fit(fSmorzato,lettura(dati[1][0],2),lettura(dati[1][0],3),smoP0,maxfev=100000)
print('questi sono i dati del pendolo smorzato',datismo,varismo.diagonal())
#pylab.plot(lettura(dati[1][0],2)-lettura(dati[1][0],2)[0],lettura(dati[1][0],3)-datismo[4],'.')
#x=np.linspace(0,40,1000)
#y=vSmorzato(x,*datismo)-datismo[4]
#pylab.title("Fit pendolo smorzato")

#fit dei battimenti e chi^2 dei battimenti
battP0=np.array([0.07,6.28/0.75,6.28/40,0,0,0,30])
parv1,parc1=curve_fit(fAccoppiato,lettura(dati[4][1],2),lettura(dati[4][1],3),battP0,maxfev=50000)
datiBattimenti,varBattimenti=curve_fit(fAccoppiato,lettura(dati[4][3],2),lettura(dati[4][3],3),parv1,maxfev=50000)
pylab.plot(lettura(dati[4][3],2),lettura(dati[4][3],3),'.')
battChi2=(((lettura(dati[4][3],2)-fAccoppiato(lettura(dati[4][3],3),*datiBattimenti)/errore)**2)).sum()
battDof=len(lettura(dati[4][3],2)-len(datiBattimenti))
battPvalue=stats.chi2.pdf(battChi2,battDof)
x=np.linspace(0,90,5000)
y=vfAccoppiato(x,*datiBattimenti)
pylab.title("Battimenti")

print('questi sono i dati dei battimenti',datiBattimenti,varBattimenti.diagonal())

#fit delle oscillazioni in fase
faseP0=np.array([30,0.015,3.15,6.28/0.75,0.03])
datiFase,varFase=curve_fit(fSmorzato,lettura(dati[2][1],2)-lettura(dati[2][1],2)[0],lettura(dati[2][1],3),faseP0,maxfev=10000)
#pylab.plot(lettura(dati[2][1],2)-lettura(dati[2][1],2)[0],lettura(dati[2][1],3)-datiFase[4],'.')
#x=np.linspace(0,30,1000)
#y=vSmorzato(x,*datiFase)-datiFase[4]
#print('questi sono i dati dei pendoli in fase',datiFase,varFase.diagonal())
#pylab.title("Pendoli in fase")

#fit delle oscillazioni in controfase
tempi=lettura(dati[3][0],0)
posizioni=lettura(dati[3][0],1)
confaseP0=np.array([60,0.007,6,6.28/0.7,0.03])
datiConFase,varConFase=curve_fit(fSmorzato,tempi-tempi[0],posizioni,confaseP0,maxfev=10000)
#pylab.plot(tempi-tempi[0],posizioni-datiConFase[4],'.')
#x=np.linspace(0,21.5,1000)
#y=vSmorzato(x,*datiConFase)-datiConFase[4]
print('questi sono i dati dei pendoli in contro-fase',datiConFase,varConFase.diagonal())
#pylab.title("Pendoli in controfase")

pylab.xlabel("t[s]")
pylab.ylabel("d[m]")
pylab.plot(x,y)
pylab.show()
