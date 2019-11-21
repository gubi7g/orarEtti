# orarEtti
din csv -> JSON pt fiecare grupa

exemplu output dorit:

```json
[   
    {
        'grupa': 'x',
        'orar': {
            'luni': {
                '9-11': {
                    'type': 'sem/curs',
                    'course': 'AM2',
                    'room': 'A03',
                    ...
                },
                ...
            },
            ...
        }
    }
]
```