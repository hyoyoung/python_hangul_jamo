#!/usr/bin/env python

import sys
import hangul

def get_next_char(infile):
    for rawline in infile:
        for rawchar in rawline.decode("utf-8", "ignore"):
            if hangul.ishangul(rawchar):
                for jamo in hangul.split(rawchar):
                    if jamo != '':
                        yield jamo
            else:
                yield rawchar

def main():
    input_filename = sys.argv[1]
    output_filename = input_filename + ".sk"
    infile = open(input_filename)
    outfile = open(output_filename, "w")

    for char in get_next_char(infile):
        outfile.write(char.encode("utf-8"))

    infile.close
    outfile.close

if __name__ == "__main__":
    main()
