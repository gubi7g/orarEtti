# orarEtti
din ~csv~ ~jpg~ csv -> JSON pt fiecare grupa

exemplu output dorit:

```
[   
    {
        'grupa': '43xYz',
        'orar': {
            'luni': {
                'par': {
                    'interval_orar': {
                        'type': 'sem/curs/lab/sport',
                        'course': 'X',
                        'room': 'Y',
                        'prof': 'Z'
                    },
                    ...
                },
                'impar': {
                    ...
                }
            },
            ...
        }
    },
    ...
]
```

## Resources

https://docs.opencv.org/master/d1/d32/tutorial_py_contour_properties.html
