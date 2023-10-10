#Luca Timpano 240236

import requests
import json
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


data_breast_cancer = requests.get('https://pkgstore.datahub.io/machine-learning/breast-cancer/breast-cancer_json/data/0149001ab9c3745142226f435bf3421f/breast-cancer_json.json').text
data_breast_cancer_json = json.loads(data_breast_cancer)


def eta(data_breast_cancer_json):                                                                           #Funzione che restituisce una lista ordinata contenente l'etè dei pazienti
    eta = []
    for patient in data_breast_cancer_json:
        if patient['age'] not in eta:
            eta.append(patient['age'])
            eta = sorted(eta)
    return eta

def calcola_dimesione(data_breast_cancer_json):                                                             #Funzione che calcola la dimensione media del tumore
    lista_eta = eta(data_breast_cancer_json)                                                                #Importo la lista contenente l'età
    diz = crea_dizionario(lista_eta)                                                                        #Creo un dizionario che ha come chiave l'età del paziente e come valore '0'
    for key in diz.keys():
        cont = 0
        somma = 0
        for patient in data_breast_cancer_json:
            if key == patient['age']:

                if len(patient['tumor-size']) == 5:                                                         #I valori potrebbero essere nella forma xx-xx
                    somma += (int(patient['tumor-size'][0:2])+int(patient['tumor-size'][3:5]))/2            #Calcolo la dimensione media per paziente

                elif len(patient['tumor-size']) == 3:                                                       #I valori potrebbero essere nella forma x-x
                    somma += (int(patient['tumor-size'][0:1])+int(patient['tumor-size'][2:3]))/2
        
                cont += 1
        diz[key] += somma/cont                                                                              #Associo al dizionario la media complessiva per età
    lista_dimension = estrai_lista(diz)                                                                     #Estraggo una lista contenente le medie per età
    return lista_dimension
    
def crea_dizionario(lista_eta):                                                                             #Funzione che crea il dizionario con chiave l'età del paziente
    ret = {}
    for eta in lista_eta:
        ret[eta] = 0
    return ret

def estrai_lista(diz):                                                                                      #Funzione che mi estrae la lista dal dizionario
    ret = []
    for value in diz.values():
        ret.append(value)
    return ret

def grafico_dimensione():                                                                                   #Funzione che 'stampa' il grafico della dimensione del tumore
    X = eta(data_breast_cancer_json)                                                                        #L'asse X corrisponde all'età
    Y = calcola_dimesione(data_breast_cancer_json)                                                          #L'asse Y corrisponde alla dimensione del tumore
    plt.style.use(['Solarize_Light2'])                                                                      #Utilizzo lo stile Solarize_Light2
    plt.title("Dimensione\n(In correlazione all'età)")
    plt.xlabel("ETA'")
    plt.ylabel("DIMENSIONE (mm)")
    plt.plot(X,Y, linewidth=3)                                                                              #linewidth == spessore del grafico
    plt.fill_between(X, Y, alpha=0.2)                                                                       #Riempimento dell'area sottesa al grafico
    plt.show()


def posizione(data_breast_cancer_json):                                                                     #Funzione che inserisce i casi nella matrice 6*6
    matrix = crea_matrice()
    for patient in data_breast_cancer_json:
        if patient['breast'] == 'right' and patient['breast-quad'] == 'right_up':                           #Inserisco i casi nel seno destro
            matrix[0][5] += 1
        elif patient['breast'] == 'right' and patient['breast-quad'] == 'left_up':
            matrix[0][3] += 1
        elif patient['breast'] == 'right' and patient['breast-quad'] == 'central':
            matrix[1][4] += 1
        elif patient['breast'] == 'right' and patient['breast-quad'] == 'right_low':
            matrix[2][5] += 1
        elif patient['breast'] == 'right' and patient['breast-quad'] == 'left_low':
            matrix[2][3] += 1
        
        elif patient['breast'] == 'left' and patient['breast-quad'] == 'right_up':                          #Inserisco i casi nel seno sinistro
            matrix[0][2] += 1
        elif patient['breast'] == 'left' and patient['breast-quad'] == 'left_up':
            matrix[0][0] += 1
        elif patient['breast'] == 'left' and patient['breast-quad'] == 'central':
            matrix[1][1] += 1
        elif patient['breast'] == 'left' and patient['breast-quad'] == 'right_low':
            matrix[2][2] += 1
        elif patient['breast'] == 'left' and patient['breast-quad'] == 'left_low':
            matrix[2][0] += 1

    return matrix

