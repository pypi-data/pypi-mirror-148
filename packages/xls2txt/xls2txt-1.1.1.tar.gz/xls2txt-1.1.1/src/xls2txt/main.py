#!/usr/bin/env python

# Copyright © 2022 erzo <erzo@posteo.de>
# This work is free. You can use, copy, modify, and/or distribute it
# under the terms of the BSD Zero Clause License, see LICENSE.

"""
Export an Excel worksheet into text files.
Create one file for each row in the worksheet.
Create one line in each file for each column in the worksheet.

WARNING: This program is based on xlrd and will therefore
"no longer read anything other than .xls files."
https://pypi.org/project/xlrd/
"""

__version__ = "1.1.1"


import os
import sys
import string
import re
import logging

import xlrd


class ExcelExporter:

	class Error(Exception):
		pass

	def __init__(self, ffn_in, sheet_name_in=None, rows=None, columns=None, column_headers=None, column_headers_override=None, line_pattern=None, insert_line=None, column_formats={}, directoryname_pattern=None, filename_pattern=None, skip_empty_rows=True, remove_existing_directory=False):
		self.remove_existing_directory = remove_existing_directory
		self.skip_empty_rows = skip_empty_rows
		self.line_pattern = line_pattern
		self.ffn_in = ffn_in
		self.wb = xlrd.open_workbook(ffn_in)
		if sheet_name_in is None:
			sheets = self.wb.sheets()
			n = len(sheets)
			if n > 1:
				sheet_names = ''.join('\n%s: %s' % (one_based_index, s.name) for one_based_index, s in enumerate(sheets, 1))
				raise self.Error("This workbook contains several sheets. Please specify which one you want to export." + sheet_names)
			if n <= 0:
				raise self.Error("This workbook contains no sheets.")
			self.ws = sheets[0]
		else:
			try:
				self.ws = self.wb.sheet_by_name(sheet_name_in)
			except Exception as e:
				try:
					one_based_index = int(sheet_name_in)
				except ValueError:
					raise self.Error("Failed to open worksheet %r. %s." % (sheet_name_in, e))
				sheets = self.wb.sheets()
				if one_based_index > len(sheets):
					raise self.Error("Cannot open worksheet %s. This workbook has only %s worksheets." % (one_based_index, len(sheets)))
				self.ws = sheets[one_based_index-1]


		self.col_parser = RangeParser(0, self.ws.ncols, number_format=RangeParser.FMT_ALPHA, has_zero=False, start_in=1)
		self.row_parser = RangeParser(0, self.ws.nrows, start_in=1)
		self.columns = list(self.col_parser.parse(columns))
		self.rows = iter(self.row_parser.parse(rows))

		self.column_formats = dict()
		for key,val in column_formats.items():
			for col in self.col_parser.parse(key):
				self.column_formats[col] = val
		self.formatter = ExcelFormatter(self.ws, self.col_parser)

		if column_headers:
			self.column_headers = column_headers
		else:
			row = next(self.rows)
			self.column_headers = [self.ws.cell_value(row, col) for col in self.columns]
		if column_headers_override:
			for colname,header in column_headers_override.items():
				try:
					col = self.col_parser.parse_int(colname)
				except ValueError:
					raise self.Error("Invalid column header override: %r is not a valid column specifier" % colname)
				try:
					col = self.columns.index(col)
				except ValueError:
					raise self.Error("Invalid column header override: column %s is not exported" % colname.upper())
				self.column_headers[col] = header

		if not filename_pattern:
			filename_pattern = "{relrow:03d}_{%s:l,space=_,newline=_}.yml" % self.col_parser.number_format[self.columns[0]]
		if directoryname_pattern:
			filename_pattern = os.path.join(directoryname_pattern, filename_pattern)
		self.filename_pattern = filename_pattern
		self.insert_line = self.parse_insert_line(insert_line)

	def parse_insert_line(self, values):
		out = []
		if not values:
			return out

		SEP = ":"
		for ln in values:
			if SEP in ln:
				lnno_str, ln = ln.split(SEP, 1)
				try:
					lnno = self.col_parser.parse_int(lnno_str)
				except ValueError:
					raise self.Error("Failed to parse column specifier %r passed to --insert-line" % lnno_str)
			else:
				lnno = 0

			out.append((lnno, ln))

		out.sort(key=lambda x: x[0])
		return out

	def run(self):
		self.create_directory()
		first_row = True
		for row in self.rows:
			if first_row:
				self.formatter.first_row = row
				first_row = False
			if self.skip_empty_rows and self.is_empty(row):
				print("skipping row %s because all cells to be exported are empty" % self.row_parser.int_to_str(row), file=sys.stderr)
				continue
			self.export_entry(row)

	def create_directory(self):
		path, fn = os.path.split(self.filename_pattern)
		if not path:
			return

		path = self.formatter.format(path, worksheet=self.ws.name, workbook=os.path.split(self.ffn_in)[1])
		if os.path.isdir(path):
			if self.remove_existing_directory:
				print("%s exists already, removing it to recreate it" % path)
				import shutil
				shutil.rmtree(path)
			else:
				print("%s exists already" % path, file=sys.stderr)
				sys.exit(1)

		os.makedirs(path)

	def is_empty(self, row):
		for col in self.columns:
			val = self.ws.cell_value(row, col)
			if val is not None and val != '':
				return False
		return True

	def export_entry(self, row):
		title = self.formatter.format(self.filename_pattern, row=row, worksheet=self.ws.name, workbook=os.path.split(self.ffn_in)[1])
		with open(title, 'wt') as f:
			self.write_entry(f, row)

	def write_entry(self, f, row):
		i = 0
		n = len(self.insert_line)
		for col, key in zip(self.columns, self.column_headers):

			while i < n and self.insert_line[i][0] <= col:
				self.write_additional_line(f, self.insert_line[i][1], row)
				i += 1

			val = self.ws.cell_value(row, col)
			fmt = self.column_formats.get(col, "")
			if isinstance(val, float) and int(val) == val:
				val = int(val)
			if fmt:
				try:
					val = self.formatter.format(fmt, val, row=row)
				except ValueError as e:
					logging.warning("failed to format val %r with format %r", val, fmt, exc_info=e)
			ln = self.formatter.format(self.line_pattern, key=key, value=val, row=row, col=col)
			print(ln, file=f)

		while i < n:
			self.write_additional_line(f, self.insert_line[i][1], row)
			i += 1

	def write_additional_line(self, f, ln, row):
		ln = self.formatter.format(ln, row=row)
		print(ln, file=f)


