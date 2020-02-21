import json
import csv
import re
from os.path import basename, splitext, join
from os import listdir

# TODO:

#   - de implementat cursuri/sem/lab care isi extind intervalul orar (verticala, orizontala este implementat)
#       -> salvam intr-o lista laboratoarele pe 3 ore (speciale)
#       -> caz super special: verifica daca este semigrupa cu 'a', si daca nu are pereche cu 'b', atunci ataseaza la grupa din stanga ====> semigrupa despre care vorbesc este o a 3-a semigrupa...

def checkWhatCourse(course):
    if course.find('curs') >= 0:
        tmpKey =  'curs'
    elif course.find('(s)') >= 0:
        tmpKey = 'seminar'
    elif course.find('(l)') >= 0:
        tmpKey = 'lab'
    elif course.find('(p)') >= 0:
        tmpKey = 'lab [SP]'
    else: # no special case
        tmpKey = 'unknown'
    
    return {'type': tmpKey}

def getGroupBasename(semigroup):
    return re.split(r'(\d+\w{1})', semigroup)[1]

def checkIfBothSemigroups(groupName, groupsList):
    x = [getGroupBasename(x) for x in groupsList].count(getGroupBasename(groupName))
    if x == 2:
        return True

def extendCellFlag(groupName, groupsList):
    if checkIfBothSemigroups(groupName, groupsList) and groupName[-1] == 'b':
        return True

def findIndexGrupa(orar, listaGrupe):
    return orar[1].index(listaGrupe[0]), orar[1].index(listaGrupe[-1])

def buildOrar(path, writeToFile=False):
    orar = []
    with open(path) as f:
        reader = csv.reader(f)

        for row in reader:
            orar.append(row)

    pattern_sala = re.compile(r'([AB][0-9]+|Infineon)')


    intervaleOrare = list(set([line[1] for line in orar]))
    pattern_interval = re.compile(r'(\w{3}|[0-9]{2})-(\w{3}|[0-9]{2})')
    intervaleOrare = [x for x in intervaleOrare if pattern_interval.findall(x)]
    nrIntervaleOrare = len(intervaleOrare)
    # print(nrIntervaleOrare)


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

    if nrIntervaleOrare == 13:
        intervaleOre = [f'{i:02}-{(i+1):02}' for i in range(8, 21)]
    else:
        intervaleOre = [f'{i:02}-{(i+1):02}' for i in range(9, 21)]

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
                    m = None
                    currentCell = orar[indexOra][indexGrupa]
                    currentGroup['orar'][zi][ora] = {}

                    if extendCellFlag(grupa, serie['grupe']): # daca este semigrupa cu b la final...

                        if currentCell != '': # daca este, dar are ceva trecut, pune-l pe ala
                            currentGroup['orar'][zi][ora] = checkWhatCourse(currentCell)
                            m = pattern_sala.search(currentCell)
                            currentGroup['orar'][zi][ora]['course'] = currentCell

                        elif orar[indexOra][indexGrupa - 1] != '': # daca este, dar nu are nimic trecut, ia-l pe cel din stanga
                            currentCell = orar[indexOra][indexGrupa - 1]

                            currentGroup['orar'][zi][ora] = checkWhatCourse(currentCell)
                            m = pattern_sala.search(currentCell)
                            currentGroup['orar'][zi][ora]['course'] = currentCell

                    elif currentCell != '': # daca nu este semigrupa cu b, dar are ceva trecut, scrie
                        currentGroup['orar'][zi][ora] = checkWhatCourse(currentCell)
                        m = pattern_sala.search(currentCell)
                        currentGroup['orar'][zi][ora]['course'] = currentCell

                    else: # daca nu are nimic trecut, nu scrie nimic
                        del currentGroup['orar'][zi][ora]
                        continue
                        
                    if m is not None:
                        currentGroup['orar'][zi][ora]['sala'] = m.group(0)

                    else:
                        try:
                            if currentGroup['orar'][zi][ora]['type'] in ['lab', 'sport']:
                                currentGroup['orar'][zi][ora]['sala'] = 'Please check announcements sheet.'

                            # if lab but we have room ,we overwrite the above.
                            if orar[indexOra][serie['stopIndexSerie'] + 1] != '':
                                currentGroup['orar'][zi][ora]['sala'] = orar[indexOra][serie['stopIndexSerie'] + 1]

                        except:
                            del currentGroup['orar'][zi][ora]


            orar_final.append(currentGroup)
    
    if writeToFile:
        with open(splitext(basename(path))[0] + '.json', 'w') as f:
            f.write(json.dumps(orar_final))
    else:
        return orar_final
    
    
for file in listdir('res'):
    if file.endswith('.csv'):
        buildOrar(join('res', file), writeToFile=True)