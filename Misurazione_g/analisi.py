import numpy as np
import matplotlib
import pylab
from scipy.odr import odrpack
from scipy.optimize import curve_fit
#masse stimate in grammi
g=9.807
massaPiattello=7.87
massaMolla=3.08
masseg=([19.95,29.9,39.85,50.01])
#sistemo la faccenda portando in kg
masse=([])#in kg
for i in range (0,len(masseg)):
	a=((masseg[i]+massaPiattello)/1000)
	masse=np.insert(masse,len(masse),a)
allungamenti=([0.088,0.134,0.182,0.227])#in metri


#tempi di 10 oscillazioni
tempi=([[7.53,7.57,7.59,7.58,7.55,7.63,7.63,7.55,7.56],
		[8.71,8.65,8.63,8.70,8.71,8.68,8.72,8.59,8.63],
		[9.55,9.65,9.62,9.54,9.59,9.67,9.69,9.64,9.68,9.51],
		[10.66,10.60,10.57,10.47,10.65,10.65,10.53,10.5,10.69,10.4]])
#divido i tempi in 10 per trovare 10 periodi
periodi=([])
DevPeriodi=([])
for i in range (0,len(tempi)):
	media=np.mean(tempi[i])/10
	std=np.std(tempi[i])/10
	periodi=np.insert(periodi,len(periodi),media)
	DevPeriodi=np.insert(DevPeriodi,len(DevPeriodi),std)
def fitPeriodi(m,k):
	return ((m+massaMolla/3000)*(2*np.pi**2))/k

fitT,varT=curve_fit(fitPeriodi,masse,periodi)

print("\n\n",fitT,varT,"\n\n")

x=np.linspace(0.025,masse[3]+0.005,100)
y=fitPeriodi(x,fitT[0])
pylab.errorbar(masse,periodi**2,yerr=DevPeriodi,fmt='.')
pylab.plot(x,y)
#pylab.xlim(18,52)
#pylab.ylim(0.5,1.2)
pylab.title("Periodi in funzione della massa")
pylab.xlabel("m[Kg]")
pylab.ylabel("T^2[s^2]")
pylab.show()
"""

def Allungamento(m,g):
	return g*m/fitT

mediaG,varG=curve_fit(Allungamento,masse,allungamenti)
pylab.plot(masse,allungamenti)
x=np.linspace(0.025,0.05,100)
y=Allungamento(x,*mediaG)
pylab.plot(x,y)
print(mediaG,varG)
pylab.show()
"""