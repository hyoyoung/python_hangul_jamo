#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import hangul

def encode_jamo(jamo):
    encode_start_value = 0x7f
    jaeum_total_size = 30
    moeum_total_size = 21

    if hangul.isJaeum(jamo):
        jaeum_start = ord('ㄱ'.decode('utf-8'))
        return chr(encode_start_value + ord(jamo) - jaeum_start)
    elif hangul.isMoeum(jamo):
        moeum_start = ord('ㅏ'.decode('utf-8'))
        return chr(encode_start_value + jaeum_total_size + ord(jamo) - moeum_start)
    return jamo.encode("utf-8")

def get_next_char(infile):
    char_upperbound = 178
    
    for rawline in infile:
        for rawchar in rawline.decode("utf-8", "ignore"):
            if hangul.ishangul(rawchar):
                for jamo in hangul.split(rawchar):
                    if jamo != '':
                        yield encode_jamo(jamo)
            else:
                other_char = rawchar.encode("utf-8")
                if (len(other_char) > 1) or (ord(other_char) > char_upperbound):
                    other_char = ' '
                yield other_char

def main():
    if len(sys.argv) < 2:
        for char in get_next_char(sys.stdin):
            sys.stdout.write(char)
        return

    input_filename = sys.argv[1]
    output_filename = input_filename + ".sk"
    infile = open(input_filename)
    outfile = open(output_filename, "w")

    for char in get_next_char(infile):
        outfile.write(char)

    infile.close
    outfile.close

if __name__ == "__main__":
    main()
