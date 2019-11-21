import csv
import re

# eu in range_orar am +1 celula in plus dupa grupele fiecarei serii.
# in grupe eu nu am asa ceva, deci trebuie tinut cont de asta.
# deci daca gasesc un curs/sem la indexul i, i se va atribui grupei i+

# exemplu output dorit:
#
# {
#     'grupa': 'x',
#     'orar': {
#         'luni': {
#             '9-11': {
#                 'type': 'sem/curs',
#                 'course': 'AM2',
#                 'room': 'A03'
#             }
#         }
#     }
# }

def findIndexGroup(event_index, length_serii):
    i = 0
    s = 0
    while(s + length_serii[i] < event_index):
        s = s + length_serii[i]
        i = i + 1
    return event_index + i

    
            


orar = []

with open('orar_an1.csv') as f:
    reader = csv.reader(f)

    for row in reader:
        orar.append(row)

serii = list(filter(None, orar[0]))
pattern_serie = re.compile(r'Anul \w{1,3} Seria \w{1}')

serii = [x for x in serii if pattern_serie.findall(x)]
nr_serii = len(serii)
print(serii)
print('numar de serii:', nr_serii)

grupe = list(filter(None, orar[1]))
# print(grupe)
pattern_grupa = re.compile(r'4\d{2}\w{1,2}')

grupe = [x for x in grupe if pattern_grupa.findall(x)]
nr_grupe = len(grupe)
print(grupe)
print('nr de sub/grupe: ', nr_grupe)

# trebuie sa stim cate grupe are fiecare serie (ajuta cu determinarea curs/sem):

length_serii = []
dict_serii = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

for letter in dict_serii:
    tmp_sum = 0
    for grupa in grupe:
        if(letter == grupa[3]):
            print(grupa)
            tmp_sum = tmp_sum + 1
    length_serii.append(tmp_sum)

print(length_serii)

effective_orar = nr_grupe + nr_serii
print(effective_orar)

range_orar = [x[1:effective_orar+2] for x in orar[2:]] # inclusiv effective_orar
print(range_orar[0])

jump_cells = []
temps = 0
for i in length_serii:
    temps = temps + i - 1
    jump_cells.append(temps)

for ind, cell in enumerate(range_orar[1][1:]):
    if cell == '' or ind in [x+1 for x in jump_cells]:
        pass
    else:
        ind_grupa = findIndexGroup(ind, length_serii)
        if(ind_grupa == -1):
            pass
        else:
            print(f'grupa {grupe[ind_grupa]} are {cell}')

# for thing in orar[2]