class ExcelFormatter(string.Formatter):

	"""
	Formats a string with values from an Excel Work Sheet.
	Cells are identified by their column name (e.g. A for the first column).
	When calling format you must pass exactly one keyword argument: row = n.
	Aside from column names one special key is allowed: row. It uses the value
	given as keyword argument.
	"""

	def __init__(self, worksheet, columns_range_parser):
		super().__init__()
		self.worksheet = worksheet
		self.columns_range_parser = columns_range_parser

	def get_value(self, key, args, kwargs):
		if isinstance(key, int):
			return super().get_value(key, args, kwargs)

		if key in kwargs:
			val = kwargs[key]
			if key == 'col':
				val = self.columns_range_parser.int_to_str(val)
			elif key == 'row':
				# basically I mean rows_range_parser.int_to_str(val) here
				# except that I don't want to convert it to a str yet, so that I can still use %03d
				val += 1
			return val
		if key == 'relrow' and 'row' in kwargs and hasattr(self, 'first_row'):
			return kwargs['row'] - self.first_row + 1

		row = kwargs['row']
		try:
			col = self.columns_range_parser.parse_int(key)
		except ValueError:
			raise KeyError("Invalid field_name: %r, should be one of %s or a column specifier" % (key, ', '.join(str(field_name) for field_name in tuple(range(len(args))) + tuple(kwargs.keys()))))
		return self.worksheet.cell_value(row, col)

	def format_field(self, value, format_spec):
		fl = format_spec.split(",")
		try:
			out = super().format_field(value, fl[0])
			del fl[0]
		except ValueError:
			out = super().format_field(value, "")

		for fmt in fl:
			out = self.processflag(fmt, out)

		return out

	def processflag(self, fmt, text):
		if fmt == "l":
			text = text.lower()
		elif fmt == "u":
			text = text.upper()
		elif fmt == "c":
			text = text.capitalize()
		elif fmt == "C":
			text = re.sub(r'\w+', lambda m: m.group().capitalize(), text)
		else:
			text = self.processarg(fmt, text)

		return text

	def processarg(self, fmt, text):
		if fmt.startswith("%%"):
			pattern = self.prepare_pattern(fmt[2:])
			pattern = '(.*?)' + pattern + '$'
			re.sub(pattern, lambda m: m.group(1), text)
			return re.sub(pattern, lambda m: m.group(1), text)
		elif fmt.startswith("%"):
			pattern = self.prepare_pattern(fmt[1:])
			pattern = '(.*)' + pattern + '$'
			return re.sub(pattern, lambda m: m.group(1), text)
		elif fmt.startswith("##"):
			pattern = self.prepare_pattern(fmt[2:])
			pattern = pattern + '(.*)$'
			re.sub(pattern, lambda m: m.group(1), text)
			return re.sub(pattern, lambda m: m.group(1), text)
		elif fmt.startswith("#"):
			pattern = self.prepare_pattern(fmt[1:], nongreedy=True)
			pattern = pattern + '(.*)$'
			return re.sub(pattern, lambda m: m.group(1), text)

		if "=" in fmt:
			old, new = fmt.split("=", 1)
			if old == "space":
				return text.replace(" ", new)
			elif old == "newline":
				return text.replace("\n", new)
			elif old == ".":
				return new * len(text)

		raise ValueError("unknown format_spec extension %r" % fmt)

	def prepare_pattern(self, pattern, nongreedy=False):
		pattern = re.escape(pattern)
		pattern = pattern.replace(re.escape('?'), '.')
		pattern = pattern.replace(re.escape('*'), '.*?' if nongreedy else '.*')
		return pattern


