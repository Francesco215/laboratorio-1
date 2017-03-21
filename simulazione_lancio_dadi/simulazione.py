import random
import numpy
import scipy
from itertools import product
def esperimento (nDadi,nLanci):
	Lanci=numpy.array([])
	for j in range (1,nLanci+1):
		a=0
		for i in range(1,nDadi+1):
			a=a+random.randint(1,6)
		Lanci=numpy.insert(Lanci,len(Lanci),a)
	return Lanci
def probabilità(nDadi, numero):
    rollAmount = 6**nDadi
    targetAmount = 0
    for i in map(sum, product(range(1,7), repeat=nDadi)):
        if i == numero:
            targetAmount += 1
    odds = targetAmount / rollAmount
    return odds

lanci=numpy.array([100,100000,10000,10000,10000])
dadi=numpy.array([1,1,2,5,10])
listaProbabilità=numpy.zeros((5,60))
medie=[]
devStan=[]

for j in range (0,len(dadi)):
	for i in range(dadi[j],dadi[j]*6):
		listaProbabilità[[j],[i]]=probabilità(dadi[j],i)
print (listaProbabilità)