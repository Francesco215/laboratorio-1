import numpy as np
import pylab
from scipy.optimize import curve_fit
from scipy import stats
from scipy import integrate as integ
tempi=np.array([[3.821,2.167,1.817,1.627,1.560,1.531,1.538,1.554,1.583,1.630],#tempi
	            [0.005,0.003,0.010,0.003,0.003,0.002,0.004,0.003,0.003,0.003],#le loro deviazioni standard
	            [0.005,0.003,0.010,0.003,0.003,0.002,0.004,0.003,0.003,0.003]])
distanze=np.array([[0.023,0.079,0.123,0.179,0.222,0.279,0.322,0.379,0.422,0.479],[0.0001,0.001]])#buchi e i loro errori
lunghezza=np.array([1.01,0.01])
residui=[]
chi=[]
g=9.807

#definisco la funzione del periodo
def FunzionePeriodo(distanza,lunghezzat):
	tempo=2*np.pi*np.sqrt((lunghezzat**2/12+(distanza**2))/(g*distanza))
	return tempo
#defisisco la funzione della derivata del periodo e la vettorizzo
def dFunzionePeriodot(distanza,lunghezzat):
	dtempo=np.pi*1/g-lunghezzat**2/(12*g*distanza**2)*np.sqrt(g*distanza/(lunghezzat**2/12+distanza**2))
	return dtempo
dFunzionePeriodo=np.vectorize(dFunzionePeriodot)
#propago l'errore della lunghezza della prima misura sui tempi e lo ripeto n volte
for i in range(0,50):
	if i==0:
		lunghezzaCalc=curve_fit(FunzionePeriodo,distanze[0][1:],tempi[0][1:],sigma=tempi[1][1:])
	else:
		tempi[2]=tempi[1]+np.absolute(distanze[1][1]*dFunzionePeriodo(distanze[0],lunghezzaCalc[0]))
		lunghezzaCalc=curve_fit(FunzionePeriodo,distanze[0],tempi[0],sigma=tempi[1])
#trovo valore ideale della lunghezza calcolata
print("lunghezza pendolo",lunghezzaCalc[0], " e incertezza",lunghezzaCalc[1])
#for loop per trovare il chi^2
for i in range(0,len(tempi[0])):
	b=((tempi[0][i]-FunzionePeriodo(distanze[0][i],lunghezzaCalc[0]))/tempi[2][i])**2
	chi.append(b)
print("chi^2=",sum(chi))
#for loop per calcolare i residui
for i in range(0,len(tempi[0])):
	b=tempi[0][i]-FunzionePeriodo(distanze[0][i],lunghezzaCalc[0])
	residui.append(b)
s=np.linspace(sum(chi), 1000, 1000000 )
ps=stats.chi2(len(chi)-1).pdf( s ) 
#lab.plot(  s,  ps  )
#lab.show()      
pValue=integ.simps(ps,s)
print("p-value=",pValue)
#faccio il grafico normale
pylab.errorbar(distanze[0],tempi[0],tempi[2],linestyle='',color='black',marker='o')
x=np.linspace(0,0.6,1000)
y=2*np.pi*np.sqrt((lunghezzaCalc[0]**2/12+(x**2))/(g*x))
pylab.plot(x,y)
pylab.ylabel('t[s]')
pylab.xlabel('d[s]')
pylab.xlim(0,0.55)
pylab.ylim(0,5.5)
pylab.grid(True)
pylab.title('Pendolo fisico')
pylab.savefig('Fit strafigo')
pylab.show()
#faccio il grafico dei residui
pylab.errorbar(distanze[0],residui,tempi[2],linestyle='',color='black',marker='o')
yo=0*x
ym=2*np.pi*(np.sqrt((lunghezza[0]**2/12+(x**2))/(g*x))-np.sqrt((lunghezzaCalc[0]**2/12+(x**2))/(g*x)))
ymp=2*np.pi*(np.sqrt(((lunghezza[0]+lunghezza[1])**2/12+(x**2))/(g*x))-np.sqrt((lunghezzaCalc[0]**2/12+(x**2))/(g*x)))
ymm=2*np.pi*(np.sqrt(((lunghezza[0]-lunghezza[1])**2/12+(x**2))/(g*x))-np.sqrt((lunghezzaCalc[0]**2/12+(x**2))/(g*x)))
pylab.plot(x,yo)
pylab.plot(x,ym)
pylab.plot(x,ymp)
pylab.plot(x,ymm)
pylab.ylabel('Δt[s]')
pylab.xlabel('d[s]')
pylab.xlim(0,0.55)
pylab.ylim(-0.18,0.11)
pylab.grid(True)
pylab.title('Grafico dei residui')
pylab.show()




