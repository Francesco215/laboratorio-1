
import numpy as np
from scipy import loadtxt
import pylab 
from scipy.optimize import curve_fit 
from scipy.stats import chi2
larghezza_bandiera=np.array([0.0210,0.0005])
distanza_bandiera=np.array([1.164,0.01])
distanzaCm=np.array([1.117,0.01])
g=9.806
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


def fPeriodo(tempoTransito,distanza_cm,p1,p2):
	v0=larghezza_bandiera[0]*distanza_cm/(tempoTransito*distanza_bandiera[0])
	theta=np.arccos(1-v0**2/(2*g*distanza_cm))
	return 2*np.pi*np.sqrt(distanza_cm/g)*(1+theta**2.*p1+p2*theta**4.)

#print(len(lettura(misure_angoli[0])[1]),len(lettura(misure_angoli[0])[0]))
p0=np.array([1.11,1/16,11/3072])
popt,pcov=curve_fit(fPeriodo,lettura(misure_angoli[0])[1],lettura(misure_angoli[0])[0],p0)
dl,dp1,dp2=pcov.diagonal()
print('distanza cm= %.2f+-%.2f,p1=%.3f +- %.3f,p2=%.3f +- %.3f'%(popt[0],dl,popt[1],dp1,popt[2],dp2))

def tempo_transito(theta):
	return larghezza_bandiera[0]*popt[0]/(distanza_bandiera[0]*np.sqrt(2*g*popt[0]*(1-np.cos(theta))))

v0=larghezza_bandiera[0]*popt[0]/(lettura(misure_angoli[0])[1]*distanza_bandiera[0])
theta=np.arccos(1-v0**2/(2*g*popt[0]))

achi2=(((lettura(misure_angoli[0])[0]-fPeriodo(lettura(misure_angoli[0])[1],*popt))/0.00007)**2).sum()
dof=len(lettura(misure_angoli[0])[0])-len(popt)
pvalue=chi2.cdf(achi2,dof)

print('chi2=%.2f,gradi di libertà=%.2f,pValue=%.2f'%(achi2,dof,pvalue))
x=np.linspace(0.36,0.4,1000)
y=fPeriodo(tempo_transito(x),*popt)
pylab.errorbar(theta,lettura(misure_angoli[0])[0],0.00007,fmt='o')
pylab.plot(x,y)
pylab.show()