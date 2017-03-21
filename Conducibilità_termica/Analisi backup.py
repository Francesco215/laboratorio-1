import numpy
import pylab
a=0.
b=0.
medie=[]
devStand=[]
#metto i nomi dei file in una lista
isolati=['misurazioni/1e2i.txt','misurazioni/2e3i.txt','misurazioni/3e4i.txt','misurazioni/5e6i.txt','misurazioni/6e7i.txt','misurazioni/7e8i.txt','misurazioni/8e9i.txt','misurazioni/9e10i.txt','misurazioni/10e11i.txt','misurazioni/11e12i.txt','misurazioni/12e13i.txt','misurazioni/13e14i.txt','misurazioni/14e15i.txt','misurazioni/16e17i.txt','misurazioni/17e18i.txt','misurazioni/18e19i.txt','misurazioni/19e20i.txt',]
nonIsolati=['misurazioni/1e2n.txt','misurazioni/2e3n.txt','misurazioni/3e4n.txt','misurazioni/5e6n.txt','misurazioni/6e7n.txt','misurazioni/7e8n.txt','misurazioni/8e9n.txt','misurazioni/9e10n.txt','misurazioni/10e11n.txt','misurazioni/11e12n.txt','misurazioni/12e13n.txt','misurazioni/13e14n.txt','misurazioni/14e15n.txt','misurazioni/16e17n.txt','misurazioni/17e18n.txt','misurazioni/18e19n.txt','misurazioni/19e20n.txt',]
altreMisurazioni=['misurazioni/1e5i.txt','misurazioni/1e5n.txt','misurazioni/1e10i.txt','misurazioni/1e10n.txt','misurazioni/1e15i.txt','misurazioni/1e15n.txt','misurazioni/1e20i.txt']
#faccio una funzione che mi ritorni la media di ogni documento
def media(misurazione):
	differenza=[]
	#Creo una lista delle differenze tra i valori otteniti
	for line in open(misurazione):
		if not line.startswith('#'):
			row=[float(item) for item in line.split()]
			differenza.append(row[1]-row[3])
	#ne calcolo la media 
	media=numpy.mean(differenza)
	return(media)
#Faccio una funzione che mi ritorni la deviazione standard di ogni documento
def deviazioneStandard(misurazione):
	differenza=[]
	#Creo una lista delle differenze tra i valori otteniti
	for line in open(misurazione):
		if not line.startswith('#'):
			row=[float(item) for item in line.split()]
			differenza.append(row[1]-row[3])
	#ne calcolo la deviazione standard
	devStd=numpy.std(differenza)
	return(devStd)

#Analisi dati
for i in range(0,len(isolati)):
	if i==0:
		a=media(isolati[i])
		b=deviazioneStandard(isolati[i])
	else:
		a=medie[i-1]+media(isolati[i])
		b=devStand[i-1]+deviazioneStandard(isolati[i])
	medie.append(a)
	devStand.append(b)
print(medie,devStand)


















