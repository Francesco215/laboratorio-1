import numpy as np
import matplotlib
import pylab
from scipy.odr import odrpack
from scipy.optimize import curve_fit
#masse stimate in grammi
g=9.807
massaPiattello=7.87
massaMolla=3.08
masseg=np.array([19.95,29.9,39.85,50.01])
#sistemo la faccenda portando in kg
masse=np.array([])#in kg
for i in range (0,len(masseg)):
	a=((masseg[i]+massaPiattello)/1000)
	masse=np.insert(masse,len(masse),a)
allungamenti=np.array([0.088,0.134,0.182,0.227])#in metri


#tempi di 10 oscillazioni
tempi=([[7.53,7.57,7.59,7.58,7.55,7.63,7.63,7.55,7.56],
		[8.71,8.65,8.63,8.70,8.71,8.68,8.72,8.59,8.63],
		[9.55,9.65,9.62,9.54,9.59,9.67,9.69,9.64,9.68,9.51],
		[10.66,10.60,10.57,10.47,10.65,10.65,10.53,10.5,10.69,10.4]])
#divido i tempi in 10 per trovare 10 periodi
periodi=([])
devPeriodi=([])
for i in range (0,len(tempi)):
	media=np.mean(tempi[i])/10
	std=np.std(tempi[i])/10
	periodi=np.insert(periodi,len(periodi),media)
	devPeriodi=np.insert(devPeriodi,len(devPeriodi),std)

def Periodo(m,k,k0):
	T2=4*np.pi**2*(m/k)+k0
	return T2

k,sk=curve_fit(Periodo,masse,periodi**2,sigma=devPeriodi)
print("\n\nk=",k[0],"+-",sk[0][0])

pylab.errorbar(masse,periodi**2,yerr=devPeriodi,fmt='.')
x=np.linspace(masse[0]-0.003,masse[len(masse)-1]+0.003,100)
y=Periodo(x,*k)
pylab.title("Stima di k")
pylab.xlabel("m[kg]")
pylab.ylabel("t^2[s^2]")
pylab.plot(x,y)
pylab.show()

def fitG(m,a,p0):
	return p0 + m*a
popt,mammt=curve_fit(fitG,masse,allungamenti)

print('\n\nk/g=',popt[0],"+-",mammt[0][0],"\n\n")
x=np.linspace(masse[0]-0.003,masse[len(masse)-1]+0.003,100)
y=fitG(x,*popt)
pylab.plot(x,y)
pylab.errorbar(masse,allungamenti,yerr=0.0015,fmt='.')
pylab.title("Grafico che mostra l'allungamento in funzione delle masse")
pylab.xlabel("m[kg]")
pylab.ylabel("∆l[m]")
pylab.show()
