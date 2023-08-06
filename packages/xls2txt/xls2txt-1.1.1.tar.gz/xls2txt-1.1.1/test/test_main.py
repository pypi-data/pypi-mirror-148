#!/usr/bin/env pytest

import os

from xls2txt.main import main

PATH = os.path.split(__file__)[0]
FN = os.path.join(PATH, 'units.xls')
DIR_OUT = os.path.join(PATH, 'test-output')

def assert_file_equals(fn, content_expected, *, strip=True):
	if strip:
		content_expected = content_expected.lstrip('\n')
	ffn = os.path.join(DIR_OUT, fn)
	with open(ffn, 'rt') as f:
		content_is = f.read()
	#content_is = content_is.splitlines()
	#content_expected = content_expected.splitlines()
	assert content_is == content_expected


def test_defaults():
	main([FN, "-y", "--directory", DIR_OUT])
	ls = os.listdir(DIR_OUT)
	ls.sort()
	assert ls == [
		'001_s.yml',
		'002_m.yml',
		'003_kg.yml',
		'004_a.yml',
		'005_k.yml',
		'006_mol.yml',
		'007_cd.yml',
	]
	assert_file_equals(ls[0], '''
Symbol: s
Name: second
Quantity: time
''')

def test_cols():
	main([FN, "-y", "--directory", DIR_OUT, "-c", "B,A,C"])
	ls = os.listdir(DIR_OUT)
	ls.sort()
	assert ls == [
		'001_second.yml',
		'002_metre.yml',
		'003_kilogram.yml',
		'004_ampere.yml',
		'005_kelvin.yml',
		'006_mole.yml',
		'007_candela.yml',
	]
	assert_file_equals(ls[0], '''
Name: second
Symbol: s
Quantity: time
''')

def test_filename():
	main([FN, "-y", "--directory", DIR_OUT, "--filename", "{C}"])
	ls = os.listdir(DIR_OUT)
	ls.sort()
	assert ls == [
		'amount of substance',
		'electric current',
		'length',
		'luminous intensity',
		'mass',
		'thermodynamic temperature',
		'time',
	]
	assert_file_equals(ls[0], '''
Symbol: mol
Name: mole
Quantity: amount of substance
''')
