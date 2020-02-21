import json
import csv
import re
from os.path import basename, splitext, join, abspath
from os import listdir
import config
print(config.addresses['in'])

# TODO:

#   - de implementat cursuri/sem/lab care isi extind intervalul orar (verticala, orizontala este implementat)
#       -> salvam intr-o lista laboratoarele pe 3 ore (speciale)
#       -> caz super special: verifica daca este semigrupa cu 'a', si daca nu are pereche cu 'b', atunci ataseaza la grupa din stanga ====> semigrupa este o a 3-a semigrupa...


def splitCoursesByWeekParity(cell):
    d = {'par': '', 'impar': ''}
    extra = {'prof': ''}

    if len(cell.split('\n')) == 1: # nu avem sali sau prof mentionat
        
        if len(cell.split('/')) == 1:
            d['par'] = d['impar'] = cell

        if len(cell.split('/')) == 2:
            courseImpar, coursePar = cell.split('/')
            d['impar'] = courseImpar
            d['par'] = coursePar

    elif len(cell.split('\n')) == 2:
        course, extra = cell.split('\n') # avem sala sau prof mentionat

        if len(course.split('/')) == 1:
            d['par'] = d['impar'] = course

        if len(course.split('/')) == 2:
            d['impar'] , d['par'] = course.split('/')

        if len(extra.split('/')) == 2:
            pass
    else: 
        # aici nu ajungem niciodata
        print(cell)
        d['par'] = d['impar'] = cell
    # print(d)
    return d


def checkWhatCourse(course):
    if course.find('curs') >= 0:
        tmpKey =  'curs'
    elif course.find('Sport') >= 0:
        tmpKey = 'sport'
    elif course.find('(s)') >= 0:
        tmpKey = 'seminar'
    elif course.find('(l)') >= 0:
        tmpKey = 'lab'
    elif course.find('(p)') >= 0:
        tmpKey = 'lab [SP]'
    else: # no special case
        tmpKey = 'unknown'
    
    return tmpKey

def getGroupBasename(semigroup):
    return re.split(r'(\d+\w{1})', semigroup)[1]

def checkIfBothSemigroups(groupName, groupsList):
    x = [getGroupBasename(x) for x in groupsList].count(getGroupBasename(groupName))
    if x == 2:
        return True
    else:
        return False

def extendCellFlag(groupName, groupsList):
    if checkIfBothSemigroups(groupName, groupsList) and groupName[-1] == 'b':
        return True

def findIndexGrupa(orar, listaGrupe):
    return orar[1].index(listaGrupe[0]), orar[1].index(listaGrupe[-1])

def buildOrar(path, writeToFile=False):
    print(path)
    orar = []

    with open(path, encoding='utf-8') as f:
        reader = csv.reader(f)

        for row in reader:
            orar.append(row)

    # print(orar)
    pattern_sala = re.compile(r'([AB]\s?[0-9]+|Infineon|[sS]ala \d*[ ]*d*e*[ ]*calc)')


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
                
                for parity in ['impar', 'par']:
                    currentGroup['orar'][zi][parity] = {}

                    for ora, indexOra in zip(intervaleOre, range(indexiInterval[0], indexiInterval[1]+1)):
                        m = None
                        currentCell = orar[indexOra][indexGrupa]
                        
                        currentGroup['orar'][zi][parity][ora] = {}
                        if extendCellFlag(grupa, serie['grupe']): # daca este semigrupa cu b la final...

                            if currentCell != '': # daca este, dar are ceva trecut, pune-l pe ala
                                # pass
                                currentGroup['orar'][zi][parity][ora]['type'] = checkWhatCourse(currentCell)
                                m = pattern_sala.search(currentCell)
                                currentGroup['orar'][zi][parity][ora]['course'] = splitCoursesByWeekParity(currentCell)[parity]

                            elif orar[indexOra][indexGrupa - 1] != '': # daca este, dar nu are nimic trecut, ia-l pe cel din stanga
                                currentCell = orar[indexOra][indexGrupa - 1]

                                currentGroup['orar'][zi][parity][ora]['type'] = checkWhatCourse(currentCell)
                                m = pattern_sala.search(currentCell)
                                currentGroup['orar'][zi][parity][ora]['course'] = splitCoursesByWeekParity(currentCell)[parity]

                        elif currentCell != '': # daca nu este semigrupa cu b, dar are ceva trecut, scrie
                            currentGroup['orar'][zi][parity][ora]['type'] = checkWhatCourse(currentCell)
                            m = pattern_sala.search(currentCell)
                            
                            currentGroup['orar'][zi][parity][ora]['course'] = splitCoursesByWeekParity(currentCell)[parity]

                        else: # daca nu are nimic trecut, nu scrie nimic
                            # print(currentGroup['orar'][zi][parity][ora])
                            del currentGroup['orar'][zi][parity][ora]
                            continue

                        # print(grupa, zi, ora)
                        if currentGroup['orar'][zi][parity][ora] and '--' in currentGroup['orar'][zi][parity][ora]['course']:
                            del currentGroup['orar'][zi][parity][ora]
                            continue
                            
                            
                        if m is not None:
                            currentGroup['orar'][zi][parity][ora]['sala'] = m.group(0)

                        else:
                            try:
                                if currentGroup['orar'][zi][parity][ora]['type'] in ['lab', 'sport']:
                                    currentGroup['orar'][zi][parity][ora]['sala'] = 'Please check announcements sheet.'

                                # if lab but we have room ,we overwrite the above.
                                if orar[indexOra][serie['stopIndexSerie'] + 1] != '':
                                    currentGroup['orar'][zi][parity][ora]['sala'] = orar[indexOra][serie['stopIndexSerie'] + 1]

                            except:
                                del currentGroup['orar'][zi][parity][ora]
                            


            orar_final.append(currentGroup)
    
    if writeToFile:
        print(join(splitext(basename(path))[0], 'jsonFiles'))
        with open(join(config.addresses['out'], splitext(basename(path))[0]) + '.json', 'w', encoding='utf-8') as f:
            json.dump(orar_final, f, ensure_ascii=False)
    else:
        return orar_final
    

for file in listdir(config.addresses['in']):
    if file.endswith('.csv'):
        buildOrar(join(config.addresses['in'], file), writeToFile=True)