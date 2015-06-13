#!/usr/bin/env python

import sys
import hangul

def get_next_char_list(infile):
    for rawline in infile:
        charlist = []
        for rawchar in rawline.decode("utf-8"):
            charlist.append(rawchar)
        yield charlist

def get_joined_char(infile):
    for charlist in get_next_char_list(infile):
        i = 0
        while i < len(charlist):
            leftchar = len(charlist) - 1 - i
            if leftchar == 1:
                yield charlist[i]
                i += 1
            elif leftchar == 2:
                if hangul.isJaeum(charlist[i]) and hangul.isMoeum(charlist[i+1]):
                    yield hangul.join((charlist[i], charlist[i+1], ''))
                    i += 2
                else:
                    yield charlist[i]
                    i += 1
            elif leftchar == 3:
                if hangul.isJaeum(charlist[i]) and hangul.isMoeum(charlist[i+1]):
                    if hangul.isJaeum(charlist[i+2]):
                        yield hangul.join((charlist[i], charlist[i+1], charlist[i+2]))
                        i += 3
                    else:
                        yield hangul.join((charlist[i], charlist[i+1], ''))
                        i += 2
                else:
                    yield charlist[i]
                    i += 1
            else:
                if hangul.isJaeum(charlist[i]) and hangul.isMoeum(charlist[i+1]):
                    if hangul.isJaeum(charlist[i+2]) and \
                       (hangul.isJaeum(charlist[i+3]) or (not hangul.ishangul(charlist[i+3]))):
                        yield hangul.join((charlist[i], charlist[i+1], charlist[i+2]))
                        i += 3
                    else:
                        yield hangul.join((charlist[i], charlist[i+1], ''))
                        i += 2
                else:
                    yield charlist[i]
                    i += 1

def main():
    input_filename = sys.argv[1]
    output_filename = input_filename + ".jk"
    infile = open(input_filename)
    outfile = open(output_filename, "w")

    for char in get_joined_char(infile):
        outfile.write(char.encode("utf-8"))

    infile.close
    outfile.close

if __name__ == "__main__":
    main()
