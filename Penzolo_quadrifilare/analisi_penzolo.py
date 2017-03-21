import numpy as np
from scipy import loadtxt
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit 
larghezza_bandiera=np.array([0.0210,0.0005])
distanza_bandiera=np.array([0.1164,0.005])
g=9.81
#plt.ion() # interactive on
misure_angoli=['dati/misura_angolo1.txt','dati/misura_angolo2.txt','dati/misura_angolo3.txt','dati/misura_angolo4.txt','dati/misura_angolo5.txt']
piccoleOscillazioni='dati/piccole_oscillazioni1.txt'

#funzione del pendolo quadrifilare
def funzione(tPassaggio,distanza_cm,distanza_bandiera,P1,P2):
	theta=np.arccos((distanza_cm*larghezza_bandiera**2)/(2*tPassaggio*distanza_bandiera*g))
	return (1+P1*theta**2+P2*theta**4)*2*np.pi*np.sqrt(distanza_cm/g)
#funzione che legge un file e restituisce un array del periodo e del tempo di passaggio
def lettura(file):
	numero,passaggio,tempo=loadtxt(file,unpack=True)
	Periodo=np.array([])
	tPassaggio=np.array([])
	for i in range(6,len(numero),4):
		Periodo=np.insert(Periodo,len(Periodo),tempo[i]-tempo[i-4])
		tPassaggio=np.insert(tPassaggio,len(tPassaggio),tempo[i-1]-tempo[i-2])
	return Periodo,tPassaggio

#mi ricavo la distanza equivalente e la metto nei parametri iniziali
distanza_cm=9.81*np.mean(lettura(piccoleOscillazioni)[0])**2/(4*np.pi**2)
p0=np.array([distanza_cm,distanza_bandiera[0],1/16,11/3072])
Periodo,tPassaggio=lettura(misure_angoli[0])

valori,covarianza=curve_fit(funzione,Periodo,tPassaggio,p0)


