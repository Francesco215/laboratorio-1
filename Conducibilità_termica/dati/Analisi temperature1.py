import math
import numpy as np
import matplotlib.pyplot as plt

def regression_line (datix, datiy, n_dati) : #Calcola la linea di miglior fit
    ux = np.average(datix)                   #Formule prese da http://mathworld.wolfram.com/LeastSquaresFitting.html   
    uy = np.average(datiy)
    sxx = -n_dati * ux**2
    sxy = -n_dati * ux * uy
    syy = -n_dati * uy**2
    
    i = 0
    while i < n_dati :
        sxx = sxx + datix[i]**2
        sxy = sxy + datix[i] * datiy[i]
        syy = syy + datiy[i]**2
        i = i + 1
    
    b = sxy / sxx
    a = uy - b * ux
    s = np.sqrt((syy - sxy**2 / sxx) / (len(x) - 2))
    delta_b = s / np.sqrt(sxx)
    delta_a = s * np.sqrt(1 / len(x) + ux**2 / sxx)
    return np.array([b, a, delta_b, delta_a])


#Creazione array medie e errori
#Riceve documenti txt nella forma "nome_documento"+i+j
medie = np.array([])
errori = np.array([])
j = 1
while j < 3 :       #Numero cilindro
    i = 1
    while i < 15 :  #Numero foro
        n = str(j) + str(i)
        percorso = "/Users/Lorenzo/Desktop/Relazioni fisica/Conducibilità termica/Temperature/temp" + n + ".txt"
        listmisure = np.genfromtxt(percorso, unpack = True, skip_header = 4)
        
        listmisura1 = [listmisure[0], listmisure[1]]
        listmisura2 = [listmisure[2], listmisure[3]]
        sigmamisura1 = np.std(listmisura1[1])
        sigmamisura2 = np.std(listmisura2[1])
        mediamisura1 = np.average(listmisura1[1])
        mediamisura2 = np.average(listmisura2[1])
        medie = np.append(medie, mediamisura1)
        errori = np.append(errori, sigmamisura1)
        print(np.round(mediamisura1, decimals = 2) , "+-" , np.round(sigmamisura1, decimals = 2) , " " , np.round(mediamisura2, decimals = 2) , "+-" , np.round(sigmamisura2, decimals = 2))
        
        i = i + 1
    print("\n")
    j = j + 1

#Analisi dati
n_dati = int(len(medie) / 2)                    #Numero dati analizzati
x = (np.linspace(0, 13, n_dati) * 2.5) + 2.5
x1 = (np.linspace(-2, 15, 1000) * 2.5) + 2.5    #Per visualizzare meglio la linea di miglior fit
medie1 = medie[0:n_dati]                        #medie cilindro non isolato
medie2 = medie[n_dati:]                         #medie cilindro isolato
errorey1 = errori[0:n_dati]                     #errori cilindro non isolato
errorey2 = errori[n_dati:]                      #errori cilindro isolato
errorex = np.ones(n_dati) * 0.1                 #errore sulle lunghezze                
regression_line1 = regression_line(x, medie1, n_dati)   #linea miglior fit cilindro non isolato
regression_line2 = regression_line(x, medie2, n_dati)   #linea miglior fit cilindro isolato
print(regression_line1)
print(regression_line2, "\n")

#Calcolo la linea di miglior fit eliminando i punti che si discostano troppo
new_medie1 = np.delete(medie1, 3)
new_medie2 = np.delete(medie2, 2)
new_x1 = np.delete(x, 3)
new_x2 = np.delete(x, 2)
new_regression_line1 = regression_line(new_x1, new_medie1, n_dati - 1)
new_regression_line2 = regression_line(new_x2, new_medie2, n_dati - 1)
print(new_regression_line1)
print(new_regression_line2, "\n")

#Creazione grafico temperature cilindro non isolato
plt.figure()
plt.title("Cilindro non isolato")
plt.errorbar(x, medie1, errorey1, errorex, fmt = 'o')
plt.plot(x1, x1 * regression_line1[0] + regression_line1[1])
plt.plot(x1, x1 * (regression_line1[0] + regression_line1[2]) + regression_line1[1] + regression_line1[3])
plt.plot(x1, x1 * (regression_line1[0] - regression_line1[2]) + regression_line1[1] - regression_line1[3])
plt.grid()
plt.ylabel('Ti [°C]')
plt.xlabel('Li [cm]')

#Creazione grafico temperature cilindro isolato
plt.figure()
plt.title("Cilindro isolato")
plt.errorbar(x, medie2, errorey2, errorex, fmt = 'o')
plt.plot(x1, x1 * regression_line2[0] + regression_line2[1])
plt.plot(x1, x1 * (regression_line2[0] + regression_line2[2]) + regression_line2[1] + regression_line2[3])
plt.plot(x1, x1 * (regression_line2[0] - regression_line2[2]) + regression_line2[1] - regression_line2[3])
plt.grid()
plt.ylabel('Ti [°C]')
plt.xlabel('Li [cm]')

plt.show()