def crea_matrice():                                                                                         #Funzione che crea una matrice 6*6 composta da soli 0
    ret = []
    for i in range(3):
        riga = [0] * 6
        ret.append(riga)
    return ret

def grafico_posizione():                                                                                    #Fuznione che 'stampa' il grafico relativo alla posizione
    matrix = posizione(data_breast_cancer_json)
    plt.style.use(['Solarize_Light2'])
    plt.title('Posizione tumore')
    plt.axvline(3,color='white',linewidth='7')                                                              #Stampo una linea che divide la matrice a metà
    sns.heatmap(matrix, cmap='cividis',annot=True,cbar_kws={'orientation':'vertical','label':'Casi diagnosticati'}, xticklabels=['','SINISTRA','','','DESTRA',''],yticklabels=[''])         #Utilizzo la libreria seaborn per stampare una heatmap
    plt.show()

def conta_meno(data_breast_cancer_json,valore):                                                             #Conta i casi relativi alla menopausa, "valore" può prendere le stringhe 'ge40' 'lt40' 'premeno'
    cont = 0
    for patient in data_breast_cancer_json:
        if patient['menopause'] == valore:
            cont += 1
    return cont

def grafico_menopausa():                                                                                    #Funzione che 'stampa' il grafico relativo alla menopausa
    num_meno_ge40 = conta_meno(data_breast_cancer_json,'ge40')                                              #Menopausa ge40
    num_no_meno_lt40 = conta_meno(data_breast_cancer_json,'lt40')                                           #Menopausa lt40       
    num_no_meno = conta_meno(data_breast_cancer_json,'premeno')                                             #Pre-menopausa  
    slices = [num_meno_ge40,num_no_meno_lt40,num_no_meno]
    plt.style.use('Solarize_Light2')
    explode = [0,0,0.08]                                                                                    #Utilizzo la fuznione explode per differenziare i casi pre-menopausa-menopausa
    plt.title('Casi diagnosticati prima e dopo la menopausa')
    labels = ['Menopausa (ge40)','Menopausa (lt40)','Pre-menopausa']
    colors = ['#ee2e31','#f4c095','#1d7874']                                                                #Colori per il grafico
    plt.pie(slices, labels=labels,colors = colors,explode = explode, autopct=make_autopct(slices))          #Utilizzo un grafico a torta
    plt.show()

def make_autopct(values):                                                                                   #Funzione per visualizzare i dati direttamente sul grafico
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{p:.2f}%  ({v:d})'.format(p=pct,v=val)
    return my_autopct

def malignità(data_breast_cancer_json):                                                                     #Funzione che restituisce una lista ordinata contente i gradi di malignità del tumore
    ret = []
    for patient in data_breast_cancer_json:
        if patient['deg-malig'] not in ret:
            ret.append(patient['deg-malig'])
    return sorted(ret)

def recurrence_events(data_breast_cancer_json,Class):                                                       #Funzione che restituisce una lista con i casi di tipo "Class" che può prendere 'recurrence-events' o 'no-recurrence-events'
    lista_eta = eta(data_breast_cancer_json)
    diz = crea_dizionario(lista_eta)
    for key in diz.keys():
        for patient in data_breast_cancer_json:
            if patient['age'] == key and patient['Class'] == Class:
                diz[key] += 1
    lista_casi = estrai_lista(diz)
    return lista_casi

def irradiat(data_breast_cancer_json,tipo):                                                                 #Funzione che restituisce una lista con i casi curabili con la radiotepia in relazione alla malignità del tumore
    lista_mal = malignità(data_breast_cancer_json)
    diz = crea_dizionario(lista_mal)
    for key in diz.keys():
        for patient in data_breast_cancer_json:
            if patient['deg-malig'] == key and patient['irradiat'] == tipo:                                 #"Tipo" può ricevere le stringhe 'yes' o 'no'
                diz[key] += 1
    lista_casi = estrai_lista(diz)
    return lista_casi

