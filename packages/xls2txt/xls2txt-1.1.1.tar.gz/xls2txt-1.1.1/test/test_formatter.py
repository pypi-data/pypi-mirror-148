#!/usr/bin/env pytest

import pytest

from xls2txt import main

class WorkSheetMock:

	ncols = 5

	def __init__(self):
		self.col_parser = main.RangeParser(-1, self.ncols, number_format=main.RangeParser.FMT_ALPHA, has_zero=False, start_in=1)

	def get_value(self, row, col):
		return self.col_parser.int_to_str(col) + str(row+1)

@pytest.fixture
def formatter():
	worksheet = WorkSheetMock()
	col_parser = worksheet.col_parser
	return main.ExcelFormatter(worksheet, col_parser)


def test_lower_case(formatter):
	assert formatter.format('{foo:l}', foo='Hello World') == 'hello world'

def test_upper_case(formatter):
	assert formatter.format('{foo:u}', foo='Hello World') == 'HELLO WORLD'

def test_first_title_case(formatter):
	assert formatter.format('{foo:c}', foo='Hello World') == 'Hello world'

def test_all_title_case(formatter):
	assert formatter.format('{foo:C}', foo='heLLo worlD') == 'Hello World'



def test_replace_str(formatter):
	assert formatter.format('{foo:space=_}', foo='Hello World') == 'Hello_World'
	assert formatter.format('{foo:space=-}', foo='Hello World') == 'Hello-World'
	assert formatter.format('{foo:space=}', foo='Hello World') == 'HelloWorld'

def test_underline(formatter):
	str_in = 'Hello World'
	str_ex = '==========='
	assert formatter.format('{foo:.==}', foo=str_in) == str_ex

def test_strip_suffix_nongreedy(formatter):
	assert formatter.format('{fn:%.*}', fn='foo.bar.baz') == 'foo.bar'

def test_strip_suffix_greedy(formatter):
	assert formatter.format('{fn:%%.*}', fn='foo.bar.baz') == 'foo'

def test_strip_prefix_nongreedy(formatter):
	assert formatter.format('{fn:#*/}', fn='/some/path/to/a/file') == 'some/path/to/a/file'

def test_strip_prefix_greedy(formatter):
	assert formatter.format('{fn:##*/}', fn='/some/path/to/a/file') == 'file'



def test_chain(formatter):
	assert formatter.format('{foo:space=-,l}',    foo='Hello World') == 'hello-world'
	assert formatter.format('{foo:l,space=}',     foo='Hello World') == 'helloworld'
	assert formatter.format('{foo:l,space=,.=-}', foo='Hello World') == '----------'
