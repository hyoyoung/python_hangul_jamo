#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import hangul

def decode_jamo(char):
    encode_start_value = 0x7f
    jaeum_total_size = 30
    moeum_total_size = 21

    jamo = ord(char)
    if (encode_start_value <= jamo):
        if (jamo < encode_start_value + jaeum_total_size):
            jaeum_start = ord('ㄱ'.decode('utf-8'))
            return unichr(jaeum_start + jamo - encode_start_value)
        else:
            moeum_start = ord('ㅏ'.decode('utf-8'))
            return unichr(moeum_start + jamo - encode_start_value - jaeum_total_size)
    else:
        return char.decode("utf-8")


def get_next_char_list(infile):
    for rawline in infile:
        rawcharlist = list(rawline)
        charlist = []
        for rawchar in rawcharlist:
            charlist.append(decode_jamo(rawchar))
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
                if hangul.isChoseong(charlist[i]) and hangul.isJungseong(charlist[i+1]):
                    yield hangul.join((charlist[i], charlist[i+1], ''))
                    i += 2
                else:
                    yield charlist[i]
                    i += 1
            elif leftchar == 3:
                if hangul.isChoseong(charlist[i]) and hangul.isJungseong(charlist[i+1]):
                    if hangul.isJongseong(charlist[i+2]):
                        yield hangul.join((charlist[i], charlist[i+1], charlist[i+2]))
                        i += 3
                    else:
                        yield hangul.join((charlist[i], charlist[i+1], ''))
                        i += 2
                else:
                    yield charlist[i]
                    i += 1
            else:
                if hangul.isChoseong(charlist[i]) and hangul.isJungseong(charlist[i+1]):
                    if hangul.isJongseong(charlist[i+2]) and \
                       (hangul.isChoseong(charlist[i+3]) or (not hangul.ishangul(charlist[i+3]))):
                        yield hangul.join((charlist[i], charlist[i+1], charlist[i+2]))
                        i += 3
                    else:
                        yield hangul.join((charlist[i], charlist[i+1], ''))
                        i += 2
                else:
                    yield charlist[i]
                    i += 1

def main():
    if len(sys.argv) < 2:
        for char in get_joined_char(sys.stdin):
            sys.stdout.write(char.encode("utf-8"))
        return
    
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