def grafico_recurrence():                                                                                   #Funzione che 'stampa' il grafico relativo alle ricadute
    X = eta(data_breast_cancer_json)
    Y = recurrence_events(data_breast_cancer_json,'recurrence-events')
    Y2 = recurrence_events(data_breast_cancer_json,'no-recurrence-events')
    plt.style.use(['Solarize_Light2'])
    plt.title("Casi di ricaduta\n(In base all'età)")
    plt.xlabel("ETA'")
    plt.ylabel("RICORRENZA")
    plt.plot(X,Y,label='Ricaduta', linewidth=3)                                                             #Sovrappongo due grafici
    plt.fill_between(X, Y, alpha=0.2)
    plt.plot(X,Y2,label='No ricaduta', color='orange', linewidth=3, linestyle= ":")                         #Utilizzo lo stile di linea ':'
    plt.fill_between(X, Y2, alpha=0.2,color='orange' )
    plt.legend()                                                                                            #Visualizzo le label dei corrispettivi grafici
    plt.show()

def grafico_irradiat():                                                                                     #Funzione che 'stampa' il grafico relativo ai casi curabili con la radioterapia

    X = malignità(data_breast_cancer_json)
    Y = irradiat(data_breast_cancer_json,'yes')
    Y2 = irradiat(data_breast_cancer_json,'no')
    indexs = np.arange(len(X))                                                                              #Uso la libreria numpy per creare un indice di lunghezza n, per affiancare i due grafici a barre 
    width = 0.5                                                                                             #Riduco la dimensione del garfico a barre a 0.5
    plt.style.use(['Solarize_Light2'])
    plt.title('RADIOTERAPIA\n(In base alla malignità)')
    plt.xlabel("MALIGNITA'")
    plt.ylabel('CASI')
    plt.bar(indexs,Y2,label='Non curabile', width=width, color='orange')
    plt.bar(indexs+width,Y, width=width,label='Curabile')
    plt.xticks(indexs+width/2, X)                                                                           #Sposto gli indici per farli corrispondere con la nuova posizione del grafico
    plt.legend()
    plt.show()

def opz():
    inp = int(input('\nVuoi visualizzare altro?\nSI(1)\nNO(0)\n'))
    if inp == 1:
        main()
    elif inp == 0:
        return -1
    else:
        print('\nInserire valore valido!\n')
        opz()

def main():                                                                                                 #Funzione main che mi permette di far scegliere l'opzione desiderata all'utente
    print('Luca Timpano 240236\nANALISI DATI SUL TUMORE AL SENO\n')
    print('SELEZIONA OPZIONE\nGRAFICO RELATIVO ALLA DIMENSIONE(1)\nGRAFICO POSIZIONE(2)\nGRAFICO CASI MENOPAUSA(3)\nGRAFICO RADIOTERAPIA(4)\nGRAFICO RICADUTE(5)')
    a = int(input('Seleziona opzione: '))
    if a == 1:
        print('Caricamento in corso...')
        print('Dati raccolti da',len(data_breast_cancer_json),'pazienti')                                   #Stampo il numero di pazienti totale su cui si sono raccolti i dati
        dimensione_media = sum(calcola_dimesione(data_breast_cancer_json))/len(calcola_dimesione(data_breast_cancer_json))
        print('Dimensione Tumore Media: ',round(dimensione_media),'mm')                                     #Stampo la dimensione media
        grafico_dimensione()
    elif a == 2:
        print('Caricamento in corso...')
        print('Dati raccolti da',len(data_breast_cancer_json),'pazienti')
        grafico_posizione()
    elif a == 3:
        print('Caricamento in corso...')
        print('Dati raccolti da',len(data_breast_cancer_json),'pazienti')
        grafico_menopausa()
    elif a == 4:
        print('Caricamento in corso...')
        print('Dati raccolti da',len(data_breast_cancer_json),'pazienti')
        print('Casi curabili con la radioterapia:',sum(irradiat(data_breast_cancer_json,'yes')),'\nCasi non curabili:',sum(irradiat(data_breast_cancer_json,'no')))         #stampo il numero di casi curabili e non curabili
        grafico_irradiat()
    elif a == 5:
        print('Caricamento in corso...')
        print('Dati raccolti da',len(data_breast_cancer_json),'pazienti')
        print('Numero di ricadute totali:',sum(recurrence_events(data_breast_cancer_json,'recurrence-events')))         #stampo il numero di ricadute
        grafico_recurrence()
    else:
        print('\nInserire valore valido!\n')
        main()
    opz()

main()

