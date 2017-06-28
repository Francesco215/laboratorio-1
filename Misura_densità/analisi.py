
import numpy as np
from scipy.odr import odrpack
from scipy import constants
from scipy import stats
import pylab

errCal=0.005
errBil=0.001

#si fà tutto in grammi al cm^3

#qundi gli input sono in cm
def sfera(d,sd):
	V=np.pi*d**3/6
	dV=np.pi*d**2*sd/6
	return V,dV


def cilindro(d,h,sd,sh):
	V=h*np.pi*d**2/4
	sV=np.pi*(d*h*sd/2+d**2*sh/4)
	return V,sV


def cubo(l1,l2,l3):
	return l1*l2*l3
Sfera=np.vectorize(sfera)
Cilindro=np.vectorize(cilindro)
Cubo=np.vectorize(cubo)

diametriSferaAcciaio=([0.952,1.268,1.429,1.666,1.825])
masseSferaAcciaio=([3.525,8.355,11.894,18.908,24.832])

def denzità(parametri,m):
	return parametri[0]*m +parametri[1]

lineare=odrpack.Model(denzità)
dati=odrpack.RealData(Sfera(diametriSferaAcciaio,errCal)[0],masseSferaAcciaio,Sfera(diametriSferaAcciaio,errCal)[1],errBil)
odr=odrpack.ODR(dati,lineare,beta0=np.array([0.00001,0.]))
fit=odr.run()
popt,mammt=fit.beta,fit.cov_beta
print(popt[0],mammt[0][0])
chi2=fit.sum_square

x=np.linspace(0,26,100)
y=denzità(popt,x)
pylab.plot(x,y)
pylab.errorbar(masseSferaAcciaio,Sfera(diametriSferaAcciaio,errCal)[0],Sfera(diametriSferaAcciaio,errCal)[1],errBil,fmt='.')
pylab.show()















