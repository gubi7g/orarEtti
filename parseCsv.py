import json
import csv
import re

orar = []
with open('orar_an3.csv') as f:
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
nr_serii = len(serii)

# grupe & re patterns
grupe = list(filter(None, orar[1]))
pattern_grupa = re.compile(r'4\d{2}\w{1,2}')
grupe = [x for x in grupe if pattern_grupa.findall(x)]
nr_grupe = len(grupe)

# trebuie sa stim cate grupe are fiecare serie
length_serii = []
dict_serii = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

for letter in dict_serii:
    tmp_sum = 0
    for grupa in grupe:
        if(letter == grupa[3]):
            tmp_sum = tmp_sum + 1
    length_serii.append(tmp_sum)

# filter out trash
effective_orar = nr_grupe + nr_serii

range_orar = [x[0:effective_orar+2]
              for x in orar[2:]]  # inclusiv effective_orar

jump_cells = []
temps = 0
for ind, i in enumerate(length_serii):
    temps = temps + i
    jump_cells.append(temps)

# celule jump: 6, 19, 24...
for ind, i in enumerate(jump_cells):
    jump_cells[ind] = jump_cells[ind] + ind + 2

# adica indexul orei si al zilei
jump_cells.append(0)
jump_cells.append(1)

orar_final = [{} for x in grupe]
ore_posibile_dict = []

# won't use it, but a cool way to use f strings for zero-padding
for i in range(8, 21):
    ore_posibile_dict.append(f'{i:02}-{(i+1):02}')

print(ore_posibile_dict)

# initialize a part of the final dict
for grupa, orar_grupa in zip(grupe, orar_final):
    orar_grupa['grupa'] = grupa
    orar_grupa['orar'] = {}
    for zi in ['luni', 'marti', 'miercuri', 'joi', 'vineri']:
        orar_grupa['orar'][zi] = {}

zi_curenta = 'luni'

# sortam invers pt a nu ne complica cu indexing gresit cand scoatem elemente din array
jump_cells.sort(reverse=True)

ora_curenta = 0

# in range_orar[i][1] avem ora! oricare i
print(range_orar)
for ind_int, interval in enumerate(range_orar):
    # pe poz 0 avem numele zilei
    if interval[0] != '' and interval[0].isalpha():
        zi_curenta = interval[0].lower()

    # pe poz 1 avem intervalul orar
    if interval[1] != '':
        ora_curenta = interval[1]

    # scoatem din campurile cu evenimente coloanele care nu ne folosesc (pt un zip bijectiv)
    for i in jump_cells:
        # print(i)
        interval.pop(i)

    print(zi_curenta, ind_int, interval)
    for (ind, cell), orar_grupa in zip(enumerate(interval), orar_final):
        if cell == '':
            continue
        else:
            # print(zi_curenta)
            if ora_curenta in orar_grupa['orar'][zi_curenta]:
                orar_grupa['orar'][zi_curenta][ora_curenta]['course'] = cell
            else:
                # daca nu este creat dict, avem eroare
                # poate ramane doar else-ul asta in loc de if/else (cred)
                orar_grupa['orar'][zi_curenta][ora_curenta] = {}
                orar_grupa['orar'][zi_curenta][ora_curenta]['course'] = cell

            # print(f'grupa {grupe[ind_grupa]} are {cell}')

# write everything to a file
with open('orar_an3.json', 'w') as f:
    f.write(json.dumps(orar_final))
