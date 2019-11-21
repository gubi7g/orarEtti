import json
import csv
import re

# eu in range_orar am +1 celula in plus dupa grupele fiecarei serii.
# in grupe eu nu am asa ceva, deci trebuie tinut cont de asta.
# deci daca gasesc un curs/sem la indexul i, i se va atribui grupei i+

# exemplu output dorit:

# [{
#     'grupa': 'x',
#     'orar': {
#         'luni': {
#             '9-11': {
#                 'type': 'sem/curs',
#                 'course': 'AM2',
#                 'room': 'A03'
#             }
#             ...
#         }
#         ...
#     }
#     'grupa': 'y',
#     ...
# ]


def findGroupIndex(event_index, length_serii):
    i = 0
    s = 0
    while(s + length_serii[i] < event_index):
        s = s + length_serii[i] + 1
        i = i + 1
    return event_index - i - 1


orar = []

with open('orar_an1.csv') as f:
    reader = csv.reader(f)

    for row in reader:
        orar.append(row)

# taie chestiile useless
orar = orar[:70]

serii = list(filter(None, orar[0]))
pattern_serie = re.compile(r'Anul \w{1,3} Seria \w{1}')

# lista cu toate seriile si numarul de serii
serii = [x for x in serii if pattern_serie.findall(x)]
nr_serii = len(serii)

grupe = list(filter(None, orar[1]))
# print(grupe)
pattern_grupa = re.compile(r'4\d{2}\w{1,2}')

grupe = [x for x in grupe if pattern_grupa.findall(x)]
nr_grupe = len(grupe)

# trebuie sa stim cate grupe are fiecare serie (ajuta cu determinarea curs/sem):

length_serii = []
dict_serii = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

for letter in dict_serii:
    tmp_sum = 0
    for grupa in grupe:
        if(letter == grupa[3]):
            tmp_sum = tmp_sum + 1
    length_serii.append(tmp_sum)


effective_orar = nr_grupe + nr_serii
# print(effective_orar)

range_orar = [x[0:effective_orar+2]
              for x in orar[2:]]  # inclusiv effective_orar

jump_cells = []
temps = 0
for ind, i in enumerate(length_serii):
    temps = temps + i
    jump_cells.append(temps)

# celule jump: 6, 19, 24
for ind, i in enumerate(jump_cells):
    jump_cells[ind] = jump_cells[ind] + ind + 2

jump_cells.append(0)
jump_cells.append(1)

# print(jump_cells)

# print(zile)

# print(zi_tmp)
orar_final = [{} for x in grupe]

ore_posibile_dict = []

for i in range(8, 21):
    ore_posibile_dict.append(f'{i:02}-{(i+1):02}')


for grupa, orar_grupa in zip(grupe, orar_final):
    orar_grupa['grupa'] = grupa
    orar_grupa['orar'] = {}
    for zi in ['luni', 'marti', 'miercuri', 'joi', 'vineri']:
        orar_grupa['orar'][zi] = {}
    # for interval in ore_posibile_dict:
    #     orar_grupa['orar'][zi][interval] = {}

# print(orar_final)
# print(range_orar[1])
zi_curenta = 'luni'
jump_cells.sort(reverse=True)
print(jump_cells)
ora_curenta = 0


# in range_orar[i][1] avem ora! oricare i
for ind_int, interval in enumerate(range_orar):
    if interval[0] != '':
        zi_curenta = interval[0].lower()
    if interval[1] != '':
        ora_curenta = interval[1]
    for i in jump_cells:
        print(i)
        interval.pop(i)
    for (ind, cell), orar_grupa in zip(enumerate(interval), orar_final):
        if cell == '':
            if cell != '':
                # print(f'___celula ignorata___ {cell} la index {ind}:')
                continue
        else:
            ind_grupa = findGroupIndex(ind, length_serii)
            # print(zi_curenta)
            if ora_curenta in orar_grupa['orar'][zi_curenta]:
                orar_grupa['orar'][zi_curenta][ora_curenta]['course'] = cell
            else:
                orar_grupa['orar'][zi_curenta][ora_curenta] = {}
                orar_grupa['orar'][zi_curenta][ora_curenta]['course'] = cell

            # print(f'grupa {grupe[ind_grupa]} are {cell}')
with open('orar_an1.json', 'w') as f:
    f.write(json.dumps(orar_final))