class RangeParser:

	TEXT_ALL = '*'

	SEP_RANGES = ','
	SEP_START_STOP = '-'

	FMT_ALPHA = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

	"""
	ranges: str -- the text to parse
	start: int -- start index for open ranges without a start
	       incl, output system
	stop: int -- stop index for open ranges without a stop
	       excl, output system
	start_in: int -- 0 if input system starts counting at zero
	                 1 if input system starts counting at one
	number_format: either a base for int or an indexable of
	               lowercase characters representing the symbols
	               of a number system, e.g. FMT_ALPHA
	has_zero: if number_format is an indexable of symbols
	          has_zero determines whether the first character
	          has the value 0 or 1
	          With number_format = FMT_ALPHA and has_zero = True
	          AB == B because A is 0 and leading As don't make a difference
	"""

	def __init__(self, start:int, stop:int, start_in:int=0, number_format=10, has_zero=True):
		self.start = start
		self.stop = stop
		self.offset = start - start_in
		self.number_format = number_format
		self.has_zero = has_zero

	def parse(self, ranges:str):
		if ranges is None:
			ranges = self.TEXT_ALL

		ranges = ranges.split(self.SEP_RANGES)
		for text in ranges:
			text = text.strip()

			if not text:
				pass

			elif text == self.TEXT_ALL:
				for i in range(self.start, self.stop):
					yield i

			elif self.SEP_START_STOP in text:
				start, stop = text.split(self.SEP_START_STOP)
				start = self.parse_int(start) if start else self.start
				stop = self.parse_int(stop) + 1 if stop else self.stop
				for i in range(start, stop):
					yield i

			else:
				yield self.parse_int(text)

	def parse_int(self, text):
		if self.number_format is None or isinstance(self.number_format, int):
			out = int(text, base=self.number_format)
		else:
			out = 0
			chars = self.number_format
			base = len(chars)
			offset = 0 if self.has_zero else 1
			for i in range(len(text)):
				c = text[-1-i]
				try:
					out += (chars.index(c) + offset) * base**i
				except ValueError:
					raise ValueError("digit %r not in alphabet %r" % (c,chars))

		out += self.offset
		return out

	def int_to_str(self, i):
		i -= self.offset

		if i < 0:
			raise ValueError('negative numbers are not supported')
		if not self.has_zero and i == 0:
			raise ValueError('0 is not supported because has_zero = False')

		alphabet = self.number_format

		if alphabet is None:
			alphabet = 10

		if isinstance(alphabet, int):
			alphabet = [str(i) for i in range(alphabet)]

		base = len(alphabet)
		offset = 0 if self.has_zero else 1
		out = ""

		while i != 0:
			i -= offset
			out = alphabet[i % base] + out
			i //= base

		if not out and self.has_zero:
			out = alphabet[0]

		return out


