import pylab
from scipy.optimize import curve_fit
p = pylab.array([55.1, 50.4, 42.6, 39.1, 60.5, 40.7])
q = pylab.array([35.8, 41.3, 52.2, 61.4, 34.4, 57.5])
Dp = pylab.array(len(p)*[0.5], 'd')
Dq = pylab.array(len(q)*[1], 'd')
errore=([ 0.00078025,0.00058627,0.00036699,0.00026525,0.00084505,0.00030246])
print(errore)		
pylab.xlabel('1/p [1/cm]')
pylab.ylabel('1/q [1/cm]')
pylab.axis([0.015,0.03,0.015,0.035])
pylab.grid(color = 'gray'), 
pylab.errorbar(1./p, 1./q, Dp/(p*p), Dq/(q*q), 'o', color = 'black')
def f(x, a, b):
    return a*x + b
popt, pcov = curve_fit(f, 1./p, 1./q, pylab.array([-1.,1.]),sigma=errore)
a, b       = popt
da, db     = pylab.sqrt(pcov.diagonal())
print('Acqua: n = %f +- %f' %(a, da))
x=pylab.linspace(0,0.05,100000)
pylab.plot(x, f(x, a, b), color = 'black')
pylab.savefig('rifrazione_acqua.png')
pylab.show()