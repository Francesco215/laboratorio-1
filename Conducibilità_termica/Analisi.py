import numpy as np
import pylab as lab
import scipy.optimize
from scipy.odr import odrpack
from scipy import stats
files=["dati/temp11.txt","dati/temp12.txt","dati/temp13.txt","dati/temp14.txt","dati/temp15.txt","dati/temp16.txt","dati/temp17.txt","dati/temp18.txt","dati/temp19.txt","dati/temp110.txt","dati/temp111.txt","dati/temp112.txt","dati/temp113.txt","dati/temp114.txt"]

W=4
S=0.004
k=200


media=np.array([])
devStand=np.array([])
for i in range (0,len(files)):
	estrazione=np.loadtxt(files[i],unpack='true')
	media=np.insert(media,len(media),np.mean(estrazione[3]-estrazione[1]))
	devStand=np.insert(devStand,len(devStand),np.std(estrazione[3]-estrazione[1]))#aggiungi errore
	
s=0.
poi=0.025
d=np.array([0.]*len(media))
for i in range(0,len(media)):
    s += poi
    d[i]=s

errDistanze=np.array([0.001]*len(d))

def F(p,x):
	return p[0]*x+p[1]

model=odrpack.Model(F)
data = odrpack.RealData(d, media, errDistanze, devStand)
odr = odrpack.ODR(data, model, beta0=np.array([W/S/k,0]) )
out = odr.run()
popt, pcov = out.beta, out.cov_beta
m,q= popt
dm,dq = np.sqrt(pcov.diagonal())
chi2 = out.sum_square
print('m = %.3f +/- %.3f\nq = %.3f +/- %.3f\n' % (m, dm,q,dq))
print('Chisquare = %.1f' % chi2)

dof = len( media ) - len( popt )

result = 1 - stats.chi2.cdf ( chi2 , dof )
if result > 0.5:
   print('p-value1= %.2f ' % (100-100*result) )
else:
   print('p-value1= %.2f ' % (100*result) )
print('Chisquare1 atteso: %.1f +/- %.1f' %(dof,np.sqrt(4./5.*dof)))

x=np.linspace( 0.001  , d[len(d)-1]+0.01, 1000   )
lab.xlabel('  asd')
lab.ylabel(' asd ')
lab.grid( color= 'gray' )

#GRAFICO
lab.title('Lenti')
lab.figure(1)
#lab.axis([ 2 , 4.6 , 0.5 , 4 ])	
lab.errorbar( d , media , devStand , errDistanze , fmt='o' )                          
lab.plot( x, F( popt , x ))                                

#lab.savefig( 'figura1.pdf' )


lab.figure(2)
lab.title('Residui')
#lab.axis([ 2 , 4.6 ,-0.1 , 0.1 ])	
lab.errorbar( d , media- F(popt, d)  , devStand , errDistanze  , fmt='o' )              
lab.plot( x, 0*x )

#lab.savefig( 'figura2.pdf' )
lab.show()








