import json
import csv
import re
import xlsxwriter
from os.path import basename, splitext, join
from os import listdir

def findIndexGrupa(orar, listaGrupe):
    return orar[1].index(listaGrupe[0]), orar[1].index(listaGrupe[-1])

def buildOrar(path, writeToFile=True):
    orar = []
    with open(path) as f:
        reader = csv.reader(f)

        for row in reader:
            orar.append(row)


    # serii & re patterns
    serii = list(filter(None, orar[0]))
    pattern_serie = re.compile(r'Anul \w{1,3} Seria \w{1}')

    # lista cu toate seriile si numarul de serii
    serii = [x for x in serii if pattern_serie.findall(x)]
    nr_serii = len(serii)

    # grupe & re patterns
    grupe = list(filter(None, orar[1]))
    pattern_grupa = re.compile(r'4\d{2}\w{1,2}')
    grupe = [x for x in grupe if pattern_grupa.findall(x)]
    nr_grupe = len(grupe)

    intervaleOre = [f'{i:02}-{(i+1):02}' for i in range(8, 21)]
    dict_serii = [{'serie': x, 'numarGrupe': 0, 'grupe': []} for x in 'ABCDEFG']

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
    currStartIndIntOrar = 2

    for ind, zi in enumerate(indexiIntervaleOrare):
        
        indexiIntervaleOrare[ind] = [currStartIndIntOrar, currStartIndIntOrar + len(intervaleOre) - 1]
        currStartIndIntOrar += len(intervaleOre) + 1
        

    orar_final = []
    for serie in dict_serii:
        for grupa, indexGrupa in zip(serie['grupe'], range(serie['startIndexSerie'], serie['stopIndexSerie'] + 1)):
            
            currentGroup = {}
            currentGroup['grupa'] = grupa
            currentGroup['orar'] = {}
            
            for indexiInterval, zi in zip(indexiIntervaleOrare, ['luni', 'marti', 'miercuri', 'joi', 'vineri']):
                currentGroup['orar'][zi] = {}
                
                for ora, indexOra in zip(intervaleOre, range(indexiInterval[0], indexiInterval[1]+1)):
                    
                    
                    if orar[indexOra][indexGrupa] != '':
                        currentGroup['orar'][zi][ora] = {'course': orar[indexOra][indexGrupa]}
                    
        
            orar_final.append(currentGroup)
    
    if writeToFile:
        with open(splitext(basename(path))[0] + '.json', 'w') as f:
            f.write(json.dumps(orar_final))
    else:
        return orar_final
    
    
    
    
# orar = []
# with open('res/orar_an3.csv') as f:
#     reader = csv.reader(f)

#     for row in reader:
#         orar.append(row)


# # serii & re patterns
# serii = list(filter(None, orar[0]))
# pattern_serie = re.compile(r'Anul \w{1,3} Seria \w{1}')

# # lista cu toate seriile si numarul de serii
# serii = [x for x in serii if pattern_serie.findall(x)]
# nr_serii = len(serii)

# # grupe & re patterns
# grupe = list(filter(None, orar[1]))
# pattern_grupa = re.compile(r'4\d{2}\w{1,2}')
# grupe = [x for x in grupe if pattern_grupa.findall(x)]
# nr_grupe = len(grupe)

# intervaleOre = [f'{i:02}-{(i+1):02}' for i in range(8, 21)]
# dict_serii = [{'serie': x, 'numarGrupe': 0, 'grupe': []} for x in 'ABCDEFG']

# for d in dict_serii:
#     letter = d['serie']
#     tmp_sum = 0
#     for grupa in grupe:
#         if(letter == grupa[3]):
#             tmp_sum = tmp_sum + 1
#             d['grupe'].append(grupa)
#     d['numarGrupe'] = tmp_sum
#     d['startIndexSerie'], d['stopIndexSerie'] = findIndexGrupa(orar, d['grupe'])

# indexiIntervaleOrare = [[] for x in range(5)]
# currStartIndIntOrar = 2

# for ind, zi in enumerate(indexiIntervaleOrare):
    
#     indexiIntervaleOrare[ind] = [currStartIndIntOrar, currStartIndIntOrar + len(intervaleOre) - 1]
#     currStartIndIntOrar += len(intervaleOre) + 1
    

# orar_final = []
# for serie in dict_serii:
#     for grupa, indexGrupa in zip(serie['grupe'], range(serie['startIndexSerie'], serie['stopIndexSerie'] + 1)):
        
#         currentGroup = {}
#         currentGroup['grupa'] = grupa
#         currentGroup['orar'] = {}
        
#         for indexiInterval, zi in zip(indexiIntervaleOrare, ['luni', 'marti', 'miercuri', 'joi', 'vineri']):
#             currentGroup['orar'][zi] = {}
            
#             for ora, indexOra in zip(intervaleOre, range(indexiInterval[0], indexiInterval[1]+1)):
                
                
#                 if orar[indexOra][indexGrupa] != '':
#                     currentGroup['orar'][zi][ora] = {'course': orar[indexOra][indexGrupa]}
                
    
#         orar_final.append(currentGroup)    

# # write everything to a file
# with open('orar_an3.json', 'w') as f:
#     f.write(json.dumps(orar_final))

for file in listdir('res'):
    if file.endswith('.csv'):
        buildOrar(join('res', file))