import csv
import re

orar = []

with open('Orar ETTI 2019-2020 semestrul I - AN 1.csv') as f:
    reader = csv.reader(f)

    for row in reader:
        orar.append(row)

rand_serie = list(filter(None, orar[0]))
pattern_serie = re.compile(r'Anul \w{1,3} Seria \w{1}')

rand_serie = [x for x in rand_serie if pattern_serie.findall(x)]
nr_serii = len(rand_serie)
print(rand_serie)

rand_grupe = list(filter(None, orar[1]))
# print(rand_grupe)
pattern_grupa = re.compile(r'4\d{2}\w{1,2}')

rand_grupe = [x for x in rand_grupe if pattern_grupa.findall(x)]
nr_subgrupe = len(rand_grupe)
print(rand_grupe)
print('nr de sub/grupe: ', nr_subgrupe)

total_

ore = [x[2:] for x in orar[2:]]
print()
print(len(ore[0]))
for ind, curs in enumerate(ore[0]):
    if curs == '':
        pass
    else:
        print(rand_grupe[ind])

# for ind, elem in 

# for thing in orar[2]