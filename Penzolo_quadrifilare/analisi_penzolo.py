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

#creo una funzione che mi legge il file e mi ritorna il periodo e il tempo di passaggio sotto forma di vettori
def lettura(file):
	numero,passaggio,tempo=loadtxt(file,unpack=True)
	Periodo=np.array([])
	tPassaggio=np.array([])
	for i in range(6,len(numero),4):
		Periodo=np.insert(Periodo,len(Periodo),tempo[i]-tempo[i-4])
		tPassaggio=np.insert(tPassaggio,len(tPassaggio),tempo[i-1]-tempo[i-2])
	return Periodo,tPassaggio

def funzione():
	v0=
	theta=np.arcos(1-v0**2/(2*g*distanza_bandiera))

