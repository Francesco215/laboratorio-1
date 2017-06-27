import numpy
import math
import pylab as lab
from scipy.odr import odrpack
from scipy import stats

p, q =numpy.loadtxt('Misure1.txt', unpack=True)
dp0= 0.01
dq0=dp0

#ATTENZIONE
p=1./p
q=1./q

dp=numpy.array([0.]*len(p))
dq=numpy.array([0.]*len(p))

dp = dp0 * p**2.
dq = dq0 * q**2.


#    1./q  =  1./f   -   1./p



def F(arr, d ):
    return 1./arr[0] - d




model=odrpack.Model(F)
data = odrpack.RealData(p, q, dp, dq)
odr = odrpack.ODR(data, model, beta0=numpy.array([ 1./ (p[0] + q[0]) ]) )
out = odr.run()
popt, pcov = out.beta, out.cov_beta
f= popt
df = numpy.sqrt(pcov.diagonal())
chi2 = out.sum_square
print('f = %.3f +/- %.3f' % (f, df))
print('Chisquare = %.1f' % chi2)

dof = len( p ) - len( popt )

result = 1 - stats.chi2.cdf ( chi2 , dof )
if result > 0.5:
   print('p-value1= %.2f ' % (100-100*result) )
else:
   print('p-value1= %.2f ' % (100*result) )
print('Chisquare1 atteso: %.1f +/- %.1f' %(dof,numpy.sqrt(4./5.*dof)))









x=numpy.linspace( 0.001  , p[len(p)-1]+ 1, 100000   )
lab.xlabel('  1 / p ')
lab.ylabel(' 1 / q ')
lab.grid( color= 'gray' )

#GRAFICO
lab.title('Lenti')
lab.figure(1)
lab.axis([ 2 , 4.6 , 0.5 , 4 ])	
lab.errorbar( p , q , dq , dp , fmt='o' )                          
lab.plot( x, F( popt , x ))                                

#lab.savefig( 'figura1.pdf' )


lab.figure(2)
lab.title('Residui')
lab.axis([ 2 , 4.6 ,-0.1 , 0.1 ])	
lab.errorbar( p , q- F(popt, p)  , dq , dp  , fmt='o' )              
lab.plot( x, 0*x )

#lab.savefig( 'figura2.pdf' )
		






print(p,q)














#DIVERGENTE



"""
si ponga la lente convergente sul banco otti-
co e si metta a fuoco l'immagine sullo schermo. A questo
punto si posizioni la lente divergente tra la convergente
e lo schermo e si misuri la distanza pi (da prendere con
il segno negativo) tra la divergente e lo schermo stes-
so. Si allontani lo schermo in modo da rimettere a fuoco
l'immagine e si misuri la nuova distanza qi (questa volta
positiva) tra la divergente e lo schermo
"""

p, q =numpy.loadtxt('Misure2.txt', unpack=True)


#ATTENZIONE
p=1./p
q=1./q

dp=numpy.array([0.]*len(p))
dq=numpy.array([0.]*len(p))

dp = dp0 * p**2.
dq = dq0 * q**2.



#    1./q  =  1./f2   +   1./p     in quanto p>0 dai dati



def F(arr, d ):
    return 1./arr[0] + d




model=odrpack.Model(F)
data = odrpack.RealData(p, q, dp, dq)
odr = odrpack.ODR(data, model, beta0=numpy.array([ 1./ ( q[0] - p[0] ) ]) )
out = odr.run()
popt, pcov = out.beta, out.cov_beta
f= popt
df = numpy.sqrt(pcov.diagonal())
chi2 = out.sum_square
print('f2 = %.3f +/- %.3f' % (f, df))
print('Chisquare2 = %.1f' % chi2)

dof = len( p ) - len( popt )

result = 1 - stats.chi2.cdf ( chi2 , dof )
if result > 0.5:
   print('p-value2= %.2f ' % (100-100*result) )
else:
   print('p-value2= %.2f ' % (100*result) )
print('Chisquare2 atteso: %.1f +/- %.1f' %(dof,numpy.sqrt(4./5.*dof)))









x=numpy.linspace( 0.001  , p[len(p)-1]+ 1, 100000   )
lab.xlabel('  1 / p ')
lab.ylabel(' 1 / q ')
lab.grid( color= 'gray' )

#GRAFICO
lab.title('Lente divergente')
lab.figure(3)
lab.axis([ 2 , 4.6 ,0.5 , 4 ])	
lab.errorbar( p , q , dq , dp , fmt='o' )                          
lab.plot( x, F( popt , x ))                                

#lab.savefig( 'figura3.pdf' )


lab.figure(4)
lab.title('Residui')
lab.axis([ 2 , 4.6 ,-0.1 ,  0.1 ])	
lab.errorbar( p , q- F(popt, p)  , dq , dp  , fmt='o' )              
lab.plot( x, 0*x )

#lab.savefig( 'figura4.pdf' )
lab.show()		







print(p,q)





