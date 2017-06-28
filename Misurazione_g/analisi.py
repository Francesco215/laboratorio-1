import numpy as np
import pylab
from scipy.optimize import curve_fit
from scipy import stats
#masse stimate in grammi
g=9.807
massaPiattello=7.87
massaMolla=3.08
masseg=np.array([19.998,30.001,39.970,50.017])
#sistemo la faccenda portando in kg
masse=np.array([])#in kg
for i in range (0,len(masseg)):
	a=((masseg[i]+massaPiattello)/1000)
	masse=np.insert(masse,len(masse),a)

allungamenti=np.array([0.076,0.114,0.15,0.186])#in metri+-1.5mm


#tempi di 10 oscillazioni
tempi=([[6.85,6.88,6.83,6.83,8.80,6.72,6.87,6.77,6.73],
		[7.99,7.88,7.96,7.87,7.76,7.76,7.71,7.80,7.89],
		[8.74,8.70,8.75,8.75,8.63,8.74,8.72,8.63,8.73],
		[9.53,9.50,9.53,9.59,9.57,9.51,9.50,9.57,9.49]])
#divido i tempi in 10 per trovare 10 periodi

periodi=([])
devPeriodi=([])
for i in range (0,len(tempi)):
	media=np.mean(tempi[i])/10
	std=np.std(tempi[i])/(10*np.sqrt(len(tempi[i])))
	periodi=np.insert(periodi,len(periodi),media)
	devPeriodi=np.insert(devPeriodi,len(devPeriodi),std)

def Periodo(m,k,k0):
	T2=4*np.pi**2*(m/k)+k0
	return T2

k,sk=curve_fit(Periodo,masse,periodi**2,sigma=devPeriodi)
achi2=((periodi**2-Periodo(masse,*k))/devPeriodi).sum()

print("\n\nk=",k[0],"+-",sk[0][0])
print('chi2=',achi2,'pValue=',stats.chi2.cdf(achi2,len(periodi)))


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
bchi2=(((allungamenti-fitG(masse,*popt))/0.005)**2).sum()

print('\n\ng/k=',popt[0],"+-",mammt[0][0])
print("chi2=",bchi2,'pValue=',stats.chi2.cdf(bchi2,len(allungamenti)))

x=np.linspace(masse[0]-0.003,masse[len(masse)-1]+0.003,100)
y=fitG(x,*popt)
pylab.plot(x,y)
pylab.errorbar(masse,allungamenti,yerr=0.0015,fmt='.')
pylab.title("Grafico che mostra l'allungamento in funzione delle masse")
pylab.xlabel("m[kg]")
pylab.ylabel("∆l[m]")
pylab.show()

g=popt[0]*k[0]
dg=popt[0]*sk[0][0]+k[0]*mammt[0][0]

print ('\n\ng=',g,'+-',dg,'\n\n')