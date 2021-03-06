import pandas as pd
import matplotlib.pyplot as plt
from math import sqrt

N = 100 #Nombre d'échantillons à prendre en compte
pas_dist = 6 #Différence de distance entre les expériences, en m.
pas_pow = 3 #différence de puissance entre les expériences, en dB.


def mean(data):
    return sum(data['sender_rssi']) / len(data)

def ecart_type(data):
    x = 0
    moyenne = mean(data)
    for val in data['sender_rssi']:
        x += pow(abs(val-moyenne), 2)
    etype = sqrt(x/len(data))

    return etype

def read_data(paths):
    datas1 = []
    datas2 = []

    for path in paths:
        datas1.append(pd.read_csv(path+'/data1.csv').tail(N))
        datas2.append(pd.read_csv(path+'/data2.csv').tail(N))

    return (datas1, datas2)

#DO: calcule la moyenne des échantillons pour chaque expérience, et trace la courbe du rssi moyen en fonction de la distance entre les noeux
#en associant chaque donnée à une valeur de distance
#INPUT: Prend un tableau de tableaux représentant les données ders expériences pour plusieurs distances différentes,
#classés par ordre de distance montante (datas[0]=distance9, datas[1]=distance12, etc...)
def trace_means_dist(datas1, datas2 = None):
    means_node_1 = []
    means_node_2 = []
    yerr1 = []
    yerr2 = []

    dist = 6
    distance = []

    for serie in datas1:
        means_node_1.append(mean(serie))
        yerr1.append(2.3263*ecart_type(serie)/sqrt(N))
    for serie in datas2:
        means_node_2.append(mean(serie))
        yerr2.append(2.3263*ecart_type(serie)/sqrt(N))

    for i in range(max(len(datas1), len(datas2))):
        distance.append(dist)
        dist += pas_dist
    print("dist", distance)

    if datas2 != None:
        means_node_1b = []
        means_node_2b = []
        yerr1b = []
        yerr2b = []
        data1b = datas2[0]
        data2b = datas2[1]
        for serie in data1b:
            means_node_1b.append(mean(serie))
            yerr1b.append(2.3263*ecart_type(serie)/sqrt(N))
        for serie in data2b:
            means_node_2b.append(mean(serie))
            yerr2b.append(2.3263*ecart_type(serie)/sqrt(N))

    plt.plot(distance, means_node_1, label='Sender 1 6m')
    plt.plot(distance, means_node_2, label='Sender 2 6m')
    plt.errorbar(distance, means_node_1, yerr=yerr1, fmt='none')
    plt.errorbar(distance, means_node_2, yerr=yerr2, fmt='none')
    if datas2 != None:
        plt.plot(ditance, means_node_1b, label='Sender 1 12m')
        plt.plot(distance, means_node_2b, label='Sender 2 12m')
        plt.errorbar(distance, means_node_1b, yerr=yerr1b, fmt='none')
        plt.errorbar(distance, means_node_2b, yerr=yerr2b, fmt='none')
    plt.xlabel('Distance (m)')
    plt.ylabel('moyenne RSSI sur 100 paquets')
    plt.legend(loc='upper left')
    plt.tight_layout()

    plt.show()

#DO: calcule la moyenne des échantillons pour chaque expérience, et trace la courbe du rssi moyen en fonction de la puissance d'émission
#en associant chaque donnée à une valeur de puissance
#INPUT: Prend un tableau de tableaux d'entiers, représentant les expériences pour différentes puissanes,
#classés par ordre de puissance montante (datas[0]=power3, datas[1]=power6, etc...)
def trace_means_pow(datas, datas2 = None):
    means_node_1 = []
    means_node_2 = []
    yerr1 = []
    yerr2 = []
    data1 = datas[0]
    data2 = datas[1]

    pow = 0
    power = []

    for serie in data1:
        means_node_1.append(mean(serie))
        yerr1.append(2.3263*ecart_type(serie)/sqrt(N))
        #valeur 2.3263 trouvée sur http://wwwmathlabo.univ-poitiers.fr/~phan/downloads/enseignement/tables-usuelles.pdf
        #pour alpha = 0.02
    for serie in data2:
        means_node_2.append(mean(serie))
        yerr2.append(2.3263*ecart_type(serie)/sqrt(N))
    print("moyennes")
    print(means_node_1)
    print(means_node_2)
    print("erreurs")
    print(yerr1)
    print(yerr2)

    for i in range(max(len(data1), len(data2))):
        power.append(pow)
        pow += pas_pow
    print("power", power)

    if datas2 != None:
        means_node_1b = []
        means_node_2b = []
        yerr1b = []
        yerr2b = []
        data1b = datas2[0]
        data2b = datas2[1]
        for serie in data1b:
            means_node_1b.append(mean(serie))
            yerr1b.append(2.3263*ecart_type(serie)/sqrt(N))
        for serie in data2b:
            means_node_2b.append(mean(serie))
            yerr2b.append(2.3263*ecart_type(serie)/sqrt(N))

    plt.plot(power, means_node_2, label='Sender 2 6m')
    plt.plot(power, means_node_1, label='Sender 1 6m')
    plt.errorbar(power, means_node_1, yerr=yerr1, fmt='none')
    plt.errorbar(power, means_node_2, yerr=yerr2, fmt='none')
    if datas2 != None:
        plt.plot(power, means_node_1b, label='Sender 1 12m')
        plt.plot(power, means_node_2b, label='Sender 2 12m')
        plt.errorbar(power, means_node_1b, yerr=yerr1b, fmt='none')
        plt.errorbar(power, means_node_2b, yerr=yerr2b, fmt='none')
    plt.xlabel('Puissance d\'émission (dB)')
    plt.ylabel('moyenne RSSI sur 100 paquets')
    plt.legend(loc='upper left')
    plt.tight_layout()

    plt.show()

#data est un tuple de dataframes pandas
def error_rate(data):
    start1 = data[0][0]['x_value'].iloc[0]
    end1 = data[0][0]['x_value'].iloc[-1]
    start2 = data[1][0]['x_value'].iloc[0]
    end2 = data[1][0]['x_value'].iloc[-1]
    error_rate1 = (end1-start1-(N-1))/N
    error_rate2 = (end2-start2-(N-1))/N
    return (error_rate1, error_rate2)

if __name__ == '__main__':

    print(error_rate(read_data(['./data/E1/E11'])))
    print(error_rate(read_data(['./data/E1/E12'])))
    print(error_rate(read_data(['./data/E1/E13'])))
    print(error_rate(read_data(['./data/E1/E14'])))
    print(error_rate(read_data(['./data/E2/E21'])))
    print(error_rate(read_data(['./data/E2/E22'])))
    print(error_rate(read_data(['./data/E2/E23'])))
    print(error_rate(read_data(['./data/E2/E24'])))
    # dist6 = read_data(['./data/E1/E11', './data/E1/E12', './data/E1/E13', './data/E1/E14'])
    # dist12 = read_data(['./data/E2/E22', './data/E2/E23', './data/E2/E24', './data/E2/E24'])
    # trace_means_pow(dist6, dist12)