def main(args=None):
	import argparse

	class ParseMapping(argparse.Action):

		def __init__(self, option_strings, dest, **kwargs):
			kwargs.setdefault('default', dict())
			kwargs.setdefault('nargs', '+')
			argparse.Action.__init__(self, option_strings, dest, **kwargs)

		def __call__(self, parser, namespace, values, option_string=None):
			out = getattr(namespace, self.dest)

			SEP = ":"
			for a in values:
				if SEP in a:
					old, new = a.split(SEP, 1)
					old = old.strip()
					new = new.strip()
				else:
					old = None
					new = a

				if old in out:
					raise argparse.ArgumentError(self, "key %s has been specified more than once." % old)

				out[old] = new

	class PrintVersion(argparse.Action):

		def __init__(self, option_strings, dest, **kwargs):
			kwargs.setdefault('nargs', 0)
			argparse.Action.__init__(self, option_strings, dest, **kwargs)

		def __call__(self, parser, namespace, values, option_string=None):
			print(__version__)
			sys.exit(0)

	p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
	p.add_argument("-v", "--version", action=PrintVersion, help="show the version number of this program and exit")
	p.add_argument("filename", help="The Excel file to read")
	p.add_argument("worksheet", nargs='?', help="The name or number of the worksheet to export (optional if there is only one worksheet)")
	p.add_argument("-c", "--columns", "--cols", metavar="COLS", default="*", help="The columns to export")
	p.add_argument("-r", "--rows", metavar="ROWS", default="*", help="The rows to export")
	p.add_argument("-a", "--no-skip-empty", action="store_true", help="Do not skip rows in which all cells to be exported are empty")
	p.add_argument("-d", "--directory-pattern", metavar="FMT", default="{workbook:%.*}"+os.path.sep+"{worksheet}", help="The directory to export to, "
			"{workbook} is the name of the input file, "
			"{worksheet} is the name of the worksheet, "
			"e.g. '%(default)s'")
	p.add_argument("-o", "--filename-pattern", metavar="FMT", help="The pattern for the output filenames, "
			"{workbook} is the name of the input file, "
			"{worksheet} is the name of the worksheet, "
			"e.g. '{relrow:03d}_{A:l,space=_,newline=_}.yml' uses the 3 digit row number as prefix, the value given in column A converted to lower case and spaces replaced by underscores, and .yml as extension")
	p.add_argument("-l", "--line-pattern", metavar="FMT", default="{key}: {value}", help=
			"How to format the lines, "
			"{key} is the column header (the value in the first row or a value specified by --column-headers or --column-headers-override), "
			"{value} is the value in the cell formatted as specified by --column-formats, "
			"{col} is the letter of the column, "
			"e.g. '{key:C}: {value}' to capitalize the header")
	p.add_argument("-C", "--column-headers", metavar="HEADER", nargs="+", help=
			"The headers for the columns to be exported")
	p.add_argument("-H", "--column-headers-override", metavar="COL:HEADER", action=ParseMapping, help=
			"Specify headers for certain columns to be used instead of the values in the title row")
	p.add_argument("-f", "--column-formats", metavar="COLS:FMT", action=ParseMapping, help=
			"How to format the values depending on their column, "
			"{} is the value in the current cell, "
			"e.g. '{:.2f}' for floats with two decimals, "
			"'0x{:x}' for hex numbers, "
			"'{:+03d}' for integers with an explicit + for positive numbers and zeros added between the sign and the number to make the resulting string at least 3 characters long")
	p.add_argument("-i", "--insert-line", metavar="[COL:]FMT", nargs="+", help=
			"Insert FMT before COL, FMT is a complete line pattern, it is *not* influenced by --line-pattern")
	p.add_argument("-y", "--yes", action="store_true", help="Remove output directory if it is already existing")

	p.epilog = """
COL:
  A single column, e.g. "A"

COLS:
  A range of columns, e.g. "A-C,G-" means columns A, B, C, G and all following.

ROWS:
  A range of rows, e.g. "1-3,7-" means rows 1, 2, 3, 7 and all following.

FMT:
  An extended format string, additionally to the standard python described in
  https://docs.python.org/3/library/string.html#format-string-syntax
  the format_spec supports the following additional features, separated by commas:
    l: convert all characters to lower case
    u: convert all characters to upper case
    c: convert the first character to upper case and all following to lower case
    C: convert the first character of each word to upper case and all other to lower case
    space=STR: replace all spaces by STR
    newline=STR: replace all line breaks by STR
    .=STR: replace each character by STR (useful for underlines)
    %PATTERN: remove the suffix PATTERN, PATTERN may contain the wild card * for an arbitrary sequence of characters (as short as possible) or ? for any single character
    %%PATTERN: remove the suffix PATTERN, PATTERN may contain the wild card * for an arbitrary sequence of characters (as long as possible) or ? for any single character
    #PATTERN: remove the prefix PATTERN, PATTERN may contain the wild card * for an arbitrary sequence of characters (as short as possible) or ? for any single character
    ##PATTERN: remove the prefix PATTERN, PATTERN may contain the wild card * for an arbitrary sequence of characters (as long as possible) or ? for any single character
  and the following additional values for field_name (except for --directory-pattern):
    row: the number of the current row
    relrow: the number of the current row relative to the first row afer the header
    COL: the value in the cell in the current row and the column specified by the field_name
"""

	args = p.parse_args(args)

	try:
		ee = ExcelExporter(args.filename, args.worksheet,
				directoryname_pattern=args.directory_pattern,
				filename_pattern=args.filename_pattern,
				column_headers=args.column_headers,
				column_headers_override=args.column_headers_override,
				column_formats=args.column_formats,
				columns=args.columns, rows=args.rows,
				line_pattern=args.line_pattern,
				insert_line=args.insert_line,
				skip_empty_rows=not args.no_skip_empty,
				remove_existing_directory=args.yes)
	except ExcelExporter.Error as e:
		print(e, file=sys.stderr)
		exit(1)

	ee.run()

if __name__ == '__main__':
	main()
