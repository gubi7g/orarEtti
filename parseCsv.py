import json
import csv
import re


def findIndexGrupa(orar, listaGrupe):
    return orar[1].index(listaGrupe[0]), orar[1].index(listaGrupe[-1])


orar = []
with open('res/orar_an3.csv') as f:
    reader = csv.reader(f)

    for row in reader:
        orar.append(row)

# taie chestiile useless
orar = orar[:70]

# serii & re patterns
serii = list(filter(None, orar[0]))
pattern_serie = re.compile(r'Anul \w{1,3} Seria \w{1}')

# lista cu toate seriile si numarul de serii
serii = [x for x in serii if pattern_serie.findall(x)]
# print(serii)
nr_serii = len(serii)

# grupe & re patterns
grupe = list(filter(None, orar[1]))
pattern_grupa = re.compile(r'4\d{2}\w{1,2}')
grupe = [x for x in grupe if pattern_grupa.findall(x)]
# print(grupe)
nr_grupe = len(grupe)

ore_posibile = [f'{i:02}-{(i+1):02}' for i in range(8, 21)]
print(ore_posibile)
dict_serii = [{'serie': x, 'numarGrupe': 0, 'grupe': []} for x in 'ABCDEFG']
# print(dict_serii)

for d in dict_serii:
    letter = d['serie']
    tmp_sum = 0
    for grupa in grupe:
        if(letter == grupa[3]):
            tmp_sum = tmp_sum + 1
            d['grupe'].append(grupa)
    d['numarGrupe'] = tmp_sum
    d['startIndexSerie'], d['stopIndexSerie'] = findIndexGrupa(orar, d['grupe'])

indexiIntervaleOrare = [[] for x in range(5)]
currentStartInd = 2

for ind, zi in enumerate(indexiIntervaleOrare):
    
    indexiIntervaleOrare[ind] = [currentStartInd, currentStartInd + len(ore_posibile) - 1]
    currentStartInd += len(ore_posibile) + 1
    
print(indexiIntervaleOrare)

orar_final = [{} for x in grupe]
for grupa, orar_grupa in zip(grupe, orar_final):
    orar_grupa['grupa'] = grupa
    orar_grupa['orar'] = {}
    indexTmpZi = 2
    
    for zi in ['luni', 'marti', 'miercuri', 'joi', 'vineri']:
        orar_grupa['orar'][zi] = {}

print(orar_final)
for serie in dict_serii:
    for grupa, currentGroup, indexSerie in zip(serie['grupe'], orar_final, range(serie['startIndexSerie'], serie['stopIndexSerie']+1)):
        for indexiInterval, zi in zip(indexiIntervaleOrare, ['luni', 'marti', 'miercuri', 'joi', 'vineri']):
            for ora, indexOra in zip(ore_posibile, range(indexiInterval[0], indexiInterval[1]+1)):
                # print(ora, indexOra)
                    currentGroup['orar'][zi]['course'] = orar[indexSerie][indexOra]
                    # print(orar[indexSerie][indexOra])
    
        orar_final.append(currentGroup)    

# write everything to a file
with open('orar_an3.json', 'w') as f:
    f.write(json.dumps(orar_final))
