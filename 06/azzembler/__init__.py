#!/usr/bin/env/python
"""
Azzembler, a blazing fast hack assembler!
"""

import argparse
import re
import sys


def main(arguments):
    """
    Main runner
    """

    parser = argparse.ArgumentParser()
    parser.add_argument(
        'input_file',
        type=argparse.FileType('r'))

    parser.add_argument('--output_file')

    parser.add_argument("--debug", dest="debug",
                        action="store_true")

    args = parser.parse_args(arguments)

    lines = file_reader(args.input_file)
    parsed = second_pass(first_pass(lines))

    if args.debug:
        print "\n".join(parsed)
    else:
        output_filename = args.output_file \
                if args.output_file \
                else args.input_file.name.replace("asm", "hack")
        file_write(output_filename, parsed)


def clean_line_from_returns(line):
    """
    Removes returns from line
    """
    return line.replace('\r\n', '')


def clean_inline_comments(line):
    """
    Remove any inline comments
    """
    if '//' not in line:
        return line

    return line.split('//')[0]


def clean_line(line):
    """
    Cleans line to be ready for processing
    """
    return clean_inline_comments(
        clean_line_from_returns(
            line
            )
        ).strip()


def file_reader(input_file):
    """
    Returns an array of clean hack commands
    """
    return [clean_line(line)
            for line in input_file
            if not line.startswith('//')
            and line != '\r\n']


def file_write(path, binary_lines):
    """
    Writes the .hack file
    """

    joined_lines = "\n".join(binary_lines)
    with open(path, "w") as hack_file:
        hack_file.write("{}\n".format(joined_lines))


SYMBOL_TABLE = {
    "SP":       0,
    "LCL":      1,
    "ARG":      2,
    "THIS":     3,
    "THAT":     4,
    "R0":       0,
    "R1":       1,
    "R2":       2,
    "R3":       3,
    "R4":       4,
    "R5":       5,
    "R6":       6,
    "R7":       7,
    "R8":       8,
    "R9":       9,
    "R10":      10,
    "R11":      11,
    "R12":      12,
    "R13":      13,
    "R14":      14,
    "R15":      15,
    "SCREEN":   16384,
    "KBD":      24576,
}


def handle_a_instruction(line):
    """
    Handle A instruction
    """
    value = line.replace("@", "")
    if re.match('^[0-9]', value) is None:
        value = SYMBOL_TABLE.get(value)
    return '{:b}'.format(int(value)).zfill(16)


JUMP_TABLE = {
    "null": "000",
    "JGT":  "001",
    "JEQ":  "010",
    "JGE":  "011",
    "JLT":  "100",
    "JNE":  "101",
    "JLE":  "110",
    "JMP":  "111",
}

DEST_TABLE = {
    "null": "000",
    "M":    "001",
    "D":    "010",
    "MD":   "011",
    "A":    "100",
    "AM":   "101",
    "AD":   "110",
    "AMD":  "111",
}


COMP_TABLE = {
    "0":    "0101010",
    "1":    "0111111",
    "-1":   "0111010",
    "D":    "0001100",
    "A":    "0110000",
    "!D":   "0001101",
    "!A":   "0110001",
    "-D":   "0001111",
    "-A":   "0110011",
    "D+1":  "0011111",
    "A+1":  "0110111",
    "D-1":  "0001110",
    "A-1":  "0110010",
    "D+A":  "0000010",
    "D-A":  "0010011",
    "A-D":  "0000111",
    "D&A":  "0000000",
    "D|A":  "0010101",
    "M":    "1110000",
    "!M":   "1110001",
    "-M":   "1110011",
    "M+1":  "1110111",
    "M-1":  "1110010",
    "D+M":  "1000010",
    "D-M":  "1010011",
    "M-D":  "1000111",
    "D&M":  "1000000",
    "D|M":  "1010101",
}


def handle_b_instruction(line):
    """
    Handle B instruction
    """

    value = line
    dest = ""
    jump = ""
    comp = ""

    if "=" in value:
        splitted_by_dest = value.split("=")
        dest = splitted_by_dest[0]
        value = splitted_by_dest[1]

    if ";" in value:
        splitted_by_jump = value.split(";")
        jump = splitted_by_jump[1]
        value = splitted_by_jump[0]

    comp = COMP_TABLE.get(value, COMP_TABLE.get("0"))
    jump = JUMP_TABLE.get(jump, JUMP_TABLE.get("null"))
    dest = DEST_TABLE.get(dest, DEST_TABLE.get("null"))

    return "111{0}{1}{2}".format(comp, dest, jump)


def is_a_instruction(line):
    """
    check if a instruction
    """
    return line.startswith('@')


def handle_instruction(line):
    """
    Handle each line
    """
    return handle_a_instruction(line) \
        if is_a_instruction(line) \
        else handle_b_instruction(line)


def add_symbol_if_needed(symbol, value):
    """
    Get symbol from lookup table, add if missing
    """

    looked_up_symbol = SYMBOL_TABLE.get(symbol, None)
    if looked_up_symbol is None:
        SYMBOL_TABLE[symbol] = value
        return True
    return False


def first_pass(lines):
    """
    Translate symbols
    """

    parsed_lines = []
    lines_without_labels = []

    line_index = 0
    next_symbol_index = 16

    for line in lines:
        if "(" in line:
            label = re.sub('[()]', '', line)
            add_symbol_if_needed(label, line_index)
        else:
            lines_without_labels.append(line)
            line_index += 1

    line_index = 0
    for line in lines_without_labels:
        if is_a_instruction(line):
            symbol = line.replace("@", "")
            if re.match('^[0-9]', symbol) is None:
                added = add_symbol_if_needed(symbol, next_symbol_index)
                if added:
                    next_symbol_index += 1

        parsed_lines.append(line)
        line_index += 1

    return parsed_lines


def second_pass(lines):
    """
    Write all the thingz
    """
    return [handle_instruction(line) for line in lines]


if __name__ == "__main__":
    main(sys.argv[1:])
