# xls2txt
This is a program to export an Excel worksheet into multiple text files.
It creates one file for each row in the worksheet.
It creates one line in each file for each column in the worksheet.

```
$ xls2txt units.xls
```
![screenshot of the Excel work sheet](doc/units.xls.png)
```
$ tree units
units
└── Sheet1
    ├── 001_s.yml
    ├── 002_m.yml
    ├── 003_kg.yml
    ├── 004_a.yml
    ├── 005_k.yml
    ├── 006_mol.yml
    └── 007_cd.yml
$ cat units/Sheet1/001_s.yml
Symbol: s
Name: second
Quantity: time
```

There are many command line arguments to customize the output.
See `xls2txt --help`.


WARNING: This program is based on xlrd and will therefore "no longer read anything other than .xls files."
https://pypi.org/project/xlrd/


# Installation
```
pipx install xls2txt
```
