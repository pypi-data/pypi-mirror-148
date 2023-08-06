#!/usr/bin/env pytest

import pytest

from xls2txt.main import RangeParser

@pytest.fixture
def col_parser():
	return RangeParser(0, 10, number_format=RangeParser.FMT_ALPHA, has_zero=False, start_in=1)

@pytest.fixture
def row_parser():
	return RangeParser(0, 100, start_in=1)

@pytest.fixture
def zero_based_dec_parser():
	return RangeParser(0, 100)


def test__parse_int__dec_zero_based(zero_based_dec_parser):
	assert zero_based_dec_parser.parse_int('0') == 0
	assert zero_based_dec_parser.parse_int('1') == 1
	assert zero_based_dec_parser.parse_int('10') == 10
	assert zero_based_dec_parser.parse_int('99') == 99
	assert zero_based_dec_parser.parse_int('123') == 123
	assert zero_based_dec_parser.parse_int('9999') == 9999

def test__parse_int__dec_one_based(row_parser):
	assert row_parser.parse_int('1') == 0
	assert row_parser.parse_int('10') == 9
	assert row_parser.parse_int('11') == 10
	assert row_parser.parse_int('99') == 98
	assert row_parser.parse_int('123') == 122
	assert row_parser.parse_int('9999') == 9998

def test__parse_int__alph(col_parser):
	assert col_parser.parse_int('A') == 0
	assert col_parser.parse_int('E') == 4
	assert col_parser.parse_int('Z') == 25
	assert col_parser.parse_int('AB') == 27
	assert col_parser.parse_int('ZZ') == 701
	assert col_parser.parse_int('ZZZ') == 18277


def test__int_to_str__dec_zero_based(zero_based_dec_parser):
	assert zero_based_dec_parser.int_to_str(0) == '0'
	assert zero_based_dec_parser.int_to_str(42) == '42'
	assert zero_based_dec_parser.int_to_str(123) == '123'
	assert zero_based_dec_parser.int_to_str(9999) == '9999'

def test__int_to_str__dec_one_based(row_parser):
	assert row_parser.int_to_str(row_parser.parse_int('1')) == '1'
	assert row_parser.int_to_str(row_parser.parse_int('42')) == '42'
	assert row_parser.int_to_str(row_parser.parse_int('123')) == '123'
	assert row_parser.int_to_str(row_parser.parse_int('9999')) == '9999'

def test__int_to_str__alph(col_parser):
	assert col_parser.int_to_str(col_parser.parse_int('A')) == 'A'
	assert col_parser.int_to_str(col_parser.parse_int('E')) == 'E'
	assert col_parser.int_to_str(col_parser.parse_int('AB')) == 'AB'
	assert col_parser.int_to_str(col_parser.parse_int('ZZ')) == 'ZZ'
	assert col_parser.int_to_str(col_parser.parse_int('ZZ') + 1) == 'AAA'
	assert col_parser.int_to_str(col_parser.parse_int('ZZZZ')) == 'ZZZZ'
