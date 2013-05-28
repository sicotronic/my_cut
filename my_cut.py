#!/usr/bin/env python

from os import remove
from sys import exit, argv, stderr
from optparse import OptionParser
from codecs import open

#Some useful constants that may change.
DELIMITER = '\t'
ENCODING = "utf-8"
LIST_SEPARATOR = ','
RANGE_SYMBOLS = '-:/'
NEW_LINE = '\r\n'


def retrieve_columns(input_file, requested_list, output_file, delim=DELIMITER):
    columns = []
    source = open(input_file, 'r', ENCODING)
    target = open(output_file, 'wb', ENCODING)
    line_number = 1
    for line in source:
        if line != '':
            string_row = ''
            fields = line.split(delim)
            amount_columns = len(fields)
            requested_aux = requested_list
            for column_number in requested_list:
                if column_number < amount_columns and column_number >= 0:
                    field = fields[column_number].strip()
                    requested_aux = requested_aux[1:]
		    if len(requested_aux) > 0:
                        field += delim
                    string_row += field
                else:#I should give errors on stderr
                    stderr.write('Error in input line %d ' % line_number)
                    stderr.write('there is no column %d \n' % column_number)
                    stderr.write('no output file was generated \n')
                    source.close()
                    target.close()
                    remove(output_file)
                    exit(0)
                    # I should clean the output_file here
            target.write(string_row + NEW_LINE)
        line_number += 1
    return columns


def fields_list_from_range(first, second):
    res = []
    if first > second:
        res = list(range(second, first + 1))[::-1]
    else:
        if first < second:
            res = list(range(first, second + 1))
        else:
            res.append(first)
    return res


def solve_field_range(field):
    for symbol in RANGE_SYMBOLS:
        if symbol in field:
            fields_range = field.split(symbol)
            if len(fields_range) != 2:
                stderr.write('the field range containing' + symbol + ' is not correct')
                exit(0)
            try:
                first = int(fields_range[0])
                second = int(fields_range[1])
            except ValueError:
                stderr.write('the fields list argument is not correct, error in the numbers')
                exit(0)
            return fields_list_from_range(first, second)
    return [int(field)]


def get_numeric_fields_list(string_fields_list):
    res = []
    for field in (string_fields_list.split(LIST_SEPARATOR)):
        res += solve_field_range(field)
    return res


def main():
    usage = 'usage: %prog [options] <input file> <fields list> <output file>\n\n'
    usage += 'fields list format:\n'
    usage += '\t* the first field of a file is the number 0.\n'
    usage += '\t* fields should be separated by comma.\n'
    usage += '\t  for example: 0,2,4\n'
    usage += '\t* fields will be retrieved in the order you give them.\n'
    usage += '\t* use \'/\', \'-\' or \':\' to give a range of fields.\n'
    usage += '\t  for example: 3-5, 3/5 or 3:5 will retrieve the fields: 3,4,5\n'
    usage += '\t  another example: 5-3 will retrieve the fields: 5,4,3\n'
    parser = OptionParser(usage=usage)
    parser.add_option("-d", "--delimiter", dest="delim", default='\t',
                  help="sets the delimiter for the csv file")
    parser.add_option("-s", "--separator", dest="separator", default = ',',
                  help="sets the separator for the fields list")
    parser.add_option("-e", "--encoding", dest="encoding", default = "utf-8",
                  help="sets the encoding for the input and output file")
    parser.add_option("-r", "--range-symbols", dest="range_symbols", default = ":-/",
                  help="sets the symbols to express range of fields")
    parser.add_option("-n", "--new-line", dest="newline", default = "\r\n",
                  help="sets the symbols to express newlines")
    options, arguments = parser.parse_args()
    if len(arguments) != 3:
        parser.error("incorrect number of arguments")
    if options.delim:
        DELIMITER = options.delim
    if options.separator:
        LIST_SEPARATOR = options.separator
    if options.encoding:
        ENCODING = options.encoding
    if options.range_symbols:
        RANGE_SYMBOLS = options.range_symbols
    if options.newline:
        RANGE_SYMBOLS = options.newline
    numeric_fields_list = get_numeric_fields_list(arguments[1])
    retrieve_columns(arguments[0], numeric_fields_list, arguments[2])

if __name__ == '__main__':
    main()
